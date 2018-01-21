from aip import AipOcr
import requests

APP_ID = '10664604'
API_KEY = 'gS29AoTg9tRi2g6ujiGskrlW'
SECRET_KEY = 'z7ABEkfYa9wYxIieL8ssSAefUQnBhijg'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

requestId = "10664604_122309"
requestId = "10664604_122311"
""" 如果有可选参数 """
options = {}
options["result_type"] = "excel"

""" 带参数调用表格识别结果 """
result = client.getTableRecognitionResult(requestId, options)
result_url = result['result']['result_data']
r = requests.get(result_url)
with open("test.xls", 'wb') as f:
    f.write(r.content)
