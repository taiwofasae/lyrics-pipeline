from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
import requests
import time
import random

SCRAPE_PROXY = 'socks5://127.0.0.1:9050'
SCRAPE_RTD_MINIMUM = 2
SCRAPE_RTD_MAXIMUM = 4

def get(url, *args, **kwargs):
    with Controller.from_port(port=9051) as c:
                c.authenticate("welcome")
                c.signal(Signal.NEWNYM)
    
    proxies = {'http': SCRAPE_PROXY, 'https': SCRAPE_PROXY}
    headers = {'User-Agent': UserAgent().random}
    headers = {
            'Accept-Encoding':'gzip, deflate, br, zstd',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language':'en-US,en;q=0.9',
            'Connection':'keep-alive',
            'Cookie':'_ga=GA1.2.1781353; _gid=GA1.2.162452; _gat=1; _ga_F9YR6W4HNZ=GS1.2.1717',
            'Sec-Ch-Ua':'"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    # merge dictionaries
    kwargs['proxies'] = kwargs.get('proxies',{}) | proxies
    kwargs['headers'] = kwargs.get('headers',{}) | headers
    
    print(f"Making anon requests to url: {url}")
    time.sleep(random.uniform(SCRAPE_RTD_MINIMUM, SCRAPE_RTD_MAXIMUM))  # RTD
    return requests.get(url, *args, **kwargs)