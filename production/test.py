# 사용자 class import
from txt_to_csv import ttoc
from production.back_SPT_Scheduler_with_validation import SPT_Scheduler
import matplotlib.pyplot as plt

# 초기 df 생성
jh_scheduler = SPT_Scheduler('t_500_20_mon.csv')
# 작업을 위한 초기 list 생성
machines = jh_scheduler.m_tolist()

# SPT rule 적용
schedule =  jh_scheduler.SPT_rule(machines)

print(schedule)