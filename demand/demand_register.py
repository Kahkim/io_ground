import csv

f = open('plan_demand_exp.txt','r')
r = csv.reader(f)

for l in r:
    print(l)