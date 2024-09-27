if __name__ == '__main__':
    try:
        # 获取第一个重定向URL
        redirect_url = get_refresh_url('http://' + os.environ.get('kvasd.dpkd.5asfws6fpm.com', 'www.soushu2025.com'))
        time.sleep(2)
        
        # 获取第二个重定向URL
        redirect_url2 = get_refresh_url(redirect_url)
        
        # 获取最终的URL
        url = get_url(redirect_url2)
        logger.info(f'{url}')
        
        # 将 redirect_url 和 url 写入 ssb_url.txt
        with open('ssb_url.txt', 'w', encoding='utf-8') as f:
            f.write(f'redirect_url: {redirect_url}\n')
            f.write(f'final_url: {url}\n')
        
        # 继续后续操作
        client = SouShuBaClient(
            urlparse(url).hostname,
            os.environ.get('SOUSHUBA_USERNAME', "libesse"),
            os.environ.get('SOUSHUBA_PASSWORD', "yF9pnSBLH3wpnLd")
        )
        client.login()
        client.space()
        credit = client.credit()
        logger.info(f'{client.username} have {credit} coins!')
        
    except Exception as e:
        logger.error(e)
        sys.exit(1)
