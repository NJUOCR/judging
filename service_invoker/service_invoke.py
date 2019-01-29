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
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def which(service_name: str):
        service_name = service_name.lower()
        assert service_name in ('ocr',)
        if service_name == 'ocr':
            return OCRInvoker()


class OCRInvoker(ServiceInvoker):
    url = 'http://ocr4judging:4444/'
    ocr_resource_root = '/usr/local/src'
    # params = {'path': '/usr/local/src/data/doc_imgs/2014东刑初字第0100号_诈骗罪208页.pdf/img-0008.jpg'}
    pattern = 'get'

    def __init__(self):
        pass

    def invoke(self, params: dict) -> str:
        rs = ServiceInvoker.link(self.url, params, pattern='get')
        print(rs)
        return rs


class Context:
    invoker: ServiceInvoker = None

    def __init__(self, invoker: ServiceInvoker):
        self.invoker = invoker

    def invoke(self, params) -> str:
        return self.invoker.invoke(params)


if __name__ == '__main__':
    ocr = OCRInvoker()
    context = Context(ocr)
    print(context.invoke(
        {
            "path": "./static/resources/documents/津南检公诉刑诉【2018】222号/00000016.png",
            # "path": "./static/resources/documents/津南检公诉刑诉【2018】66号/00000135.png",
            # "path": "./static/resources/documents/津南检公诉刑诉【2018】632号/00000041.png",
            # "path": "./static/resources/documents/津南检公诉刑诉【2018】632号/00000098.png",
            "auxiliary": True,
            "x1": 0.1,
            "y1": 0.1,
            "x2": 0.9,
            "y2": 0.6
        }
    ))
