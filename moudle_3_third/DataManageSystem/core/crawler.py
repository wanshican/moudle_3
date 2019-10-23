#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# 爬取评论数据，并对差评进行分析

import json
import re
import time
import csv
import jieba
import jieba.analyse
from urllib.parse import urlparse
from datetime import datetime, timedelta
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from . import log_function

log = log_function.use_log(log_file='spider.log')

class Throttle:
    """阀门类，对相同域名的访问添加延迟时间，避免访问过快
    """
    def __init__(self, delay):
        # 延迟时间，避免访问过快
        self.delay = delay
        # 用字典保存访问某域名的时间
        self.domains = {}
        
    def wait(self, url):
        """对访问过的域名添加延迟时间
        """
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


class Downloader:
    """下载类，根据url返回内容
    """
    def __init__(self, headers=None, num_retries=3, proxies=None, delay=2, timeout=30):
        self.headers = headers
        self.num_retries = num_retries
        self.proxies = proxies
        self.throttle = Throttle(delay)
        self.timeout = timeout

    def download(self, url, is_json=False):
        log.info('下载页面:' + url)
        self.throttle.wait(url)
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            log.info(response.status_code)
            if response.status_code == 200:
                if is_json:
                    return response.json()
                else:
                    return response.content
            return None
        except RequestException as e:
            log.error('error:' + e.response)
            html = ''
            if hasattr(e.response, 'status_code'):
                code = e.response.status_code
                log.error('error code:' + code)
                if self.num_retries > 0 and 500 <= code < 600:
                    # 遇到5XX 的错误就重试
                    html = self.download(url)
                    self.num_retries -= 1
            else:
                code = None
        return html


class Recorder:
    """记录类，根据不同保存类型使用相应方法。
    通过类对象使用回掉函数方式直接调用
    """
    def __init__(self, save_type='csv'):
        self.save_type = save_type

    def __call__(self, filename, fields, all_list):
        if hasattr(self, self.save_type):
            func = getattr(self, self.save_type)
            return func(filename, fields, all_list)
        else:
            return {'status': 1, 'statusText': 'no record function'}

    def csv(self, filename, fields, all_list):
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                # fields = ('id', '名称', '价格', '评价人数', '好评率')
                writer.writerow(fields)
                for row in all_list:
                    writer.writerow(row)
            return {'status': 0, 'statusText': 'csv saved'}
        except Exception as e:
            print(e)
            return {'status': 1, 'statusText': 'csv error'}


class ItemCommentSpider:
    """抓取商品评价信息
    """
    def __init__(self, headers=None, num_retries=3, proxies=None, delay=2, timeout=30):
        self.headers = headers
        self.num_retries = num_retries
        self.proxies = proxies
        self.throttle = Throttle(delay)
        self.timeout = timeout
        self.download = Downloader(headers, num_retries, proxies, delay, timeout)
            
    def get_comment_by_json(self, url):
        # http://sclub.jd.com/comment/productPageComments.action?productId=6946647&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
        data = self.download.download(url, is_json=True)
        comments = data['comments']
        data_list = []
        for c in comments:
            row = []
            row.append(c['creationTime'])
            row.append(c['productSize'])
            row.append(c['productColor'])
            # row.append(c['productSales'][0]['saleValue'])
            row.append(c['content'])
            data_list.append(row)
        return data_list

    def fetch_data(self, url, filename, page_start, page_end, page_offset, callback=None):
        all_list = []
        page_num = 1
        for page in range(page_start, page_end, page_offset):
            data_list = self.get_comment_by_json(url.format(page))
            all_list += data_list
            log.info(f'完成第{page_num}页')
            page_num += 1

        if callback:
            callback(filename, ('creationTime', 'productSize', "productColor", "content"), all_list)


class Analysis:
    '''分析评论数据'''
    def __init__(self, filename):
        self.filename = filename

    def get_all_text(self):
        """取出所有评价的句子
        """
        comment_list = []
        with open(self.filename) as f:
            rows = csv.reader(f)
            for row in rows:
                one_comment = row[-1]
                comment_list.append(one_comment)

        return ''.join(comment_list[1:]) 

    def cut_text(self, all_text):
        """找到评价中重要关键词
        """
        jieba.analyse.set_stop_words('stop_words.txt')
        text_tags = jieba.analyse.extract_tags(all_text, topK=30)
        return text_tags

    def get_bad_words(self, text_tags, all_text):
        """根据关键词找到对应的句子
        """
        words = {}
        for tag in text_tags:
            tag_re = re.compile(f'(\w*{tag}\w*)')
            words[tag] = tag_re.findall(all_text)
        return words

def main(url='https://sclub.jd.com/comment/productPageComments.action?productId=100006769698&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'):
    headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "referer": "https://passport.jd.com"
        } 
    spider = ItemCommentSpider(headers=headers)
    # url = 'https://sclub.jd.com/comment/productPageComments.action?productId=100006769698&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'
    spider.fetch_data(url, 'db.csv', 0, 30, 1, Recorder('csv'))

    data = Analysis('db.csv')
    all_text = data.get_all_text()
    text_tags = data.cut_text(all_text)
    print(text_tags)
    words = data.get_bad_words(text_tags, all_text)
    for k, v in words.items():
        print(k, '-->', len(v), v)

if __name__ == '__main__':
    main()