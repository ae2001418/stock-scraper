import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# 設定台北時間 (因為雲端電腦通常是 UTC 時間，我們需要手動調整或單純抓取當下)
# 這裡我們簡單做，抓到的資料直接寫入，日期抓當天即可

def scrape_and_save():
    url = "https://www.wantgoo.com/index/0000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.wantgoo.com/",  # 告訴網站你是從他們首頁點進來的
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    
    filename = "data.csv"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 定位成交量
        target_label = soup.find(string="成交量(億)")
        volume = None
        
        if target_label:
            parent = target_label.parent
            value_element = parent.find_next_sibling() or parent.parent.find("b")
            if value_element:
                volume = value_element.text.strip().replace(",", "")

        if volume:
            # 取得今天的日期
            today_date = datetime.now().strftime("%Y-%m-%d")
            print(f"[{today_date}] 抓取成功：{volume}")

            # 檢查檔案是否存在
            file_exists = os.path.isfile(filename)
            
            # 使用 'a' (append) 模式附加資料
            with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["日期", "成交量(億)"])
                
                writer.writerow([today_date, volume])
        else:
            print("抓取失敗：找不到數值")

    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":

    scrape_and_save()
