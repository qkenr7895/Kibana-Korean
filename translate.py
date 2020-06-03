# -*- coding: utf-8 -*-
import os
import json
import unicodedata
import sys
import re
from google.cloud import translate_v2 as translate

#구글 API key 등록.
#Google Cloud에서 프로젝트 생성 후 발급받은 키를 GOOGLE_APPLICATION_CREDENTIALS 환경변수에 넣어줍니다.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'My First Project-6030b0908fde.json'

strings_to_transalte = []
key = "messages"
file_name = "ko-KR.json"

# 해당 문자열이 한글인지 아닌지 검사합니다.
# 해당 문자열이 한글이면 번역을 중단하고 다음 문자열로 넘어갑니다.
# api 사용을 줄이기 위해 해당 코드를 이용합니다.
def isHangul(text):
    # 파이썬 버전 확인
    pyVer3 =  sys.version_info >= (3, 0)
    
    if pyVer3 :
        encText = text
    else:
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(encText)))
    return hanCount > 0

# json 파일로부터 번역할 문자열을 가져옵니다.
# json_file[messages]를 읽어 key와 value값 중 value값을 배열에 저장합니다.
def import_json_file():
    with open(file_name, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        for temp in json_data[key]:
            strings_to_transalte.append(json_data[key][temp])

# 번역완료한 문자열 json 파일에 씁니다.
def export_json_file():
    count = 0
    with open(file_name, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        json_keys = json_data[key]
        for temp in json_keys:
            json_data[key][temp] = strings_to_transalte[count]
            count += 1

    with open(file_name, 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, ensure_ascii=False, indent="\t")

# 추출한 문자열을 google api를 사용하여 번역합니다.
# API 사용을 줄이기 위해 이미 번역이 완료된 문자열은 건너뜁니다.
# 개행 문자(\n)가 포함되어 있는 문자열의 경우, 번역기에서 가끔 \n을 다른 문자로 변환하기 떄문에 번역 대상에서 제외합니다.
# 변수({variable})가 포함되어 있는 문자열 역시, 번역기에서 원본을 그대로 유지하지 않기 때문에 번역 대상에서 제외합니다.
# 결론적으로, 개행문자(\n)와 변수({variable})이 포함된 문자열의 경우 직접 번역해야 합니다.
def translate_strings(text):
    client = translate.Client()
    chars_to_filter = {"{", "}", "\n"}

    # 한글인지 아닌지 검사
    if isHangul(text) == True:
        print("한글")
        return text

    # 번역불가능한 문자가 있는지 검사
    # e.g. \n, {variable}
    for temp_char in chars_to_filter:
        if temp_char in text :
            print("잘못된 문자")
            return text
    
    # api 오류가 날 수 있으므로 반드시 에러 체크를 해줍니다.
    try:
        print(client.translate(text,target_language='ko')['translatedText'])
        return client.translate(text,target_language='ko')['translatedText']
    except:
        print("api 에러")
        return "api error"

if __name__ == "__main__":    
    import_json_file()

    for index, temp_string in enumerate(strings_to_transalte):
        print(index,"번 번역 시도중...")
        result = translate_strings(temp_string)
        if result == "api error":
            break
        strings_to_transalte[index] = result

    export_json_file()
    
