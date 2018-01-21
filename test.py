from aip import AipOcr
import json

APP_ID = '10664604'
API_KEY = 'gS29AoTg9tRi2g6ujiGskrlW'
SECRET_KEY = 'z7ABEkfYa9wYxIieL8ssSAefUQnBhijg'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('C:\\CloudStation\\! - WORKING\\20171227 - ITAM上线计划\\领用登记表扫描\\新X1\\000002.PNG')

""" 调用表格文字识别 """
result = client.tableRecognitionAsync(image)
print(result)
if 'result' in result:
    print(result['result'])
    print(result['result'][0]['request_id'])
