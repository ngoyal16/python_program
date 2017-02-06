import requests, os
from bs4 import BeautifulSoup
from math import ceil


def getQueryformat(data):
    for i in range(len(data)):
        if i < len(data)-1:
            data[i] += '%2C'
        if ' ' in data[i]:
            data[i] = '+'.join(data[i].split(' '))
    return ''.join(data)


base_url = 'http://www.jobsite.co.uk'
location = '&location='+getQueryformat(['london'])
sector = '&sector='.join(['','AC', 'FI', 'CY', 'GR', 'HR', 'IT', 'ME', 'MK', 'MD', 'PO', 'PS', 'PU', 'RC', 'SC'])
vacancy_type = '&vacancy_type='.join(['','Contract'])
keywords = '&query='+getQueryformat([''])
title = '&title_query='+getQueryformat([''])
radius = '50'
min_salary = '40000'
max_salary = ''


def getSoup(p):
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    url = 'http://www.jobsite.co.uk/vacancies?search_type=advanced&engine=stepmatch&search_referer=external-other'+keywords+'&logic=any'+location+'&radius='+radius+title+'&title_logic=any'+'&p='+p+'&daysback=A&sort_by=relevance&search_currency_code=GBP&salary_type_unit=A&salary_min='+min_salary+'&salary_max='+max_salary+vacancy_type+sector 
    #print(url)
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


#total_pages = 1
total_pages = ceil(int(getSoup(1).select('.resultsTotal strong')[1].getText()) / 25)
for page in range(1,total_pages+1):
    soup = getSoup(str(page))
    jobs = soup.findAll('div', {'class':'lineage vacRow clearfix job'})
    jobs += soup.findAll('div', {'class':'semi vacRow clearfix job'})
    print(len(jobs))

    for i in range(len(jobs)):
        print('-------------------------------------------\n')
        link = jobs[i].select('a')[0].get('href')
        position = jobs[i].select('a')[0].getText()
        jobDesc = jobs[i].select('p')[0].getText()
        salary = jobs[i].select('.vacSalary')[1].getText()
        location = jobs[i].select('.vacLocation')[1].getText()
        date = jobs[i].select('.vacPosted')[1].getText()
        jobType = jobs[i].select('.vacType')[1].getText()
        print('Position    => %s\n' % position)
        print('Link        => %s\n' % (base_url+link))
        print('JobDesc     => %s\n' % jobDesc)
        print('Salary      => %s\n' % salary)
        print('Location    => %s\n' % location)
        print('Date Posted => %s\n' % date)
        print('Job Type    => %s\n' % jobType)     
