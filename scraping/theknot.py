import requests, bs4
import xlwt as xl

domain = "https://www.theknot.com"

caterer_list = []

def getSoup(url):
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	return soup

def getData(url):
	soup = getSoup(url)
	
	s = soup.select('.card-container')
	for i in s: #Taking slice of 3 per page for testing
		#print("*************************************************")
		#container
		caterer_info = {}
		
		#Getting link
		link = domain + i.find('a').get('href')
		print(link)
		#Requesting this link
		nxtsoup = getSoup(link)
		
		#Getting Vendor Name
		vendor_info = nxtsoup.select('#vendor-info')
		#print(vendor_info[0].find('h1').getText()+"\n")
		caterer_info['Name'] = vendor_info[0].find('h1').getText()
		
		#Getting Vendor Details
		details = nxtsoup.select('.col-lg-12')
		try:
			param = details[0].findAll('span')
			texts = details[0].findAll('p')
			for i,j in zip(param, texts):
				#print(i.getText() + " -> " + j.getText() + "\n")
				caterer_info[i.getText()] = ''.join(j.getText().split('\n'))
				#print(j.getText()+ "\n")
		except IndexError:
			pass
		
		#Getting Vendor Address
		try:
			address = ''.join(nxtsoup.select('.address')[0].getText().split('\n'))
			phone = ''.join(nxtsoup.select('.phone')[0].getText().split('\n'))
			#print("Address -> " + address)
			#print("Phone -> " + phone)
			caterer_info["Address"] = address
			caterer_info["Phone"] = phone
		except IndexError:
			pass
		
		#Getting Vendor Social Links
		ext_links = nxtsoup.select('.contact-methods .external-links .label-value')
		for i in ext_links:
			#print(i.getText() + " -> " + i.find('a').get('href'))
			caterer_info[i.getText()] = i.find('a').get('href')
		caterer_list.append(caterer_info)
		
#Getting Total Vendors
url = 'https://www.theknot.com/marketplace/catering-san-francisco-ca'
soup = getSoup(url)
total_vendors = int(soup.select('#vendor-count')[0].getText().split(' ')[0])

#Offset used in chaging page numbers
#Switching Page Numbers
for offset in range(0,total_vendors,30):
	url = 'https://www.theknot.com/marketplace/catering-san-francisco-ca?offset='+str(offset)
	getData(url)

#Printing Each Dictionary item in list
doc = xl.Workbook()
sheet = doc.add_sheet("Vendor List")
attrbs = ['Name','Price Range','Cuisine','Dietary Options','Wedding Categories','Address','Phone','WEBSITE','FACEBOOK','TWITTER','INSTAGRAM','PINTEREST']
for i,j in enumerate(attrbs):
	sheet.write(0,i,j)

for row,vendor in enumerate(caterer_list):
	for key,value in vendor.items():
		#print(key + " -> " + value)
		sheet.write(row+1,attrbs.index(key),value)

doc.save("data.xlsx")
