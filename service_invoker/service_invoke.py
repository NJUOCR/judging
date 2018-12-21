#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from abc import abstractmethod

import requests


class ServiceInvoker:

    @abstractmethod
    def invoke(self, params) -> str:
        pass

    @staticmethod
    def link(url: str, pars: dict, pattern: str = 'get') -> str or False:
        assert pattern in ('get', 'post')
        try:
            return (requests.get(url, pars)).text if pattern == 'get' else requests.post(url, pars).text
        except Exception:
            return False

    @staticmethod
    def which(service_name: str):
        service_name = service_name.lower()
        assert service_name in ('ocr', )
        if service_name == 'ocr':
            return OCRInvoker()


class OCRInvoker(ServiceInvoker):
    url = r'http://192.168.68.38:5678'
    # params = {'path': '/usr/local/src/data/doc_imgs/2014东刑初字第0100号_诈骗罪208页.pdf/img-0008.jpg'}
    pattern = 'get'

    def __init__(self):
        pass

    def invoke(self, params)->str:
        return ServiceInvoker.link(self.url, params, pattern='get')


class Context:
    invoker: ServiceInvoker = None

    def __init__(self, invoker: ServiceInvoker):
        self.invoker = invoker

    def invoke(self)->str:
        return self.invoker.invoke()


