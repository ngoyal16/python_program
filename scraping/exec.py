import requests, re
from bs4 import BeautifulSoup
from math import ceil

pattern = re.compile('var ClientGoogleTagManagerDataLayer = .*')
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def getDigitalData(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    scripts = soup.find_all('script')

    digitalData = {}
    for script in scripts:
        scriptData = str(script.string).strip().replace('\n', ' ')
        if(pattern.match(scriptData)):
            data = re.sub(r"\s+", " ",  scriptData)
            print(data)
            data = data.split("} if (")[0]
            data = data.lstrip("var ClientGoogleTagManagerDataLayer = ")
            data = data.split(',')
            '''
            for i in range(len(data)):
                subdata = data[i].split(',')[0].split(': ')
                subdata[0] = subdata[0][subdata[0].find(' ')+1:]
                digitalData[subdata[0]] = (subdata[1]).replace('\"', '')
           '''     
    #print(data)

getDigitalData('https://www.exec-appointments.com/job/1463080/chief-financial-officer/')
'''
def getSoup(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    res = requests.get(base_url + url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


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

'''
