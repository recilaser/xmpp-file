


from sanic import Sanic
from sanic.response import json
from config import  CONFIG
import asyncio

from xmppfile.db import setup_connection, close_connection

from xmppfile.openapi import bp


#from sanic_session import RedisSessionInterface

from sanic.websocket import WebSocketProtocol
import socket

app = Sanic()
app.config.from_object(CONFIG)
app.blueprint(bp)
#app.db = await ConnectionPool(loop=loop).init(app.config['DB_CONFIG'])


#普通请求http连接
@app.route("/json")
async  def rn(request):
    return json('hello word3332233')

#websocket连接
@app.websocket("/scokit")
async def feed(request, ws):
    try:
        while True:
            data = 'hello  wj!'
            print('Sending: ' + data)
            await ws.send(data)
            data = await ws.recv()
            print('Received: ' + data)
    except Exception as e:
        print(e)


#连接数据库
async def start_db(app, loop):
    _data_pool = await setup_connection(app, loop)
    bp.pool = _data_pool


#断开数据库
async def close_db(app,loop):
    await close_connection(app, loop)

 #before_server_start：在服务器启动之前执行
@app.listener('before_server_start')
async def before_server_start(app, loop):
    pass

@app.listener('after_server_start')
async def after_server_start(app, loop):

    await start_db(app,loop)


@app.listener('before_server_stop')
async def before_server_stop(app, loop):

    await close_db(app,loop)



if __name__ =="__main__":
    '''
      sanic 启动时创建数据库连接池，服务正常结束时关闭连接池
      '''
  #  session = RedisSessionInterface(redis_getter=startup_redis_pool)


    #before_server_start：在服务器启动之前执行
    #after_server_start：在服务器启动之后执行
    #before_server_stop：在服务器关闭之前执行
    #after_server_stop：在服务器关闭之后执行

    app.run(host='127.0.0.1',port=8888,debug=app.config['DEBUG'],workers=app.config['WORKERS'])

