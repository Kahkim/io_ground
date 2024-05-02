import numpy as np
import matplotlib.pyplot as plt

def draw_gantt_chart(processing_times, sequence):
    num_jobs = len(sequence)
    num_machines = len(processing_times)

    # 각 기계의 작업 시작 시간과 종료 시간 계산
    machine_completion_times = np.zeros((num_machines, num_jobs))
    for job_index in range(num_jobs):
        for machine_index in range(num_machines):
            if machine_index == 0:
                start_time = 0
            else:
                start_time = machine_completion_times[machine_index - 1, job_index]

            end_time = start_time + processing_times[machine_index][sequence[job_index]]
            machine_completion_times[machine_index, job_index] = end_time

    # 각 기계의 작업 간트 차트 그리기
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for machine_index in range(num_machines):
        for job_index in range(num_jobs):
            start_time = machine_completion_times[machine_index, job_index - 1] if job_index > 0 else 0
            end_time = machine_completion_times[machine_index, job_index]
            plt.barh(machine_index, end_time - start_time, left=start_time, color=colors[job_index % len(colors)], align='center')
            # 작업의 시작과 끝 표시
            plt.text(start_time, machine_index, f'S{sequence[job_index]}', va='center', ha='right', color='black', fontweight='bold')
            plt.text(end_time, machine_index, f'E{sequence[job_index]}', va='center', ha='left', color='black', fontweight='bold')

    plt.xlabel('Time')
    plt.ylabel('Machine')
    plt.title('Gantt Chart')
    plt.yticks(range(num_machines), ['Machine %d' % (i+1) for i in range(num_machines)])
    plt.show()

# 최적의 작업 스케줄과 처리 시간
optimal_sequence = [0, 1, 2, 3, 4, 5, 6]  # 예시
processing_times = [
    [2, 3, 4, 6, 5, 4, 3],
    [3, 2, 3, 2, 4, 5, 3],
    [4, 3, 2, 5, 3, 2, 4],
    [3, 4, 5, 2, 3, 4, 2],
    [2, 4, 3, 2, 4, 3, 2]
]

draw_gantt_chart(processing_times, optimal_sequence)

