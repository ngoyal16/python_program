import requests
import re
from bs4 import BeautifulSoup

pattern = re.compile('var digitalData = .*')
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def getDigitalData(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    scripts = soup.find_all('script')

    for script in scripts:
        scriptData = str(script.string).strip().replace('\n', ' ')
        if(pattern.match(scriptData)):
            data = re.sub(r"\s+", " ",  scriptData)
            data = data.split("} if (")[0]
            data = data.lstrip("var digitalData = ")
            data = data.split(',')
            digitalData = {}
            for i in range(len(data)):
                subdata = data[i].split(',')[0].split(': ')
                subdata[0] = subdata[0][subdata[0].find(' ')+1:]
                subdata[1] = (subdata[1]).replace('\"', '')
                digitalData[subdata[0]] = subdata[1]
            return(digitalData)
