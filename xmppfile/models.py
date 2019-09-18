
from xmppfile import fields


FIELDS_TO_PGTYPES = {
    fields.boolean: 'bool',
    fields.integer: 'int4',
    fields.text: 'text',
    fields.html: 'text',
    fields.date: 'date',
    fields.datetime: 'timestamp',
    fields.binary: 'bytea',
    fields.many2one: 'int4',
    fields.serialized: 'text',
}