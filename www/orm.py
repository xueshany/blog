# -*- coding: utf-8 -*-
# ORM ( Object Relational Mapping, 对象关系映射）
# http://www.cnblogs.com/weixia-blog/p/7257528.html
import logging
import asyncio
import aiomysql

def log(sql,args==()):
    logging.info('SQL: %s' % sql)

# Create connect pool
# Parameter: host,port,user,password,db,charset,autocommit
#            maxsize,minsize,loop
async def create_pool( loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    # 连接池由全局变量__pool存储，缺省情况下将编码设置为utf-8,自动提交事务
    __pool = awaite aiomysql.create_pool(
        host = kw.get('host':'location'),
        port = kw.get('port',3306),
        user = kw['user'],
        password = kw['db'],
        charset = kw.get('charset','utf-8'),
        autocommit = kw.get('maxsize',10),
        minisize = kw.get('minisize',1),
        loop = loop
    )

async def select(sql, args, size =None):
    # 执行select语句
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?','%s'),args or ())
            # await 协程中调用另一个协程，并直接返回子协程的结果
            # sql 语句占位符是？，mysql的占位符是%s，select（）函数在内部自动替换
            # 要始终坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击。
            if size:
            # 如果传入参数size，就通过fetchmany（）获得最多指定数量的记录
            # 否则通过fetchall（）获取所有记录
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs

async def execute(sql,args,autocommit=True):
    # 执行insert，update，delete语句
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # execute（）函数和select函数不同，cursor对象不返回结果集，是通过rowcount返回结果数
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return  affected


