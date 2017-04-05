import xlwt
import ast
import time
import re
import os
import bitlydatahandler
newsEnding = re.compile('.*news\.txt$')
#run = True
path = ""
#For how long the program should run before its starts again, in seconds
#sleepInterval = 10
#How many times should the program run
#numberOfRuns = 5

def findNewsFiles(path):
    file_paths = []
    for file_name in os.listdir(path):
        if(newsEnding.match(file_name)):
            file_path = path + file_name
            file_paths.append(file_path)
    return file_paths


def main(numberOfRuns, sleepInterval):
    run=True
    paths = findNewsFiles("./data/")
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Clicks history")
    sheet1.write(0, 0, "URL")
    sheet1.write(0, 1, u'Antal click vid tiden: ' + str(time.asctime(time.localtime(time.time()))))


    colTime = 1
    row = 1
    for path in paths:
        with open(path, 'r') as file:
            data=file.read().split('\n')

        print time.asctime(time.localtime(time.time()))
        for line in data:
            if line!='':
                dataDict = ast.literal_eval(line)
                url=dataDict["long_url"]
                clicks=dataDict["global_clicks"]
                sheet1.write(row, 0, url)
                sheet1.write(row, colTime, clicks)
                row=row+1

    sheet2 = book.add_sheet("Classifier results")
    sheet2.write(0, 0, "Article")
    sheet2.write(0, 1, "Class by classifier")
    classPath = "./data/news/classifications.txt"
    with open(classPath, 'r') as classFile:
        classData=classFile.read().split('\n')
    row=1
    for line in classData:
        if line!='':
            sheet2.write(row, 0, line.split(';')[0])
            sheet2.write(row, 1, line.split(';')[1])
            row = row + 1

    while run:
        colTime = colTime+1
        sheet1.write(0, colTime, u'Antal click vid tiden: ' + str(time.asctime(time.localtime(time.time()))))
        print path
        print time.asctime(time.localtime(time.time()))
        updatedData = bitlydatahandler.updateClicks(path)
        row = 1
        for line in updatedData:
            if line!='':
                clicks=line["global_clicks"]
                sheet1.write(row, colTime, clicks)
                row=row+1
        if colTime > numberOfRuns:
            run = False
            print "DONE"
        else:
            time.sleep( sleepInterval )

    book.save("ResultsBitly.xls")