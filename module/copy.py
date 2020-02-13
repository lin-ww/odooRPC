#!/usr/bin/env python3
from odooRPC import OdooRPC
from tools import Record, safe_eval
import sys

__author__ = 'Lin Wenwen'
__mail__ = '514706098@qq.com'
__date__ = '2020-02-10'
__doc__ = ''
__version__ = ''
YAML_EXAMPLE = """
- copy:
    origin:
      url: http://127.0.0.1:8069
      username: 123
      password: 123
      db: demo
      model: res.partner
      domain: "[(1, '=', 1)]"
      fields: false
    destination:
      - url: http://127.0.0.1:8069
        username: 123
        password: 123
        db: demo
        model: res.partner
        domain: "[('name', '=', 'origin.name')]"
        copy_fields:
          name: name
"""


def main(book):
    origin_conf = book['copy'].get('origin') or {}
    destination_confs = book['copy'].get('destination') or {}
    origin_rpc = OdooRPC(origin_conf.get('url'), origin_conf.get('db'), origin_conf.get('username'), origin_conf.get('password'))
    origin_domain = safe_eval(str(origin_conf.get('domain') or '[]'))
    origin_model = str(origin_conf.get('model'))
    origin_fields = origin_conf.get('fields')
    origin_results = origin_rpc.execute_kw(origin_model, 'search_read', [origin_domain], {'fields': origin_fields})
    for res in origin_results:
        origin = Record(res)
        for destination_conf in destination_confs:
            destination_rpc = OdooRPC(destination_conf.get('url'), destination_conf.get('db'), destination_conf.get('username'), destination_conf.get('password'))
            destination_model = str(destination_conf.get('model'))
            copy_fields = destination_conf.get('copy_fields', {})
            create_val = {field_d: getattr(origin, field_o) for field_o, field_d in copy_fields.items() if field_o in res}
            sys.stdout.write('Create new record according to origin_record(%s)...\n' % (origin.id))
            sys.stdout.write('%s\n' % destination_rpc.execute_kw(destination_model, 'create', [create_val]))
