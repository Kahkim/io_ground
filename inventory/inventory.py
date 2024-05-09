from configs import * 

class Inventory:
    def __init__(self):
        self.num_stock = 0
    
    def fill_in(self, n):
        self.num_stock = min(self.num_stock+n, MAX_STOCK)

    def fill_out(self, n):
        self.num_stock = max(self.num_stock-n, MIN_STOCK)