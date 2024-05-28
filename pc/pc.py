#軟創二乙
#511172176
#李則霖

import socket
import json
import requests
from datetime import datetime, timezone
from collections import defaultdict, Counter

def fetch_weather_forecast(api_key, city_name):
    """使用OpenWeatherMap API獲取城市的英文天氣預報"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric&lang=en"
    response = requests.get(url)
    return response.json()

def process_weather_data(data):
    """處理天氣數據，聚合每天的平均溫度和最常見的天氣描述"""
    daily_summary = defaultdict(lambda: {'temps': [], 'descriptions': []})#用defaultdict+lambda建立預設字典
    for entry in data['list']:  #for遍歷data
        date = datetime.fromtimestamp(entry['dt'], timezone.utc).strftime('%Y-%m-%d') #日期
        temp = entry['main']['temp'] #定義溫度變數
        description = entry['weather'][0]['description'] #定義天氣狀態變數
        daily_summary[date]['temps'].append(temp) #添加溫度
        daily_summary[date]['descriptions'].append(description) #添加天氣狀態
    return daily_summary

def send_weather_data_over_socket(data, host, port):
    """透過socket發送天氣數據"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #使用with確保正常關閉socket
        s.bind((host, port))
        s.listen() #監聽
        print("等待連線...")
        conn, addr = s.accept() #連線確認
        with conn:
            print('已連線', addr)
            for date, info in data.items(): #for遍歷data
                avg_temp = sum(info['temps']) / len(info['temps']) #平均天氣
                most_common_desc = Counter(info['descriptions']).most_common(1)[0][0] #出現最多次的狀態
                #轉成JSON
                message = json.dumps({"date": date, "avg_temp": f"{avg_temp:.2f}", "condition": most_common_desc})
                conn.sendall(message.encode('utf-8')) #發送
                response = conn.recv(1024)
                if not response:
                    break 
                print("已發送消息:", message) #沒有數據接收結束

# 使用OpenWeatherMap API密鑰和城市名
api_key = '95a09082dafd88d8c93df38eebf4****'
city_name = 'Taipei'
data = fetch_weather_forecast(api_key, city_name)
daily_summary = process_weather_data(data)
# 設定為IP地址和端口
host = '192.168.0.10'
port = 12345
send_weather_data_over_socket(daily_summary, host, port)