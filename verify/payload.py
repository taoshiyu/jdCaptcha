import random
import time

state = {
    "canceled": False,
    "fp_req": True,
    "st": "",
    "firstStep": None,
    "imgJsonStr": "",
    "captchaType": 0,
    "isAppDisplayEmbed": False,
    "appId": "",
    "md5Salt": "dzHdg!axOg537gYr3zf&dSrvm@t4a+8F", # js 固定值?
    "sessionId": "JbWImgABAAAGMkrAw2sAMNxTs2D5Axxt3dU_7n5OZLar7YGQyCkT-_oA8ndZMag9-61zSynmd7IiGztFUMXyPAAA", # 来自接口
    "width": 0,
    "language": 1,
    "account": None,
    "ccode": None,
    "eid": None,
    "pin": None,
    "display": "popup",
    "host": "https://captcha-api-global.jdcloud.com",
    "tdat_code": 57972,
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
    "devcInfo": "{\"capfp\":{},\"cvs\":\"b8af64bcaaf7285873eb89cf7df48484\",\"wgl\":\"1eca15a225dcee18245e9f23267dcfba\",\"pr\":\"1\",\"cd\":\"24\",\"fv\":\"\",\"fts\":\"Arial,Calibri,Cambria,Consolas,Courier,CourierNew,Georgia,Helvetica,Impact,LucidaConsole,LucidaSansUnicode,MSGothic,MSPGothic,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Symbol,Candara,Constantia,Corbel,Ebrima,FangSong,Gabriola,MicrosoftYaHei,MicrosoftYiBaiti,MingLiUExtB,PMingLiUExtB,SimHei,SimSun,SimSunExtB\",\"scr\":\"1920x1080,1920x1032\",\"cpu\":\"20\",\"pt\":\"Win32\",\"tzo\":\"Asia/Shanghai\",\"lan\":\"zh-CN\",\"wvr\":\"Google Inc. (Intel)~ANGLE (Intel, Intel(R) UHD Graphics 770 (0x00004680) Direct3D11 vs_5_0 ps_5_0, D3D11)\",\"wdr\":false,\"mem\":8,\"sdv\":\"2.0\",\"lns\":\"zh-CN,zh\",\"tsp\":\"0\"}",
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
    "tdat_ctx": "13130303032393939393530303032433633434132303831443330323343393136403932353331403832463337354233303031313030303", # 来自js
    "isMouseMove": False,
    "isInitOnload": False,
    "sen": 0,
    "appid": 360472534,# 来自接口
    "sceneid": 1016966843 # 来自接口
}

import math
import random

def random_str(length):
    e = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
         "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    n = ''
    for i in range(length):
        n += e[math.floor(35*random.random())]
    return n


from utils import js_now



def fp_payload(t:dict):
    e = js_now()
    n = e % 19
    r = t.appId
    o = t.md5Salt
    i = t.sessionId
    a = t.host
    s = t.tdat_code
    c = t.devcInfo
    u = t.language
    f = t.urlMap
    l = t.tdat_ctx
    d = {
        "si": i,
        'ct': "",
        'version': 2,
        'lang': u,
        'client': t.platformOS,
        'appConfig': {
            'appId': r,
            'md5Salt': o
        }
    }
    # d['ct'] = G(random_str(n) + str(len(d['si'])).zfill(4)) + d['si'] + c + e, s, l)


def prepare_std_string(e, use_utf8=True):
    """
    模拟 JS 代码逻辑：将输入转换为字节流并计算长度。
    e: 输入数据 (str, bytes, bytearray, 或 array.array)
    use_utf8: 对应原代码中的变量 'c'
    """

    # 1. 处理类似 ArrayBuffer 的输入
    if isinstance(e, (bytes, bytearray)):
        data_bytes = e
        is_string = False
    elif isinstance(e, str):
        data_bytes = e
        is_string = True
    else:
        raise TypeError("Cannot pass non-string/non-bytes to std::string")

    # 2. 计算长度 (变量 'l')
    if use_utf8 and is_string:
        # 对应原代码中复杂的 charCodeAt 循环（即 UTF-8 编码后的字节数）
        encoded_data = data_bytes.encode('utf-8')
        length = len(encoded_data)
    elif is_string:
        # 对应原代码中检查 255 < h 的逻辑：仅支持 ASCII/Latin-1
        try:
            encoded_data = data_bytes.encode('latin-1')
            length = len(encoded_data)
        except UnicodeEncodeError:
            raise ValueError("String has UTF-16 code units that do not fit in 8 bits")
    else:
        # 处理 TypedArray/Bytes 情况
        encoded_data = data_bytes
        length = len(data_bytes)

    # 3. 模拟内存分配 (变量 'k')
    # Emscripten 布局: [4字节长度头] + [实际数据] + [1字节空终止符 \0]
    # k >> 2 存储的是长度
    memory_block = bytearray(4)  # 模拟 N[k >> 2] = l

    # 将长度转为 4 字节小端序（模拟 C++ 整数存储）
    import struct
    memory_block = bytearray(struct.pack('<I', length))

    # 4. 填充数据 (模拟 I[k + 4 + g] = ...)
    memory_block.extend(encoded_data)

    # 5. 添加空终止符 (l + 1 中的 +1)
    memory_block.append(0)

    return memory_block


if __name__ == '__main__':
    arg0 = "hs6ro0088I_T2VgABAAABy6-h_l0AMHga9Ncu-SrOIxWXEP5ZzqVv_Gb3XzB1MmAWrYl_pBZd9vfgjZWBQ6CU8Npct4B6rAAA{\"capfp\":{},\"cvs\":\"b8af64bcaaf7285873eb89cf7df48484\",\"wgl\":\"1eca15a225dcee18245e9f23267dcfba\",\"pr\":\"1\",\"cd\":\"24\",\"fv\":\"\",\"fts\":\"Arial,Calibri,Cambria,Consolas,Courier,CourierNew,Georgia,Helvetica,Impact,LucidaConsole,LucidaSansUnicode,MSGothic,MSPGothic,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Symbol,Candara,Constantia,Corbel,Ebrima,FangSong,Gabriola,MicrosoftYaHei,MicrosoftYiBaiti,MingLiUExtB,PMingLiUExtB,SimHei,SimSun,SimSunExtB\",\"scr\":\"1920x1080,1920x1032\",\"cpu\":\"20\",\"pt\":\"Win32\",\"tzo\":\"Asia/Shanghai\",\"lan\":\"zh-CN\",\"wvr\":\"Google Inc. (Intel)~ANGLE (Intel, Intel(R) UHD Graphics 770 (0x00004680) Direct3D11 vs_5_0 ps_5_0, D3D11)\",\"wdr\":false,\"mem\":8,\"sdv\":\"2.0\",\"lns\":\"zh-CN,zh\",\"tsp\":\"0\"}1767087174000"
    arg0_result  = prepare_std_string(arg0)
    assert arg0_result == arg0
    print(arg0_result)
    arg1 = "13130303032393939393530303032433633434132303831443330323343393136403932353331403832463337354233303031313030303"
    arg1_result = prepare_std_string(arg1)
    assert arg1_result == arg1
