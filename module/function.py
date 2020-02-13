#!/usr/bin/env python3
from odooRPC import OdooRPC
from tools import safe_eval
import sys

__author__ = 'Lin Wenwen'
__mail__ = '514706098@qq.com'
__date__ = '2020-02-10'
__doc__ = ''
__version__ = ''
YAML_EXAMPLE = """
- function:
    url: http://127.0.0.1:8069
    username: 123
    password: 123
    db: demo
    model: res.partner
    domain:
    function_name: "read"
    function_para_list: []
    function_para_dict:
      domain: "[(1,'=',1)]"
"""


def main(book):
    conf = book['function']
    rpc = OdooRPC(conf.get('url'), conf.get('db'), conf.get('username'), conf.get('password'))
    model = str(conf.get('model'))
    function_name = str(conf.get('function_name'))
    function_para_list = conf.get('function_para_list') or []
    function_para_dict = conf.get('function_para_dict') or {}
    domain = safe_eval(str(conf.get('domain', '[]')))
    if domain is False or domain is None:
        result = rpc.execute_kw(model, function_name, function_para_list, function_para_dict)
    else:
        ids = rpc.execute_kw(model, 'search', [domain])
        result = rpc.execute_kw(model, function_name, [ids] + function_para_list, function_para_dict)

    sys.stdout.write('{}\n'.format(result))
