import pandas as pd   
import numpy as np

class ttoc:
    def __init__(self, filename, C):
        self.filename = filename
        self.C = C
        self.lines = self.read_file()
        self.job_seq, self.machine_count, self.list_j = self.create_num()        
        self.process_all = self.create_all_process()
        self.df = self.make_df()

    def read_file(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines[3:]

    def create_num(self):
        txt_job = self.lines[:self.C]
        list_j = [line.strip() for line in txt_job]

        # machine 개수
        machine_count = list_j[0].split()[0::2]

        # job 순서 생성
        job_seq = [i+1 for i in range(len(list_j))]

        return job_seq, machine_count, list_j      

    def create_all_process(self):

        # processing time 분할
        job_time = []
        for i in range(len(self.list_j)):
            job_time.append(self.list_j[i].split()[1::2])
    
        # machine별 processing time 생성
        process_list = []
        for j in range(len(self.machine_count)):
            for i in range(len(self.job_seq)):
                process_list.append(job_time[i][j])
    
        # numpy를 사용하여 process_list를 reshape
        process_all = np.array(process_list).reshape(len(self.machine_count), len(self.job_seq)).tolist()

        return process_all

    def make_df(self):
        # job열 정의
        df = pd.DataFrame(data={'JobID' : self.job_seq})
        # df에 M1 ~ M20에 따른 Job Processing time 입력
        for i in range(len(self.machine_count)):
                df[f'M{i+1}'] = self.process_all[i] 

        return df

    def to_csv(self, output_filename):
        self.df.to_csv(output_filename, index=False)

# 사용예시

# Class 불러오기
from txt_to_csv import ttoc
import numpy as np
# txt파일 입력
filename = 't_500_20_sun'
# job 수 설정
C = 500
# csv저장 파일 입력
# output_filename = 't_500_20_tue.csv'
# txt파일에서 job 수 만큼 불러와서 csv로 저장
ttoc_instance = ttoc(filename+'.txt', C)
ttoc_instance.to_csv(filename+'.csv')
