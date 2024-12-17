import json
import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
import time

# ggg从远程 URL 获取 JSON 数据
url = 'https://github.com/ChinaGodMan/UserScripts/raw/main/docs/ScriptsPath.json'
try:
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，将引发 HTTPError
    data = response.json()  # 解析 JSON 数据
except requests.exceptions.RequestException as e:
    print(f"错误：无法从 {url} 获取 JSON 数据: {e}")
    exit()
except json.JSONDecodeError as e:
    print(f"错误：解析 JSON 数据时出错: {e}")
    exit()

for script in data.get('scripts', []):
    # 获取 GreasyFork 的 ID 和备份路径
    greasyfork_id = script.get('GreasyFork')
    
    if not greasyfork_id:
        print("错误：脚本数据不完整")
        continue

    # 根据 isSleazy 的值选择不同的 URL
    is_sleazy = script.get('isSleazy', False)
    base_url = 'https://sleazyfork.org' if is_sleazy else 'https://greasyfork.org'
    url = f'{base_url}/zh-CN/scripts/{greasyfork_id}/stats.json'
    scriptname=script.get('name')
    # 获取数据
    response = requests.get(url)
    
    # 调试信息
    print(f"{scriptname}请求 URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text[:500]}")  # 只打印前500个字符
    
    # 检查响应内容是否为有效的 JSON
    if response.status_code != 200:
        print(f"错误：请求失败，状态码 {response.status_code}")
        continue
    
    try:
        star_json = json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"解析 JSON 时出错: {e}")
        continue  # 如果解析出错，跳过这个脚本
    
    star_date = []
    star_installs = []
    star_temp = 0
    
    for i in star_json:
        star_date.append(str(i))
        star_temp += star_json[i].get('installs', 0)
        star_installs.append(star_temp)
    
    # 打印调试信息
    print("日期:", star_date)
    print("安装数:", star_installs)
    
    # 确保固定输出文件夹 "stats" 存在
    output_dir = 'stats'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 绘制图像
    plt.style.use("cyberpunk")
    plt.figure(figsize=(20, 10), dpi=100)
    plt.rcParams['font.sans-serif'] = ['HYWenHei']  # 用来正常显示中文标签
    plt.title(script.get('name'), fontdict={'size': 30})
    plt.xlabel("时间(Time)", fontdict={'size': 30})
    plt.ylabel("总安装数 Installs（Greasy Fork）", fontdict={'size': 30})
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(pd.to_datetime(star_date), star_installs, linewidth=4.0)
    
    # 使用 greasyfork_id 作为文件名保存图片
    output_path = os.path.join(output_dir, f'{greasyfork_id}.png')
    plt.savefig(output_path)
    plt.close()
    
    # 延时 3 秒钟
    time.sleep(3)
