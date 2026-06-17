"""Telegram notification helper."""
import os
import logging
import httpx

logger = logging.getLogger(__name__)


async def notify_lead(lead: dict) -> bool:
    """Send lead to Telegram. Returns True on success, False otherwise."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id or token.startswith("MOCK") or chat_id.startswith("MOCK"):
        logger.info("[telegram] mock token/chat — skipping real send. lead=%s", lead.get("id"))
        return False

    text = (
        "🛠 <b>Новая заявка на ремонт холодильника</b>\n\n"
        f"👤 <b>Имя:</b> {lead.get('name', '—')}\n"
        f"📞 <b>Телефон:</b> {lead.get('phone', '—')}\n"
        f"🏷 <b>Бренд:</b> {lead.get('brand', '—')}\n"
        f"❗️ <b>Проблема:</b> {lead.get('problem', '—')}\n"
        f"💬 <b>Сообщение:</b> {lead.get('message', '—')}\n"
        f"🕒 <b>Создано:</b> {lead.get('created_at', '—')}\n"
        f"🔗 <b>Источник:</b> {lead.get('source', 'site')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                return True
            logger.warning("[telegram] non-200 response: %s %s", resp.status_code, resp.text)
            return False
    except Exception as exc:  # noqa: BLE001
        logger.warning("[telegram] error: %s", exc)
        return False
