

import base64
import time


def btoa(data):
    if isinstance(data, str):
        data = data.encode()
    else:
        data = data
    return base64.b64encode(data).decode()


def atob(data):
    if isinstance(data, str):
        data = data.encode()
    else:
        data = data
    return base64.b64decode(data).decode()


def js_now():
    return int(time.time() * 1000)


def unescape(s):
    return s.encode('raw_unicode_escape').decode('unicode_escape')


if __name__ == '__main__':
    a = atob('ZGVwQ2l0eT1DQU4mYXJyQ2l0eT1QS1gmZmxpZ2h0RGF0ZT0yMDI1MTExMyZhZHVsdE51bT0xJmNoaWxkTnVtPTAmaW5mYW50TnVtPTAmY2FiaW5PcmRlcj0wJmFpckxpbmU9MSZmbHlUeXBlPTAmaW50ZXJuYXRpb25hbD0wJmFjdGlvbj0wJnNlZ1R5cGU9MSZjYWNoZT0wJnByZVVybD0maXNNZW1iZXI9Jmxhbmd1YWdlPXpoJmJ1c2luZXNzVHlwZT1DT01NT04maXNNdWx0aXBhc3M9MQ')
    print(a)
