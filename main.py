import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from datetime import datetime

def scrape_and_save():
    # 改用 "HiStock 嗨投資" 的台股大盤頁面，這裡比較不會擋雲端 IP
    url = "https://histock.tw/stock/twa.aspx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    filename = "data.csv"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        volume = None
        
        # 策略：在頁面上尋找 "成交金額" 這四個字
        target_label = soup.find(string=re.compile("成交金額"))
        
        if target_label:
            # 找到標籤後，往上找父層級，通常數值就在附近
            parent = target_label.parent
            
            # 取得父層級的所有文字 (例如: "成交金額：4459.18億")
            full_text = parent.text.strip()
            
            # 使用正規表達式抓取其中的數字 (包含逗號和小數點)
            # 抓取邏輯：找 "成交金額" 後面的數字
            match = re.search(r'[\d,]+\.?\d*', full_text.split("成交金額")[-1])
            
            if match:
                volume = match.group(0).replace(",", "")
            else:
                # 如果同一行沒找到，試試看下一個標籤 (有些網站是分開寫的)
                next_node = parent.find_next_sibling()
                if next_node:
                    volume = next_node.text.strip().replace(",", "").replace("億", "")

        if volume:
            today_date = datetime.now().strftime("%Y-%m-%d")
            print(f"[{today_date}] 抓取成功 (來源:HiStock)：{volume} 億")

            file_exists = os.path.isfile(filename)
            
            with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["日期", "成交量(億)"])
                writer.writerow([today_date, volume])
        else:
            print("抓取失敗：找不到成交金額數值")
            # 印出部分網頁內容來除錯
            print("網頁標題:", soup.title.text if soup.title else "無標題")

    except Exception as e:
        print(f"程式執行錯誤: {e}")

if __name__ == "__main__":
    scrape_and_save()
