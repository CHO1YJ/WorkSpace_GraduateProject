import json

with open('json_data/Traffic_lights_data.json', 'r', encoding="UTF-8") as f:
    # json_data = json.load(f)
    contents = f.read()  # string 타입
    json_data = json.loads(contents)

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

# 데이터 전체 구조 출력
print(json.dumps(json_data, indent="\t") )