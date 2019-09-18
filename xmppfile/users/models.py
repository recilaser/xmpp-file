
import datetime

from  peewee import (
    Model,
    DateTimeField,
    IntegerField,
    PrimaryKeyField,
    ForeignKeyField,    #外键
    CharField,
    BooleanField,
)


# 用户基本数据表
class cf_users(Model):

    id = PrimaryKeyField()

    accesskeysecret = CharField(max_length=255, verbose_name='私钥')

    account = CharField(max_length=255, verbose_name='账号')

    password = CharField(max_length=255, verbose_name='密码')

    odoouser_id = IntegerField(null=False, verbose_name='odoo用户id')

    nickname = CharField(max_length=255, verbose_name='用户昵称')

    code = CharField(max_length=255, verbose_name='用户节点编码')

    purview_level = IntegerField(null=False, verbose_name='权限等级分类')

    valid = CharField(verbose_name='账号是否有效')

    class Meta:
        database = 'db'
        # 这里是数据库链接，为了方便建立多个表，可以把这个部分提炼出来形成一个新的类#table_name = 'persons'  # 这里可以自定义表名


'''
      owner = pw.ForeignKeyField(rel_model=Person, null=False)
if __name__ == "__main__":
    # 创建表
    User.create_table()  # 创建User表
    Tweet.create_table()  # 创建Tweet表
'''




#基础字段
class cf_base(Model):

    # id = PrimaryKeyField()
    # name = CharField(max_length=128, verbose_name='role name')
    # create_time = DateTimeField(verbose_name='create time',
    #                         default=datetime.datetime.utcnow)
    # age = IntegerField(null=False, verbose_name="user's age")
    # sex = CharField(max_length=32, verbose_name="user's sex")
    pass


#关系型 分类字段
class cf_relation_base(Model):
    # id = PrimaryKeyField()
    # name = CharField(max_length=128, verbose_name='role name')
    # create_time = DateTimeField(verbose_name='create time',
    #                             default=datetime.datetime.utcnow)
    # age = IntegerField(null=False, verbose_name="user's age")
    # sex = CharField(max_length=32, verbose_name="user's sex")
    pass


#操作基础表
class cf_operate_base(Model):

    pass





#权限表
class cf_purvuew(Model):
    pass


#业务文件管理表
class cf_files(Model):
    pass


#文件内容表
class cf_content(Model):
    pass
