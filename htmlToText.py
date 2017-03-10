import os
import urllib2
from bs4 import BeautifulSoup
import time
from time import strftime

print "Getting the news"

url = "https://en.wikipedia.org/wiki/Mangrove_swallow"

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/48.0')]
html = opener.open(url)

#html = urllib.urlopen(url).read()
print "The news are here! Starting parsing"
soup = BeautifulSoup(html, 'html.parser')

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

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
path = './data/news/'
file_path_and_name = path+'news ' + soup.title.string + ' ' + time_for_filename + '.txt'
#  ' + soup.title.string + ' ' + time_for_filename + '
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
print "Done"
