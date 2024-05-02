import requests
from bs4 import BeautifulSoup

def get_stock_price(stock_code):
    # 3일간의 주식 정보를 가져오기 위한 URL
    url = f"https://finance.naver.com/item/sise_day.nhn?code={stock_code}"

    # 네이버 금융의 User-Agent 정보
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }

    # HTTP GET 요청 보내기
    response = requests.get(url, headers=headers)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # HTML 파싱을 위해 BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')

        # 주식 정보가 포함된 테이블 찾기
        stock_table = soup.find("table", {"class": "type2"})

        # 테이블에서 각 행을 가져와 출력
        rows = stock_table.find_all("tr", {"onmouseover":"mouseOver(this)"})[0:3]  # 최근 3일간의 정보만 가져옴        
        for row in rows:
            # print(row)
            cols = row.find_all("td")
            date = cols[0].text.strip()
            close_price = cols[1].text.strip()
            change_price = cols[2].text.strip()
            diff_ratio = cols[3].text.strip()
            print("날짜:", date)
            print("종가:", close_price)
            print("전일대비:", change_price)
            print("등락률:", diff_ratio)

    else:
        print("주식 정보를 가져오지 못했습니다.")

# 삼성전자 주식 코드: 005930
stock_code = "005930"
get_stock_price(stock_code)
