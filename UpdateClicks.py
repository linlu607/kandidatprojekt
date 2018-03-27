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

    classPath = "./data/news/classifications.txt"
    with open(classPath, 'r') as classFile:
        classData=classFile.read().split('\n')
    dictionaryOfURLandClass = {}
    for line in classData:
        if line!='':
            dictionaryOfURLandClass[line.split(';')[2]] = line.split(';')[1]
    
    paths = findNewsFiles("./data/")
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Clicks")
    rowReal = 0

    for path in paths:
        colTime = 2
        with open(path, 'r') as file:
            data=file.read().split('\n')

        sheet1.write(rowReal, 0, "URL")
        sheet1.write(rowReal, 2, u'Tid: ' + path[len(path)-26:len(path)-9])
        rowReal = rowReal + 1
        counterReal = 0
        print "File " + path + " is start file no. %d" % (paths.index(path)+1)
        for line in data:
            if line!='':
                dataDict = ast.literal_eval(line)
                url=dataDict["long_url"]
                clicks=dataDict["global_clicks"]
                try:
                    sheet1.write(rowReal, 0, url)
                    sheet1.write(rowReal, colTime, clicks)
                    rowReal=rowReal+1
                    counterReal = counterReal + 1
                except KeyError as e:
                    print "THIS URL HAS BEEN SAVED WEIRDLY." #"A CLASS (unknown) WILL BE ASSIGNED HERE EVENTHOUGH IT MAY HAVE BEEN ASSIGNED A CLASS PREVIOUSLY!"
                    print url
        
        updatePaths = findUpdateFiles("./data/", path)
        print "Is updatePaths for " + path + " empty (False = there's stuff to do)?", updatePaths.empty()
        while updatePaths.empty() is False:
            updatePath = updatePaths.get()
            colTime = colTime + 1
            rowReal = rowReal - counterReal - 1
            sheet1.write(rowReal, colTime, u'Tid: ' + updatePath[len(updatePath)-22:len(updatePath)-5])
            rowReal=rowReal+1
            with open(updatePath, 'r') as file:
               updateArray = ast.literal_eval(file.read())
            for sampleUpdate in updateArray:
                clicks = sampleUpdate["global_clicks"]
                url=sampleUpdate["long_url"]
                try:
                    sheet1.write(rowReal, colTime, clicks)
                    rowReal=rowReal+1
                except KeyError as e:
                    print "THAT WEIRD URL STRIKES AGAIN, THIS TIME IN UPDATING!"
        rowReal = rowReal + 2
    
    book.save("ResultsBitly.xls")
    print "Done updating, done saving excel."

