# -*- coding: cp1252 -*-
import urllib
from bs4 import BeautifulSoup


url = "http://www.aftonbladet.se/nyheter/a/4ax5e/teorin-de-skots-bakifran--inne-i-bilen"
html = urllib.urlopen(url).read()
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



#for word in text.split():   
#    if i==1:
#        print("första ordet som finns är: " + word)
        #print i, c
#extracting the hole text

#print(text)

path = './data/news/'
o = open(path+"news1.txt","a")
realText=""
for line in text.split("\n"):
    #if "BBC" in line:
    tmp=len(line.split(" "))
    if(tmp>10):
        line=line+"\n"
        o.write(line.encode("utf8"))
        print(line)
o.close


print("done")
#text = text.encode('ascii', 'ignore').decode('ascii')
#print 'test'
#sys.stdout.close()	
#print(text)    
#trying to extract just the news article
#print(realText)
