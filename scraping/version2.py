from bs4 import BeautifulSoup
from selenium import webdriver

url ='view-source:http://www.jobsite.co.uk/job/business-continuity-manager-957493975?src=search&tmpl=lin&sctr=IT&position=12&page=1&engine=stepmatch&search_referer=external-other'

browser = webdriver.Chrome('/home/imnobody0396/Documents/chromedriver')
browser.get(url)

src = browser.page_source
soup = BeautifulSoup(src, 'lxml')


f = open('src.txt', 'w')
f.write(soup.prettify())
f.close()

f = open('/home/imnobody0396/Desktop/src.txt', 'r')
c = 0
for i in f.readlines():
    if c>2:
        break
    if 'discipline' in i.lower():
        print(i)
        c += 1
        
f.close()
