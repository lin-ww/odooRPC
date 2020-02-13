#!/usr/bin/env python3
import argparse
import os
import sys
import yaml
import xmlrpc.client
bindir = os.path.dirname(os.path.realpath(__file__))
__author__ = 'Lin Wenwen'
__mail__ = '514706098@qq.com'
__date__ = '2020-02-10'
__doc__ = ''
__version__ = ''


class Args:
    def __new__(self, test=False):
        parser = argparse.ArgumentParser(
            description='author: {0}\nmail: {1}\ndate: {2}\nversion: {3}\n\n{4}'.format(__author__, __mail__, __date__, __version__, __doc__),
            epilog='', formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-i', help='input', dest='input', type=open, required=True)
        if test:
            return parser.parse_args(['-i', '{}/test.yml'.format(bindir)])
        else:
            return parser.parse_args()


class OdooRPC(xmlrpc.client.ServerProxy):
    def __init__(self, url, db, username, password):
        self.username = str(username)
        self.password = str(password)
        self.db = str(db)
        self.url = str(url)
        self.uid = self.authenticate()

    def authenticate(self, para={}):
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        return common.authenticate(self.db, self.username, self.password, para)

    def execute_kw(self, model, method, para_list=[], para_dict={}):
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        result = models.execute_kw(self.db, self.uid, self.password, model, method, para_list, para_dict)
        return result


def main():
    args = Args(test=True)
    books = yaml.load(args.input, Loader=yaml.FullLoader)
    for book in books:
        for func in book:
            __import__("module.%s" % func, fromlist=[func]).main(book)


if __name__ == '__main__':
    main()
