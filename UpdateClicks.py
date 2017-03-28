import xlwt
import ast
import datetime
import time
colTime=1
while True:

    filename = "./data/newsJson.txt"
    with open(filename, 'r') as file:
        data=file.read().split('\n')#.replace('\n', '')


    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0, 0, "url")
    localtime = time.asctime( time.localtime(time.time()) )
    print localtime

    sheet1.write(0, 1, "Antal click vid tiden " + localtime)
    tmp=1
    for line in data:
        if line!='':
            dataDict = ast.literal_eval(line)

            url=dataDict["long_url"]
            url=str(url).replace("http://","")
            print(dataDict["long_url"])
            clicks=dataDict["global_clicks"]
            sheet1.write(tmp, 0, url)
            sheet1.write(tmp, colTime, clicks)
            tmp=tmp+1

    book.save("ResultsBitly.xls")
    time.sleep( 3600 )
    colTime=colTime+1