from flask import Flask, render_template, redirect, request, url_for
from flask import jsonify
from flask import g

import pymysql
import pymysql.cursors

import datetime
import pandas as pd
import ast

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import configs
import utils
 
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

    cur = g.db.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        select UID, TID, ICON_URL, 
        (SELECT SUM(REVENUE + EXPENSE) FROM LEDGER AS L WHERE L.UID=T.UID AND L.TID=T.TID) AS CUR_BALANCE
        from TEAMS T
        where STATUS='ACTIVE' order by REG_DATE DESC
    """)
    data_list = cur.fetchall()

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
        SELECT date_format(D.DATE, '%%Y-%%m-%%d') as DAT, D.PRICE as ACT, F.DEMAND_FOR as FORC, ABS(D.PRICE-F.DEMAND_FOR) as ABSERR
        FROM DEMANDS AS D LEFT JOIN DEMAND_FOR AS F 
        ON D.DATE=F.PDATE AND F.UID=%s AND F.TID=%s
        ORDER BY D.DATE DESC LIMIT 10
    '''
    cur.execute(sql, (uid, tid))
    fore_list = cur.fetchall()

    print(jsonify(fore_list).get_data(as_text=True))
    return jsonify(fore_list)


@app.route('/board/<uid>/<tid>', methods=['GET']) # 메인 로그인 화면
def board(uid, tid):
    error = None
    cur = g.db.cursor(pymysql.cursors.DictCursor)    

    # forecasting #######################
    sql = '''
        SELECT D.DATE as DAT, D.PRICE as ACT, F.DEMAND_FOR as FORC, ABS(D.PRICE-F.DEMAND_FOR) as ABSERR
        FROM DEMANDS AS D LEFT JOIN DEMAND_FOR AS F 
        ON D.DATE = F.PDATE AND F.UID = %s AND F.TID=%s
        ORDER BY D.DATE DESC LIMIT 60
    '''
    cur.execute(sql, (uid, tid))
    fore_list = cur.fetchall()

    sql = '''
        SELECT PDATE, DEMAND_FOR FROM DEMAND_FOR
        WHERE UID = %s AND TID=%s AND PDATE >= date_format(NOW(), '%%Y-%%m-%%d')
        ORDER BY PDATE DESC LIMIT 60   
    '''
    cur.execute(sql, (uid, tid))
    fore_future_list = cur.fetchall()    

    df = pd.DataFrame(fore_list)
    df2 = pd.DataFrame(fore_future_list)
    if len(df2)>0:
        y_min = (min(df.loc[:,'ACT'].min(), df.loc[:,'FORC'].min(), df2.loc[:,'DEMAND_FOR'].min()))
        y_max = (max(df.loc[:,'ACT'].max(), df.loc[:,'FORC'].max(), df2.loc[:,'DEMAND_FOR'].max()))
    else:
        y_min = (min(df.loc[:,'ACT'].min(), df.loc[:,'FORC'].min()))
        y_max = (max(df.loc[:,'ACT'].max(), df.loc[:,'FORC'].max()))        
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(go.Scatter(x=df.loc[:,'DAT'].values, y=df.loc[:,'ACT'].values, mode='lines+markers', name='Actual'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.loc[:,'DAT'].values, y=df.loc[:,'FORC'].values, mode='lines+markers', name='Forecasted'), row=1, col=1)    
    if len(df2)>0: fig.add_trace(go.Scatter(x=df2.loc[:,'PDATE'].values, y=df2.loc[:,'DEMAND_FOR'].values, mode='lines+markers', name='Forecasted-future'), row=1, col=1)    
    fig.add_trace(go.Bar(
        x=df.loc[:,'DAT'].values,
        y=df.loc[:,'ABSERR'].values,
        name="ABS err",        
        marker=dict(color="lightslategray"),
    ), row=2, col=1)    
    fig.update_yaxes(range=[y_min*0.8, y_max*1.05], row=1, col=1)
    fig.update_yaxes(row=2, col=1)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)    

    # production ###########################
    sql = '''
        SELECT PDATE, STATUS, TYPE, SCHEDULE, QTY, JOBS, MAKESPAN FROM PRODUCTIONS WHERE UID = %s AND TID=%s 
        ORDER BY PDATE DESC LIMIT 30
    '''
    cur.execute(sql, (uid, tid))
    sche_list = cur.fetchall()

    sql = '''
        SELECT PDATE, DISC_RATIO FROM SALES WHERE UID = %s AND TID=%s ORDER BY PDATE DESC LIMIT 30
    '''
    cur.execute(sql, (uid, tid))
    sales_list = cur.fetchall()    

    sql = '''
        SELECT PROD_DATE, PROD_QTY, SALES_DATE, SALES_QTY, LAST_UPDATED 
        FROM INVENTORY_HIST WHERE UID = %s AND TID=%s ORDER BY PROD_DATE DESC, SALES_DATE ASC
    '''
    cur.execute(sql, (uid, tid))
    inven_list = cur.fetchall()    

    sql = '''
        SELECT DATE, REVENUE, EXPENSE, ACT, DES, LAST_UPDATED FROM LEDGER WHERE UID = %s AND TID=%s 
        ORDER BY DATE DESC, SEQ ASC
    '''
    cur.execute(sql, (uid, tid))
    ledger_list = cur.fetchall()            
    
    return render_template('board.html', uid=uid, tid=tid, 
                           fore_list=fore_list, fore_future_list=fore_future_list, sche_list=sche_list, 
                           inven_list=inven_list, sales_list=sales_list, ledger_list=ledger_list,
                           graphJSON=graphJSON,
                           error = error)


@app.route('/plans_frm/<uid>/<tid>', methods=['GET'])
def plans_frm(uid, tid): 
    # d1 = datetime.datetime.now() + datetime.timedelta(days=configs.PLANNING_LEADTIME)    
    # d1 = d1.strftime('%Y-%m-%d') + ' ' + d1.strftime('%a')

    next_week_days = utils.next_week_days(datetime.datetime.now())    

    return render_template('plans_frm.html', uid=uid, tid=tid, next_week_days=next_week_days)

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

    planning_dates = utils.next_week_days(datetime.datetime.now())    

    # demand 처리 ########################
    demand_for = []
    demand_for.append(request.form['demand_fore_d_0'])
    demand_for.append(request.form['demand_fore_d_1'])    
    demand_for.append(request.form['demand_fore_d_2'])
    demand_for.append(request.form['demand_fore_d_3'])
    demand_for.append(request.form['demand_fore_d_4'])

    # print(demand_for)

    for i in range(len(planning_dates)):
        sql = """INSERT INTO    DEMAND_FOR(UID, TID, PDATE, DEMAND_FOR)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE DEMAND_FOR=VALUES(DEMAND_FOR)"""
        d =  demand_for[i] if demand_for[i].isnumeric() else '0'
        cur.execute(sql,(uid, tid, planning_dates[i], d))
        
    ################################################

    # schedule 처리 ########################
    sql = """INSERT INTO    PRODUCTIONS(UID, TID, PDATE, TYPE, SCHEDULE, JOBS)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                                TYPE=VALUES(TYPE),
                                SCHEDULE=VALUES(SCHEDULE),
                                JOBS=VALUES(JOBS)
                                """
    for i in range(len(planning_dates)):
        sche_seq = ''
        sche_qty = -1
        if request.form['sche_type_d_'+str(i)]=='seq':
            sche_seq = request.form['sche_seq_d_'+str(i)]
            sche_qty = len(ast.literal_eval(sche_seq))            
        else:
            sche_qty = request.form['sche_qty_d_'+str(i)]
            sche_qty = sche_qty if sche_qty.isnumeric() else '0'

        cur.execute(sql,(uid, tid, planning_dates[i], request.form['sche_type_d_'+str(i)], 
                         sche_seq, sche_qty))
    ################################################

    # sales 처리 ########################
    sql = """INSERT INTO    SALES(UID, TID, PDATE, DISC_RATIO)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE DISC_RATIO=VALUES(DISC_RATIO)"""

    for i in range(len(planning_dates)):
        d =  request.form['sales_d_'+str(i)] if request.form['sales_d_'+str(i)].isnumeric() else '0'
        cur.execute(sql,(uid, tid, planning_dates[i], d))
    ################################################

    g.db.commit()  
    return redirect(url_for('board', uid=uid, tid=tid))


@app.route('/plans_sales_frm/<uid>/<tid>', methods=['GET'])
def plans_sales_frm(uid, tid): 
    # d1 = datetime.datetime.now() + datetime.timedelta(days=configs.PLANNING_LEADTIME)    
    # d1 = d1.strftime('%Y-%m-%d') + ' ' + d1.strftime('%a')

    planning_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    return render_template('plans_sales_frm.html', uid=uid, tid=tid, planning_date=planning_date)


@app.route('/plans_sales/<uid>/<tid>', methods=['POST'])
def plans_sales(uid, tid):
    error = None

    cur = g.db.cursor(pymysql.cursors.DictCursor)    

    # auth key 확인
    auth_key = request.form['auth_key']
    # print(uid, tid)
    cur.execute("select UID, TID from TEAMS where STATUS='ACTIVE' and UID=%s and TID=%s and AUTH_KEY=%s", (uid, tid, auth_key))
    data_list = cur.fetchall()
    if len(data_list)<1:        
        return redirect(url_for('error_page', err_msg='UID, TID is not valid or auth key is not correct.'))

    planning_date = datetime.datetime.now() + datetime.timedelta(days=1) 

    # sales 처리 ########################
    sql = """INSERT INTO    SALES(UID, TID, PDATE, DISC_RATIO)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE DISC_RATIO=VALUES(DISC_RATIO)"""

    i = 1
    d =  request.form['sales_d_'+str(i)] if utils.is_number(request.form['sales_d_'+str(i)]) else '0'
    cur.execute(sql,(uid, tid, planning_date, d))
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