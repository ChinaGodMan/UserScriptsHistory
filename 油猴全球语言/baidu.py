import hashlib
import requests
import time

def calculate_md5(value):
    md5 = hashlib.md5()
    md5.update(value.encode('utf-8'))
    return md5.hexdigest()

def baidu_translate(from_text, target_lang, appid='20240513002050392', secret_key='evAKKTnaxMEpHrnCxwDC'):
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    salt =  str(int(time.time())) # 可以生成随机数来代替
    sign = calculate_md5(appid + from_text + salt + secret_key)
    params = {
        'q': from_text,
        'from': 'auto',
        'to': target_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果状态码不是200，则抛出HTTPError异常
        result = response.json()
        if 'trans_result' in result and len(result['trans_result']) > 0:
            trans_result = result['trans_result'][0]
            form_text = trans_result['src']
            to_text = trans_result['dst']
            print(f"翻译结果：{form_text} -> {to_text}")
            return to_text
        else:
            print("百度翻译返回的结果为空")
            return None
    except requests.exceptions.RequestException as e:
        print(f"百度翻译请求失败: {e}")
        return None

# 示例用法
translated_text = baidu_translate("/// @name:zh-CN        ChatGPT 代码字体变小f", "en")
print(translated_text)
