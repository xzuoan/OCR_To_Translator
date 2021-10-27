import requests
import json
import js2py
import re
# from lxml import etree

# 翻译模块
class Translat_Toor:
    def __init__(self):
        self.url = 'https://fanyi.baidu.com'
        self.headers = {
                'Host': 'fanyi.baidu.com',
                'Referer': 'https://www.baidu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    def get_token(self):
        global session
        session = requests.session()
        session.headers = self.headers
        session.get(self.url)
        res = session.get(self.url).text
        token = re.search(r"token: '(.*?)',", res, re.S).group(1)
        # res = etree.HTML(res)
        # token = res.xpath('/html/body/script[1]/text()')[0][34:66]
        return token

    def send_post(self, words, sign, token):
        data = {
                'from': 'en',
                'to': 'zh',
                'query': words,
                'simple_means_flag': 3,
                'sign': sign,
                'token': token,
                'domain': 'common'}
        res = json.loads(session.post(url=self.url+ '/v2transapi', params=data).text)
        try:
            result = res['trans_result']['data'][0]['dst']
            return result
        except:
            return 'null'

    def read_js(self):
        with open('.\sign.js', 'r', encoding='utf8') as f:
            return f.read()

def Tanstlat(words):
    a = Translat_Toor()
    token= a.get_token()
    run_js = js2py.EvalJs({})
    run_js.execute(a.read_js())
    sign = run_js.e(words)
    text = a.send_post(words, sign, token)
    return text