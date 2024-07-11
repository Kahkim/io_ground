# import pymysql
# conn = pymysql.connect(host='192.168.0.3', user='io_ground', passwd='dkshk24@!', db='io_ground')

# cur = conn.cursor()

# cur.execute("INSERT INTO Test(TYPE, Contents) VALUES ('AA','TEXT!!!')")
# conn.commit()

# cur.execute('select * from Test')
# ret = cur.fetchall()
# for r in ret:
#     print(r)

# conn.close()

import datetime

date = datetime.datetime.strptime('2024-06-12', '%Y-%m-%d')
print(date.weekday())

next_day_date = date + datetime.timedelta(days=1)
print(next_day_date)


now = datetime.datetime.now()
print(now)
next_day_date = now + datetime.timedelta(days=1)
print(next_day_date)
next_day_date = now + datetime.timedelta(days=2)
print(next_day_date)