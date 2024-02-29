import requests
from datetime import datetime, timezone
from collections import defaultdict, Counter

def fetch_weather_forecast(api_key, city_name, lang='zh_tw'):
    """從OpenWeatherMap獲取5天的天氣預報數據，結果為中文"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric&lang={lang}"
    response = requests.get(url)
    return response.json()

def process_weather_data(data):
    """處理天氣數據，聚合每天的信息"""
    daily_summary = defaultdict(lambda: {'temps': [], 'descriptions': []})
    total_temp = 0
    total_count = 0

    for entry in data['list']:
        # 將Unix時間戳轉換為日期
        date = datetime.fromtimestamp(entry['dt'], timezone.utc).strftime('%Y-%m-%d')
        temp = entry['main']['temp']
        description = entry['weather'][0]['description']

        daily_summary[date]['temps'].append(temp)
        daily_summary[date]['descriptions'].append(description)
        total_temp += temp
        total_count += 1

    # 打印每天的平均溫度和最常見的天氣描述
    for date, info in daily_summary.items():
        avg_temp = sum(info['temps']) / len(info['temps'])
        most_common_desc = Counter(info['descriptions']).most_common(1)[0][0]
        print(f"{date}: 平均溫度 = {avg_temp:.2f}°C, 天氣 = {most_common_desc}")

    # 計算並打印5天的整體平均溫度
    overall_avg_temp = total_temp / total_count
    print(f"\n5天的整體平均溫度 = {overall_avg_temp:.2f}°C")

# 用API密鑰替換api_key，並替換city_name為想查詢的城市
api_key = '95a09082dafd88d8c93df38eebf4dfb7'  # 替換為API密鑰
city_name = 'Taipei'

data = fetch_weather_forecast(api_key, city_name)
if data:
    process_weather_data(data)
