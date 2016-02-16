#
# Walks through workdetail html
# Important:  Many books are a collection of works
# The text is very inconsistant sometimes good, sometimes not there
# probably best to just get a blob of text
#
#####################################################################################

from bs4 import BeautifulSoup as BS

BASE_NAME = "workdetail.jsp?contentid="
BADNUM = [26, 59, 67] #  For some reason these numbers are no good
WHITESPACE = " 　\u3000"


def parsehtml(inhtml: str) -> None:
    soup = BS(inhtml, "html5lib")
    print(soup.prettify())
    soupi = soup.find_all('img')
    soup8 = str(soupi[8]).split('/')
    bookid = soup8[6]
    filenames = []
    filenames.append(soup8[7])
    for i in range(10, len(soupi)):
        filenames.append(str(soupi[i]).split('/')[7])
    soupgrab = str(soup.find(id="work_text")).split('\n')
    textblock = ""
    for i in range(1, len(soupgrab) - 1):   #Start and end are HTML
        textblock += soupgrab[i].strip(WHITESPACE) + "\n"
    soup_info = soup.find_all(id="calligrapher_info")
    strstr = str(soup_info).split("name=")[1]
    calligrapher = strstr.split("\"")[0]
    dynesty = strstr.split("</a>,")[1]



for i in range(1, 81):
    if i not in BADNUM:
        infile = open(BASE_NAME + str(i), mode="r")
        inred = infile.read()
        parsehtml(inred)
        infile.close()

