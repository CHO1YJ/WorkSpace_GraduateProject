import json

with open('json_data/Traffic_lights_data.json', 'r', encoding="UTF-8") as f:
    # 1. json 파일을 읽어오는 함수 load를 사용하는 방식
    json_data = json.load(f)
    # 2. json 형태의 문자열 string을 읽어오는 함수 loads를 사용하는 방식
    # contents = f.read()
    # json_data = json.loads(contents)
    # 해당 알고리즘은 1번과 2번 모두 적용 가능

# Traffic_Light_Cars 정보를 조회
print(json_data["Traffic_Light_Cars"])
# Traffic_Light_People 정보를 조회 -> 0번째 배열의 Wheelchair key를 통해 value에 접근
print("사람으로 확인되는 인원은 " + \
      str(json_data["Traffic_Light_People"][0]["People"]) \
      + "명 입니다.")
print("휠체어를 탄 것으로 확인되는 인원은 " + \
      str(json_data["Traffic_Light_People"][0]["Wheelchair"]) \
      + "명 입니다.")
print("노약자로 확인되는 인원은 " + \
      str(json_data["Traffic_Light_People"][0]["Silver"]) \
      + "명 입니다.")

print("차량으로 확인되는 대수는 " + \
      str(json_data["Traffic_Light_Cars"][0]["Cars_1"]) \
      + "대 입니다.")
print("차량으로 확인되는 대수는 " + \
      str(json_data["Traffic_Light_Cars"][1]["Cars_2"]) \
      + "대 입니다.")
# 데이터 전체 구조 출력
print(json.dumps(json_data, indent="\t") )