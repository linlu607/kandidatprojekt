import xlwt
import ast
import re

filename = "./data/newsJson.txt"

with open(filename, 'r') as file:
    data=file.read().split('\n')#.replace('\n', '')


book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
sheet1.write(0, 0, "url")
sheet1.write(0, 1, "Antal click")
tmp=1
for line in data:
    if line!='':
        dataDict = ast.literal_eval(line)
        print(dataDict["long_url"])
        url=dataDict["long_url"]
        clicks=dataDict["global_clicks"]
        sheet1.write(tmp, 0, url)
        sheet1.write(tmp, 1, clicks)
        tmp=tmp+1


book.save("trial.xls")