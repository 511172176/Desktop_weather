# Python程式設計 - 桌面天氣

## 主題發想
- **目標**：讓日常查詢天氣更便利化。
- **解決方案**：利用API取得每天及未來5天的天氣資訊，並且利用socket傳輸到IoT裝置，可以放在隨時可看到的位置增加生活便利性。

## 延伸構思
- **自動化執行**：把程式轉換為執行檔，預設於開機時執行，這樣就能隨時看到最新的天氣預報資訊。

## 資源
- **天氣API**：[OpenWeatherMap](https://home.openweathermap.org/)

## 硬件
- **開發語言**：Python、MicroPython
- **開發板**：ESP32
- **OLED螢幕**：1.3吋SH1106

## 實現方式
1. **設定OpenWeatherMap API**：在OpenWeatherMap網站上註冊並取得API密鑰。
2. **撰寫Python程式**：
   - 使用requests模組從OpenWeatherMap API取得天氣資訊。
   - 使用socket模組建立伺服器，將天氣資訊傳送到ESP32裝置。
3. **撰寫MicroPython程式**：
   - 在ESP32上執行，使用Wi-Fi連接到Python程式建立的伺服器。
   - 從伺服器接收天氣資訊，並使用SH1106模組將資訊顯示在OLED螢幕上。
4. **自動化執行**：
   - 將Python程式轉換為執行檔。
   - 設定電腦開機時自動執行該執行檔。

## 預期效果
- 使用者能夠在不特地查詢的情況下，直接從擺放在桌面上的ESP32裝置看到即時及未來幾天的天氣預報，提高生活便利性。
