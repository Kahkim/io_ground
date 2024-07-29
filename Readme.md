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


# 생산

## 입력
* 1,2,3,4,5,6,7,8,9,10
* 일단...
    * 1job = 1,000제품 <- 설정가능
    * makespan = 1job * 1,000


# System trigger

## trigger types

* Live trigger
    * for LIVE <- 4pm sales, 5pm production, then inventoring everyday (today)

* Step trigger
    * for RETRO <-- able to set CUR_DATE for sale, production, and inventoring.
    * 우선구현 필요

# 해야할 거

## 엔진 돌아갈때 위험요소

* qty 및 job seq 갯수 범위 1~500

* schedule job id seq 안 맞는거

## inventory 정보관리

* 날짜별 inventory level 확인 가능해야 함

* 생산일별 - 판매일별 정보있어야 함

## 할인 로직 변경
 
 * demand = demand * 할인율

 * price = price * 한인율