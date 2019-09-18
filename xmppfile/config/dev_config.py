from .config import Config
#开发环境
class DevConfig(Config):

    DEBUG = True
    #数据库连接
    DB_CONFIG = {
        'host': '127.0.0.1',
        'user': 'odoo',
        'password': 'odoo',
        'port': '5432',
        'database': 'xmpp'
    }
