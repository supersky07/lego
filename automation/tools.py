# -*- coding:utf-8 -*-  

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import string
import sys
import requests
from lxml import etree
import random
from urlparse import urlparse

reload(sys) 
sys.setdefaultencoding('utf-8')

dcap = dict(DesiredCapabilities.PHANTOMJS) 
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")

# 判断节点是否存在，省的程序报错
def isElementExist(self, element):
        flag = True
        try:
            self.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag

def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return header

# 暂时只支持amazon, jd, tmall
def getPriceBySelenium(url, type):
    try:
        obj = webdriver.PhantomJS(desired_capabilities=dcap)
        obj.set_page_load_timeout(60)
        obj.get(url)
        time.sleep(2)
        
        if type == 'amazon':
            price = obj.find_element_by_xpath('//span[@id="priceblock_ourprice"]').text
        elif type == 'jd':
            price = obj.find_element_by_xpath('//div[@id="summary-wrap"]/*/*/*/*/span[contains(@class, "price")]').text
        elif type == 'tmall':
            flag = isElementExist(obj, '//div[@class="tm-promo-price"]/span[@class="tm-price"]')
            if flag:
                price = obj.find_element_by_xpath('//div[@class="tm-promo-price"]/span[@class="tm-price"]').text
            else:
                price = obj.find_element_by_xpath('//span[@class="tm-price"]').text
        else:
            price = 0
            
        # obj.quit()

        price = re.compile(r'[1-9]\d*\.\d*').findall(price)[0]

        return price
    except Exception as e:
        print e
        return 0

def getPriceByRequests(url, type):
    try:
        headers = randHeader()

        if type == 'amazon':
            html = requests.get(url, headers=headers).content
            selector = etree.HTML(html)
            price = selector.xpath('//span[@id="priceblock_ourprice"]/text()')[0]
            price = price.replace(',', '')
            price = re.compile(r'[1-9]\d*\.\d*').findall(price)[0]
        elif type == 'jd':
            url_json = urlparse(url)
            product_id = re.compile(r'[1-9]\d*').findall(url_json.path)[0];
            price_url = 'https://p.3.cn/prices/mgets?callback=jQuery4385995&skuIds=J_' + product_id
            
            html = requests.get(price_url, headers=headers).content
            price = re.compile(r'\"p\"\:\"(.+?)\"').findall(html)[0]

        return price
    except Exception as e:
        print e
        return 0
# print getPriceBySelenium("https://www.amazon.cn/%E7%8E%A9%E5%85%B7/dp/B00PY3EYQO/ref=sr_1_2", "amazon")
# print getPriceByRequests("https://www.amazon.cn/gp/product/B00NVDJQ3A/ref=amb_link_6?pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-1&pf_rd_r=BBPE8GB3T9RT12WY59GN&pf_rd_t=101&pf_rd_p=574b13f8-228e-459a-b985-5e68cb4d6e55&pf_rd_i=2128402051&th=1", "amazon")
# print getPriceBySelenium("https://item.jd.hk/1972648073.html", "jd")
# print getPriceByRequests("https://item.jd.hk/1972648073.html", "jd")
# print getPriceBySelenium("https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.4c637810D1Z8Kg&id=527351469273&skuId=3137609351477&areaId=110100&user_id=766568254&cat_id=2&is_b=1&rn=79f6888c4e4ade3200f135e9ce3a30cc", "tmall")
# print getPriceBySelenium("https://detail.tmall.com/item.htm?spm=a220o.1000855.1998025129.1.5c90c348snvu2B&abtest=_AB-LR32-PR32&pvid=5827e719-39c2-4f84-894f-a3eb63ec1762&pos=1&abbucket=_AB-M32_B13&acm=03054.1003.1.1539344&id=44107677533&scm=1007.12144.81309.23864_0", 'tmall')