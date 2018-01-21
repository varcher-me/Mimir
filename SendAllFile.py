import os
import re
import time
from aip import AipOcr

path = 'd:\\picture'
parents = os.listdir(path)
file_object = open(os.path.join(path, "thefile.txt"), 'w')
APP_ID = '10664604'
API_KEY = 'gS29AoTg9tRi2g6ujiGskrlW'
SECRET_KEY = 'z7ABEkfYa9wYxIieL8ssSAefUQnBhijg'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
last_file = "d:\\picture\\杂\\000012.PNG"
start_new = False


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def tableReg(imgFullFileName):
    files = get_file_content(imgFullFileName)
    result = client.tableRecognitionAsync(files)
    if 'result' in result:
        print(result['result'])
        return result['result'][0]['request_id']
    else:
        print(result)
        return 0


start_new = False
for i in os.walk(path):
    for fileName in i[2]:
        if re.search('PNG', fileName, re.I):
            fullFileName = os.path.join(i[0], fileName)
            if fullFileName == last_file:
                start_new = True
            if start_new:
                print(fullFileName)
                regno = tableReg(fullFileName)
                file_object.write(fullFileName+'\t'+regno+'\n')
                time.sleep(1)

file_object.close()




