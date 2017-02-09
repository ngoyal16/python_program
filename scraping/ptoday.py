import requests
from bs4 import BeautifulSoup
from math import ceil

base_url = 'https://jobs.personneltoday.com'

position = '/'
job_type = '/'
sector = '/'
salary = '/'
location = '/united-kingdom'
contract_type = '/contract'
hours = '/full-time'

url = '/jobs'
for param in (position, job_type, sector, salary, location, contract_type, hours):
    if param != '/':
        url += param
print(url)

def getSoup(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    res = requests.get(base_url + url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


#total_pages = ceil(int(getSoup(url).select('h2')[0].getText().split()[1])/20)
total_pages = 1 # Comment for full data.
for page in range(1, total_pages+1):
    soup = getSoup(url + str(page))
    s = soup.select('.lister__item')
    #print(len(s))
    
    for i in range(len(s)):
        data = {}
        print('---------------------------------')
        data['Link'] = s[i].select('a')[0].get('href')
        data['Position'] = s[i].select('a')[0].getText()
        data['Location'] = s[i].select('p span')[0].getText()
        data['Salary'] = s[i].select('p span')[1].getText()
        data['Company'] = s[i].select('p span')[2].getText()

        for key,value in data.items():
            print(key + " : " + value)


