"""JSON file storage helpers."""
from __future__ import annotations
import json
import os
import asyncio
from pathlib import Path
from typing import Any, Optional

import aiofiles

ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

_locks: dict[str, asyncio.Lock] = {}


def _lock_for(name: str) -> asyncio.Lock:
    if name not in _locks:
        _locks[name] = asyncio.Lock()
    return _locks[name]


def _path_for(name: str) -> Path:
    safe = name.replace("/", "_").replace("..", "")
    return DATA_DIR / f"{safe}.json"


async def read_json(name: str, default: Any) -> Any:
    path = _path_for(name)
    if not path.exists():
        return default
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        raw = await f.read()
    if not raw.strip():
        return default
    return json.loads(raw)


async def write_json(name: str, data: Any) -> None:
    path = _path_for(name)
    lock = _lock_for(name)
    async with lock:
        tmp = path.with_suffix(".tmp")
        async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))
        os.replace(tmp, path)


async def read_or_seed(name: str, seed: Any) -> Any:
    path = _path_for(name)
    if not path.exists():
        await write_json(name, seed)
        return seed
    return await read_json(name, seed)


async def ensure_seeded(name: str, seed: Any) -> Any:
    """Write seed only if file doesn't exist."""
    path = _path_for(name)
    if not path.exists():
        await write_json(name, seed)
    return await read_json(name, seed)
