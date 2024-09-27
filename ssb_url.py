# -*- coding: utf-8 -*-
"""
实现搜书吧论坛登入和发布空间动态
"""
import os
import re
import sys
from copy import copy

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_refresh_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 403:
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tags = soup.find_all('meta', {'http-equiv': 'refresh'})

        if meta_tags:
            content = meta_tags[0].get('content', '')
            if 'url=' in content:
                redirect_url = content.split('url=')[1].strip()
                print(f"Redirecting to: {redirect_url}")
                return redirect_url
        else:
            print("No meta refresh tag found.")
            return None
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return None

def get_url(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    links = soup.find_all('a', href=True)
    for link in links:
        if link.text == "搜书吧":
            return link['href']
    return None
    
def update_clini_file(url: str):
    """
    该函数读取 `cl.ini` 文件，查找 custom_proxy_group=🌍 自定义 行，
    并用新的 URL 格式替换。
    """
    cl_ini_path = 'cl.ini'  # 根据需要调整路径

    try:
        # 读取 cl.ini 文件内容
        with open(cl_ini_path, 'r', encoding='utf-8') as file:
            cl_ini_content = file.read()

        # 查找并替换 custom_proxy_group 行，只修改这一行的内容
        proxy_group_pattern = r'(custom_proxy_group=🌍 自定义).*'
        new_proxy_group = f'custom_proxy_group=🌍 自定义`url-test`.*`{url}`300,,50'
        updated_content = re.sub(proxy_group_pattern, new_proxy_group, cl_ini_content)

        # 将更新后的内容写回 cl.ini
        with open(cl_ini_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        logger.info(f"成功将 cl.ini 中的自定义代理组更新为: {new_proxy_group}")

    except FileNotFoundError:
        logger.error(f"未找到文件 {cl_ini_path}。")
    except Exception as e:
        logger.error(f"更新 cl.ini 时发生错误: {e}")

if __name__ == '__main__':
    try:
        redirect_url = get_refresh_url('http://' + os.environ.get('kvasd.dpkd.5asfws6fpm.com', 'www.soushu2025.com'))
        time.sleep(2)
        redirect_url2 = get_refresh_url(redirect_url)
        url = get_url(redirect_url2)
        domain = urlparse(url).hostname
        # 将域名写入 ssb_url.txt
        with open('ssb_url.txt', 'w', encoding='utf-8') as file:
            file.write(domain + '\n')  # 只写入域名而不是完整 URL
        with open('ssb_clash.txt', 'w', encoding='utf-8') as clash_file:
            clash_file.write(f"DOMAIN-SUFFIX,{domain}\n")  # 写入格式化的内容
        logger.info(f'{url}')
       update_clini_file(url)
    
        sys.exit(0)
