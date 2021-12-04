import random

import bs4.element
import requests
import json
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import os
import pandas as pd


# 爬取当当网商品评论的爬虫
class DDCmt_Crawler:
    def __init__(self, file_path: str, proxy=True):
        assert os.path.exists(file_path) is True
        self.writer = pd.ExcelWriter(file_path, mode='a', if_sheet_exists='new',
                                     datetime_formatstr='YYYY-MM-DD HH:MM:SS')
        self.proxies_list = []
        self.batch_size = 5
        self.min_proxies_num = 2
        self.proxies_blame = {}
        self.blame_limit = 5
        self.total_proxy_num = 0
        self.proxy = proxy

    def crawl_product(self, product_id, start=1, end=201, c_list=None):
        headers = {
            'host': "product.dangdang.com",
            'Referer': fr"http://product.dangdang.com/{product_id}.html",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41",
        }
        params = {
            'productId': product_id,
            'mainProductId': product_id,
            'pageIndex': 1,
            'sortType': 2,  # 全爬完，按时间排序
            'filterType': 1,  # 全爬完，不过滤
        }
        url = r"http://product.dangdang.com/index.php?r=comment%2Flist"
        # self.get_proxy(5)

        c_iter = c_list if c_list is not None else range(start, end)
        for page in tqdm(c_iter):
            # 爬取
            params['pageIndex'] = page
            proxies = self.get_cur_proxy()
            # print(proxies)
            data = self.get(url, headers, params, proxies)
            if data is None:  # 爬取失败
                self.blame_proxy(proxies)
                continue
            # 解析
            result = self.parse_page(data)
            if result is None:  # 解析到结尾
                print("正常?")
                break
            # 保存
            result_df = pd.DataFrame(result)
            result_df.to_excel(self.writer, index=False, header=True)
            # 等待 0~3s
            time.sleep(random.random() * 3)
        else:
            print("正常结束")
        self.writer.save()

    def get(self, url, headers, params, proxies):
        try:
            rsp = requests.get(url, params=params, headers=headers, proxies=proxies)
            data = json.loads(rsp.text)['data']['list']['html']
            return data
        except Exception as e:
            print(params['pageIndex'])
            return None

    def parse_item(self, item: bs4.element.Tag):
        star = item.find('em').string  # 10分
        comment = item.find(attrs={'class': 'describe_detail'}).find('span').string  # 书籍很不错
        zan = item.find(attrs={'class': 'j_zan'}).attrs['data-number']  # 52
        reply = item.find(attrs={'class': 'reply'}).attrs['data-number']  # 8
        name = item.find(attrs={'class': 'name'}).string  # 无昵称用户 家乡的兔兔... 匿名用户
        level = item.find(attrs={'class': 'level'}).string
        yg = item.find(attrs={'class': 'icon_yg'})  # None or Tag 是否已购买
        cmt_time = item.find(attrs={'class': 'starline'}).find('span').string  # 2017-09-08 14:02:11
        pic = item.find('ul', attrs={'class': 'pic_show'})  # None或者Tag含有ul
        result_dict = {
            'star': int(star[:-1]),
            'comment': comment,
            'zan': int(zan),
            'reply': int(reply),
            'name': name,
            'level': level,
            'yg': 0 if yg is None else 1,
            # 'time': time.strptime(cmt_time, "%Y-%m-%d %H:%M:%S"),
            'time': cmt_time,
            'pic': 0 if pic is None else len(pic.find_all('li')),
        }
        return result_dict

    def parse_page(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find(attrs={'class': 'fanye_box'}) is None:
            return None
        cmt_list = soup.find_all(attrs={'class': 'comment_items clearfix'})
        return [self.parse_item(cmt) for cmt in cmt_list]

    def get_proxy(self, num):
        url = r"http://api.xdaili.cn/xdaili-api/greatRecharge/getGreatIp"
        param = {
            'spiderId': "",
            'orderno': "",
            'returnType': 2,
            'count': num
        }
        rsp = requests.get(url, params=param)
        proxy_list = json.loads(rsp.text)['RESULT']
        for api_proxy in proxy_list:
            self.proxies_list.append({
                "http": f"http://{api_proxy['ip']}:{api_proxy['port']}",
                "https": f"http://{api_proxy['ip']}:{api_proxy['port']}",
            })
            self.proxies_blame[f"http://{api_proxy['ip']}:{api_proxy['port']}"] = 0
        self.total_proxy_num += num
        print(f"get proxy: {num}")

    def get_cur_proxy(self):
        if self.proxy is False:
            return None
        if len(self.proxies_list) <= self.min_proxies_num:
            self.get_proxy(self.batch_size)
        return random.choice(self.proxies_list)

    def blame_proxy(self, proxies):
        if self.proxy is False:
            return
        key = proxies['http']
        self.proxies_blame[key] += 1
        if self.proxies_blame[key] >= self.blame_limit:
            for i, p in enumerate(self.proxies_list):
                if p['http'] == key:
                    del self.proxies_list[i]


crawler = DDCmt_Crawler("tmp.xlsx")
# crawler.crawl_product(22765017, 153, 201)
# crawler.crawl_product(28973100, 1, 210)
# crawler.crawl_product(28989328, 1, 210, c_list=[5, 6, 8, 9])
crawler.crawl_product(29206655, 1, 210)
