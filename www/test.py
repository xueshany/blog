# http://www.cnblogs.com/weixia-blog/p/7257528.html
# test orm
# from orm import Model, StringField,IntegerField
#
# class User(Model):
#     __table__ = 'user'
#
#     id = IntegerField(primary_key = True)
#     name = StringField()
#
# user = User(id = 123, name ='Tommy')
#
# users = User.findAll()

#　test sql
import orm,asyncio
from models import User,Blog,Comment

@asyncio.coroutine
def test(loop):
    yield from orm.create_pool(loop=loop, user='root', password='123', database='awesome', port = 3306)
    u = User(name='dflhuang', email='dflhuang@qq.com', passwd='0123', image='about:blank', id='110')
    yield from u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()