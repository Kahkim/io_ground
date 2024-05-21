import pymysql
conn = pymysql.connect(host='192.168.0.3', user='io_ground', passwd='dkshk24@!', db='io_ground')

cur = conn.cursor()

cur.execute("INSERT INTO Test(TYPE, Contents) VALUES ('AA','TEXT!!!')")
conn.commit()

cur.execute('select * from Test')
ret = cur.fetchall()
for r in ret:
    print(r)

conn.close()