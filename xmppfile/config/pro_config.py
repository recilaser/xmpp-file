from  .config import  Config
#生产环境
class ProConfig(Config):

    DEBUG = False
    #数据库连接
    # 数据库连接

DB_CONFIG = {
        'host': '127.0.0.1',
        'user': 'odoo',
        'password': 'odoo',
        'port': '5432',
        'database': 'xmpp'
    }