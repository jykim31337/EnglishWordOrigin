import traceback

import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

urlBase = """https://dic.daum.net/search.do?q={0}&dic=eng"""
urlDetail = """https://dic.daum.net/word/view.do?wordid={0}"""

path = "E:\\OneDrive\\학습\\영어\\2024\\"
fileName = "wordbook-all.csv"
targetFileName = "target.txt"

options = webdriver.ChromeOptions()
#options.add_argument("headless")
driver = webdriver.Chrome(options=options)

def returnSoup(getUrl):
	
	driver.get(getUrl)
	html = driver.page_source
	
	#driver.close()
	
	soup = BeautifulSoup(html, "html.parser")
	return soup

def search_daum_dic_1(getUrl):
	print('FirstUrl: ', getUrl)
	soup = returnSoup(getUrl)
	tit_cleansch = soup.find(attrs={'class':'tit_cleansch'})
	
	if tit_cleansch != None:
		data_tiara_id = tit_cleansch.attrs.get('data-tiara-id')
		sendUrl = urlDetail.format(data_tiara_id)
		#print('SecondUrl: ', sendUrl)
		soup = returnSoup(sendUrl)
		return search_daum_dic_3(soup)
	else:
		return search_daum_dic_3(soup)	

#def search_daum_dic_2(getUrl):
#	soup = returnSoup(getUrl)
#	search_daum_dic_3(soup)
	

def search_daum_dic_3(soup):
	#txt_refer = soup.find_all(attrs={'class':'txt_refer on'})
	#txt_refer = soup.find_all()
	txt_refer = soup.find_all(attrs={'class':'ex_refer'})

	strResult = ''
	
	if len(txt_refer) == 0:
		strResult += ''
	else:
		for item in txt_refer:
			parseText = item.get_text().strip()
			if "어원" in parseText:
				
				txt_refer = item.find_all(attrs={'class':'txt_refer on'})
				
				if len(txt_refer) == 1:
					parseText = txt_refer[0].get_text().strip()
					parseText = parseText.replace('[어원] ', '').replace('\n', ' | ')
				else:
					print('CHECK_THIS')

				if len(strResult) != 0:
					strResult += ' | ' + parseText
				else:
					strResult = parseText
	
	print('strResult: [' + strResult + ']')
	
	return strResult


def readFile(fileName):
	result = []
	f = open(fileName, 'r', encoding='UTF8')
	
	while True:
		line = f.readline()
		if not line: 
			break
		lineSplit = line.split(',')
		result.append(lineSplit[0])
		
	f.close()
	
	return result

def doWork(wordList):

	resultList = []

	for word in wordList:	
		urlBaseFormat = urlBase.format(word)
		result = search_daum_dic_1(urlBaseFormat)
		writeLine = word + "\t" + result + "\n"
		resultList.append([word, result, len(result)])
		
	return resultList

def saveWork(list):
	targetFile = path + targetFileName
	f = open(targetFile, 'w', encoding='UTF8')
	for item in list:
		writeLine = item[0] + "\t" + item[1] + "\n"
		f.write(writeLine)
	f.close()


def main(args=None):
	print("main: Start")
	
	wordList = readFile(path + fileName)
	
	try:
		'''
		wordList = [
			'excel'
			, 'excite'
			, 'exhaust'
			, 'expect'
			, 'expected'
			, 'experience'
			, 'experiment'
			, 'expert'
			, 'extend'
			, 'extensive'
			]
		'''

		wordListLen = len(wordList)

		I_IDX= wordListLen
		J_IDX = 5
		totalResult = [[0]*J_IDX for _ in range(I_IDX)]
		finalResult = [[0]*J_IDX for _ in range(I_IDX)]

		for j in range(0, J_IDX):
			result = doWork(wordList)
			
			for i in range(0, wordListLen):
				totalResult[i][j] = result[i]

		for i in range(0, wordListLen):
			if (totalResult[i][0] == totalResult[i][1] == totalResult[i][2]) == True:
				finalResult[i][0] = wordList[i]
				finalResult[i][1] = totalResult[i][0][1]
			else:
				finalResult[i][0] = wordList[i]
				
				sortedResult = sorted(totalResult[i], reverse = True, key = lambda x:x[2])
				print('sortedResult: ', sortedResult)
				finalResult[i][1] = sortedResult[0][1]

				pass
				

		driver.close()

		saveWork(finalResult)
		#word = 'test'
		##word = 'welfare'
		#urlBaseFormat = urlBase.format(word)
		#search_daum_dic_1(urlBaseFormat)

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