#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from abc import abstractmethod

import requests


class ServiceInvoker:

    @abstractmethod
    def invoke(self) -> str:
        pass

    @staticmethod
    def link(url: str, pars: dict, pattern: str = 'get') -> str:
        assert pattern in ('get', 'post')
        return (requests.get(url, pars)).text if pattern == 'get' else requests.post(url, pars).text


class OCRInvoker(ServiceInvoker):
    url = r'http://192.168.68.38:5678'
    params = {'path': '/usr/local/src/data/doc_imgs/2014东刑初字第0100号_诈骗罪208页.pdf/img-0008.jpg'}
    pattern = 'get'

    def __init__(self, pars: dict):
        self.params = pars

    def invoke(self)->str:
        return ServiceInvoker.link(self.url, self.params, pattern='get')


class Context:
    invoker: ServiceInvoker = None

    def __init__(self, invoker: ServiceInvoker):
        self.invoker = invoker

    def invoke(self)->str:
        return self.invoker.invoke()


