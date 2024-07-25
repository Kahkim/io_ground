from matplotlib import pyplot as plt
import random

def sort_by_schedule(job_seq, ptimes):
    sorted_ptimes = ptimes.iloc[0:0]
    for jobid in job_seq:
         sorted_ptimes.loc[jobid] = ptimes.loc[jobid]
    return sorted_ptimes    

def build_schedule(job_seq, ptimes):
    
    df = sort_by_schedule(job_seq, ptimes).copy()

    # 편의상 df copy
    # df = df_schedule.copy()
    num_machines = df.shape[1]
    
    for i in range(num_machines):
        df[f'M{i+1}_in'] = 0
        df[f'M{i+1}_out'] = 0

    # 첫 time들 설정
    first_job_id = job_seq[0]
    df['M1_in'][first_job_id] = 0        
    df['M1_out'][first_job_id] = df['M1_in'][first_job_id] + ptimes['M1'][first_job_id]
    for i in range(1, num_machines):
        df[f'M{i+1}_in'][first_job_id] = df[f'M{i}_out'][first_job_id]
        df[f'M{i+1}_out'][first_job_id] = df[f'M{i+1}_in'][first_job_id] + ptimes[f'M{i+1}'][first_job_id]
    # print(df)
    # iterative하게 반복
    for i in range(1, len(job_seq)):
        job = job_seq[i]
        job_b = job_seq[i-1]
        for j in range(1, num_machines):
            # print(job, job_b, j)
            df['M1_in'][job] = df['M1_out'][job_b]
            df['M1_out'][job] = df['M1_in'][job] + ptimes['M1'][job]
            # 첫번째 M2에서의 out 시간이 두번째 M1에서의 in 시간보다 크다면, M2 in 시간은 M2의 전 out 시간이다.
            # 반대로 작거나 같다면, 같은 Job 내의 M2 in 시간은M1 out 시간과 같다.
            if df[f'M{j}_out'][job] < df[f'M{j+1}_out'][job_b]:
                df[f'M{j+1}_in'][job] = df[f'M{j+1}_out'][job_b]
            elif df[f'M{j}_out'][job] >= df[f'M{j+1}_out'][job_b]:
                df[f'M{j+1}_in'][job] = df[f'M{j}_out'][job]
            df[f'M{j+1}_out'][job] = df[f'M{j+1}_in'][job] + ptimes[f'M{j+1}'][job]                
    
    return df

def plot_gantt_chart(schedule, figsize=(50, 38), fontsize=20, outfile='gantt_chart.png'):
    df = schedule
    num_machines = int(schedule.shape[1]/3)
    plt.figure(figsize=figsize)
    plt.rcParams.update({'font.size': fontsize})
    
    num_jobs = len(df)
    # 랜덤한 색 생성
    colors = []
    for _ in range(num_jobs):
        # 랜덤한 RGB 값을 생성하여 colors 리스트에 추가
        colors.append('#{:06x}'.format(random.randint(0, 0xFFFFFF)))

    # Job 번호 범례
    legend_handles = []
    for jobid, _ in df.iterrows():        
        color = colors[jobid - 1]
        legend_handles.append(plt.Rectangle((0, 0), 1, 1, color=color, label=f'Job {jobid}'))

    # 간트 생성
    for _, (jobid, row) in enumerate(df.iterrows()):
        for j in range(num_machines,0,-1):
            M_list = [row[f'M{j}_in'], row[f'M{j}']]
            plt.barh(y=f'Machine {j}', left=M_list[0], width=M_list[1], color=colors[jobid - 1], alpha=0.5)
            plt.text(M_list[0] + M_list[1] / 2, num_machines-j, str(df.loc[jobid, f'M{j}']), ha='center', va='center', color='black')
    
    ticks = list(range(0, num_machines))
    ticks_names = []
    for i in range(num_machines,0,-1):
        ticks_names.append(f'Machine {i}')

    plt.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Time')
    plt.ylabel('Machine')
    plt.title('Gantt Chart')
    plt.yticks(ticks, ticks_names)
    plt.savefig(outfile, bbox_inches='tight')
    plt.grid(axis='x')
    plt.show()