# -*- coding: cp1252 -*-
import xlwt
import ast
import datetime
import time
import re
import bitlydatahandler
colTime=1
run = True
while run:
    
    path = "./data/2017-03-28_104236_news.txt"

    if(colTime == 1):
        with open(path, 'r') as file:
            data=file.read().split('\n')
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        sheet1.write(0, 0, "URL")
        print time.asctime(time.localtime(time.time()))
        sheet1.write(0, 1, u'Data inläst till excelarket: ' + str(time.asctime(time.localtime(time.time()))))
        tmp=1
        for line in data:
            if line!='':
                dataDict = ast.literal_eval(line)
                url=dataDict["long_url"]
                clicks=dataDict["global_clicks"]
                sheet1.write(tmp, 0, url)
                sheet1.write(tmp, colTime, clicks)
                tmp=tmp+1
    else:
        sheet1.write(0, colTime, u'Data inläst till excelarket: ' + str(time.asctime(time.localtime(time.time()))))
        print time.asctime(time.localtime(time.time()))
        updatedData = bitlydatahandler.updateClicks(path)
        tmp=1
        for line in updatedData:
            if line!='':
                #dataDict = ast.literal_eval(line)
                clicks=line["global_clicks"]
                sheet1.write(tmp, colTime, clicks)
                tmp=tmp+1

    book.save("ResultsBitly.xls")
    time.sleep( 3600 )
    colTime=colTime+1
    if(colTime > 5):
        run = False
