import  os

class Config():
    #Application config
    TIMEZONE = 'Asia/Beijing'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    REQUEST_MAX_SIZE =	100000000	#请求数据的最大值 (bytes)
    REQUEST_MAX_SIZE = 200000000
    REQUEST_BUFFER_QUEUE_SIZE =	100	# 流缓存队列的大小
    REQUEST_TIMEOUT	= 30	 # 请求超时时间 (sec)
    RESPONSE_TIMEOUT	= 30	# 响应超时时间 (sec)
    KEEP_ALIVE	 = True	 #是否保持长链接
    KEEP_ALIVE_TIMEOUT	= 5	 #保持TCP链接的时间 (sec)
    GRACEFUL_SHUTDOWN_TIMEOUT	= 15.0	#等待强制关闭非空闲链接的时间 (sec)
    ACCESS_LOG	= True	#是否启用访问日志
    WORKERS = 4   #接收的进程数

    # webSocket 相关设置
    WEBSOCKET_MAX_SIZE = 2 ** 20  # 请求数据的最大值 (bytes)
    WEBSOCKET_MAX_QUEUE = 32  # 请求队列
    WEBSOCKET_READ_LIMIT = 2 ** 16
    WEBSOCKET_WRITE_LIMIT = 2 ** 16

