# app/cache.py
import json
import hashlib
from typing import Any
from app.database import redis_client

# Default TTL constants (in seconds)
SEARCH_CACHE_TTL = 43200  # 12 hours
CHAT_THREAD_TTL = 86400   # 24 hours

def build_search_key(query: str, location: str = "") -> str:
    """Generates a deterministic Redis key hash for search parameters."""
    normalized = f"{query.lower().strip()}:{location.lower().strip()}"
    query_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return f"search:{query_hash}"

async def get_cached_search(query: str, location: str = "") -> list[dict] | None:
    """Retrieves parsed search results from Redis if present."""
    key = build_search_key(query, location)
    cached_data = await redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

async def set_cached_search(query: str, parsed_results: list[dict], location: str = "", ttl: int = SEARCH_CACHE_TTL) -> None:
    """Stores parsed search results in Redis with a 12h default TTL."""
    key = build_search_key(query, location)
    await redis_client.set(
        name=key,
        value=json.dumps(parsed_results),
        ex=ttl
    )

async def append_chat_turn(thread_id: str, role: str, content: str) -> None:
    """Appends a turn to the chat thread list and refreshes the 24h TTL."""
    key = f"chat:{thread_id}"
    payload = json.dumps({"role": role, "content": content})
    
    async with redis_client.pipeline() as pipe:
        pipe.rpush(key, payload)
        pipe.expire(key, CHAT_THREAD_TTL)
        await pipe.execute()

async def get_chat_turns(thread_id: str) -> list[dict]:
    """Retrieves all chat messages for an active thread."""
    key = f"chat:{thread_id}"
    raw_turns = await redis_client.lrange(key, 0, -1)
    return [json.loads(turn) for turn in raw_turns]