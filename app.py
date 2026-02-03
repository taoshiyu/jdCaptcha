from bustapi import BustAPI,request
import json
from verify.captcha_solver import JDCaptchaSolver
from loguru import logger
app = BustAPI()
from ddddocr import DdddOcr
ocr_object = DdddOcr(det=False,show_ad=False)
import base64


def solve_ocr(img):
    b2_content = base64.b64decode(img.split(',')[1].encode())
    result = ocr_object.classification(b2_content)
    return result


@app.get('/test')
def test():
    return 'hello world'

@app.post('/solve_captcha')
def captcha_solve():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    # logger.info(data)
    options = data.get('options')
    location_url = data.get('location_url')
    proxy_url = data.get('proxy_url')
    solver = JDCaptchaSolver(options,proxy_url=proxy_url,location_url=location_url)
    try:
        result = solver.solve()
    except Exception as e:
        return {'code':2,'msg':str(e)}
    if result is None:
        return {'code':1,'msg':'失败'}
    else:
        return {'code':0,'msg':'成功','data':result}


@app.post('/solve_ocr')
def ocr_solve():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    try:
        kaptcha = data.get('kaptcha')
        ocr_result = solve_ocr(kaptcha)
        return {'code': 0, 'msg': '','data':ocr_result}
    except Exception as e:
        return {'code':2,'msg':str(e),'data':None}


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5051)