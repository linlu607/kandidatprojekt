import urllib
from bs4 import BeautifulSoup

url = "http://www.svt.se/nyheter/lokalt/stockholm/kallor-till-svt-dubbelmordet-gangrelaterat"
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

counter=0
textFile=""
realText=""
for i, c in enumerate(text):
    textFile=textFile+c
    if c==" ":
        counter=counter+1
    if c=="\n":
        counter=0

    if counter==20: 
        realText=realText+textFile
        textFile=""
        
    if counter>20:
        textFile=""
        realText=realText+c    
        
        #print i, c
#extracting the hole text
        
#print(text)    

path = './data/news'
o = open(path+'news1.txt', 'a+')
o.write(str(text))
o.close()

