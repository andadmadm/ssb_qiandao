# -*- coding: utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup
import logging

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
                logger.info(f"Redirecting to: {redirect_url}")
                return redirect_url
        else:
            logger.warning("No meta refresh tag found.")
            return None
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return None

def get_url(url: str):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')

        links = soup.find_all('a', href=True)
        for link in links:
            if link.text == "搜书吧":
                return link['href']
        return None
    except Exception as e:
        logger.error(f'Error fetching URL: {e}')
        return None

if __name__ == '__main__':
    try:
        initial_url = os.environ.get('kvasd.dpkd.5asfws6fpm.com', 'www.soushu2025.com')
        
        # 获取第一个重定向URL
        redirect_url = get_refresh_url('http://' + initial_url)

        # 如果第一个重定向URL存在，继续获取最终的URL
        if redirect_url:
            redirect_url2 = get_refresh_url(redirect_url)
            # 将最终的URL写入 ssb_url.txt
            with open('ssb_url.txt', 'w', encoding='utf-8') as f:
                f.write(f'final_url: {redirect_url2}\n')
            logger.info(f'Final URL: {redirect_url2}')
        else:
            logger.error('No redirect URL found.')
            
    except Exception as e:
        logger.error(e)
        sys.exit(1)
