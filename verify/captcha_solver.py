from verify.utils import js_now
from loguru import logger

import subprocess
import json
import time
from requests import Session
from urllib.parse import urlencode

import threading


class DataDict(dict):

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        return self.__setitem__(name, value)



class NodeBridge:
    def __init__(self):
        # 启动 Node.js 子进程
        self.process = subprocess.Popen(
            ['node', './bridge.js'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 等待 Wasm 初始化完成信号
        while True:
            line = self.process.stdout.readline().strip()
            if line == "READY":
                print("Node.js 桥接器就绪")
                break
            time.sleep(0.1)

    def encrypt(self, arg0, arg1):
        # 发送参数
        payload = json.dumps(["getEncryptData",arg0, arg1])
        self.process.stdin.write(payload + '\n')
        self.process.stdin.flush()

        # 读取结果
        response = self.process.stdout.readline().strip()
        return json.loads(response)

    def captchaAuth(self,arg0):
        payload = json.dumps(["getCaptchaAuth",arg0])
        self.process.stdin.write(payload + '\n')
        self.process.stdin.flush()

        # 读取结果
        response = self.process.stdout.readline().strip()
        return json.loads(response)



class ThreadSafeEncryptor:
    def __init__(self):
        self._bridge = NodeBridge()  # 之前定义的桥接类
        self._lock = threading.Lock()  # 定义互斥锁

    def encrypt(self, a, b):
        with self._lock:  # 确保同一时间只有一个线程在读写管道
            return self._bridge.encrypt(a, b)

    def captchaAuth(self,a):
        with self._lock:
            return self._bridge.captchaAuth(a)


bridge = ThreadSafeEncryptor()

import math
import random


def random_str(length):
    e = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
         "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    n = ''
    for i in range(length):
        n += e[math.floor(35 * random.random())]
    return n


class JDCaptchaSolver:

    def __init__(self, options,proxies=None,location_url = '',ua=None):
        # {
        #   "appid": 360472534,
        #   "sceneid": 1016966843,
        #   "sessionId": "DbqFeQABAAACvgOGCQgAMOZiKheOsMR5riuXLEITICQEXpnzQpK9y_R0ushvS5mJre77SNJ1TNyoTSQIVzu6RQAA"
        # }
        self.location_url = location_url
        if not ua:
            ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        self.ua = ua
        self.devcInfo = DataDict({'capfp': {},
                                  'cd': '24',
                                  'cpu': '20',
                                  'cvs': 'b8af64bcaaf7285873eb89cf7df48484',
                                  'fts': 'Arial,Calibri,Cambria,Consolas,Courier,CourierNew,Georgia,Helvetica,Impact,LucidaConsole,LucidaSansUnicode,MSGothic,MSPGothic,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Symbol,Candara,Constantia,Corbel,Ebrima,FangSong,Gabriola,MicrosoftYaHei,MicrosoftYiBaiti,MingLiUExtB,PMingLiUExtB,SimHei,SimSun,SimSunExtB',
                                  'fv': '',
                                  'lan': 'zh-CN',
                                  'lns': 'zh-CN,zh',
                                  'mem': 8,
                                  'pr': '1',
                                  'pt': 'Win32',
                                  'scr': '1920x1080,1920x1032',
                                  'sdv': '2.0',
                                  'tsp': '0',
                                  'tzo': 'Asia/Shanghai',
                                  'wdr': False,
                                  'wgl': '1eca15a225dcee18245e9f23267dcfba',
                                  'wvr': 'Google Inc. (Intel)~ANGLE (Intel, Intel(R) UHD Graphics 770 (0x00004680) Direct3D11 vs_5_0 ps_5_0, D3D11)'
                                  })
        self.state = DataDict({
            "canceled": False,
            "fp_req": True,
            "st": "",
            "firstStep": None,
            "imgJsonStr": "",
            "captchaType": 0,
            "isAppDisplayEmbed": False,
            "appId": "",
            "md5Salt": "dzHdg!axOg537gYr3zf&dSrvm@t4a+8F",  # js 固定值?
            "sessionId": options['sessionId'],
            # 来自接口
            "width": 0,
            "language": 1,
            "account": None,
            "ccode": None,
            "eid": None,
            "pin": None,
            "display": "popup",
            "host": "https://captcha-api-global.jdcloud.com",
            "tdat_code": 57972,  # 固定值
            "platformType": 1,
            "langMap": {
                "code_1": "点击完成验证",
                "code_2": "安全检测中",
                "code_3": "验证码类型不匹配",
                "code_4": "请输入验证码",
                "code_9": "请按照箭头路线滑动手指",
                "code_10": "完成验证",
                "code_11": "重新发送",
                "code_12": "提交",
                "code_14_1": "验证失败请重试",
                "code_15": "验证错误请重试",
                "code_16": "验证码输入错误，请重新输入",
                "code_17": "短信验证码已过期,请重新发送",
                "code_18": "刷新验证码失败",
                "code_19": "轨迹不一致，请重试",
                "code_20": "拖动滑块向右滑动",
                "code_21": "滑动验证成功",
                "code_22": "滑动验证失败",
                "code_23": "滑动验证中",
                "code_25": "拖动滑块填充拼图",
                "code_27": "没有对齐，请再来一次",
                "code_28": "验证码请求超时，请刷新重试",
                "slidTips": "请按照图中轨迹滑动手指",
                "error_1": "错误代码:1，请稍后重试",
                "error_2": "刷新失败，错误代码:2",
                "code_5": "安全验证",
                "code_6": "确定",
                "code_7": "加载中",
                "code_8": "请点击上图中的：",
                "code_13": "验证成功",
                "code_14": "验证失败，请重新验证",
                "code_24": "服务器异常",
                "code_24_1": "服务异常，请稍后重试",
                "code_26": "操作频繁，请稍后重试",
                "code_30": "请求过于频繁，请稍后重试",
                "code_31": "服务异常，请稍后重试",
                "code_32": "网络异常，请稍后重试",
                "code_33": "请求超时，请稍后重试",
                "code_34": "验证码操作频繁，请稍后重试",
                "code_35": "验证码请求超时，请稍后重试",
                "code_36": "刷新超时，请稍后重试",
                "code_37": "请旋转立方体依次点击: ",
                "code_38": "拖动交换2个图块复原图片",
                "code_39": "拖动滑块使图片角度为正",
                "code_40": "请拖动滑块将图像还原",
                "code_o_5": "为了您的使用安全，请完成验证",
                "code_o_25": "向右拖动箭头到底",
                "code_o_21": "验证成功",
                "code_o_27": "验证失败",
                "code_502": "网络错误",
                "code_504": "网络超时"
            },
            "platformOS": "m",
            "device": {},
            "version": "",
            "udid": "",
            "setFp": "",
            "devcInfo": json.dumps(self.devcInfo, separators=(',', ':')),
            "urlMap": {
                "report": "https://jcapmonitor.m.jd.com/web_jcap_report",
                "img": "https://captcha-api-global.jdcloud.com/static/img/",
                "iframe": "https://captcha-api-global.jdcloud.com/static/html/captchaStorage.html",
                "js": "https://captcha-api-global.jdcloud.com/static/js/",
                "fp": "/cgi-bin/api/fp",
                "refresh": "/cgi-bin/api/refresh",
                "check": "/cgi-bin/api/check",
                "v": 20180110
            },
            "tdat_ctx": "13130303032393939393530303032433633434132303831443330323343393136403932353331403832463337354233303031313030303",
            # 来自js
            "isMouseMove": False,
            "isInitOnload": False,
            "sen": 0,
            "appid": options['appid'],  # 来自接口
            "sceneid": options['sceneid']  # 来自接口
        })
        self.session = Session()
        self.session.proxies = proxies
        self.session.timeout = 30

    def fp_payload(self):
        e = js_now()
        n = e % 19
        r = self.state.appid
        o = self.state.md5Salt
        i = self.state.sessionId
        a = self.state.host
        s = self.state.tdat_code
        c = self.state.devcInfo
        u = self.state.language
        f = self.state.urlMap
        l = self.state.tdat_ctx
        d = {
            "si": i,
            'ct': "",
            'version': 2,
            'lang': u,
            'client': self.state.platformOS,
            'appConfig': {
                'appid': '',
                'md5Salt': o
            }
        }
        # d['ct'] = G(random_str(n) + str(len(d['si'])).zfill(4)) + d['si'] + c + e, s, l)
        encrypt_data = bridge.encrypt(f'{random_str(n)}{str(len(d['si'])).zfill(4)}{d['si']}{c}{e}',l)
        d['ct'] = json.dumps( encrypt_data['data'])
        return d

    def check_payload(self,t=''):
        # t = '{"ht":228,"wt":368,"x":217,"y":36}' 图片尺寸和点击坐标
        r = self.state.appId
        o =  self.state.md5Salt
        i =  self.state.sessionId
        a =  self.state.language
        s =  self.state.tdat_code
        c =  self.state.host
        u =  self.state.st
        f =  self.state.devcInfo
        l =  self.state.urlMap
        d =  self.state.platformOS
        p =  self.state.tdat_ctx
        t = urlencode(t) if t else ''
        h =js_now()
        g = h % 41
        v = {
            "touchList": [
                {
                    "eid": "click",
                    "did": "",
                    "cn": "model_btn__KK_G5",
                    "sx": 253,
                    "sy": 714,
                    "px": 253,
                    "py": 593,
                    "time": 1767098983890
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "model_btn-text__UkwVt",
                    "sx": 217,
                    "sy": 700,
                    "px": 217,
                    "py": 579,
                    "time": 1767098984585
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "navigation_imgtail__TMQ5c",
                    "sx": 1688,
                    "sy": 860,
                    "px": 1688,
                    "py": 739,
                    "time": 1767163122282
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "inputGroup_groupContainer__4nhEd",
                    "sx": 482,
                    "sy": 633,
                    "px": 482,
                    "py": 512,
                    "time": 1767163122977
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "searchCore_searchButton__sxBzy",
                    "sx": 829,
                    "sy": 705,
                    "px": 829,
                    "py": 584,
                    "time": 1767163125612
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "model_btn-text__UkwVt",
                    "sx": 484,
                    "sy": 734,
                    "px": 484,
                    "py": 613,
                    "time": 1767163133194
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "model_btn-text__UkwVt",
                    "sx": 490,
                    "sy": 698,
                    "px": 490,
                    "py": 577,
                    "time": 1767163133803
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "style_tableWrapper__Yby3D",
                    "sx": 772,
                    "sy": 932,
                    "px": 772,
                    "py": 811,
                    "time": 1767163151105
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "model_btn-text__UkwVt",
                    "sx": 308,
                    "sy": 736,
                    "px": 308,
                    "py": 615,
                    "time": 1767172294303
                },
                {
                    "eid": "click",
                    "did": "",
                    "cn": "model_btn-text__UkwVt",
                    "sx": 265,
                    "sy": 703,
                    "px": 265,
                    "py": 582,
                    "time": 1767172295118
                }
            ]
        }
        m = self.state.devcInfo
        tk  = bridge.encrypt(f'{h}{str(len(u)).zfill(4)}{str(len(u)).zfill(4)}{str(len(t)).zfill(6)}{t}{json.dumps(v,separators=(',',':'))}{random_str(g)}',p)
        ct = bridge.encrypt(f'{random_str(h % 19)}{str(len(i)).zfill(4)}{i}{m}{h}',p)
        y = {
            'si': i,
            'lang': a,
            'tk': json.dumps(tk['data'],separators=(',',':')),
            'ct': json.dumps(ct['data'],separators=(',',':')),
            'version': 2,
            'client': d,
            'appConfig': {
                'appid': '',
                'md5Salt': o
            }
        }
        return y

    def _require_captcha(self):
        response = self.session.get('https://captcha-api-global.jdcloud.com/home/requireCaptcha.js')
        logger.debug(f'_require_captcha set cookie: {response.cookies.get_dict()}')

    def _request_fp(self):
        payload = self.fp_payload()
        captcha_auth = bridge.captchaAuth(payload['appConfig']['appid'])['data']
        del payload['appConfig']
        logger.debug(captcha_auth)
        url = 'https://captcha-api-global.jdcloud.com/cgi-bin/api/fp'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://www.airchina.com.cn',
            'referer': 'https://www.airchina.com.cn',
            'user-agent': self.ua,
            'x-jdcloud-captcha-auth': captcha_auth,
            # 'cookie': '_cfuvid=I3qIURlduD39_.JOiY8tRbhLnV.EXxWGWXOODF0_fJ8-1767163154.991286-1.0.1.1-pnO8dJClC4oHBHBsNpRlw5GNR1R9NNJOGVxjIzqVVAE',
        }
        response = self.session.options(url,headers=headers)
        logger.debug(f'fp set cookie: {response.cookies.get_dict()}')
        logger.debug(response.status_code)
        response = self.session.post(url,headers=headers,data=payload)
        # {"st":"","code":16801,"s_code":11006,"msg":"加载异常，请重试"}
        # {"st":"","code":16808,"s_code":12203,"msg":"验证未通过"}
        resp_json = response.json()
        if resp_json['code'] !=0:
            logger.debug(resp_json)
            return None
        return resp_json

    def _request_check(self):

        payload = self.check_payload()
        captcha_auth = bridge.captchaAuth(payload['appConfig']['appid'])['data']
        del payload['appConfig']
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://www.airchina.com.cn',
            'referer': 'https://www.airchina.com.cn/',
            'user-agent': self.ua,
            'x-jdcloud-captcha-auth': captcha_auth,
            # 'cookie': '_cfuvid=7HCDxaPbfJ5n5k.Tjuyguz9JA7dg0NCH4j71D9Ja2fI-1767173154.9954734-1.0.1.1-FrOUQQTThz3qefaPmmsHmtWGuoNIcIMGtMayCYeLOd0',
        }
        url = 'https://captcha-api-global.jdcloud.com/cgi-bin/api/check'
        response=  self.session.post(url,data=payload,headers=headers)

    def solve(self):
        self._require_captcha()
        fp_result = self._request_fp()
        self.state['st'] = fp_result['st']
        logger.debug(fp_result)
        check_result = self._request_check()
        logger.debug(check_result)



if __name__ == '__main__':
    from urllib.parse import quote
    from requests import Session
    ip = '113.64.246.112:10110'
    proxy = f'http://hsroot:{quote("Dj7+t&I4glbw?UQ]")}@{ip}'
    proxies = {
        'http':proxy,
        'https':proxy,
    }
    session = Session()
    session.proxies = proxies
    cookies  = {
        '_gcl_au': '1.1.487927579.1764674629',
        '_ga': 'GA1.1.456567214.1764674631',
        'current_PoS': 'AIRCHINA_CN',
        'currentLang': 'en',
        'HWWAFSESTIME': '1766296761654',
        'HWWAFSESID': 'de43d94b1da2d3ef9e',
        # 'principal': 'Bearer%20eyJraWQiOiI4OTUwODJmMi0wMWRiLTQzNDctODI2MC01MmNhYmRkNDE3YzYiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOGYxYTI4YTI1OWY0YzBkYjVmMjUxYjNkYTZkYmI5MyIsImF1ZCI6InByb193ZWJzaXRlIiwibmJmIjoxNzY2Mzg5NTgxLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIl0sImlzcyI6Imh0dHBzOi8vcHJpdmF0ZS1nYXRld2F5LWN1c3RvbWVyLWNlbnRlci5oY2xvdWQuYWlyY2hpbmEuY24iLCJleHAiOjE3ODE5NDE1ODEsImlhdCI6MTc2NjM4OTU4MX0.zBo9082Z0iALd2Qht595tlzSPxw_6qJSFeBnpwRuHjJVtDoftwumtqgL2E7BKqr8KTUJwRELNvD4VuxByzgwauvufzlMfDWl9K7cZYfBsrZHJT-qYPRjaFicbtPCEh5bWJPlnBlAtrwFNjIgVtLjCFpTbNZoS8dUjlCCrnnCzh4G6QrmYlpRiptdEMw327Qbb5p7dItO60wDQFptFftzZ8K88baptGI2jS1whJAfMvRkm-baSUWTMUnyqJNqmU7yUfPZ8WM1Z-64-O3-Y1MFB1_eIxvLGWuNf0Z_quRDtEvacU-uYoGafGhmQxFRUSzX8AL2pLvcPwoI26vYQgatKKpcKugDO80Am4XszPMy4tfdd0SKiJnZaHfGxixTxQExIQWjH4Kjr5Xu2R1bkIeJzRUES-fxSOYpGZy9j0dzFk1KLgVMFqrjmBWutSKJFO4RSb7DgyjQ96Qf9jzimMPcuwgu8xYiBSIqqdxsADOX4xJe_ejqAwQpRRiwtcVnbgYu9u5_D0x7-lDHtVEkhtGSAcsM3ODsEtDXY-7B6KsKL24r5nd49fKoWEqQO5-xLZ_Oja5xHhFeqxYJC2ykBIMYQnp4tFl9fdeaiaMOBallg2FgUhSmfH_-pbtSbN_fUKBjbaf9PA_s2tCBH8oCWOBuZLus7kQ-ASoENNH--69AFQ0',
        'SESSION': 'ZjNlNTZiY2UtMGNjOS00MTBjLWFjMzQtMWQzNDY3NzE2ZGM3',
        'TKAEQLILOIB0YIMO': 'tak01j5DQKKO7BHBY3P2HHF6MDQRW6ROMASQ37PS5L6JFN7HB2MOVFJKMYAYPZREHZ24FPFNMSJVR23Y5W3JGIUZW76JK4BF7WWOAW64JFMFFO3IW5SBNFXWPKKSHZUWILLF6OTIPQZG6CNY4AMOXY5KH77KWCN3VQ',
        '_ga_CGYVD7S4G4': 'GS2.1.s1767163122$o101$g1$t1767163154$j28$l0$h0',
        'ariauseGraymode': 'false',
    }
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.airchina.com.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.airchina.com.cn/flight/oneway/pek-llv/2026-01-26',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sgm-context': '913615102144410400;913615102144410400',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'x-device-token': 'tak01j5DQKKO7BHBY3P2HHF6MDQRW6ROMASQ37PS5L6JFN7HB2MOVFJKMYAYPZREHZ24FPFNMSJVR23Y5W3JGIUZW76JK4BF7WWOAW64JFMFFO3IW5SBNFXWPKKSHZUWILLF6OTIPQZG6CNY4AMOXY5KH77KWCN3VQ',
        'x-locale': 'zh-CN',
        # 'cookie': '_gcl_au=1.1.487927579.1764674629; _ga=GA1.1.456567214.1764674631; current_PoS=AIRCHINA_CN; currentLang=en; HWWAFSESTIME=1766296761654; HWWAFSESID=de43d94b1da2d3ef9e; principal=Bearer%20eyJraWQiOiI4OTUwODJmMi0wMWRiLTQzNDctODI2MC01MmNhYmRkNDE3YzYiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOGYxYTI4YTI1OWY0YzBkYjVmMjUxYjNkYTZkYmI5MyIsImF1ZCI6InByb193ZWJzaXRlIiwibmJmIjoxNzY2Mzg5NTgxLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIl0sImlzcyI6Imh0dHBzOi8vcHJpdmF0ZS1nYXRld2F5LWN1c3RvbWVyLWNlbnRlci5oY2xvdWQuYWlyY2hpbmEuY24iLCJleHAiOjE3ODE5NDE1ODEsImlhdCI6MTc2NjM4OTU4MX0.zBo9082Z0iALd2Qht595tlzSPxw_6qJSFeBnpwRuHjJVtDoftwumtqgL2E7BKqr8KTUJwRELNvD4VuxByzgwauvufzlMfDWl9K7cZYfBsrZHJT-qYPRjaFicbtPCEh5bWJPlnBlAtrwFNjIgVtLjCFpTbNZoS8dUjlCCrnnCzh4G6QrmYlpRiptdEMw327Qbb5p7dItO60wDQFptFftzZ8K88baptGI2jS1whJAfMvRkm-baSUWTMUnyqJNqmU7yUfPZ8WM1Z-64-O3-Y1MFB1_eIxvLGWuNf0Z_quRDtEvacU-uYoGafGhmQxFRUSzX8AL2pLvcPwoI26vYQgatKKpcKugDO80Am4XszPMy4tfdd0SKiJnZaHfGxixTxQExIQWjH4Kjr5Xu2R1bkIeJzRUES-fxSOYpGZy9j0dzFk1KLgVMFqrjmBWutSKJFO4RSb7DgyjQ96Qf9jzimMPcuwgu8xYiBSIqqdxsADOX4xJe_ejqAwQpRRiwtcVnbgYu9u5_D0x7-lDHtVEkhtGSAcsM3ODsEtDXY-7B6KsKL24r5nd49fKoWEqQO5-xLZ_Oja5xHhFeqxYJC2ykBIMYQnp4tFl9fdeaiaMOBallg2FgUhSmfH_-pbtSbN_fUKBjbaf9PA_s2tCBH8oCWOBuZLus7kQ-ASoENNH--69AFQ0; SESSION=ZjNlNTZiY2UtMGNjOS00MTBjLWFjMzQtMWQzNDY3NzE2ZGM3; TKAEQLILOIB0YIMO=tak01j5DQKKO7BHBY3P2HHF6MDQRW6ROMASQ37PS5L6JFN7HB2MOVFJKMYAYPZREHZ24FPFNMSJVR23Y5W3JGIUZW76JK4BF7WWOAW64JFMFFO3IW5SBNFXWPKKSHZUWILLF6OTIPQZG6CNY4AMOXY5KH77KWCN3VQ; _ga_CGYVD7S4G4=GS2.1.s1767163122$o101$g1$t1767163154$j28$l0$h0; ariauseGraymode=false',
    }
    json_data = {
        'params': '3587a9960e706a2eb8b9fb92305efda1ae929c50b3beba105e75a2e1d3ea88d194198c5052e48b95baf3e4543536a8695e25faaabef9a2c9296572cff2a4b00719f5d6e549e6cf883ca7af6393d8b7f289ba9ad494676e8655f6b686d7cb5c7176eaa09f87d6f3aeac197c85debb379b66ce1814274587a1e02bb7a27626d67c30fccaa974b1fa032847a87331b258da4da813adea2e03073ab7031c0f6efef40caface14c89f96be7556324f8a9fd13a3fa3950ca60fc66fe19df59b517dce98e1968ec8e77d895f256ac43a3545f4dd6e38e54e0b8bdf152f5fa820be9249a77c5e93d3858face63b0dd6dda4c11e1858d4322e7f8efdb15379b2d41e11c8e6b2098436100c77c0e9b6e367df3c4a42ce6e06805f90a038ff0edd6a9819c40c8c39512de374a4017fb62dec094fe7453c8a39caaf5a8e88aca74c14b488eed391f1118ed4edffdbe23c0edaf0435bb332b814b935e9c2d6926046e220221f63b3d61f060f26023fd7663f9281adb2f217c0c958f94c1305a1db749cd34c399431c51e0ac725e',
        'RequestParameterEncryptionIdentificationBit': True,
    }
    response = session.post('https://www.airchina.com.cn/gateway/api/flight/list',cookies=cookies,headers=headers,json=json_data)
    options = response.json().get('Options')
    captcha_solver = JDCaptchaSolver(options)
    time.sleep(1)
    captcha_solver.solve()

    pass
