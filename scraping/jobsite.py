import requests, os
from bs4 import BeautifulSoup
from math import ceil

base_url = 'http://www.jobsite.co.uk'

def getSoup(p):
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    url = 'http://www.jobsite.co.uk/vacancies?search_type=advanced&engine=stepmatch&search_referer=internal&query=&logic=any&title_query=&title_logic=any&location=&radius=50&p=%d&daysback=A&sort_by=relevance&search_currency_code=GBP&salary_type_unit=A&salary_min=40000&salary_max=&vacancy_type=Contract&sector=AC&sector=FI&sector=CY&sector=GR&sector=HR&sector=IT&sector=ME&sector=MK&sector=MD&sector=PO&sector=PS&sector=PU&sector=RC&sector=SC'%p
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


total_pages = 1
#total_pages = ceil(2465/25) Uncomment this for all pages
for page in range(1,total_pages+1):
    soup = getSoup(page)
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
        

