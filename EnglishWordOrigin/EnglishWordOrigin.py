import traceback

import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

urlBase = """https://dic.daum.net/search.do?q={0}&dic=eng"""
urlDetail = """https://dic.daum.net/word/view.do?wordid={0}"""

def returnSoup(getUrl):
	options = webdriver.ChromeOptions()
	options.add_argument("headless")
	
	driver = webdriver.Chrome(options=options)
	driver.get(getUrl)
	html = driver.page_source
	
	driver.close()
	
	soup = BeautifulSoup(html, "html.parser")
	return soup

def search_daum_dic_1(getUrl):
	soup = returnSoup(getUrl)
	tit_cleansch = soup.find(attrs={'class':'tit_cleansch'})
	
	if tit_cleansch != None:
		data_tiara_id = tit_cleansch.attrs.get('data-tiara-id')
		sendUrl = urlDetail.format(data_tiara_id)
		soup = returnSoup(getUrl)
		search_daum_dic_3(soup)
	else:
		search_daum_dic_3(soup)	

def search_daum_dic_2(getUrl):
	soup = returnSoup(getUrl)
	search_daum_dic_3(soup)
	

def search_daum_dic_3(soup):
	txt_refer = soup.find_all(attrs={'class':'txt_refer on'})	

	strResult = ''
	
	if len(txt_refer) == 0:
		strResult += 'None\n'
		#strResult += 'None, '
	else:
		for item in txt_refer:
			parseText = item.get_text().strip()
			#if parseText and parseText.replace('[', '').replace(']', '').replace('{', '').replace('}', '').startswith('어원'):
			if "어원" in parseText:
				print ('parseText: [' + parseText + ']')
				if len(strResult) != 0:
					strResult += ', ' + parseText
				else:
					strResult = parseText
	
	print('strResult: [' + strResult + ']')

def main(args=None):
	print("main: Start")
	
	try:
		word = 'test'
		#word = 'welfare'
		urlBaseFormat = urlBase.format(word)
		search_daum_dic_1(urlBaseFormat)

	except Exception as exptn:
		print("main: Exception")
		print(type(exptn))
		print(exptn.args)
		print(exptn)
		print('exptn: ', traceback.format_exc())
	else:
		print("main: Ok")
	print("main: End")
		


if __name__ == "__main__":
	main()