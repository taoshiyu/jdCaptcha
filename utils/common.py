import re


def parse_callback_params(json_resp):
    match = re.search(r'.*\((.*?)\)', json_resp, re.S)
    if match:
        return match.group(1)


def get_mime_type(content):
    signatures = {
        b'\xff\xd8\xff': 'image/jpeg',
        b'\x89PNG\r\n\x1a\n': 'image/png',
        b'GIF87a': 'image/gif',
        b'GIF89a': 'image/gif',
        b'BM': 'image/bmp',
        b'II*\x00': 'image/tiff',  # 小端序TIFF
        b'MM\x00*': 'image/tiff',  # 大端序TIFF
        b'RIFF....WEBP': 'image/webp',
        b'%PDF': 'application/pdf',  # PDF也可能包含图片
    }
    for signature, mime_type in signatures.items():
        if content.startswith(signature):
            # 对于变长签名，如WEBP需要特殊处理
            if signature == b'RIFF....WEBP' and len(content) >= 12:
                if content[8:12] == b'WEBP':
                    return 'image/webp'
            return mime_type


if __name__ == '__main__':
    import json

    json_resp = 'light.packetRequest._packetCallbacks.callback0({"stat":"ok","info":{"product":[{"name":"rds","validated":true,"message":""}],"rdsToken":"ctXvukrrxeF0B8SNO4R42SZiOSW62seg","packet":"all"}})'
    print(json.loads(parse_callback_params(json_resp)))
