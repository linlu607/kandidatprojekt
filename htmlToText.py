import os
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError, HTTPRedirectHandler
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import re
from time import strftime

def buildURLList(fake_or_not):
    # In the future this should read links as lines from a .txt
    urlList = []
    if fake_or_not == 0:
        links = open('LinksFakeNews.txt',"r")
    elif fake_or_not == 1:
        links = open('LinkRealNews.txt',"r")
    else:
        return urlList

    lines = links.read()
    links.close()
    for line in lines.split("\n"):
        urlList.append(line)
    return urlList

print "Getting the news"

opener = urllib2.build_opener()
#opener.add_handler(BaseHandler.HTTPRedirectHandler)
opener.addheaders = [('User-Agent', 'Mozilla/48.0')]

runList = []
runList.append('training_fake/')
runList.append('training_real/')
r = 0
for run in runList:
    urlList = buildURLList(r)
    r = r + 1
    for url in urlList:
            try:
                req = opener.open(url)
            except HTTPError as e:
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
                print url
            except URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
                print url
            else:

                html = req.open()
                print "The news are here! Starting parsing"
                soup = BeautifulSoup(html, 'html.parser')

                # kill all script and style elements
                for script in soup(["script", "style"]):
                    script.extract()    # rip it out

                for comment in soup.findAll("div", class_=re.compile('(C|c)omment.*')):
                    comment.extract()

                # get text
                text = soup.get_text()

                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)

                print "Article parsed, reading."

                # Stuff should happen here

                print "Commiting to memory"

                time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
                path = './data/news/'+ run

                title = ""
                i = 0
                if soup.title is None :
                    title = 'noTitle'
                else:
                    for part in soup.title.string.split(" "):
                        temp = ""
                        for character in list(part):
                            if character.isalpha():
                                temp = temp + character
                        title = title + " " + temp
                        i = i + 1
                        if i > 4:
                            break

                file_path_and_name = path+'news ' + title.encode("utf8") + ' ' + time_for_filename + '.txt'
                if not os.path.exists(os.path.dirname(file_path_and_name)):
                    try:
                        os.makedirs(os.path.dirname(file_path_and_name))
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                savedArticle = open(file_path_and_name,"w")
                for line in text.split("\n"):
                    tmp=len(line.split(" "))
                    if(tmp>10):
                        line=line+"\n"
                        savedArticle.write(line.encode("utf8"))
                        savedArticle.flush()
                #        print(line)
                savedArticle.close
                print "Article saved"
print "Done"
