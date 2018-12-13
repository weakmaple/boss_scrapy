# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
from twisted.internet.defer import DeferredLock
import requests
import random
import json
from boss_scrapy.settings import DEFAULT_REQUEST_HEADERS,USER_AGENT_LIST
from boss_scrapy.try_to_getProxy import ProxyModel

class RandomProxy(object):

    def __init__(self):
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent

        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            #请求代理
            self.update_proxy()
            request.meta['proxy'] = self.current_proxy.proxy

    def process_response(self, request, response, spider):
        # 如果对方重定向（302）去验证码的网页，换掉代理IP
        # 'captcha' in response.url 指的是有时候验证码的网页返回的状态码是200，所以用这个作为辨识的标志
        if response.status != 200 or 'captcha' in response.url:
            # 如果来到这里，说明这个请求已经被boss直聘识别为爬虫了
            # 所以这个请求就相当于什么都没有获取到
            # 所以要重新返回request，让这个请求重新加入到调度中
            # 下次再发送
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            self.update_proxy()
            print('%s代理失效' % self.current_proxy.proxy)
            request.meta['proxy'] = self.current_proxy.proxy
            return request

        # 如果是正常的话，记得最后要返回response
        # 如果不返回，这个response就不会被传到爬虫那里去
        # 也就得不到解析
        return response

    def update_proxy(self):
        #lock是属于多线程中的一个概念，因为这里scrapy是采用异步的，可以直接看成多线程
        #所以有可能出现这样的情况，爬虫在爬取一个网页的时候，忽然被对方封了，这时候就会来到这里
        #获取新的IP，但是同时会有多条线程来这里请求，那么就会出现浪费代理IP的请求，所以这这里加上了锁
        #锁的作用是在同一时间段，所有线程只能有一条线程可以访问锁内的代码，这个时候一条线程获得新的代理IP
        #而这个代理IP是可以用在所有线程的，这样子别的线程就可以继续运行了，减少了代理IP（钱）的浪费
        self.lock.acquire()
        # 判断换线程的条件
        # 1.目前没有使用代理IP
        # 2.到线程过期的时间了
        # 3.目前IP已经被对方封了
        # 满足以上其中一种情况就可以换代理IP了
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            url = r'https://h.wandouip.com/get/ip-list?pack=%s&num=1&xy=1&type=2&lb=\r\n&mr=1&' % random.randint(100, 1000)
            response = requests.get(url=url, headers=DEFAULT_REQUEST_HEADERS)
            text = json.loads(response.text)
            print(text)
            data = text['data'][0]
            proxy_model = ProxyModel(data)
            print('重新获取了一个代理：%s' % proxy_model.proxy)
            self.current_proxy = proxy_model
            # return proxy_model
        self.lock.release()