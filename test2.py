# import pymysql
# conn = pymysql.connect(host='192.168.0.3', user='io_ground', passwd='dkshk24@!', db='io_ground')

# cur = conn.cursor()

# sql = '''
#     SELECT SUM(QTY) AS INVEN FROM INVENTORY WHERE UID=%s AND TID=%s AND QTY>0 AND PROD_DATE<%s
# '''
# print(sql, ('DGU', 'T1', '2024-07-16'))
# cur.execute(sql, ('DGU', 'T1', '2024-07-16'))
# inven = cur.fetchall()
# print(inven)


# conn.close()

# import datetime

# d1 = datetime.datetime.now().strftime("%V")
# print(d1)

# date = datetime.datetime.strptime('2024-07-20', '%Y-%m-%d').strftime("%V")
# print(date)
# date = datetime.datetime.strptime('2024-07-21', '%Y-%m-%d').strftime("%V")
# print(date)
# date = datetime.datetime.strptime('2024-07-22', '%Y-%m-%d').strftime("%V")
# print(date)

# next_day_date = date + datetime.timedelta(days=1)
# print(next_day_date)


# now = datetime.datetime.now()
# print(now)
# next_day_date = now + datetime.timedelta(days=1)
# print(next_day_date)
# next_day_date = now + datetime.timedelta(days=2)
# print(next_day_date)




# Python3 code to demonstrate working of
# Next weekday from Date
# Using timedelta() + weekday()
import datetime

def next_week_days(d):
    # printing original date
    # print("The original date is : " + d.strftime('%Y-%m-%d'))
    # initializing weekday index
    weekday_idx = 0
    # computing delta days
    days_delta = weekday_idx - d.weekday()
    if days_delta <= 0:
        days_delta += 7
    # adding days to required result
    res = d + datetime.timedelta(days_delta)
    # printing result
    ret = []
    ret.append(res.strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=2)).strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=3)).strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=4)).strftime('%Y-%m-%d'))
    return ret

# initializing dates
test_date = datetime.datetime.strptime('2024-07-20', '%Y-%m-%d')
print(next_week_days(test_date))
