import yfinance as yf

def get_stock_data(ticker, start_date, end_date):
    try:
        # 주식 데이터 가져오기
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def save_to_csv(stock_data, filename):
    try:
        # 데이터프레임을 CSV 파일로 저장
        stock_data.to_csv(filename)
        print(f"Data saved to {filename} successfully.")
    except Exception as e:
        print(f"Error occurred while saving data to CSV: {e}")
        
def main():
    ticker = "005930.KS"  # 삼성전자의 티커 (한국거래소: .KS)
    start_date = "2024-04-01"  # 시작일
    end_date = "2024-06-01"    # 종료일

    # 주식 데이터 가져오기
    stock_data = get_stock_data(ticker, start_date, end_date)
    
    if stock_data is not None:
        print(stock_data.head())  # 데이터의 처음 5행 출력
        print(stock_data.tail())  # 데이터의 마지막 5행 출력
    
    # CSV 파일로 저장
    save_to_csv(stock_data, "stock_data.csv")

if __name__ == "__main__":
    main()
