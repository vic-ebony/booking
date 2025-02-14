import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"下載網頁失敗：{e}")
        return None

def search_keyword_in_page(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator="\n")
    
    if keyword in text:
        print(f"在網頁中找到關鍵字：'{keyword}'")
        # 可進一步做細部解析或提取相關區塊
    else:
        print(f"網頁中找不到關鍵字：'{keyword}'")

def main():
    # 替換成目標飯店網站的 URL
    url = "https://www.fleurdechinehotel.com/fdc-tw/pages/31/31/406"
    keyword = "情人節 活動"
    
    html = fetch_page(url)
    if html:
        search_keyword_in_page(html, keyword)

if __name__ == "__main__":
    main()
