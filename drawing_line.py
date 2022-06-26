#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 이미지 데이터에 대한 좌표 추출 준비과정
mode = True
coor_xy = [0, 0]
flag_click = False
list_coordinate = []
save_lists = []
count = 0

# Mouse Callback함수; 이미지 데이터에 대한 좌표 추출
def draw_coor(event, x,y, flags, param):
	global coor_xy, flag_click
	if event == cv2.EVENT_LBUTTONDOWN:
		flag_click = True
		coor_x = x
		coor_y = y
		coor_xy = np.array([coor_x, coor_y])

# img = cv2.imread('test_data/test1.jpg')
img = cv2.imread('data/vdo_data/img_0.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_coor)

# 좌표의 행렬 데이터 생성 및 저장
while True:
	cv2.imshow('image', img)
	k = cv2.waitKey(1) & 0xFF

	if flag_click == True:
		if count < 4:
			if count == 0:
				print("Click 'm' to save coordinates of box!")
				print("Click 'd' if you want to display saving lists")
				print("Click 'x' if you want to initialize saving lists")
			print(coor_xy)
			list_coordinate.append(coor_xy)
			count = count + 1
			if count == 4:
				print("Click for initialization")
				if mode == False:
					print("Completed saving coordinates")
					save_lists.append(list_coordinate)
				count = count + 1
		else:
			print(list_coordinate)
			count = 0
			list_coordinate = []
	flag_click = False

	if k == ord('m'):
		mode = not mode
	elif k == ord('d'):
		print("Completed saving lists")
		print(save_lists)
	elif k == ord('x'):
		print("Completed deleting lists")
		save_lists = []
	elif k == 27:        # esc를 누르면 종료
		break

cv2.destroyAllWindows()

# '''

'''
class drawing_box:
	def __init__(self, mode, coor_xy, flag_click):
		self.mode = mode
		self.coor_xy = coor_xy
		self.flag_click = flag_click


	# Mouse Callback함수
	def draw_coor(event, x,y, flags, param):
		global coor_xy, flag_click
		if event == cv2.EVENT_LBUTTONDOWN:
			flag_click = True
			coor_x = x
			coor_y = y
			coor_xy = np.array([coor_x, coor_y])

	img = cv2.imread('test_data/test1.jpg')
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', draw_coor)

	while True:
		cv2.imshow('image', img)
		k = cv2.waitKey(1) & 0xFF

		if flag_click == True:
			print(coor_xy)
		flag_click = False
		if k == ord('m'):  # 사각형, 원 Mode변경
			mode = not mode
		elif k == 27:  # esc를 누르면 종료
			break

	cv2.destroyAllWindows()
'''










