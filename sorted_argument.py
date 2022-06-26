import numpy as np

a = [[[802,700],[990,701],[777,786],[990,783]], \
     [[1005,698],[1194,702],[1010,786],[1222,783]], \
         [[1209,705],[1409,711],[1240,788],[1451,787]]]

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

temp_str_num = []
temp_list_coor = []
result_coor = np.zeros((3, 4, 2), dtype=int)
row_count = 0
col_count = 0
for n in range(len(b)):
    if b[n] != '[' and b[n] != ']' and b[n] != ',':
        if type(int(b[n])) == int:
            temp_str_num.append(int(b[n]))
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
        if b[n - 1] == ']':
            result_coor[row_count][col_count] = temp_list_coor
            col_count = col_count + 1
            temp_list_coor = []
    elif n > 2 and b[n] == '[' and b[n - 1] == '[':
        col_count = 0
        row_count = row_count + 1
        
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


