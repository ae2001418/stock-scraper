import cloudscraper  # 改用這個強大的套件
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_and_save():
    url = "https://www.wantgoo.com/index/0000"
    
    # 建立強力爬蟲
    scraper = cloudscraper.create_scraper() 
    
    filename = "data.csv"

    try:
        # 使用 scraper 來發送請求
        response = scraper.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")

        target_label = soup.find(string="成交量(億)")
        volume = None
        
        if target_label:
            parent = target_label.parent
            value_element = parent.find_next_sibling() or parent.parent.find("b")
            if value_element:
                volume = value_element.text.strip().replace(",", "")

        if volume:
            today_date = datetime.now().strftime("%Y-%m-%d")
            print(f"[{today_date}] 抓取成功：{volume}")

            file_exists = os.path.isfile(filename)
            
            with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["日期", "成交量(億)"])
                writer.writerow([today_date, volume])
        else:
            print("抓取失敗：找不到數值，可能網頁結構改變")

    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    scrape_and_save()
