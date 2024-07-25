import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

class SPT_Scheduler:
    def __init__(self, file_name):
        # CSV 파일에서 데이터 읽기
        self.df = pd.read_csv(file_name, encoding='UTF-8')                
        # print(self.df.shape)

    def m_tolist(self):
        df = self.df
        machines = []     
        for i in range(len(df.columns)-1):
            machines.append(df.iloc[:,i+1].values)
            machines[i] = machines[i].tolist()
        self.machines = machines
        return machines
    
    def SPT_rule(self, machines):
        # SPT 일반화
        machines = self.machines
        order = sorted(machines[0])

        idx_list = range(1, len(machines[0]) + 1)
        df = pd.DataFrame(order, index=idx_list, columns=['M1'])
        df_job = df.sort_index(ascending=True)

        df_machine = pd.DataFrame({'Job_order': list(idx_list)})
        for i in range(len(machines)):
            df_machine[f'M{i+1}'] = machines[i]

        df_schedule = pd.merge(df_job, df_machine, on='M1', how='inner')
        df_schedule = df_schedule.drop_duplicates(ignore_index=True)

        reindex_name = ['Job_order']
        for i in range(1, len(machines) + 1):
            reindex_name.append(f'M{i}')
        df_schedule = df_schedule.reindex(columns = reindex_name)
        self.df_schedule = df_schedule
        return df_schedule

    # NEH 알고리즘
    def neh_algorithm(self):
        df = self.df
        num_jobs = df.shape[0]
        def calculate_makespan(df, sequence):
            num_jobs = len(sequence)
            num_machines = df.shape[1]
            
            end_times = np.zeros((num_jobs, num_machines))
            
            for i, job in enumerate(sequence):
                for j in range(num_machines):
                    if j == 0:
                        if i == 0:
                            end_times[i, j] = df.iloc[job, j]
                        else:
                            end_times[i, j] = end_times[i-1, j] + df.iloc[job, j]
                    else:
                        if i == 0:
                            end_times[i, j] = end_times[i, j-1] + df.iloc[job, j]
                        else:
                            end_times[i, j] = max(end_times[i-1, j], end_times[i, j-1]) + df.iloc[job, j]
            
            return end_times[-1, -1]
        
        # 각 작업의 총 처리 시간 계산
        total_times = df.sum(axis=1)
        
        # 총 처리 시간에 따라 내림차순 정렬
        sorted_jobs = np.argsort(-total_times)
        
        # 초기 작업 순서 결정
        best_sequence = [sorted_jobs[0], sorted_jobs[1]]
        best_makespan = calculate_makespan(df, best_sequence)
        
        for job in sorted_jobs[2:]:
            min_makespan = float('inf')
            best_position = 0
            
            for i in range(len(best_sequence) + 1):
                temp_sequence = best_sequence[:i] + [job] + best_sequence[i:]
                makespan = calculate_makespan(df, temp_sequence)
                if makespan < min_makespan:
                    min_makespan = makespan
                    best_position = i
            
            best_sequence.insert(best_position, job)
        
        optimal_order = optimal_order = [i+1 for i in best_sequence]
        optimal_makespan = calculate_makespan(df, best_sequence)
        
        idx_list = range(1, len(df) + 1)
        df_order = pd.DataFrame(optimal_order, index=idx_list, columns=['Job_order'])
        
        df_machine = df.rename(columns={'Job': 'Job_order'})
        
        df_schedule = pd.merge(df_order, df_machine, on='Job_order', how='inner')
        self.df_schedule = df_schedule
        return df_schedule

    def all_schedule(self):
        

        # 편의상 df copy
        df_schedule = self.df_schedule
        df = df_schedule.copy()
        len_machines = len(self.machines)
        # 초기 값 설정
        len_df = len(df['Job_order'])
        for i in range(len_machines):
            df[f'M{i+1}_in'] = 0
            df[f'M{i+1}_out'] = 0
        # for i in range(len_machines-1):
        #     df[f'Idle_time_M{i+2}'] = 0
        print(df)
        # 첫 time들 설정
        df['M1_in'][0] = 0
        df['M1_out'][0] = df['M1_in'][0] + df['M1'][0]
        for i in range(1, len_machines):
            df[f'M{i+1}_in'][0] = df[f'M{i}_out'][0]
            df[f'M{i+1}_out'][0] = df[f'M{i+1}_in'][0] + df[f'M{i+1}'][0]
        # for i in range(len_machines-1):
        #     df[f'Idle_time_M{i+2}'][0] = df[f'M{i+2}_in'][0]

        # iterative하게 반복
        for i in range(1, len_df):
            for j in range(1, len_machines):
                df['M1_in'][i] = df['M1_out'][i-1]
                df['M1_out'][i] = df['M1_in'][i] + df['M1'][i]
                # 첫번째 M2에서의 out 시간이 두번째 M1에서의 in 시간보다 크다면, M2 in 시간은 M2의 전 out 시간이다.
                # 반대로 작거나 같다면, 같은 Job 내의 M2 in 시간은M1 out 시간과 같다.
                if df[f'M{j}_out'][i] < df[f'M{j+1}_out'][i-1]:
                    df[f'M{j+1}_in'][i] = df[f'M{j+1}_out'][i-1]
                elif df[f'M{j}_out'][i] >= df[f'M{j+1}_out'][i-1]:
                    df[f'M{j+1}_in'][i] = df[f'M{j}_out'][i]
                df[f'M{j+1}_out'][i] = df[f'M{j+1}_in'][i] + df[f'M{j+1}'][i]
        # for i in range(1, len_df):
        #     for j in range(1, len_machines):
        #         # M2, M3의 Idle_time은 현 job의 in time 과 전 job의 out time의 차이이다. 비는 시간
        #         df[f'Idle_time_M{j+1}'][i] = df[f'M{j+1}_in'][i] - df[f'M{j+1}_out'][i-1]
                
        self.df = df
        return df
    
    def to_csv(self, output_filename):
        self.df.to_csv(output_filename, index=False)
    
    def info_machines(self):
        machines = self.machines
        df = self.df
        len_df = len(df)
        len_machines = len(machines)

        # 정보 Data Frame 생성
        info_df = pd.DataFrame()
        self.info_df = info_df

        # Machine 이름 생성
        Machine_name = []
        for i in range(len_machines):
            Machine_name.append(f'M{i+1}')

        # Makespan열 추가
        Makespan = df[f'{Machine_name[-1]}_out'][len_df-1]

        return print('Makespan: ',Makespan)
    

    def plot_gantt_chart(self):
        machines = self.machines
        df = self.df
        plt.figure(figsize=(50, 38))
        
        num_jobs = len(self.df)
        # 랜덤한 색 생성
        colors = []
        for _ in range(num_jobs):
            # 랜덤한 RGB 값을 생성하여 colors 리스트에 추가
            colors.append('#{:06x}'.format(random.randint(0, 0xFFFFFF)))

        # Job 번호를 범례로 따로 빼주기
        legend_handles = []
        for i, row in self.df.iterrows():
            color = colors[i]
            legend_handles.append(plt.Rectangle((0, 0), 1, 1, color=color, label=f'Job {self.df.loc[i, "Job_order"]}'))

        # Job 번호를 범례로 따로 빼주기
        legend_handles = []
        for i, row in self.df.iterrows():
            color = colors[self.df.loc[i, 'Job_order'] - 1]
            legend_handles.append(plt.Rectangle((0, 0), 1, 1, color=color, label=f'Job {self.df.loc[i, "Job_order"]}'))

        # 자동으로 간트 생성
        for i, (index, row) in enumerate(self.df.iterrows()):
            for j in range(len(machines),0,-1):
                M_list = [row[f'M{j}_in'], row[f'M{j}']]
                plt.barh(y=f'Machine {j}', left=M_list[0], width=M_list[1], color=colors[self.df.loc[index, 'Job_order'] - 1], alpha=0.5)
                plt.text(M_list[0] + M_list[1] / 2, len(machines)-j, str(self.df.loc[index, f'M{j}']), ha='center', va='center', color='black')
        
        ticks = list(range(0,len(machines)))
        ticks_names = []
        for i in range(len(machines),0,-1):
            ticks_names.append(f'Machine {i}')

        plt.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1, 1))
        plt.xlabel('Time')
        plt.ylabel('Machine')
        plt.title('Gantt Chart')
        plt.yticks(ticks, ticks_names)
        plt.savefig('gantt_chart.png', bbox_inches='tight')
        plt.grid(axis='x')
        plt.show()

        return plt
    


    # validation.
    #job 개수 확인
    def check_job(self):
        df = self.df
        value=df['Job_order'].sort_values().values
        print(f'스케줄링에 들어있는 job:{value}')
        print(f'job 개수: {len(value)}개')

        machine_count = 20  
        for index, row in df.iterrows():
            job_order = int(row['Job_order'])
            for i in range(1, machine_count + 1):
                in_col = f'M{i}_in'
                out_col = f'M{i}_out'
                processing_col = f'M{i}'
                # M{i}_in, M{i}_out, M{i} 값이 모두 존재해야 함
                if pd.isnull(row[in_col]) or pd.isnull(row[out_col]) or pd.isnull(row[processing_col]):
                    print(f"1.작업 {job_order}의 {in_col}, {out_col}, {processing_col} 중 하나가 비어 있습니다.")
                    return 
        print("1.csv 파일 이상 없음")
        return 

    #계단식 작업을 수행하는지 확인
    def check_job_sequence(self):
        df = self.df
        machine_count = 20  # M1부터 M20까지
        for job in df['Job_order'].unique():
            job_df = df[df['Job_order'] == job]
            for i in range(1, machine_count):
                current_machine_out = job_df.iloc[0][f'M{i}_out']
                next_machine_in = job_df.iloc[0][f'M{i+1}_in']
                if current_machine_out > next_machine_in:
                    #이전 머신에서의 작업이 끝나지 않았는데 그 작업을 현재 수행하고 있을 경우 뜨는 에러
                    print(f"2.작업 순서 부적합: Job {job}의 M{i}_out 시간이({current_machine_out})이 M{i+1}_in 시간({next_machine_in})보다 늦습니다.")
                    return 
        print("2.작업 순서 적합")
        return 

    #작업이 겹쳤는지 확인
    def check_overlap(self):
        df = self.df
        machine_count = 20  # M1부터 M20까지
        for i in range(1, machine_count + 1):
            in_col = f'M{i}_in'
            out_col = f'M{i}_out'
            for j in range(len(df) - 1):
                current_job_out = df.iloc[j][out_col]
                next_job_in = df.iloc[j + 1][in_col]
                if current_job_out > next_job_in:
                    print(f"3.작업 겹침 부적합: Job {df.iloc[j]['Job_order']}의 {out_col} ({current_job_out})이 다음 작업 {df.iloc[j + 1]['Job_order']}의 {in_col} ({next_job_in})보다 늦습니다.")
                    return False
        print("3.작업 겹침 없음")
        return True

    #M{i}_out = M{i}_in + M{i} 검증
    def check_processing_times(self):
        df = self.df
        machine_count = 20  # M1부터 M20까지
        for i in range(1, machine_count + 1):
            in_col = f'M{i}_in'
            out_col = f'M{i}_out'
            processing_col = f'M{i}'
            for index, row in df.iterrows():
                expected_out = row[in_col] + row[processing_col]
                if row[out_col] != expected_out:
                    print(f"4.프로세싱 타임 부적합: Job {int(row['Job_order'])}의 {out_col} 시간이 예상 {expected_out}과 다릅니다.")
                    return 
        print("4.프로세싱 타임 적합")
        return 

# 사용 예시

# Class 불러오기
# from SPT_Scheduler import SPT_Scheduler
# 초기 df 생성, csv파일 input에는 ttoc에서 받아온 csv.
# df_t = SPT_Scheduler('???.csv')
# # machine 정의
# machines = df_t.m_tolist()
# # SPT 규칙 적용
# df_t.SPT_rule(machines)
# # 적용 결과 df반환
# df_t.all_schedule()
# # 제출할 CSV 저장
# df_t.to_csv(output_filename='ex.csv')
# # Makespan 계산
# df_t.info_machines()
# # Ganttchart 시각화
# plt.rcParams.update({'font.size': 20})
# df_t.plot_gantt_chart()
