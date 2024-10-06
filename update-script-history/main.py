import json
import os
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
import time

# 使用 curl 下载 JSON 数据
def download_json(url):
    try:
        result = subprocess.run(['curl', '-L', '-s', url], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"错误：无法从 {url} 获取 JSON 数据: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"错误：解析 JSON 数据时出错: {e}")
        return None

# 从远程 URL 获取 JSON 数据
data = download_json('https://github.com/ChinaGodMan/UserScripts/raw/main/docs/ScriptsPath.json')
if data is None:
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
    scriptname = script.get('name')
    
    # 获取数据
    star_json = download_json(url)
    
    # 调试信息
    print(f"{scriptname}请求 URL: {url}")
    
    # 检查响应内容是否为有效的 JSON
    if star_json is None:
        print(f"错误：请求失败，无法获取数据")
        continue
    
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
