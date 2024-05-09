import pandas as pd
import numpy as np
from datetime import datetime
from inventory.inventory import Inventory
from sales.sales import Sales

from configs import * 

class Company:

    def __init__(self):
        self.inven = Inventory()
        self.sales = Sales()
        self.date_list = self.sales.get_date_list()

        self.balance = 100000
        self.tot_sales = 0

    def get_today_demand(self, day):
        return self.sales.get_demand(day)

    # 3시 판매
    def go_sale(self, day):
        
        # 판매 재고처리
        demand = self.get_today_demand(day)
        sales_amount = min(demand, self.inven.num_stock)
        self.inven.fill_out(sales_amount)
        self.tot_sales += sales_amount

        # 회계 수입 처리
        income = PRICE_PER_UNIT * sales_amount
        self.balance += income

        print(f'# demand {demand}, sales {sales_amount}, income {income}')

    # 4시 생산
    def go_prod(self):
        
        # 무조건 x개 생산
        n = 200000
        self.inven.fill_in(n)

        # 회계 지출 처리
        outcome = 0
        if n > 0:
            outcome += PROD_SETUP_COST 
            outcome += PROD_COST_UNIT * n
            self.balance -= outcome

        print(f'# production {n}, outcome {outcome}')

    # 5시 잔여재고 처리
    def go_inven_mgt(self):
        
        # 재고비용 0
        pass

def main():
    company = Company()
    
    # for x in company.date_list.values:        
    #     if np.datetime64('2024-01-02') == x:
    #     # if np.datetime64('2024-01-02T00:00:00.000000000') == x:
    #         print(x)

    num_days = 5

    for day, i in zip(company.date_list[:num_days], range(num_days)):
        
        print(f'day {day} {'-'*20} {i}')
        print(f'begining ===')
        print(f'# inventory {company.inven.num_stock}')
        print(f'balance {company.balance}')

        company.go_sale(day)
        
        if i % 2 == 0 and i != num_days-1:
            company.go_prod()

        company.go_inven_mgt()

        print(f'ending ===')
        print(f'# inventory {company.inven.num_stock}')
        print(f'balance {company.balance}')
        print(f'tot_sales {company.tot_sales}')
        print('\n')

if __name__ == "__main__":
    main()
