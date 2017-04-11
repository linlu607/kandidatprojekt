import xlwt
import ast
import time
import re
import os
import bitlydatahandler
import Queue
newsEnding = re.compile('.*news\.txt$')
path = ""

def findNewsFiles(path):
    file_paths = []
    for file_name in os.listdir(path):
        if(newsEnding.match(file_name)):
            file_path = path + file_name
            file_paths.append(file_path)
    return file_paths

def findUpdateFiles(path, origin):
    file_paths = Queue.PriorityQueue()
    timestampAndNews = origin[(len(origin)-26):(len(origin)-4)]
    updateForm = re.compile(timestampAndNews + '[_]{1}.*')
    for file_name in os.listdir(path):
        if(updateForm.match(file_name)):
            file_path = path + file_name
            file_paths.put(file_path, int(file_name[(len(file_name)-11):(len(file_name)-5)]))
    return file_paths

def main():
    paths = findNewsFiles("./data/")
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Clicks history")
    row = 0
    urlsAndClasses = []
    with open('./data/links/articleURLAndTitle.txt', 'r') as f:
        urlsAndClasses = ast.literal_eval(f.read())
    for path in paths:
        colTime = 1
        with open(path, 'r') as file:
            data=file.read().split('\n')

        sheet1.write(row, 0, "URL")
        sheet1.write(row, 1, u'Antal click vid tiden: ' + path[len(path)-26:len(path)-9])
        row = row + 1
        counter = 0
        print "File " + path + " is start file no. %d" % (paths.index(path)+1)
        for line in data:
            if line!='':
                dataDict = ast.literal_eval(line)
                url=dataDict["long_url"]
                clicks=dataDict["global_clicks"]
                sheet1.write(row, 0, url)
                sheet1.write(row, colTime, clicks)
                row=row+1
                counter = counter + 1
        
        updatePaths = findUpdateFiles("./data/", path)
        updateArray = []
        print "Is updatePaths for " + path + " empty?", updatePaths.empty()
        while updatePaths.empty() is False:
            updatePath = updatePaths.get()
            colTime = colTime + 1
            row = row - counter - 1
            sheet1.write(row, colTime, u'Antal click vid tiden: ' + updatePath[len(updatePath)-22:len(updatePath)-5])
            row = row + 1
            with open(updatePath, 'r') as file:
               updateArray = ast.literal_eval(file.read())
            for sampleUpdate in updateArray:
                clicks = sampleUpdate["global_clicks"]
                sheet1.write(row, colTime, clicks)
                row=row+1
        row = row + 2

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
            sheet2.write(row, 2, line.split(';')[2])
            row = row + 1
    book.save("ResultsBitly.xls")

