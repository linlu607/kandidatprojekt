import urllib
from bs4 import BeautifulSoup

print "Getting the news"
url = "https://en.wikipedia.org/wiki/Terminal_High_Altitude_Area_Defense"
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

print "Article parsed, reading."

# Stuff should happen here

print "Commiting to memory"

path = './data/news/'
o = open(path+'news1.txt', 'w')
print text
o.write(text.encode('utf8'))
o.close()
print "Done"

