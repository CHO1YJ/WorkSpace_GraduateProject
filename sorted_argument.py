import numpy as np

# 만들고자 하는 좌표의 행렬
a = [[[802,700],[990,701],[777,786],[990,783]], \
     [[1005,698],[1194,702],[1010,786],[1222,783]], \
         [[1209,705],[1409,711],[1240,788],[1451,787]]]

# 터미널의 Argument를 통해 입력한 좌표의 행렬의 문자열 출력
b = ['[', '[', '[', '8', '0', '2', ',', '7', '0', '0', ']', ',', \
     '[', '9', '9', '0', ',', '7', '0', '1', ']', ',', \
     '[', '7', '7', '7', ',', '7', '8', '6', ']', ',', \
     '[', '9', '9', '0', ',', '7', '8', '3', ']', ']', ',', \
     '[', '[', '1', '0', '0', '5', ',', '6', '9', '8', ']', ',', \
     '[', '1', '1', '9', '4', ',', '7', '0', '2', ']', ',', \
     '[', '1', '0', '1', '0', ',', '7', '8', '6', ']', ',', \
     '[', '1', '2', '2', '2', ',', '7', '8', '3', ']', ']', ',', \
     '[', '[', '1', '2', '0', '9', ',', '7', '0', '5', ']', ',', \
     '[', '1', '4', '0', '9', ',', '7', '1', '1', ']', ',', \
     '[', '1', '2', '4', '0', ',', '7', '8', '8', ']', ',', \
     '[', '1', '4', '5', '1', ',', '7', '8', '7', ']', ']', ']']

print(np.shape(a))

temp_str_num = [] # 문자열 출력을 int로 변환하여 담을 배열 정의
temp_list_coor = [] # int로 변환되어 좌표로 구성된 것을 담을 배열 정의
result_coor = np.zeros((3, 4, 2), dtype=int) # 결과적으로 생성할 좌표의 행렬 정의
# 시간 복잡도를 감안하여 for문을 줄이기 위해 행과 열의 카운트 정의
row_count = 0
col_count = 0
# 문자열 출력을 좌표의 행렬로 변환하는 알고리즘
for n in range(len(b)):
    # 문자열을 int형으로 변환하는 과정
    if b[n] != '[' and b[n] != ']' and b[n] != ',':
        if type(int(b[n])) == int:
            temp_str_num.append(int(b[n]))
    # 숫자로 변환된 것을 좌표로 변환하는 과정
    elif b[n] == ',':
        if len(temp_str_num) == 2:
            temp_list_coor.append(temp_str_num[0] * 10 + \
                                  temp_str_num[1] * 1)
        elif len(temp_str_num) == 3:
            temp_list_coor.append(temp_str_num[0] * 100 + \
                                  temp_str_num[1] * 10 + \
                                  temp_str_num[2] * 1)
        elif len(temp_str_num) == 4:
            temp_list_coor.append(temp_str_num[0] * 1000 + \
                                  temp_str_num[1] * 100 + \
                                  temp_str_num[2] * 10 + \
                                  temp_str_num[3] * 1)
        temp_str_num = []
        # 변환된 좌표를 축적하여 좌표의 행렬을 구축하는 과정
        if b[n - 1] == ']':
            result_coor[row_count][col_count] = temp_list_coor
            col_count = col_count + 1
            temp_list_coor = []
    # 시간 복잡도를 줄이기 위해 행과 열을 이동시키기 위한 과정
    elif n > 2 and b[n] == '[' and b[n - 1] == '[':
        col_count = 0
        row_count = row_count + 1
        
    # 마지막 숫자에 대하여 결과가 나타나지 않아 이를 해결하기 위한 코드
    elif b[n] == ']' and b[n - 1] == ']' and b[n - 2] == ']':
        if len(temp_str_num) == 2:
            temp_list_coor.append(temp_str_num[0] * 10 + \
                                  temp_str_num[1] * 1)
        elif len(temp_str_num) == 3:
            temp_list_coor.append(temp_str_num[0] * 100 + \
                                  temp_str_num[1] * 10 + \
                                  temp_str_num[2] * 1)
        elif len(temp_str_num) == 4:
            temp_list_coor.append(temp_str_num[0] * 1000 + \
                                  temp_str_num[1] * 100 + \
                                  temp_str_num[2] * 10 + \
                                  temp_str_num[3] * 1)
        if b[n - 1] == ']':
            result_coor[row_count][col_count] = temp_list_coor
            col_count = col_count + 1
            temp_list_coor = []
            
str_b = result_coor


