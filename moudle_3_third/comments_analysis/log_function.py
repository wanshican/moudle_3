#!/usr/bin/env Python
# -*- coding:utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import logging

# logging.disable(logging.CRITICAL)
def use_log(logger_name='log', log_file=os.path.join(BASE_DIR, 'log', 'log.log'), level=logging.DEBUG):
    # 创建 logger对象
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # 添加等级

    # 创建控制台 console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # 创建文件 handler
    fh = logging.FileHandler(filename=log_file, encoding='utf-8')

    # 创建 formatter
    formatter = logging.Formatter('[line:%(lineno)d] %(asctime)s %(levelname)s %(message)s')

    # 添加 formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 把 ch， fh 添加到 logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

def main():
    # 测试
    logger = use_log()
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

if __name__ == '__main__':
    main()
