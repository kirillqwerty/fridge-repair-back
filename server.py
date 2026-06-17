"""FastAPI app for Refrigerator Repair Minsk website."""
from __future__ import annotations
import logging
import os
import re
import uuid
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import aiofiles
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
    Request,
)
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# Local modules (imported after load_dotenv for proper env access)
from auth import (
    authenticate,
    create_token,
    get_admin_user,
    require_admin,
    set_admin_password,
    verify_password,
)
from seed_data import (
    INITIAL_BENEFITS,
    INITIAL_BRANDS,
    INITIAL_CONTACTS,
    INITIAL_FAQ,
    INITIAL_GUARANTEES,
    INITIAL_MASTERS,
    INITIAL_PORTFOLIO,
    INITIAL_PROCESS_STEPS,
    INITIAL_REVIEWS,
    INITIAL_SERVICES,
    INITIAL_STATS,
)
from storage import ensure_seeded, read_json, write_json
from telegram_notify import notify_lead

# Upload dir
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ремонт холодильников Минск API")
api = APIRouter(prefix="/api")


# ---------- Pydantic models ----------


class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6, max_length=128)


class ServiceItem(BaseModel):
    id: Optional[str] = None
    name: str
    price_from: float
    price_to: float
    unit: str = "BYN"
    note: str = ""
    order: int = 0


class ReviewItem(BaseModel):
    id: Optional[str] = None
    author: str
    city: str = "Минск"
    rating: int = 5
    date: str = ""
    text: str
    brand: str = ""
    problem: str = ""
    image_url: str = ""
    featured: bool = False
    order: int = 0


class ContactsModel(BaseModel):
    phones: list[str]
    hours: str
    days: str = ""
    address: str
    company_name: str = ""
    email: str = ""
    footer_note: str = ""
    telegram_link: str = ""
    viber_link: str = ""
    whatsapp_link: str = ""


class PortfolioItem(BaseModel):
    id: Optional[str] = None
    title: str
    description: str = ""
    before_url: str = ""
    after_url: str = ""
    brand: str = ""
    order: int = 0


class MasterItem(BaseModel):
    id: Optional[str] = None
    name: str
    role: str = ""
    experience: str = ""
    specialization: str = ""
    image_url: str = ""
    order: int = 0


class FAQItem(BaseModel):
    id: Optional[str] = None
    question: str
    answer: str
    order: int = 0


class BenefitItem(BaseModel):
    id: Optional[str] = None
    icon: str
    title: str
    description: str = ""
    order: int = 0


class ProcessStep(BaseModel):
    id: Optional[str] = None
    step: int
    title: str
    description: str = ""


class BrandUpdate(BaseModel):
    intro: Optional[str] = None
    features: Optional[list[str]] = None
    common_issues: Optional[list[str]] = None
    meta_description: Optional[str] = None
    price_overrides: Optional[list[dict]] = None


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=5, max_length=40)
    brand: str = ""
    problem: str = ""
    message: str = ""
    consent: bool = True
    source: str = "site"


class StatsModel(BaseModel):
    rating: float
    reviews_count: int
    years_experience: int
    repairs_done: int
    guarantee_months: int
    arrival_minutes: int


# ---------- Startup seeding ----------


@app.on_event("startup")
async def on_startup() -> None:
    # ensure all JSON files are present
    await get_admin_user()  # seeds default admin
    await ensure_seeded("contacts", INITIAL_CONTACTS)
    await ensure_seeded("services", INITIAL_SERVICES)
    await ensure_seeded("benefits", INITIAL_BENEFITS)
    await ensure_seeded("reviews", INITIAL_REVIEWS)
    await ensure_seeded("faq", INITIAL_FAQ)
    await ensure_seeded("masters", INITIAL_MASTERS)
    await ensure_seeded("portfolio", INITIAL_PORTFOLIO)
    await ensure_seeded("brands", INITIAL_BRANDS)
    await ensure_seeded("stats", INITIAL_STATS)
    await ensure_seeded("process_steps", INITIAL_PROCESS_STEPS)
    await ensure_seeded("guarantees", INITIAL_GUARANTEES)
    await ensure_seeded("leads", [])
    logger.info("Startup seeding complete")


# ---------- Helpers ----------


def _id() -> str:
    return str(uuid.uuid4())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(text: str) -> str:
    text = (text or "").lower().strip()
    return re.sub(r"[^a-z0-9-]+", "-", text).strip("-")


async def _sorted_load(name: str, default: list) -> list:
    items = await read_json(name, default)
    if isinstance(items, list):
        items.sort(key=lambda x: x.get("order", 0))
    return items


BRAND_PRICE_FACTORS = {
    "atlant": 0.92,
    "beko": 0.96,
    "indesit": 0.98,
    "ariston": 1.0,
    "daewoo": 1.0,
    "sharp": 1.04,
    "samsung": 1.08,
    "lg": 1.08,
    "electrolux": 1.1,
    "bosch": 1.14,
    "aeg": 1.16,
    "liebherr": 1.22,
}


def _safe_num(value: Any, default: float = 0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _round_price(value: float) -> int:
    if value <= 0:
        return 0
    return int(round(value / 5) * 5)


def _normalize_services(items: list[dict] | None) -> list[dict]:
    payload: list[dict] = []
    if not isinstance(items, list):
        return payload

    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        payload.append(
            {
                "id": item.get("id") or _id(),
                "name": str(item.get("name") or "").strip() or "Услуга",
                "price_from": _safe_num(item.get("price_from"), 0),
                "price_to": _safe_num(item.get("price_to"), 0),
                "unit": str(item.get("unit") or "BYN").strip() or "BYN",
                "note": str(item.get("note") or ""),
                "order": int(_safe_num(item.get("order"), idx + 1)),
            }
        )
    payload.sort(key=lambda x: x.get("order", 0))
    return payload


def _default_brand_services(brand: dict, base_services: list[dict]) -> list[dict]:
    """Create a separate brand price list when the brand has no saved custom list yet."""
    slug = brand.get("slug", "")
    factor = BRAND_PRICE_FACTORS.get(slug, 1.0)
    result = []

    for idx, service in enumerate(base_services):
        price_from = _round_price(_safe_num(service.get("price_from"), 0) * factor)
        price_to = _round_price(_safe_num(service.get("price_to"), 0) * factor)
        note = service.get("note", "")

        if slug in {"samsung", "lg"} and "No Frost" in service.get("name", ""):
            note = note or "Частая услуга для No Frost"
        if slug in {"bosch", "liebherr", "aeg", "electrolux"} and "платы" in service.get("name", "").lower():
            note = note or "Цена зависит от модели платы"
        if slug == "atlant" and service.get("name") == "Замена компрессора":
            note = note or "Популярные компрессоры обычно в наличии"

        result.append(
            {
                **service,
                "id": service.get("id") or _id(),
                "price_from": price_from,
                "price_to": price_to,
                "note": note,
                "order": service.get("order", idx + 1),
            }
        )

    return _normalize_services(result)


def _brand_services(brand: dict, base_services: list[dict]) -> list[dict]:
    custom = brand.get("price_overrides")
    if isinstance(custom, list) and len(custom) > 0:
        return _normalize_services(custom)
    return _default_brand_services(brand, base_services)


# ---------- PUBLIC: site data ----------


@api.get("/health")
async def health() -> dict:
    return {"status": "ok", "time": _now_iso()}


@api.get("/site-data")
async def get_site_data() -> dict:
    contacts = await read_json("contacts", INITIAL_CONTACTS)
    services = await _sorted_load("services", INITIAL_SERVICES)
    benefits = await _sorted_load("benefits", INITIAL_BENEFITS)
    reviews = await _sorted_load("reviews", INITIAL_REVIEWS)
    faq = await _sorted_load("faq", INITIAL_FAQ)
    masters = await _sorted_load("masters", INITIAL_MASTERS)
    portfolio = await _sorted_load("portfolio", INITIAL_PORTFOLIO)
    brands = await read_json("brands", INITIAL_BRANDS)
    stats = await read_json("stats", INITIAL_STATS)
    process_steps = await read_json("process_steps", INITIAL_PROCESS_STEPS)
    if isinstance(process_steps, list):
        process_steps.sort(key=lambda x: x.get("step", 0))
    guarantees = await read_json("guarantees", INITIAL_GUARANTEES)
    return {
        "contacts": contacts,
        "services": services,
        "benefits": benefits,
        "reviews": reviews,
        "faq": faq,
        "masters": masters,
        "portfolio": portfolio,
        "brands": brands,
        "stats": stats,
        "process_steps": process_steps,
        "guarantees": guarantees,
    }


@api.get("/brands/{slug}")
async def get_brand(slug: str) -> dict:
    brands = await read_json("brands", INITIAL_BRANDS)
    brand = next((b for b in brands if b.get("slug") == slug), None)
    if not brand:
        raise HTTPException(status_code=404, detail="Бренд не найден")

    base_services = await _sorted_load("services", INITIAL_SERVICES)
    services = _brand_services(brand, base_services)
    contacts = await read_json("contacts", INITIAL_CONTACTS)
    reviews_all = await _sorted_load("reviews", INITIAL_REVIEWS)
    brand_reviews = [
        r
        for r in reviews_all
        if r.get("brand", "").lower() == brand.get("name", "").lower()
        or r.get("brand", "").lower() == brand.get("name_en", "").lower()
        or r.get("brand", "").lower() == slug
    ]
    return {
        "brand": brand,
        "services": services,
        "contacts": contacts,
        "reviews": brand_reviews,
    }


# ---------- PUBLIC: leads ----------


@api.post("/leads")
async def create_lead(lead: LeadCreate) -> dict:
    if not lead.consent:
        raise HTTPException(status_code=400, detail="Требуется согласие на обработку данных")
    item = lead.model_dump()
    item["id"] = _id()
    item["created_at"] = _now_iso()
    item["status"] = "new"
    leads = await read_json("leads", [])
    leads.append(item)
    await write_json("leads", leads)
    # Attempt Telegram notification (safe-fail)
    telegram_sent = False
    try:
        telegram_sent = await notify_lead(item)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Telegram notify failed: %s", exc)
    return {"ok": True, "id": item["id"], "telegram_sent": telegram_sent}


# ---------- AUTH ----------


@api.post("/auth/login")
async def login(req: LoginRequest) -> dict:
    user = await authenticate(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    token = create_token(user["username"])
    return {"access_token": token, "token_type": "bearer", "username": user["username"]}


@api.get("/auth/me")
async def me(user: dict = Depends(require_admin)) -> dict:
    return {"username": user["username"]}


@api.post("/auth/change-password")
async def change_password(
    req: ChangePasswordRequest, user: dict = Depends(require_admin)
) -> dict:
    current_user = await get_admin_user()
    if not verify_password(req.current_password, current_user.get("password_hash", "")):
        raise HTTPException(status_code=400, detail="Текущий пароль введён неверно")
    await set_admin_password(req.new_password)
    return {"ok": True}


# ---------- ADMIN: services ----------


@api.get("/services")
async def list_services() -> list:
    return await _sorted_load("services", INITIAL_SERVICES)


@api.put("/services")
async def replace_services(items: list[ServiceItem], _: dict = Depends(require_admin)) -> list:
    payload = []
    for it in items:
        d = it.model_dump()
        if not d.get("id"):
            d["id"] = _id()
        payload.append(d)
    payload.sort(key=lambda x: x.get("order", 0))
    await write_json("services", payload)
    return payload


@api.post("/services")
async def create_service(item: ServiceItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("services", [])
    d = item.model_dump()
    d["id"] = _id()
    if not d.get("order"):
        d["order"] = (max([i.get("order", 0) for i in items]) + 1) if items else 1
    items.append(d)
    await write_json("services", items)
    return d


@api.put("/services/{item_id}")
async def update_service(item_id: str, item: ServiceItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("services", [])
    idx = next((i for i, x in enumerate(items) if x.get("id") == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    new_data = item.model_dump()
    new_data["id"] = item_id
    items[idx] = new_data
    await write_json("services", items)
    return new_data


@api.delete("/services/{item_id}")
async def delete_service(item_id: str, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("services", [])
    new_items = [x for x in items if x.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    await write_json("services", new_items)
    return {"ok": True}


# ---------- ADMIN: reviews ----------


@api.get("/reviews")
async def list_reviews() -> list:
    return await _sorted_load("reviews", INITIAL_REVIEWS)


@api.post("/reviews")
async def create_review(item: ReviewItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("reviews", [])
    d = item.model_dump()
    d["id"] = _id()
    if not d.get("order"):
        d["order"] = (max([i.get("order", 0) for i in items]) + 1) if items else 1
    items.append(d)
    await write_json("reviews", items)
    return d


@api.put("/reviews/{item_id}")
async def update_review(item_id: str, item: ReviewItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("reviews", [])
    idx = next((i for i, x in enumerate(items) if x.get("id") == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    new_data = item.model_dump()
    new_data["id"] = item_id
    items[idx] = new_data
    await write_json("reviews", items)
    return new_data


@api.delete("/reviews/{item_id}")
async def delete_review(item_id: str, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("reviews", [])
    new_items = [x for x in items if x.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    await write_json("reviews", new_items)
    return {"ok": True}


# ---------- ADMIN: contacts ----------


@api.get("/contacts")
async def get_contacts() -> dict:
    return await read_json("contacts", INITIAL_CONTACTS)


@api.put("/contacts")
async def update_contacts(req: ContactsModel, _: dict = Depends(require_admin)) -> dict:
    data = req.model_dump()
    await write_json("contacts", data)
    return data


# ---------- ADMIN: portfolio ----------


@api.get("/portfolio")
async def list_portfolio() -> list:
    return await _sorted_load("portfolio", INITIAL_PORTFOLIO)


@api.post("/portfolio")
async def create_portfolio(item: PortfolioItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("portfolio", [])
    d = item.model_dump()
    d["id"] = _id()
    if not d.get("order"):
        d["order"] = (max([i.get("order", 0) for i in items]) + 1) if items else 1
    items.append(d)
    await write_json("portfolio", items)
    return d


@api.put("/portfolio/{item_id}")
async def update_portfolio(item_id: str, item: PortfolioItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("portfolio", [])
    idx = next((i for i, x in enumerate(items) if x.get("id") == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Не найдено")
    new_data = item.model_dump()
    new_data["id"] = item_id
    items[idx] = new_data
    await write_json("portfolio", items)
    return new_data


@api.delete("/portfolio/{item_id}")
async def delete_portfolio(item_id: str, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("portfolio", [])
    new_items = [x for x in items if x.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Не найдено")
    await write_json("portfolio", new_items)
    return {"ok": True}


# ---------- ADMIN: masters ----------


@api.get("/masters")
async def list_masters() -> list:
    return await _sorted_load("masters", INITIAL_MASTERS)


@api.post("/masters")
async def create_master(item: MasterItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("masters", [])
    d = item.model_dump()
    d["id"] = _id()
    if not d.get("order"):
        d["order"] = (max([i.get("order", 0) for i in items]) + 1) if items else 1
    items.append(d)
    await write_json("masters", items)
    return d


@api.put("/masters/{item_id}")
async def update_master(item_id: str, item: MasterItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("masters", [])
    idx = next((i for i, x in enumerate(items) if x.get("id") == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Не найдено")
    new_data = item.model_dump()
    new_data["id"] = item_id
    items[idx] = new_data
    await write_json("masters", items)
    return new_data


@api.delete("/masters/{item_id}")
async def delete_master(item_id: str, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("masters", [])
    new_items = [x for x in items if x.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Не найдено")
    await write_json("masters", new_items)
    return {"ok": True}


# ---------- ADMIN: FAQ ----------


@api.get("/faq")
async def list_faq() -> list:
    return await _sorted_load("faq", INITIAL_FAQ)


@api.post("/faq")
async def create_faq(item: FAQItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("faq", [])
    d = item.model_dump()
    d["id"] = _id()
    if not d.get("order"):
        d["order"] = (max([i.get("order", 0) for i in items]) + 1) if items else 1
    items.append(d)
    await write_json("faq", items)
    return d


@api.put("/faq/{item_id}")
async def update_faq(item_id: str, item: FAQItem, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("faq", [])
    idx = next((i for i, x in enumerate(items) if x.get("id") == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Не найдено")
    new_data = item.model_dump()
    new_data["id"] = item_id
    items[idx] = new_data
    await write_json("faq", items)
    return new_data


@api.delete("/faq/{item_id}")
async def delete_faq(item_id: str, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("faq", [])
    new_items = [x for x in items if x.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Не найдено")
    await write_json("faq", new_items)
    return {"ok": True}


# ---------- ADMIN: brands ----------


@api.get("/brands")
async def list_brands() -> list:
    return await read_json("brands", INITIAL_BRANDS)


@api.put("/brands/{slug}")
async def update_brand(slug: str, req: BrandUpdate, _: dict = Depends(require_admin)) -> dict:
    brands = await read_json("brands", INITIAL_BRANDS)
    idx = next((i for i, b in enumerate(brands) if b.get("slug") == slug), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Бренд не найден")
    changes = {k: v for k, v in req.model_dump().items() if v is not None}
    if "price_overrides" in changes:
        changes["price_overrides"] = _normalize_services(changes["price_overrides"])
    brands[idx] = {**brands[idx], **changes}
    await write_json("brands", brands)
    return brands[idx]


# ---------- ADMIN: stats ----------


@api.get("/stats")
async def get_stats() -> dict:
    return await read_json("stats", INITIAL_STATS)


@api.put("/stats")
async def update_stats(req: StatsModel, _: dict = Depends(require_admin)) -> dict:
    data = req.model_dump()
    await write_json("stats", data)
    return data


# ---------- ADMIN: leads ----------


@api.get("/leads")
async def list_leads(_: dict = Depends(require_admin)) -> list:
    items = await read_json("leads", [])
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


@api.delete("/leads/{item_id}")
async def delete_lead(item_id: str, _: dict = Depends(require_admin)) -> dict:
    items = await read_json("leads", [])
    new_items = [x for x in items if x.get("id") != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    await write_json("leads", new_items)
    return {"ok": True}


# ---------- ADMIN: upload ----------


@api.post("/upload")
async def upload_file(
    file: UploadFile = File(...), _: dict = Depends(require_admin)
) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Файл не указан")
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTS:
        raise HTTPException(status_code=400, detail=f"Разрешены только: {', '.join(sorted(ALLOWED_IMAGE_EXTS))}")
    fname = f"{uuid.uuid4().hex}{ext}"
    path = UPLOAD_DIR / fname
    async with aiofiles.open(path, "wb") as out:
        content = await file.read()
        if len(content) > 8 * 1024 * 1024:  # 8 MB
            raise HTTPException(status_code=400, detail="Файл слишком большой (максимум 8 МБ)")
        await out.write(content)
    url = f"/uploads/{fname}"
    return {"url": url, "filename": fname, "size": len(content)}




# ---------- SERVER-SIDE SEO + React build serving ----------


def _frontend_build_dir() -> Optional[Path]:
    env_dir = os.environ.get("FRONTEND_BUILD_DIR")
    candidates = []
    if env_dir:
        candidates.append(Path(env_dir))
    candidates.extend(
        [
            ROOT_DIR / "build",
            ROOT_DIR / "frontend" / "build",
            ROOT_DIR.parent / "frontend" / "build",
        ]
    )

    for candidate in candidates:
        index_file = candidate / "index.html"
        if index_file.exists():
            return candidate.resolve()
    return None


def _public_origin(request: Request) -> str:
    return os.environ.get("PUBLIC_SITE_URL", str(request.base_url).rstrip("/"))


def _escape(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _plain_phone(phone: str) -> str:
    return re.sub(r"[^+\d]", "", phone or "")


def _local_business_schema_for_server(origin: str, contacts: dict, stats: dict, image: str) -> dict:
    phone = (contacts.get("phones") or [SITE_PHONE_FALLBACK])[0]
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": contacts.get("company_name") or "Ремонт холодильников в Минске",
        "url": origin,
        "image": image,
        "telephone": _plain_phone(phone),
        "priceRange": "30-400 BYN",
        "areaServed": "Минск",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": contacts.get("address") or "Минск",
            "addressLocality": "Минск",
            "addressCountry": "BY",
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "08:00",
                "closes": "22:00",
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": stats.get("rating", 5),
            "reviewCount": stats.get("reviews_count", 234),
        },
    }


SITE_PHONE_FALLBACK = "+375 (29) 609-54-31"


async def _seo_payload_for_path(path: str, request: Request) -> dict:
    origin = _public_origin(request)
    contacts = await read_json("contacts", INITIAL_CONTACTS)
    stats = await read_json("stats", INITIAL_STATS)
    brands = await read_json("brands", INITIAL_BRANDS)
    phone = (contacts.get("phones") or [SITE_PHONE_FALLBACK])[0]
    image = os.environ.get("DEFAULT_OG_IMAGE") or f"{origin}/assets/fridge-repair-hero.svg"
    clean_path = "/" + path.strip("/") if path else "/"

    payload = {
        "title": "Ремонт холодильников в Минске — выезд за 30 минут, гарантия 1 год",
        "description": "Профессиональный ремонт холодильников всех популярных марок на дому в Минске. Гарантия 1 год, фиксированные цены, без выходных 8:00–22:00.",
        "canonical": f"{origin}{clean_path if clean_path != '/' else '/'}",
        "image": image,
        "robots": "index,follow",
        "json_ld": [_local_business_schema_for_server(origin, contacts, stats, image)],
    }

    brand_match = re.fullmatch(r"/?brand/([a-z0-9-]+)/?", path.strip("/"))
    if brand_match:
        slug = brand_match.group(1)
        brand = next((b for b in brands if b.get("slug") == slug), None)
        if brand:
            payload["title"] = f"Ремонт холодильников {brand.get('name')} в Минске — выезд мастера, гарантия"
            payload["description"] = brand.get("meta_description") or f"Ремонт холодильников {brand.get('name')} в Минске на дому. Отдельный прайс для бренда, диагностика, запчасти и гарантия 1 год. Звоните: {phone}."
            payload["canonical"] = f"{origin}/brand/{slug}"
            payload["json_ld"].append(
                {
                    "@context": "https://schema.org",
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{origin}/"},
                        {"@type": "ListItem", "position": 2, "name": brand.get("name"), "item": f"{origin}/brand/{slug}"},
                    ],
                }
            )
    elif path.strip("/").startswith("admin"):
        payload["title"] = "Админ-панель — ремонт холодильников"
        payload["description"] = "Служебная страница администрирования сайта."
        payload["robots"] = "noindex,nofollow"
        payload["json_ld"] = []

    return payload


def _upsert_meta_tag(document: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, document, count=1, flags=re.IGNORECASE | re.DOTALL)
    if count:
        return updated
    return document.replace("</head>", f"  {replacement}\n</head>")


def _inject_seo(index_html: str, seo: dict) -> str:
    title = _escape(seo.get("title"))
    description = _escape(seo.get("description"))
    canonical = _escape(seo.get("canonical"))
    image = _escape(seo.get("image"))
    robots = _escape(seo.get("robots") or "index,follow")

    document = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", index_html, count=1, flags=re.IGNORECASE | re.DOTALL)
    document = _upsert_meta_tag(
        document,
        r"<meta\s+name=[\"']description[\"'][^>]*>",
        f'<meta name="description" content="{description}" />',
    )
    document = _upsert_meta_tag(
        document,
        r"<meta\s+name=[\"']robots[\"'][^>]*>",
        f'<meta name="robots" content="{robots}" />',
    )

    # Remove old server-generated block and insert fresh tags before </head>.
    document = re.sub(
        r"\n\s*<!-- SERVER_SEO_START -->.*?<!-- SERVER_SEO_END -->\s*\n",
        "\n",
        document,
        flags=re.IGNORECASE | re.DOTALL,
    )
    json_ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(item, ensure_ascii=False)}</script>'
        for item in seo.get("json_ld", [])
    )
    server_block = f"""
    <!-- SERVER_SEO_START -->
    <link rel="canonical" href="{canonical}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{image}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image}" />
    {json_ld}
    <!-- SERVER_SEO_END -->
"""
    return document.replace("</head>", f"{server_block}</head>")

# ---------- App wiring ----------


app.include_router(api)

# Serve uploads
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exc_handler(request, exc: HTTPException):  # type: ignore[override]
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
async def robots_txt(request: Request) -> str:
    origin = _public_origin(request)
    return f"User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: {origin}/sitemap.xml\n"


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml(request: Request) -> Response:
    origin = _public_origin(request)
    brands = await read_json("brands", INITIAL_BRANDS)
    urls = [f"{origin}/"]
    urls.extend(f"{origin}/brand/{b.get('slug')}" for b in brands if b.get("slug"))
    body = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *[f"  <url><loc>{_escape(url)}</loc><changefreq>weekly</changefreq><priority>{'1.0' if url.endswith('/') else '0.8'}</priority></url>" for url in urls],
            '</urlset>',
        ]
    )
    return Response(content=body, media_type="application/xml")


@app.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
async def serve_react_app(full_path: str, request: Request):
    """Serve React build through FastAPI and inject route-specific SEO into index.html."""
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")

    build_dir = _frontend_build_dir()
    if not build_dir:
        raise HTTPException(
            status_code=404,
            detail="React build not found. Run npm run build and set FRONTEND_BUILD_DIR if needed.",
        )

    requested = (build_dir / full_path).resolve()
    try:
        requested.relative_to(build_dir)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")

    if requested.is_file():
        return FileResponse(requested)

    # Missing static asset should be a real 404, not the SPA index.
    if "." in Path(full_path).name:
        raise HTTPException(status_code=404, detail="Not found")

    index_file = build_dir / "index.html"
    index_html = index_file.read_text(encoding="utf-8")
    seo = await _seo_payload_for_path(full_path, request)
    return HTMLResponse(_inject_seo(index_html, seo))
