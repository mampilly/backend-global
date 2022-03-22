'''Redis Connection'''
import os
import redis
from app.core.config import config

redis_pool = None


def init():
    '''Redis Initilization'''
    global redis_pool
    print("PID %d: initializing redis pool..." % os.getpid())
    redis_pool = redis.ConnectionPool(
        host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
    return redis_pool


def get_redis_connection():
    '''recive redis connection from pool'''
    redis_conn = redis.Redis(connection_pool=init())
    return redis_conn
