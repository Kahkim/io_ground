from flask import Flask, render_template, redirect, request, url_for
from flask import jsonify
from flask import g

import pymysql
import pymysql.cursors

import datetime
import pandas as pd

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

    cur.execute("select UID, TID, ICON_URL from TEAMS where STATUS='ACTIVE' order by REG_DATE DESC")
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
 
    return render_template('main.html', data_list=data_list, error = error)

@app.route('/board_fore_api/<uid>/<tid>', methods=['GET']) # 메인 로그인 화면
def board_fore_api(uid, tid):
    error = None

    cur = g.db.cursor(pymysql.cursors.DictCursor)    

    sql = '''
        SELECT D.DATE as DAT, D.PRICE as ACT, F.DEMAND_FOR as FORC, ABS(D.PRICE-F.DEMAND_FOR) as ABSERR
        FROM DEMANDS AS D LEFT JOIN DEMAND_FOR AS F 
        ON D.DATE = F.PDATE AND F.UID = %s AND F.TID=%s
        ORDER BY D.DATE DESC LIMIT 10
    '''
    cur.execute(sql, (uid, tid))
    fore_list = cur.fetchall()

    return jsonify(fore_list)


@app.route('/board/<uid>/<tid>', methods=['GET']) # 메인 로그인 화면
def board(uid, tid):
    error = None

    cur = g.db.cursor(pymysql.cursors.DictCursor)    

    sql = '''
        SELECT D.DATE as DAT, D.PRICE as ACT, F.DEMAND_FOR as FORC, ABS(D.PRICE-F.DEMAND_FOR) as ABSERR
        FROM DEMANDS AS D LEFT JOIN DEMAND_FOR AS F 
        ON D.DATE = F.PDATE AND F.UID = %s AND F.TID=%s
        ORDER BY D.DATE DESC LIMIT 10
    '''
    cur.execute(sql, (uid, tid))
    fore_list = cur.fetchall()

    sql = '''
        SELECT PDATE, DEMAND_FOR FROM DEMAND_FOR
        WHERE UID = %s AND TID=%s AND PDATE > NOW()
        ORDER BY PDATE DESC    
    '''
    cur.execute(sql, (uid, tid))
    fore_future_list = cur.fetchall()    

    sql = '''
        SELECT PDATE, TYPE, SCHEDULE, QTY FROM PRODUCTIONS WHERE UID = %s AND TID=%s ORDER BY LAST_UPDATED DESC
    '''
    cur.execute(sql, (uid, tid))
    sche_list = cur.fetchall()

    sql = '''
        SELECT PROD_DATE, QTY FROM INVENTORY WHERE UID = %s AND TID=%s ORDER BY PROD_DATE DESC
    '''
    cur.execute(sql, (uid, tid))
    inven_list = cur.fetchall()    
 
    sql = '''
        SELECT PDATE, DISC_RATIO FROM SALES WHERE UID = %s AND TID=%s ORDER BY PDATE DESC
    '''
    cur.execute(sql, (uid, tid))
    sales_list = cur.fetchall()    

    sql = '''
        SELECT DATE,  AMOUNT, ACT, DES, LAST_UPDATED FROM LEDGER WHERE UID = %s AND TID=%s ORDER BY LAST_UPDATED ASC, SEQ DESC
    '''
    cur.execute(sql, (uid, tid))
    ledger_list = cur.fetchall()        
 

    return render_template('board.html', uid=uid, tid=tid, 
                           fore_list=fore_list, fore_future_list=fore_future_list, sche_list=sche_list, 
                           inven_list=inven_list, sales_list=sales_list, ledger_list=ledger_list,
                           error = error)



@app.route('/plans_frm/<uid>/<tid>', methods=['GET'])
def plans_frm(uid, tid): 
    d1 = datetime.datetime.now() + datetime.timedelta(days=configs.PLANNING_LEADTIME)    
    # d2 = datetime.datetime.now() + datetime.timedelta(days=2)        
    # d3 = datetime.datetime.now() + datetime.timedelta(days=3)            

    d1 = d1.strftime('%Y-%m-%d') + ' ' + d1.strftime('%a')
    # d2 = d2.strftime('%Y-%m-%d') + ' ' + d2.strftime('%a')
    # d3 = d3.strftime('%Y-%m-%d') + ' ' + d3.strftime('%a')

    return render_template('plans_frm.html', uid=uid, tid=tid, d1=d1, lt=configs.PLANNING_LEADTIME)

@app.route('/plans_c/<uid>/<tid>', methods=['POST'])
def plans_c(uid, tid):
    error = None

    cur = g.db.cursor(pymysql.cursors.DictCursor)    

    # auth key 확인
    auth_key = request.form['auth_key']
    # print(uid, tid)
    cur.execute("select UID, TID from TEAMS where STATUS='ACTIVE' and UID=%s and TID=%s and AUTH_KEY=%s", (uid, tid, auth_key))
    data_list = cur.fetchall()
    if len(data_list)<1:        
        return redirect(url_for('error_page', err_msg='UID, TID is not valid or auth key is not correct.'))

    # demand 처리 ########################
    demand_for = []
    demand_for.append(request.form['demand_fore_d_1'])
    # demand_for.append(request.form['demand_fore_d_2'])
    # demand_for.append(request.form['demand_fore_d_3'])

    demand_for_dates = []
    d1 = datetime.datetime.now() + datetime.timedelta(days=configs.PLANNING_LEADTIME)    
    # d2 = datetime.datetime.now() + datetime.timedelta(days=2)        
    # d3 = datetime.datetime.now() + datetime.timedelta(days=3)            
    demand_for_dates.append(d1.strftime('%Y-%m-%d'))
    # demand_for_dates.append(d2.strftime('%Y-%m-%d'))
    # demand_for_dates.append(d3.strftime('%Y-%m-%d'))

    for df in range(len(demand_for)):
        sql = """INSERT INTO    DEMAND_FOR(UID, TID, PDATE, DEMAND_FOR)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE DEMAND_FOR=VALUES(DEMAND_FOR)"""

        cur.execute(sql,(uid, tid, demand_for_dates[df], demand_for[df]))
        
    ################################################

    # schedule 처리 ########################
    sql = """INSERT INTO    PRODUCTIONS(UID, TID, PDATE, TYPE, SCHEDULE, QTY)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                                TYPE=VALUES(TYPE),
                                SCHEDULE=VALUES(SCHEDULE),
                                QTY=VALUES(QTY)
                                """
    sche_seq = ''
    sche_qty = -1
    if request.form['sche_type']=='seq':
        sche_seq = request.form['sche_seq']
    else:
        sche_qty = request.form['sche_qty']

    cur.execute(sql,(uid, tid, d1.strftime('%Y-%m-%d'), request.form['sche_type'], sche_seq, sche_qty))
    ################################################

    # sales 처리 ########################
    sql = """INSERT INTO    SALES(UID, TID, PDATE, DISC_RATIO)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE DISC_RATIO=VALUES(DISC_RATIO)"""

    cur.execute(sql,(uid, tid, d1.strftime('%Y-%m-%d'), request.form['sales']))
    ################################################

    g.db.commit()  
    return redirect(url_for('board', uid=uid, tid=tid))


@app.route('/error_page', methods=['GET', 'POST']) # 메인 로그인 화면
def error_page():
    err_msg=request.args.get('err_msg')
    # print(err_msg)
    return render_template('error.html', err_msg=err_msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)