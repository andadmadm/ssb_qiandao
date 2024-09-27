# -*- coding: utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup
import logging
import time  # 确保导入 time 模块

# 设置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        links = soup.find_all('a', href=True)
        for link in links:
            if link.text == "搜书吧":
                return link['href']
    except Exception as e:
        print(f'Error fetching URL: {e}')
    return None

if __name__ == '__main__':
    try:
        redirect_url = get_refresh_url('http://' + os.environ.get('kvasd.dpkd.5asfws6fpm.com', 'www.soushu2025.com'))
        time.sleep(2)
        
        if redirect_url:  # 确保 redirect_url 不为 None
            redirect_url2 = get_refresh_url(redirect_url)
            url = get_url(redirect_url2)
            if url:  # 确保 url 不为 None
                with open('ssb.txt', 'w', encoding='utf-8') as f:
                    f.write(f'{url}\n')
                logger.info(f'{url}')
            else:
                logger.warning("No URL found.")
        else:
            logger.warning("No redirect URL found.")
    except Exception as e:
        logger.error(f'An unexpected error occurred in main: {e}')
