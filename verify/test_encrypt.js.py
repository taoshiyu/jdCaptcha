import subprocess
import json
import time


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

    def encrypt(self, arg0, arg1,arg2):
        # 发送参数
        payload = json.dumps([arg0, arg1,arg2])
        self.process.stdin.write(payload + '\n')
        self.process.stdin.flush()

        # 读取结果
        response = self.process.stdout.readline().strip()
        return json.loads(response)

    def getCaptchaAuth(self,arg0,arg1):
        payload = json.dumps([arg0,arg1])
        self.process.stdin.write(payload + '\n')
        self.process.stdin.flush()

        # 读取结果
        response = self.process.stdout.readline().strip()
        return json.loads(response)


import threading

class ThreadSafeEncryptor:
    def __init__(self):
        self._bridge = NodeBridge() # 之前定义的桥接类
        self._lock = threading.Lock() # 定义互斥锁

    def encrypt(self, a, b):
        with self._lock: # 确保同一时间只有一个线程在读写管道
            return self._bridge.encrypt("getEncryptData",a, b)

    def captchaAuth(self,a):
        with self._lock:
            return self._bridge.getCaptchaAuth("getCaptchaAuth",a)

# 现在你可以安全地在多线程中共享这个实例了

# 使用示例
bridge = ThreadSafeEncryptor()  # 只初始化一次
time.sleep(3)
while True:
    arg0 = 'w0088DbqFeQABAAACvgOGCQgAMOZiKheOsMR5riuXLEITICQEXpnzQpK9y_R0ushvS5mJre77SNJ1TNyoTSQIVzu6RQAA{"capfp":{},"cvs":"b8af64bcaaf7285873eb89cf7df48484","wgl":"1eca15a225dcee18245e9f23267dcfba","pr":"1","cd":"24","fv":"","fts":"Arial,Calibri,Cambria,Consolas,Courier,CourierNew,Georgia,Helvetica,Impact,LucidaConsole,LucidaSansUnicode,MSGothic,MSPGothic,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Symbol,Candara,Constantia,Corbel,Ebrima,FangSong,Gabriola,MicrosoftYaHei,MicrosoftYiBaiti,MingLiUExtB,PMingLiUExtB,SimHei,SimSun,SimSunExtB","scr":"1920x1080,1920x1032","cpu":"20","pt":"Win32","tzo":"Asia/Shanghai","lan":"zh-CN","wvr":"Google Inc. (Intel)~ANGLE (Intel, Intel(R) UHD Graphics 770 (0x00004680) Direct3D11 vs_5_0 ps_5_0, D3D11)","wdr":false,"mem":8,"sdv":"2.0","lns":"zh-CN,zh","tsp":"0"}1767163180000'
    arg1 = "13130303032393939393530303032433633434132303831443330323343393136403932353331403832463337354233303031313030303"
    print(bridge.encrypt(arg0, arg1))
    print(bridge.captchaAuth(""))
    break



# print(res)