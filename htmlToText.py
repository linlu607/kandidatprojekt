import os
<<<<<<< HEAD

=======
>>>>>>> ed9905d7edaad9d56e6c8955a202dc3aa9a324aa
import urllib
from bs4 import BeautifulSoup
import time
from time import strftime
<<<<<<< HEAD



url = "http://www.aftonbladet.se/nyheter/a/4ax5e/teorin-de-skots-bakifran--inne-i-bilen"

=======

print "Getting the news"
url = "https://en.wikipedia.org/wiki/Terminal_High_Altitude_Area_Defense"
>>>>>>> ed9905d7edaad9d56e6c8955a202dc3aa9a324aa
html = urllib.urlopen(url).read()
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

<<<<<<< HEAD

=======
>>>>>>> ed9905d7edaad9d56e6c8955a202dc3aa9a324aa
print "Article parsed, reading."

# Stuff should happen here

print "Commiting to memory"

path = './data/news/'
time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
file_path_and_name = path+'news ' + soup.title.string + ' ' + time_for_filename + '.txt'
if not os.path.exists(os.path.dirname(file_path_and_name)):
    try:
        os.makedirs(os.path.dirname(file_path_and_name))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
<<<<<<< HEAD

o = open(file_path_and_name,"a")
realText=""
for line in text.split("\n"):
    tmp=len(line.split(" "))
    if(tmp>10):
        line=line+"\n"
        o.write(line.encode("utf8"))
        print(line)
o.close
=======
o = open(file_path_and_name, 'w')
o.write(text.encode('utf8'))
o.close()
print text
>>>>>>> ed9905d7edaad9d56e6c8955a202dc3aa9a324aa
print "Done"

