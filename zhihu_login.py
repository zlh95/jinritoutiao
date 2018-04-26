import requests
import http.cookiejar as cookielib
import re
import hmac
import time
from hashlib import sha1
import json
import base64
from PIL import Image
from lxml import etree

#建立session，保持连接
session = requests.session()
#把cookies导入文件
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
#提取保存的cookies
try:
    session.cookies.load(ignore_discard=True) #从文件中导出cookies
except:
    print('cookies未能加载')

# 伪造header
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent,
    'Connection': 'keep-alive'
}

def is_login(account,password):
    '''
    # 通过个人中心页面返回状态码来判断是否登录
    # 通过allow_redirects 设置为不获取重定向后的页面
    :return: None
    '''
    response = session.get("https://www.zhihu.com/inbox", headers=header, allow_redirects=False,verify=False)
    if response.status_code != 200:
        zhihu_login(account,password)
    else:
        print('你已经登陆！')


def get_xsrf_dc0():
    '''
    # 获取xsrf code和d_c0
    # 在请求登录页面的时候页面会将xsrf code 和d_c0加入到cookie中返回给客户端
    :return:response.cookies['_xsrf'],response.cookies['d_c0']
    '''
    response = session.get("https://www.zhihu.com/signup", headers=header)
    return response.cookies['_xsrf'],response.cookies['d_c0']

def get_signature(time_str):
    '''
    # 生成signature,利用hmac加密
    # 根据分析之后的js，可发现里面有一段是进行hmac加密的
    # 分析执行加密的js 代码，可得出加密的字段，利用python 进行hmac几码
    :param time_str:
    :return:
    '''
    h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=sha1)
    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    now = time_str
    h.update((grant_type + client_id + source + now).encode('utf-8'))
    return h.hexdigest()

def get_identifying_code(headers):
    '''
    # 判断页面是否需要填写验证码
    # 如果需要填写则弹出验证码，进行手动填写
    # 请求验证码的url 后的参数lang=en，意思是取得英文验证码
    # 原因是知乎的验证码分为中文和英文两种
    # 中文验证码是通过选择倒置的汉字验证的，破解起来相对来说比较困难，
    # 英文的验证码则是输入验证码内容即可，破解起来相对简单，因此使用英文验证码
    response = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    :param headers:
    :return:captcha
    '''
    response = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    r = re.findall(r'"show_captcha":(\w+)',response.text)
    if r[0] == 'False':
        return
    else:
        response = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=header)
        show_captcha = json.loads(response.text)['img_base64']
        with open('captcha.jpg','wb') as f:
            f.write(base64.b64decode(show_captcha))
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        captcha = input('请输入验证码：')
        session.post('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=header,
                     data={"input_text": captcha})
        return captcha

def zhihu_login(account, password):
    '''知乎登陆'''
    post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    XXsrftoken, XUDID = get_xsrf_dc0()
    header.update({
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",  # 固定值
        "X-Xsrftoken": XXsrftoken,
    })
    time_str = str(int((time.time() * 1000)))
    # 直接写在引号内的值为固定值，
    # 只要知乎不改版反爬虫措施，这些值都不会变
    post_data = {
        "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
        "grant_type": "password",
        "timestamp": time_str,
        "source": "com.zhihu.web",
        "password": password,
        "username": account,
        "captcha": "",
        "lang": "en",
        "ref_source": "homepage",
        "utm_source": "",
        "signature": get_signature(time_str),
        'captcha': get_identifying_code(header)
    }

    response = session.post(post_url, data=post_data, headers=header, cookies=session.cookies)
    if response.status_code == 201:
        # 保存cookie，下次直接读取保存的cookie，不用再次登录
        session.cookies.save()
    else:
        print("登录失败")


if __name__ == '__main__':
    #account = input('请输入账号：')
    #password = input('请输入密码：')
    is_login(account='+8618511693445',password='123*asd')

    def get_all_post_url():
        '''
        #通过分析得出访问轮子哥的主页的第一页只能抓到两篇文章的url，其他的隐藏在html文本中，
        #通过用正则表达式获取前五篇文章的url，然后通过F12发现其他的文章是动态加载的，然后构建
        #url获取所有文章的url
        #:return:all_post_url
        '''
        response = session.get("https://www.zhihu.com/people/excited-vczh/posts?page=1",headers=header)
        post_url_5 = re.findall(r'http://\w{8}\.\w{5}\.\w{3}/\w+/\d{8}',response.content.decode(response.apparent_encoding))
        response = session.get('https://www.zhihu.com/api/v4/members/excited-vczh/articles?include=data%5B*%5D.comment_count%2Csuggest_edit%2Cis_normal%2Cthumbnail_extra_info%2Cthumbnail%2Ccan_comment%2Ccomment_permission%2Cadmin_closed_comment%2Ccontent%2Cvoteup_count%2Ccreated%2Cupdated%2Cupvoted_followees%2Cvoting%2Creview_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=5&limit=15&sort_by=created',headers=header)
        post_url_15= response.content.decode(response.apparent_encoding)
        p = json.loads(post_url_15)
        l = p['data']
        remaining_15 = [i['url'] for i in l]
        post_url_5.extend(remaining_15)
        first_page_15 = post_url_5
        all_post_url = []
        for offest in range(20,120,20):
            response2 = session.get('https://www.zhihu.com/api/v4/members/excited-vczh/articles?include=data%5B*%5D.comment_count%2Csuggest_edit%2Cis_normal%2Cthumbnail_extra_info%2Cthumbnail%2Ccan_comment%2Ccomment_permission%2Cadmin_closed_comment%2Ccontent%2Cvoteup_count%2Ccreated%2Cupdated%2Cupvoted_followees%2Cvoting%2Creview_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={0}&limit=20&sort_by=created'.format(offest), headers=header)
            j = json.loads(response2.content.decode(response.apparent_encoding))
            k = j['data']
            post_url = [i['url'] for i in k]
            all_post_url.extend(post_url)
        first_page_15.extend(all_post_url)
        all_post_url = first_page_15
        return all_post_url

    def get_post_detail():
        response = session.get("https://www.zhihu.com/people/excited-vczh/posts?page=1", headers=header,verify=False)
        post_url_5 = re.findall(r'http://\w{8}\.\w{5}\.\w{3}/\w+/\d{8}',response.content.decode(response.apparent_encoding))
        print(post_url_5[0])
        response = requests.get(post_url_5[1],headers={'Host': 'zhuanlan.zhihu.com','User-Agent': 'Fiddler'})
        print(response.content.decode(response.apparent_encoding))
        html = etree.HTML(response.content.decode(response.apparent_encoding))
        title = html.xpath('//*[@id="root"]/div/main/div/article/header/h1/text()')
        print(title)



