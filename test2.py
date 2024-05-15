
inventory = 100 # global variable 전역변수

def sales():
    global inventory
    inventory = inventory - 10
    print('sales inventory', inventory)

def production():
    global inventory
    inventory = inventory + 1000
    print('production inventory', inventory)

sales()
production()
print(inventory)