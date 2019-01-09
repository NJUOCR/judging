#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from abc import abstractmethod
import os
import requests
import json


class ServiceInvoker:

    @abstractmethod
    def invoke(self, params) -> str:
        pass

    @staticmethod
    def link(url: str, pars: dict, pattern: str = 'get') -> str or False:
        assert pattern in ('get', 'post')
        print('invoking outer service: %s \n %s' % (url, json.dumps(pars, ensure_ascii=False, indent=2)))
        try:
            return (requests.get(url, pars)).text if pattern == 'get' else requests.post(url, pars).text
        except Exception:
            return False

    @staticmethod
    def which(service_name: str):
        service_name = service_name.lower()
        assert service_name in ('ocr',)
        if service_name == 'ocr':
            return OCRInvoker()


class OCRInvoker(ServiceInvoker):
    url = 'http://172.18.0.2:555/'
    ocr_resource_root = '/usr/local/src'
    # params = {'path': '/usr/local/src/data/doc_imgs/2014东刑初字第0100号_诈骗罪208页.pdf/img-0008.jpg'}
    pattern = 'get'

    def __init__(self):
        pass

    def invoke(self, params: dict) -> str:
        params['path'] = OCRInvoker.ocr_resource_root + params['path']
        return ServiceInvoker.link(self.url, params, pattern='get')


class Context:
    invoker: ServiceInvoker = None

    def __init__(self, invoker: ServiceInvoker):
        self.invoker = invoker

    def invoke(self, params) -> str:
        return self.invoker.invoke(params)


if __name__ == '__main__':
    ocr = OCRInvoker()
    context = Context(ocr)
    print(context.invoke({'path': 'static/resources/media/查找被害人，确认死者身份/死亡时间/视听时间/课程表.png'}))
