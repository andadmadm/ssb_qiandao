# -*- coding: utf-8 -*-
"""
实现搜书吧论坛登入和发布空间动态
"""
import os
import re
import sys
import time
import logging
from urllib.parse import urlparse
from copy import copy

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(ch)

def get_refresh_url(url: str) -> str:
    """获取页面中重定向的 URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', {'http-equiv': 'refresh'})
        
        if meta_tag:
            content = meta_tag.get('content', '')
            if 'url=' in content:
                return content.split('url=')[1].strip()
        logger.info("No meta refresh tag found.")
    except requests.RequestException as e:
        logger.error(f"Failed to get refresh URL: {e}")
    return None

def get_url(url: str) -> str:
    """从页面中获取搜书吧的链接"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        link = soup.find('a', href=True, text="搜书吧")
        return link['href'] if link else None
    except requests.RequestException as e:
        logger.error(f"Failed to get URL: {e}")
        return None

def save_to_file(domain: str):
    """保存域名到文件"""
    with open('ssb_url.txt', 'w', encoding='utf-8') as url_file:
        url_file.write(domain + '\n')
    
    with open('ssb_clash.txt', 'w', encoding='utf-8') as clash_file:
        clash_file.write(f"DOMAIN-SUFFIX,{domain}\n")

if __name__ == '__main__':
    try:
        base_url = 'http://' + os.environ.get('kvasd.dpkd.5asfws6fpm.com', 'www.soushu2025.com')
        redirect_url = get_refresh_url(base_url)
        time.sleep(2)
        
        final_url = get_refresh_url(redirect_url) if redirect_url else None
        if final_url:
            domain = urlparse(final_url).hostname
            save_to_file(domain)
            logger.info(f"Domain saved: {domain}")
        
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
