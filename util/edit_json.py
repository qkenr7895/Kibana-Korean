######################################################################################################################
#
#   kibana에서 i18n_extract를 사용하면 단순히 문자열뿐 아니라, 사용이 불가능한 key값도 함께 추출됩니다. 예를들어
#
#   "xpack.canvas.elements.filterDebugHelpText": "Shows the underlying global filters in a workpad"
#
#   위와 같이 key값과 value 값이 1:1로 매핑이 되어야 하는데, 몇몇의 경우 아래와 같이
#
#   "xpack.canvas.elementConfig.totalLabel": {
#       "text": "Total",
#       "comment": "The label for the total number of elements in a workpad"
#   }
#
#   하나의 key값에 여러 value가 함께 있음을 알 수 있습니다. 
#
#   통일 되지 않은 형식은 api를 사용하기 어려울 뿐더러,
# 
#   번역을 했다고 하더라도 저 상태 그대로 kibana에 적용하면 에러가 발생하면서 kibana가 실행되지 않습니다.
#
#   따라서 추출 후 가장먼저 번역파일의 형식을 통일시켜주는 것이 중요합니다.
#
####################################################################################################################
import json
import sys
import re

strings_to_translate = []
keys_to_translate = []
key = "messages"
file_to_edit = "file_to_edit.json"          # 변경할 파일 
new_file = "edited_file.json"               # 번경사항이 저장되는 파일

#####################################################################################
#
#   file_to_edit에 원본 json파일(예를 들어 en.json)의 이름을 넣어주면 됩니다.
#
#   원본 json파일이란 key값과 value값이 1:1로 매핑이 되지 않아, comment 필드를 제거해야 하는 파일을 뜻합니다.
#
#   new_file은 원본 json 파일의 변경사항이 저장되는 파일입니다. 다시 말해 key값과 value값이 1:1로 매핑되는 파일입니다.
#
#   new file은 아래의 형식을 가져야 합니다.
#
#   {
#       "messages": {}
#   }
#
#   en.json파일에는 messages key말고도 여러 항목들이 존재합니다. 따라서 현재 소스코드를 사용하여 new file을 생성했으면
#
#   아래의 항목을 참고해 new file에 붙여넣어 주십시오.   
#
#   "formats": {
#       "number": {
#           "currency": {
#               "style": "currency"
#           },
#           "percent": {
#               "style": "percent"
#           }
#       },
#       ...
#       ...
#       ...
#   }
#
######################################################################################

def edit_json():
    with open(file_to_edit, encoding='utf-8') as to_edit, open(new_file, encoding='utf-8') as new:
        json_to_edit = json.load(to_edit)
        json_new = json.load(new)

        for temp in json_to_edit[key]:
            try:
                json_new[key][temp] = json_to_edit[key][temp]["text"]
            except:
                try:
                    json_new[key][temp] = json_to_edit[key][temp]
                except:
                    print("에러")

    with open(new_file, 'w', encoding='utf-8') as make_file:
        json.dump(json_new, make_file, ensure_ascii=False, indent="\t")

if __name__ == "__main__":    
    edit_json()