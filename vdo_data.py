import cv2

# 영상 데이터에 대한 좌표 추출 준비과정
cap = cv2.VideoCapture('test_data/test2.mp4')

# Mouse Callback함수; 영상 데이터에 대한 좌표 추출
cap.isOpened()
ret, frame = cap.read() # 영상을 frame 단위로 분리
if ret:
	cv2.imshow('frame', frame)
	#  이미지의 각 이름을 자동으로 지정, 저장 경로 정의
	path = 'data/vdo_data/img_from_video' + '.jpg'
	cv2.imwrite(path, frame) # 이미지 저장

cap.release()
cv2.destroyAllWindows()