import pandas as pd
import numpy as np

class Sales:
    
    def __init__(self):
        self.demands = pd.read_csv('sales/005930.csv', header=0, engine='python')
        # 콤마, 빈칸, 날짜타입 전처리
        self.demands = self.demands.replace(',', '', regex=True)
        self.demands = self.demands.replace(' ', '', regex=True)
        self.demands['날짜'] = pd.to_datetime(self.demands['날짜'])
        self.demands['종가'] = self.demands['종가'].astype('int64')
        # index 설정
        self.demands.reset_index(drop=True, inplace=True)
        self.demands.set_index(['날짜'], inplace=True)        
        # 종가만
        self.demands = self.demands[['종가']]
        # 날짜기준 정렬
        self.demands.sort_index(inplace=True)
        # # 일단 10개만
        # self.demands = self.demands.iloc[:5, :]

        # print(self.demands)

    def get_demand(self, day):
        return self.demands.loc[day]['종가']

    def get_date_list(self):
        days = self.demands.index.unique().values       
        days = days.astype('datetime64[D]') 
        return days

    def get_sales_stragegy():
        return 1.0

def main():
    sales = Sales()
    sales.get_date_list()
    # print(sales.demands.info())
    # print(sales.demands)
    # for day in sales.get_date_list():
    #     print(day)
    print(sales.get_demand('2024-04-11'))

if __name__ == "__main__":
    main()
