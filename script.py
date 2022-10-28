import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def Manitoba_schools() -> None:
	districts = "https://web36.gov.mb.ca/school/school?action=district"
	soup = BeautifulSoup(requests.get(districts).content, "html.parser")

	options = soup.find("select",{"name":"DivisionSelection"}).findAll("option")

	id_ = [option.get('value') for option in options[1:]]
	id_.pop(1)
	id_.pop(4)

	mylist = []
	for i in id_:
		search_page = f"https://web36.gov.mb.ca/school/school?action=district&DivisionSelection={i}"
		request = requests.get(search_page)
		soup = BeautifulSoup(request.text, "lxml")
		n_schools = soup.findAll('div', attrs = {'class':'n_schools'})
		n_schools= re.findall("[0-9]+",str(n_schools))
		High=n_schools[2]
		schools = f"https://web36.gov.mb.ca/school/school?action=district&High={High}&Low=1&DivisionSelection={i}"
		request = requests.get(schools)
		soup = BeautifulSoup(request.text, "lxml")

		data = soup.findAll('div', attrs = {'class':'sc_address'})

		data = [[x.get_text(separator="<br>", strip=True) for x in y.findAll('div')] for y in data]
		mylist.extend(data[1:])

	df = pd.DataFrame(mylist)
	headerName=['Name', 'Info']
	df.columns=headerName

	df['Address'] = df['Info'].str.split("<br>", n = 1, expand=True)[0]
	df['City'] = df['Info'].str.split("<br>", n = 2, expand=True)[1]
	df['Postal Code'] = df['Info'].str.split("<br>", n = 3, expand=True)[2]
	df['Phone'] = df['Info'].str.split("<br>", n = 5, expand=True)[4]
	df['Fax'] = df['Info'].str.split("<br>", n = 7, expand=True)[6]
	df['Grades'] = df['Info'].str.split("<br>", n = 9, expand=True)[8]
	df['Program'] = df['Info'].str.split("<br>", n = 11, expand=True)[10]

	df = df.drop('Info', axis=1)

	df.to_csv("output.tsv", sep = "\t",index=False)

if __name__ == '__main__':
    Manitoba_schools()
