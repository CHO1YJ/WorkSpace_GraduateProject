import time
pattern_time = 10
data_flag = True
num_repetition = 0
while (pattern_time != 0 ):
    if data_flag == True and pattern_time < 5:
        pattern_time = 5
        num_repetition = num_repetition + 1
        if num_repetition >= 5:
            data_flag = False
    print(pattern_time)
    pattern_time = pattern_time-1
    time.sleep(1)
    

# 시간 및 구간 측정
# import time
# from datetime import timedelta

# start = time.process_time()

# sum = 0
# for i in range(10000000):
#     sum += i

# end = time.process_time()

# print("Time elapsed: ", end - start)  # seconds
# print("Time elapsed: ", timedelta(seconds=end-start))