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
    dateclose = soup.findAll('div', {'class':'cf margin-bottom-5'})
    for i in dateclose:
        if 'Closes' in i.getText():
            digitalData['JobDateCloses'] = i.getText().replace('\t','').replace('\n','').replace('\r','').replace('Closes', '') 

    for script in scripts:
        scriptData = str(script.string).strip().replace('\n', ' ')
        if(pattern.match(scriptData)):
            data = re.sub(r"\s+", " ",  scriptData)
            data = data.split("'' }];")[0]
            data = data.lstrip("var ClientGoogleTagManagerDataLayer = ")
            data = data.split(',')

            for i in range(len(data)):
                subdata = data[i].split(': ')
                subdata[0] = subdata[0][subdata[0].find(' ')+1:].replace('\'', '')
                try:
                    digitalData[subdata[0]] = (subdata[1]).replace('\'', '')
                except:
                    pass

    return digitalData


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
#print(url)

#total_pages = ceil(int(getSoup(url).select('h2')[0].getText().split()[1])/20)
total_pages = 1 # Comment for full data.
for page in range(1, total_pages+1):
    soup = getSoup(url + str(page))
    s = soup.select('.lister__item')
    #print(len(s))
    
    for i in range(len(s)):
        data = {}
        print('---------------------------------')
        data['job_link'] = s[i].select('a')[0].get('href')
        data['job_position'] = s[i].select('a')[0].getText()
        data['job_location'] = s[i].select('p span')[0].getText()
        data['job_salary'] = s[i].select('p span')[1].getText()
        data['job_company'] = s[i].select('p span')[2].getText()
        data['job_id'] = data['job_link'].split('/')[2]

        data.update(getDigitalData(base_url + data['job_link']))

        for key,value in data.items():
            print(key + " : " + value)

