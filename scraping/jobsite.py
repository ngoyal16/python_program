import requests, os, re
from bs4 import BeautifulSoup
from math import ceil

pattern = re.compile('var digitalData = .*')
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
            data = data.split("} if (")[0]
            data = data.lstrip("var digitalData = ")
            data = data.split(',')
            
            for i in range(len(data)):
                subdata = data[i].split(',')[0].split(': ')
                subdata[0] = subdata[0][subdata[0].find(' ')+1:]
                digitalData[subdata[0]] = (subdata[1]).replace('\"', '')
                
    return(digitalData)


def getQueryformat(data):
    for i in range(len(data)):
        if i < len(data)-1:
            data[i] += '%2C'
        if ' ' in data[i]:
            data[i] = '+'.join(data[i].split(' '))
    return ''.join(data)


def getSoup(p):    
    url = base_url+'/vacancies?search_type=advanced&engine=stepmatch&search_referer=external-other'+keywords+'&logic=any'+location+'&radius='+radius+title+'&title_logic=any'+'&daysback=A&sort_by=relevance&search_currency_code=GBP&salary_type_unit=A&salary_min='+min_salary+'&salary_max='+max_salary+vacancy_type+sector+'&p='+p 
    #print(url)
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


base_url = 'http://www.jobsite.co.uk'
location = '&location='+getQueryformat(['london'])
sector = '&sector='.join(['','AC', 'FI', 'CY', 'GR', 'HR', 'IT', 'ME', 'MK', 'MD', 'PO', 'PS', 'PU', 'RC', 'SC'])
vacancy_type = '&vacancy_type='.join(['','Contract'])
keywords = '&query='+getQueryformat([''])
title = '&title_query='+getQueryformat([''])
radius = '50'
min_salary = '40000'
max_salary = ''


total_pages = 1
#total_pages = ceil(int(getSoup(1).select('.resultsTotal strong')[1].getText()) / 25)
for page in range(1,total_pages+1):
    soup = getSoup(str(page))
    jobs = soup.findAll('div', {'class':'lineage vacRow clearfix job'})
    jobs += soup.findAll('div', {'class':'semi vacRow clearfix job'})
    print(len(jobs))

    for i in range(len(jobs)):
        data = {}
        print('-------------------------------------------\n')
        data['Link'] = jobs[i].select('a')[0].get('href')
        data['Position'] = jobs[i].select('a')[0].getText()
        data['JobDesc'] = jobs[i].select('p')[0].getText()
        data['Salary'] = jobs[i].select('.vacSalary')[1].getText()
        data['Location'] = jobs[i].select('.vacLocation')[1].getText()
        data['Date Posted'] = jobs[i].select('.vacPosted')[1].getText()
        data['Job Type'] = jobs[i].select('.vacType')[1].getText()

        data.update(getDigitalData(base_url+data['Link']))
        
        for i,j in data.items():
            print(i + ' => ' + j)
        #print(getDigitalData(base_url+link))
