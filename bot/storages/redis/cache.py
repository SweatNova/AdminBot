import json
from typing import Any, Optional
from bot.storages.redis.client import redis_client

async def get_cache(key: str) -> Optional[Any]:
	data = await redis_client.get(key)
	if not data:
		return None
	return json.loads(data)

async def set_cache(key: str, ttl: int, value: Any):
	await redis_client.setex(
		key,
		ttl,
		json.dumps(value, default=str)
	)

async def delete_cache(key: str):
	await redis_client.delete(key)
