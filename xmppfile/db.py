import  asyncpg

import logging
logger = logging.getLogger(__name__)


def log(sql, args=()):
    logger.info('SQL: %s' % sql)



async def startup_redis_pool():
#     # redis
#     _redis_pool = await asyncio_redis.Pool.create(host='127.0.0.1', port=6379, poolsize=10)
#     bp.redis = _redis_pool
#     return _redis_pool
    pass


'''
创建数据库连接池
监听数据库连接数变化
select * from pg_stat_activity;
'''
async def setup_connection(app, loop):
    global _pool
    logger.info('create database connection pool...')
    _pool = await asyncpg.create_pool(**app.config.DB_CONFIG,loop=loop,max_size=1000)
   # print('connection --success')
    logger.info('connection --success')
    return _pool



'''
关闭数据库
select * from pg_stat_activity;
'''
async  def close_connection(app,loop):

    await  _pool.close()
    logger.info('database pool died ')



'''
数据库基本方法封装
'''
async def select(sql, *args, size=None):
    log(sql, args)
    async with _pool.acquire() as con:
        rs = await con.fetch(sql, *args)
        logger.info('rows returned: %s' % len(rs))
        return rs


async def execute(sql, *args, autocommit=True):
    log(sql)
    async with _pool.acquire() as con:
        rs = await con.execute(sql, *args)
        return rs


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('$' + str(n+1))
    return ', '.join(L)
