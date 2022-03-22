'''Rate limiting via Redis'''
import logging
from datetime import timedelta
from redis import Redis
from app.core.database.cache import get_redis_connection
from app.exceptions.application_exception import exception


def rate_request(key, limit, period):
    """Rate request wrapping redis connection"""
    return request_is_limited(get_redis_connection(), key, limit, period)


def request_is_limited(r: Redis, key: str, limit: int, period: timedelta):
    """Rate Limiting"""
    if r.setnx(key, limit):
        r.expire(key, int(period.total_seconds()))
    bucket_val = r.get(key)
    if bucket_val and int(bucket_val) > 0:
        r.decrby(key, 1)
        return False
    return True


def rate_limit(auth, limit, period):
    """Rate limit main function"""
    if rate_request(auth, limit, timedelta(seconds=period)):
        raise exception.too_many_rquests()
    logging.info('✅ Request is allowed')
    return True
