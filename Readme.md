# 수요(주가)

## 업데이트

* Naver 주식 서비스 crawler
    * Projects/io_ground/stock_retriever.py
    * 첫 페이지 10개 수집
    * DEMANDS 테이블 입력 using ON DUPLICATE KEY UPDATE PRICE=VALUES(PRICE)

* crontab 매일 4시 수집
    * 0 16 * * * source /home/kahkim/Projects/io_ground/stock_retriever_daily_cron.sh >> /home/kahkim/Projects/io_ground/__pycache__/stock_retriever_daily_cron.log 2>&1

# Team 관리

## Team status

* LIVE / RETRO / DEACT

# System trigger

## trigger types

* Live trigger
    * for LIVE <- 4pm sales, 5pm production, then inventoring everyday (today)

* Step trigger
    * for RETRO <-- able to set CUR_DATE for sale, production, and inventoring.
    * 우선구현 필요

# Plan register

* 서버측에서 사용자의 계획 등록기
* (임시) plans txt 입력받아 등록
    * demand_register.py
        * plan_demand_exp.txt
    * prod_register.py
        * plan_prod.txt -> UID, TID, 내일 생산량
    * sales_register.py
        * plan_sales.txt -> UID, TID, 내일 판매량