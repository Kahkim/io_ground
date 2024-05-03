class Inventory:
    def __init__(self):
        self.num_stock = 0
        self.max_num_stock = 150000
        self.min_num_stock = 0
    
    def fill_in(self, n):
        self.num_stock = min(self.num_stock+n, self.max_num_stock)

    def fill_out(self, n):
        self.num_stock = max(self.num_stock-n, self.min_num_stock)