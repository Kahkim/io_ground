from flask import Flask, render_template, redirect, request, url_for
from flask import g

import pymysql
import pymysql.cursors

import datetime

import configs
 
app = Flask(__name__)
app.secret_key = "MYSCRETKEY"

@app.before_request
def before_request():
    if request.endpoint == "static":
        return   
    conn = pymysql.connect(host='192.168.0.3', user='io_ground', passwd='dkshk24@!', db='io_ground')
    print ('opening connection')
    g.db = conn

@app.after_request
def after_request(response):
    if request.endpoint == "static":
        return response
    if g.db is not None:
        print ('closing connection')
        g.db.close()
    return response

@app.route('/', methods=['GET']) # 메인 로그인 화면
def main():
    error = None

    # 페이지에서 입력한 값을 받아와 변수에 저장
    # id = request.form['id']
    # pw = request.form['pw']

    cur = g.db.cursor(pymysql.cursors.DictCursor)

    cur.execute("select UID, TID from TEAMS where STATUS='ACTIVE'")
    data_list = cur.fetchall()
    # print(data_list)

    print(f'data_list {len(data_list)}')
    # for r in ret:
    #     print(r)

    # conn.close()
    # cursor = conn.cursor() # connection으로부터 cursor 생성
    # sql = "SELECT id FROM users WHERE id = %s AND pw = %s" # 실행할 SQL문
    # value = (id, pw)
    # cursor.execute("set names utf8") # 한글이 정상적으로 출력이 되지 않는 경우를 위해
    # cursor.execute(sql, value) # 메소드로 전달해 명령문을 실행

    # data = cursor.fetchall() # SQL문을 실행한 결과 데이터를 꺼냄
    # cursor.close()
    # conn.close()

    # if data:
    #     session['login_user'] = id # 로그인 된 후 페이지로 데이터를 넘기기 위해 session을 사용함
    #     return redirect(url_for('home')) # home 페이지로 넘어감 (url_for 메소드를 사용해 home이라는 페이지로 넘어간다)
    # else:
    #     error = 'invalid input data detected !' # 에러가 발생한 경우
 
    return render_template('main.html', data_list=data_list, error = None)

@app.route('/board/<uid>/<tid>', methods=['GET']) # 메인 로그인 화면
def board(uid, tid):
    return render_template('board.html', uid=uid, tid=tid, error = None)

@app.route('/plans_frm/<uid>/<tid>', methods=['GET'])
def plans_frm(uid, tid): 
    d1 = datetime.datetime.now() + datetime.timedelta(days=1)    
    d2 = datetime.datetime.now() + datetime.timedelta(days=2)        
    d3 = datetime.datetime.now() + datetime.timedelta(days=3)            

    d1 = d1.strftime('%Y-%m-%d') + ' ' + d1.strftime('%a')
    d2 = d2.strftime('%Y-%m-%d') + ' ' + d2.strftime('%a')
    d3 = d3.strftime('%Y-%m-%d') + ' ' + d3.strftime('%a')

    return render_template('plans_frm.html', uid=uid, tid=tid, d1=d1, d2=d2, d3=d3)

@app.route('/plans_c/<uid>/<tid>', methods=['POST'])
def plans_c(uid, tid):
    error = None

    cur = g.db.cursor(pymysql.cursors.DictCursor)    

    # auth key 확인
    auth_key = request.form['auth_key']
    # print(auth_key)
    cur.execute("select UID, TID from TEAMS where STATUS='ACTIVE' and UID=%s and TID=%s and AUTH_KEY=%s", (uid, tid, auth_key))
    data_list = cur.fetchall()
    if len(data_list)<1:        
        return redirect(url_for('error_page', err_msg='UID, TID is not valid or auth key is not correct.'))

    demand_for = []
    demand_for.append(request.form['demand_fore_d_1'])
    demand_for.append(request.form['demand_fore_d_2'])
    demand_for.append(request.form['demand_fore_d_3'])

    demand_for_dates = []
    d1 = datetime.datetime.now() + datetime.timedelta(days=1)    
    d2 = datetime.datetime.now() + datetime.timedelta(days=2)        
    d3 = datetime.datetime.now() + datetime.timedelta(days=3)            
    demand_for_dates.append(d1.strftime('%Y-%m-%d'))
    demand_for_dates.append(d2.strftime('%Y-%m-%d'))
    demand_for_dates.append(d3.strftime('%Y-%m-%d'))

    for df in range(len(demand_for)):
        sql = """INSERT INTO    DEMAND_FOR(UID, TID, PDATE, DEMAND_FOR)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE DEMAND_FOR=VALUES(DEMAND_FOR)"""

        cur.execute(sql,(uid, tid, demand_for_dates[df], demand_for[df]))
        g.db.commit()  
 
    return redirect(url_for('board', uid=uid, tid=tid))


@app.route('/error_page', methods=['GET', 'POST']) # 메인 로그인 화면
def error_page():
    err_msg=request.args.get('err_msg')
    # print(err_msg)
    return render_template('error.html', err_msg=err_msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)