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
    daily_summary = defaultdict(lambda: {'temps': [], 'descriptions': []})
    for entry in data['list']:
        date = datetime.fromtimestamp(entry['dt'], timezone.utc).strftime('%Y-%m-%d')
        temp = entry['main']['temp']
        description = entry['weather'][0]['description']
        daily_summary[date]['temps'].append(temp)
        daily_summary[date]['descriptions'].append(description)
    return daily_summary

def send_weather_data_over_socket(data, host, port):
    """透過socket發送天氣數據"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("等待連線...")
        conn, addr = s.accept()
        with conn:
            print('已連線', addr)
            for date, info in data.items():
                avg_temp = sum(info['temps']) / len(info['temps'])
                most_common_desc = Counter(info['descriptions']).most_common(1)[0][0]
                message = json.dumps({"date": date, "avg_temp": f"{avg_temp:.2f}", "condition": most_common_desc})
                conn.sendall(message.encode('utf-8'))
                response = conn.recv(1024)
                if not response:
                    break
                print("已發送消息:", message)

# 使用OpenWeatherMap API密鑰和城市名
api_key = '95a09082dafd88d8c93df38eebf4dfb7'
city_name = 'Taipei'
data = fetch_weather_forecast(api_key, city_name)
daily_summary = process_weather_data(data)
# 設定為IP地址和端口
host = '192.168.0.10'
port = 12345
send_weather_data_over_socket(daily_summary, host, port)
