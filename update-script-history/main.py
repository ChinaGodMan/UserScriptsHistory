import json
import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
import time


def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，将引发 HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"错误：无法从 {url} 获取 JSON 数据: {e}")
    except json.JSONDecodeError as e:
        print(f"错误：解析 JSON 数据时出错: {e}")
    return None


def fetch_script_stats(greasyfork_id, is_sleazy,call=True):
    base_url = 'https://api.sleazyfork.org' if is_sleazy else 'https://api.greasyfork.org'
    url = f'{base_url}/scripts/{greasyfork_id}/stats.json'
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 404:
            # 如果返回 404，取反 is_sleazy 并重新调用自身
            print(f"警告：{url} 返回 404，尝试切换平台...")
            if call:
                return fetch_script_stats(greasyfork_id, not is_sleazy,False)
            else:
                return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"错误：请求 {url} 时失败: {e}")
    except json.JSONDecodeError as e:
        print(f"错误：解析脚本统计数据时出错: {e}")
    return None


def plot_script_stats(script_name, greasyfork_id, star_json):
    """
    绘制并保存脚本的统计图像
    :param script_name: 脚本名称
    :param greasyfork_id: 脚本 ID,用于保存文件名
    :param star_json: 脚本统计数据 JSON
    """
    star_date = []
    star_installs = []
    star_temp = 0

    for date, stats in star_json.items():
        star_date.append(date)
        star_temp += stats.get('installs', 0)
        star_installs.append(star_temp)
    output_dir = 'stats'
    os.makedirs(output_dir, exist_ok=True)

    # 绘制图像
    plt.style.use("cyberpunk")
    plt.figure(figsize=(20, 10), dpi=100)
    plt.rcParams['font.sans-serif'] = ['HYWenHei']  # 用来正常显示中文标签
    plt.title(script_name, fontdict={'size': 30})
    plt.xlabel("日期(Date)", fontdict={'size': 30})
    plt.ylabel("安装数 Installs(Greasy Fork)", fontdict={'size': 30})
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(pd.to_datetime(star_date), star_installs, linewidth=4.0)
    output_path = os.path.join(output_dir, f'{greasyfork_id}.png')
    mplcyberpunk.make_lines_glow()  # 使线条发光
    mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)  # 添加渐变填充
    plt.savefig(output_path)
    plt.close()


def main():
    # 人民的勤务员脚本列表
    url = 'https://github.com/ChinaGodMan/UserScripts/raw/main/docs/ScriptsPath.json'
    data = fetch_json_data(url)

    if not data:
        print("错误：无法获取脚本列表")
        return

    for script in data.get('scripts', []):
        greasyfork_id = script.get('greasyfork_id')
        if not greasyfork_id:
            print("错误：脚本数据不完整")
            continue

        script_name = script.get('name', 'Unknown Script')
        is_sleazy = script.get('isSleazy', False)

        # 获取脚本统计数据
        star_json = fetch_script_stats(greasyfork_id, is_sleazy)
        if not star_json:
            continue

        # 绘制图像
        plot_script_stats(script_name, greasyfork_id, star_json)

        # 延时 3 秒钟
        time.sleep(3)


if __name__ == "__main__":
    main()
