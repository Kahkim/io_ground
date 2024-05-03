import pandas as pd
import numpy as np
from datetime import datetime
from inventory.inventory import Inventory
from sales.sales import Sales

class Company:

    def __init__(self):
        self.inven = Inventory()
        self.sales = Sales()
        self.date_list = self.sales.get_date_list()

    def get_today_demand(self):
        return 350

    # 3시 판매
    def go_sale(self):
        
        # 무조건 300개 판매
        n = self.get_today_demand()
        self.inven.fill_out(n)

        print(f'#sales {n}')

    # 4시 생산
    def go_prod(self):
        
        # 무조건 400개 생산
        n = 400
        self.inven.fill_in(n)

        print(f'#production {n}')

    # 5시 잔여재고 처리
    def go_inven_mgt(self):
        
        # 재고비용 0
        pass

def main():
    company = Company()
    
    for x in company.date_list.values:        
        if np.datetime64('2024-01-02') == x:
        # if np.datetime64('2024-01-02T00:00:00.000000000') == x:
            print(x)

    for day in range(1):
        
        print(f'day {day}', '-'*20)
        print(f'#inventory {company.inven.num_stock}')

        company.go_sale()

        company.go_prod()

        company.go_inven_mgt()

        print(f'#inventory {company.inven.num_stock}')

if __name__ == "__main__":
    main()
