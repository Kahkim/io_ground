import pandas as pd
import numpy as np
from datetime import datetime
from inventory.inventory import Inventory
from sales.sales import Sales

from configs import * 

class Company:

    def __init__(self):
        self.inven = Inventory(100000)
        self.sales = Sales()
        self.date_list = self.sales.get_date_list()

        self.balance = INIT_BALANCE
        # self.tot_sales = 0

    def get_today_demand(self, day):
        return self.sales.get_demand(day)

    # 3시 판매
    def go_sale(self, day):
        
        # 판매 재고처리
        demand = self.get_today_demand(day)
        sales_amount = min(demand, self.inven.num_stock)
        self.inven.fill_out(sales_amount)
        # self.tot_sales += sales_amount

        # 회계 수입 처리
        income = PRICE_PER_UNIT * sales_amount
        self.balance += income

        print(f'\tsales -> # demand: {f(demand)}, # sales: {f(sales_amount)}, revenue: ${f(income)}')

    # 4시 생산
    def go_prod(self):
        
        # 무조건 x개 생산
        n = 75000
        self.inven.fill_in(n)

        # 회계 지출 처리
        cost = 0
        if n > 0:
            cost += PROD_SETUP_COST 
            cost += PROD_COST_UNIT * n
            self.balance -= cost

        print(f'\tprod -> # production {f(n)}, cost: ${f(cost)}')

    # 5시 잔여재고 처리
    def go_inven_mgt(self):
        
        # 회계 지출 처리
        cost = self.inven.num_stock * INV_COST_UNIT
        self.balance -= cost

        print(f'\tinven -> # inventory {f(self.inven.num_stock)}, cost: ${f(cost)}')

def main():
    company = Company()
    
    # for x in company.date_list.values:        
    #     if np.datetime64('2024-01-02') == x:
    #     # if np.datetime64('2024-01-02T00:00:00.000000000') == x:
    #         print(x)

    num_days = 15

    for day, i in zip(company.date_list[:num_days], range(num_days)):
        
        print(f'day {day} {'-'*20} {i}')
        print(f'begining')
        print(f'\t# inventory {f(company.inven.num_stock)}')
        print(f'\tbalance: ${f(company.balance)}')

        company.go_sale(day)
        
        if i != num_days-1:
            company.go_prod()

            company.go_inven_mgt()

        print(f'ending')
        # print(f'\t# inventory {f(company.inven.num_stock)}')
        print(f'\tbalance: ${f(company.balance)}')
        # print(f'\ttot_sales {fc(company.tot_sales)}')
        print('\n')

if __name__ == "__main__":
    main()
