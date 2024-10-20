import string
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
                'Priority': 'u=0, i',
        #     'Cookie':'_ga=GA1.2.3456; _gid=GA1.2.43245; _gat=1; _ga_F9YR6W4HNZ=GS1.2.2000',
        #     'Sec-Ch-Ua':'"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Ch-Ua-Mobile':'?0',
                'Sec-Ch-Ua-Platform':'"Windows"',
                'Sec-Fetch-Dest':'document',
                'Sec-Fetch-Mode':'navigate',
                'Sec-Fetch-Site':'none',
                'Sec-Fetch-User':'?1',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
        }
    
        if random.randint(0, 1) == 1:
                del headers['Priority']

        if random.randint(0, 1) == 1:
                ga = random.randint(7777, 1000000)
                gid = random.randint(7777, 1000000)
                gat = random.randint(7777, 1000000)
                gf = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)) 
                gaf = random.randint(7777, 1000000)
                headers['Cookie'] = f'_ga=GA1.2.{ga}; _gid=GA1.2.{gid}; _gat=1; _ga_F{gf}=GS1.2.{gaf}'



        # merge dictionaries
        kwargs['proxies'] = kwargs.get('proxies',{}) | proxies
        kwargs['headers'] = kwargs.get('headers',{}) | headers

        print(f"Making anon requests to url: {url}")
        time.sleep(random.uniform(SCRAPE_RTD_MINIMUM, SCRAPE_RTD_MAXIMUM))  # RTD
        return requests.get(url, *args, **kwargs)