import urllib
from bs4 import BeautifulSoup
import time
from time import strftime

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
time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
file_path_and_name = path+'news ' + soup.title.string + ' ' + time_for_filename + '.txt'
o = open(file_path_and_name, 'w')
o.write(text.encode('utf8'))
o.close()
print text
print "Done"

