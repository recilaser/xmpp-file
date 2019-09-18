
import logging
from datetime import date, datetime
from collections import defaultdict
from peewee import ModelBase
from playhouse.postgres_ext import ArrayField

# 基础类型
#
# Char：字符型，使用size参数定义字符串长度。
# Text：文本型，无长度限制。
# Boolean：布尔型（True，False）
# Interger：整型
# Float：浮点型，使用digits参数定义整数部分和小数部分位数。如digits=(10,6)
# Datetime：日期时间型
# Date：日期型
# Binary：二进制型
# selection：下拉框字段。


# 关系类型
#
# One2many：一对多关系。
#
# 定义：otm = fields.One2many("关联对象 _name", "关联字段",string="字段显示名",...)
# 例：analytic_line_ids = fields.One2many('account.analytic.line', 'move_id', string='Analytic lines')"
#
# Many2one
#
# 定义：mto = fields.Many2one("关联对象 _name", string="字段显示名",...)
# 可选参数：ondelete，可选值为‘cascade’和‘null’，缺省为null。表示one端删除时many端是否级联删除。
#
# Many2many
#
# 定义：mtm = fields.Many2many("关联对象 _name", "关联表/中间表","关联字段1","关联字段2",string="字段显示名",...)
# 其中，关联字段、关联表/中间表可不填，中间表缺省为：表1_表2_rel
# 例：partner_id= fields.Many2many("res.partner", string="字段显示名",...)"



#
# create 创建记录
# 原型：def create(self, vals)
# vals：记录属性值字典
#
# search 查找记录
# 原型：def search(self, args, offset=0, limit=None, order=None, count=False)
# args：domain格式的条件列表；offset：结果忽略条数；limit：最大查询条数
#
# read 读取记录属性值
# 返回指定ids记录的指定fields字段值，采用列表加字典的数据结构（[{},{},…]）返回。
# 原型：def read(self, fields=None, load='_classic_read'):
# fields：列表可指定要读取的属性名称
#
# search_read
# 原型：def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None)
# 用法即search方法与read方法相结合。
#
# unlink 删除记录
# 原型：def unlink(self)
#
# write 修改记录
# 原型：def write(self, vals)
# vals：修改属性值字典

logger = logging.getLogger('sanic')

class Field:
    def __init__(self, description=None, required=None, name=None):
        self.name = name
        self.description = description
        self.required = required

    def serialize(self):
        output = {}
        if self.name:
            output['name'] = self.name
        if self.description:
            output['description'] = self.description
        if self.required is not None:
            output['required'] = self.required
        return output
# ---------------------------------------------------------
# Simple fields
# ---------------------------------------------------------
class Integer(Field):
    def serialize(self):
        return {
            "type": "integer",
            "format": "int64",
            **super().serialize()
        }


class String(Field):
    def serialize(self):
        return {
            "type": "string",
            **super().serialize()
        }


class Boolean(Field):
    def serialize(self):
        return {
            "type": "boolean",
            **super().serialize()
        }


class Tuple(Field):
    pass


class Date(Field):
    def serialize(self):
        return {
            "type": "date",
            **super().serialize()
        }


class DateTime(Field):
    def serialize(self):
        return {
            "type": "dateTime",
            **super().serialize()
        }


class Dictionary(Field):
    def __init__(self, fields=None, **kwargs):
        self.fields = fields or {}
        super().__init__(**kwargs)

    def serialize(self):
        return {
            "type": "object",
            "properties": {key: serialize_schema(schema) for key, schema in self.fields.items()},
            **super().serialize()
        }


class List(Field):
    def __init__(self, items=None, *args, **kwargs):
        self.items = items or []
        if type(self.items) is not list:
            self.items = [self.items]
        super().__init__(*args, **kwargs)

    def serialize(self):
        if len(self.items) > 1:
            items = Tuple(self.items).serialize()
        elif self.items:
            items = serialize_schema(self.items[0])
        return {
            "type": "array",
            "items": items
        }


class Float(Field):
    def __init__(self, fields=None, **kwargs):
        self.fields = fields or {}
        super().__init__(**kwargs)
    def serialize(self):
        return {
            "type": "real",
            **super().serialize()
        }


class many2one(Field):
    pass

class one2many(Field):
   pass
class many2many(Field):
   pass


definitions = {}


class Object(Field):
    def __init__(self, cls, *args, object_name=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.cls = cls
        self.object_name = object_name or cls.__name__

        if self.cls not in definitions:
            definitions[self.cls] = (self, self.definition)

    @property
    def definition(self):
        return {
            "type": "object",
            "properties": {
                key: serialize_schema(schema)
                for key, schema in self.cls.__dict__.items()
                if not key.startswith("_")
            },
            **super().serialize()
        }

    def serialize(self):
        return {
            # "type": "object",

            # "schema": {
            #    "$ref": "#/definitions/{}".format(self.object_name)
            # },
            "$ref": "#/definitions/{}".format(self.object_name),
            **super().serialize()
        }


class PeeweeObject(Field):
    def __init__(self, cls, *args, object_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cls = cls
        self.object_name = object_name or cls.__name__

        if self.cls not in definitions:
            definitions[self, cls] = (self, self.definition)

    @property
    def definition(self):
        return {
            'type': 'object',
            'properties': {
                value.field.column_name if value.field.column_name else key: self.field_serialize(value)
                for key, value in self.cls.__dict__.items()
                if not key.startswith('_') and key != 'DoesNotExist'
            },
            **super().serialize()
        }

    def db_field_serialize(self, ttype, desc=None, format=None, related=None):
        if related:
            schema_type = type(related)
            if issubclass(schema_type, ModelBase):
                return PeeweeObject(related).serialize()
            if schema_type is type:
                if ttype == 'array': return List(related).serialize()
                if ttype == 'json': return Dictionary(related).serialize()
                return Object(related).serialize()
        else:
            value = {'type': ttype}
            if desc: value.update({'description': desc})
            if format: value.update({'format': format})
            return value

    def field_serialize(self, schema):
        field = schema.field
        db_field = field.field_type
        if isinstance(field, ArrayField):
            return self.db_field_serialize('array', field.verbose_name, None,
                                           field.help_text)
        elif db_field == 'DEFAULT':
            return self.db_field_serialize('string', field.verbose_name, None,
                                           field.help_text)
        elif db_field == 'INT':
            if hasattr(field, 'rel_model'):
                return self.db_field_serialize('integer', field.verbose_name,
                                               None, field.rel_model)
            return self.db_field_serialize('integer', field.verbose_name, None,
                                           field.help_text)
        elif db_field == 'BIGINT':
            return self.db_field_serialize('integer', field.verbose_name,
                                           'int64', field.help_text)
        elif db_field == 'SMALLINT':
            return self.db_field_serialize('integer', field.verbose_name,
                                           'int', field.help_text)
        elif db_field == 'AUTO':
            return self.db_field_serialize('integer', field.verbose_name,
                                           'int', field.help_text)
        elif db_field == 'FLOAT':
            return self.db_field_serialize('number', field.verbose_name,
                                           'float', field.help_text)
        elif db_field == 'DOUBLE':
            return self.db_field_serialize('number', field.verbose_name,
                                           'double', field.help_text)
        elif db_field == 'DECIMAL':
            return self.db_field_serialize('number', field.verbose_name,
                                           None, field.help_text)
        elif db_field == 'VARCHAR' or db_field == 'CHAR' or db_field == "TEXT":
            return self.db_field_serialize('string', field.verbose_name,
                                           None, field.help_text)
        elif db_field == 'UUID':
            return self.db_field_serialize('string', field.verbose_name,
                                           'uuid', field.help_text)
        elif db_field == 'BLOB':
            return self.db_field_serialize('string', field.verbose_name,
                                           'binary', field.help_text)
        elif db_field == 'DATETIME':
            return self.db_field_serialize('string', field.verbose_name,
                                           'date-time', field.help_text)
        elif db_field == 'DATE':
            return self.db_field_serialize('string', field.verbose_name,
                                           'date', field.help_text)
        elif db_field == 'TIME':
            return self.db_field_serialize('string', field.verbose_name,
                                           'date-time', field.help_text)
        elif db_field == 'BOOL':
            return self.db_field_serialize('boolean', field.verbose_name, None,
                                           field.help_text)
        elif db_field == 'JSON' or db_field == 'JSONB':
            return self.db_field_serialize('object', field.verbose_name, None,
                                           field.help_text)

    def serialize(self):
        return {
            "$ref": "#/definitions/{}".format(self.object_name),
            **super().serialize()
        }


def serialize_schema(schema):
    schema_type = type(schema)
    # --------------------------------------------------------------- #
    # Class
    # --------------------------------------------------------------- #
    if schema_type is type:
        if issubclass(schema, Field):
            return schema().serialize()
        elif schema is dict:
            return Dictionary().serialize()
        elif schema is list:
            return List().serialize()
        elif schema is int:
            return Integer().serialize()
        elif schema is str:
            return String().serialize()
        elif schema is bool:
            return Boolean().serialize()
        elif schema is date:
            return Date().serialize()
        elif schema is datetime:
            return DateTime().serialize()
        else:
            return Object(schema).serialize()

    # --------------------------------------------------------------- #
    # Object
    # --------------------------------------------------------------- #
    else:
        if issubclass(schema_type, ModelBase):
            return PeeweeObject(schema).serialize()
        elif issubclass(schema_type, Field):
            return schema.serialize()
        elif schema_type is dict:
            return Dictionary(schema).serialize()
        elif schema_type is list:
            return List(schema).serialize()

    return {}