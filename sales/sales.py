import pandas as pd

class Sales:
    
    def __init__(self):
        self.demands = pd.read_csv('sales/005930.csv', header=0, engine='python')
        # 콤마, 빈칸, 날짜타입 전처리
        self.demands = self.demands.replace(',', '', regex=True)
        self.demands = self.demands.replace(' ', '', regex=True)
        self.demands['날짜'] = pd.to_datetime(self.demands['날짜'])
        # index 설정
        self.demands.reset_index(drop=True, inplace=True)
        self.demands.set_index(['날짜'], inplace=True)        
        # 종가만
        self.demands = self.demands[['종가']]
        # 날짜기준 정렬
        self.demands.sort_index(inplace=True)
        # 일단 10개만
        self.demands = self.demands.iloc[:5, :]

    # def get_demand(self, date):
    #     print(self.demands.loc[])

    def get_date_list(self):
        return self.demands.index.unique()

    def get_sales_stragegy():
        return 1.0

def main():
    sales = Sales()
    print(sales.demands.info())
    print(sales.demands)

if __name__ == "__main__":
    main()
