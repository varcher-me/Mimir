import os
import re
import requests
import time
from aip import AipOcr

APP_ID = '10664604'
API_KEY = 'gS29AoTg9tRi2g6ujiGskrlW'
SECRET_KEY = 'z7ABEkfYa9wYxIieL8ssSAefUQnBhijg'
options = {}
options["result_type"] = "excel"
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_recognition(inner_path, inner_name, inner_id):
    """ 带参数调用表格识别结果 """
    try:
        result = client.getTableRecognitionResult(inner_id, options)
        result_url = result['result']['result_data']
        r = requests.get(result_url)
        file_to_write = os.path.join(inner_path, inner_name+".xls")
        with open(file_to_write, 'wb') as f:
            f.write(r.content)
        print(file_to_write, "Created.")
    except:
        print(result)


file_to_open = "d:\\picture\\thefile1.txt"
file_object = open(file_to_open, 'r')
for line in file_object:
    # print(line)
    match = re.match("(.*)\t(.*)", line)
    origin_picture_filepath = match.group(1)
    origin_picture_accessid = match.group(2)
    match = re.match("(.*)([0-9]{6})\.PNG", origin_picture_filepath)
    print(match.string)
    new_path = match.group(1)
    new_file = match.group(2)
    new_file_path = os.path.join(new_path, new_file+".xls")
    if os.path.isfile(new_file_path):
        print(os.path.isfile(new_file_path), "existed.")
    else:
        get_recognition(new_path, new_file, origin_picture_accessid)
        time.sleep(1)
