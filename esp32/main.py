import socket
import json
import network
import machine
import sh1106
import time

# 連接到 Wi-Fi
def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print('連接成功:')
    print(station.ifconfig())

# 初始化 OLED 顯示
def init_oled():
    # 使用 SoftI2C 來代替 I2C
    i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
    oled = sh1106.SH1106_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()
    return oled

# 分頁顯示天氣數據，並持續保持螢幕更新
def display_weather(oled, weather_data):
    while True:  # 使用無限迴圈以保持螢幕更新
        for page in range((len(weather_data) + 2) // 3):  # 循環分頁
            oled.fill(0)  # 清屏
            for index in range(3):  # 每頁顯示3天
                data_index = page * 3 + index
                if data_index < len(weather_data):
                    data = weather_data[data_index]
                    date = data['date'].split('-')[1:]  # 獲取月和日
                    formatted_date = "/".join(date)
                    display_text = '{} {:.2f} C'.format(formatted_date, float(data['avg_temp']), data['condition'])

                    oled.text(display_text, 0, index * 20)
                    oled.text(data['condition'], 0, index * 20 + 10)
            oled.show()
            time.sleep(5)  # 暫停幾秒後再顯示下一頁

# 連接到伺服器並獲取天氣數據
def connect_to_server(oled, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    weather_data = []
    while True:
        data = s.recv(1024)
        if not data:
            break
        weather_data.append(json.loads(data.decode('utf-8')))
        s.send("ack".encode('utf-8'))
    s.close()
    display_weather(oled, weather_data)

# 主函數
def main():
    ssid = ''
    password = ''
    connect_wifi(ssid, password)
    oled = init_oled()
    host = '192.168.0.10'  # 伺服器IP
    port = 12345  # 伺服器端口
    connect_to_server(oled, host, port)

if __name__ == "__main__":
    main()

