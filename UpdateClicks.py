# -*- coding: cp1252 -*-
import xlwt
import ast
import datetime
import time
colTime=1
while True:
    filename = "./data/newsJson.txt"

    with open(filename, 'r') as file:
        data=file.read().split('\n')


    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0, 0, "URL")
    sheet1.write(0, 1, "Data inläst till excelarket: " + datetime.datetime.now)
    tmp=1
    for line in data:
        if line!='':
            dataDict = ast.literal_eval(line)
            print(dataDict["long_url"])
            url=dataDict["long_url"]
            clicks=dataDict["global_clicks"]
            sheet1.write(tmp, 0, url)
            sheet1.write(tmp, colTime, clicks)
            tmp=tmp+1

    book.save("ResultsBitly.xls")
    time.sleep( 3600 )
    colTime=colTime+1
