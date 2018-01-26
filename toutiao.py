import json
import re
from hashlib import md5
import os
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pymongo
from multiprocessing import Pool
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {'User-Agent': Agent}

def get_one_index(offset,KEYWORD):  #通过分析，得到首页返回结果（json字符串）
    data = {
        'offset':offset,  #offset是可变的
        'format':'json',
        'keyword':KEYWORD, #keyword是可以自己定义的
        'autoload':'true',
        'count':'20',
        'cur_tab':'3',
        'from':'gallery'
        }
    #在源代码中没有找到想要抓取的数据，猜测应该是采用Ajax加载的，在XHR(XML HttpRequest用于在不重新加载页面的情况下更新网页)
    #中返回的Query String Parameters（通过在url中携带参数）找到url携带参数
    try:
        url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
        #urlencode把字典对象进行编码成url参数
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:#requests的所有异常继承于它
        print('解析首页失败')
        return None

def parse_page_index(html): #通过返回的json字符串提取详情页图集的url
    data = json.loads(html) #将已编码的JSON字符串解码为Python字典对象
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):  #得到详情页的返回状态
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('解析详细页失败')
        return None

def parse_page_detail(html,url): #解析子页面
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    #print(title)
    images_pattern = re.compile('gallery: JSON.parse\((.*?)\),\n',re.S)
    result = re.search(images_pattern,html)
    if result:
        #print(result.group(1))
        data = json.loads(result.group(1)) #loads方法应该是把json对象转化为字典，但这里不知道为什么成了字符串对象？
        #print(data)
        #print(type(data))
        data = eval(data)  # 将字符串对象转化为字典，用eval或exec方法。
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            #print(sub_images)
            images = [item.get('url') for item in sub_images]
            #print(images)
            for image in images:
                image = image.replace('\\','')
                #print(image)
                download_image(image)
            return {
                'title':title,
                'url':url,
                'images':images

                }

def download_image(url):
    print('正在下载',url)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None



def save_image(content):
    file_path = '{0}\{1}.{2}'.format('E:\\toutiao',md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()




def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('成功存储到MongoDB',result)
        return True
    return False


def main(offset):
    html = get_one_index(offset,KEYWORD)
    for url in parse_page_index(html):
        #print(url)
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            if result:
                #print(result)
                save_to_mongo(result)



if __name__ == '__main__':
    groups = [i*10 for i in range(group_start,group_end)]
    pool = Pool()
    pool.map(main,groups)
