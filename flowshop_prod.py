import itertools
import numpy as np
import time
from datetime import datetime, timedelta

def timer(func) :

    def wrapper(*args, **kwargs) :

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        elapsed_time = end_time - start_time
        td = timedelta(seconds=elapsed_time)
        
        print(f"{func.__name__} 함수의 실행 시간 : {str(td)}초")

        return result

    return wrapper

def print_schedule(sequence, processing_times):
    num_jobs = len(sequence)
    num_machines = len(processing_times)
    machine_completion_times = [[0] * num_jobs for _ in range(num_machines)]

    # 각 작업의 시작 시간과 종료 시간 계산
    for job_index in range(num_jobs):
        for machine_index in range(num_machines):
            if job_index == 0:
                start_time = 0
            else:
                start_time = max(machine_completion_times[machine_index][job_index - 1], machine_completion_times[machine_index - 1][job_index])

            end_time = start_time + processing_times[machine_index][sequence[job_index]]
            machine_completion_times[machine_index][job_index] = end_time

    # 스케줄 표 출력
    print("Machine\tJob\tStart\tEnd")
    for job_index in range(num_jobs):
        for machine_index in range(num_machines):
            start_time = machine_completion_times[machine_index][job_index] - processing_times[machine_index][sequence[job_index]]
            end_time = machine_completion_times[machine_index][job_index]
            print(f"{machine_index + 1}\t{sequence[job_index] + 1}\t{start_time}\t{end_time}")

def calculate_completion_time(sequence, processing_times):
    num_jobs = len(sequence)
    num_machines = len(processing_times)
    completion_times = [0] * num_machines

    for job_index in range(num_jobs):
        for machine_index in range(num_machines):
            if machine_index == 0:
                completion_times[machine_index] += processing_times[machine_index][sequence[job_index]]
            else:
                completion_times[machine_index] = max(completion_times[machine_index], completion_times[machine_index - 1]) + processing_times[machine_index][sequence[job_index]]

    return completion_times[-1]

@timer
def find_optimal_sequence(processing_times):
    num_jobs = len(processing_times[0])
    sequences = list(itertools.permutations(range(num_jobs)))
    print('#jobs:', len(sequences))
    optimal_sequence = None
    min_completion_time = float('inf')

    for sequence in sequences:
        # print(sequence)
        completion_time = calculate_completion_time(sequence, processing_times)
        if completion_time < min_completion_time:
            min_completion_time = completion_time
            optimal_sequence = sequence

    return optimal_sequence, min_completion_time


# 설비 3대와 작업 5개에 대한 처리 시간
# processing_times = [
#     [2, 3, 4, 6, 5],
#     [3, 2, 3, 2, 4],
#     [4, 3, 2, 5, 3]
# ]

# 설비 20 job 100
processing_times = np.random.randint(low=90, high=99, size=(20,10))
# print(processing_times)

optimal_sequence, min_completion_time = find_optimal_sequence(processing_times)

print("Optimal Sequence:", optimal_sequence)
print("\nSchedule:")
# print_schedule(optimal_sequence, processing_times)







# import matplotlib.pyplot as plt

# def draw_gantt_chart(sequence, processing_times):
#     num_jobs = len(sequence)
#     num_machines = len(processing_times)

#     # 각 기계의 작업 시작 시간과 종료 시간 계산
#     machine_completion_times = [[0] * num_jobs for _ in range(num_machines)]
#     for job_index in range(num_jobs):
#         for machine_index in range(num_machines):
#             if machine_index == 0:
#                 start_time = 0
#             else:
#                 start_time = machine_completion_times[machine_index - 1][job_index]

#             end_time = start_time + processing_times[machine_index][sequence[job_index]]
#             machine_completion_times[machine_index][job_index] = end_time

#     # 각 작업의 시작과 끝을 간트 차트로 그리기
#     colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
#     for machine_index in range(num_machines):
#         for job_index in range(num_jobs):
#             start_time = machine_completion_times[machine_index][job_index] - processing_times[machine_index][sequence[job_index]]
#             end_time = machine_completion_times[machine_index][job_index]
#             plt.barh(machine_index, end_time - start_time, left=start_time, color=colors[sequence[job_index] % len(colors)], align='center')
#             plt.text(start_time, machine_index, f'Job {sequence[job_index] + 1}', va='center', ha='right', color='black', fontweight='bold')
#             plt.text(end_time, machine_index, f'{end_time}', va='center', ha='left', color='black', fontweight='bold')

#     plt.xlabel('Time')
#     plt.ylabel('Machine')
#     plt.title('Gantt Chart')
#     plt.yticks(range(num_machines), ['Machine %d' % (i+1) for i in range(num_machines)])
#     plt.grid(True)
#     plt.show()

# # # 설비 3대와 작업 5개에 대한 처리 시간
# # processing_times = [
# #     [2, 3, 4, 6, 5],
# #     [3, 2, 3, 2, 4],
# #     [4, 3, 2, 5, 3]
# # ]

# optimal_sequence, min_completion_time = find_optimal_sequence(processing_times)

# draw_gantt_chart(optimal_sequence, processing_times)

