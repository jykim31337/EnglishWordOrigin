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
	#print('FirstUrl: ', getUrl)
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

	
def get_example(soup):
	
	#print("get_example Start")
	
	try:
		'''
		$('.list_example')[0].children[0]
		$('.list_example')[3].children.length
		'''
		#list_word = soup.find_all(attrs={'class':'list_word'})
		#on = list_word[0].find_all(attrs={'class':'on'})
		txt_example = soup.find_all(attrs={'class':'list_example'})
		#cont_example = item.find_all(attrs={'class':'cont_example'})
		if len(txt_example) == 0:
			return ''
	
		examples = "";

		for te in txt_example:
			if len(te) == 0:
				return ''
			else:
				box_example = te.find_all(attrs={'class':'box_example'})
				
				box_exampleList = []

				for be in box_example:
					txt_ex = be.find_all(attrs={'class':'txt_ex'})
					if len(txt_ex) == 2:
						txt_example = txt_ex[0].get_text().strip()
						mean_example = txt_ex[1].get_text().strip()
						box_exampleList.append([txt_example, mean_example, len(txt_example) + len(mean_example)])
						
				if len(box_exampleList) != 0:
					sortedResult = sorted(box_exampleList, key = lambda x:x[2])
					
					if len(examples) != 0:
						examples += "<br>"	
						
					addItem = sortedResult[0][0] + '<br>' + sortedResult[0][1]

					examples += addItem
		
	except Exception as exptn:
		print("get_example exception")
		print(type(exptn))
		print(exptn.args)
		print(exptn)
		print('exptn: ', traceback.format_exc())
	else:
		#print("get_example Ok")
		pass
	
	#print("get_example End")
	
	return examples

#def search_daum_dic_2(getUrl):
#	soup = returnSoup(getUrl)
#	search_daum_dic_3(soup)

def search_daum_dic_3(soup):
	
	#print("search_daum_dic_3 Start")
	
	strResult = ''
	
	try:
		#txt_refer = soup.find_all(attrs={'class':'txt_refer on'})
		#txt_refer = soup.find_all()
		txt_refer = soup.find_all(attrs={'class':'ex_refer'})
	
		if len(txt_refer) == 0:
			strResult += ''
		else:
			for item in txt_refer:
				parseText = item.get_text().strip()
				if "어원" in parseText:
				
					txt_refer = item.find_all(attrs={'class':'txt_refer on'})
				
					if len(txt_refer) == 1:
						parseText = txt_refer[0].get_text().strip()
						parseText = parseText.replace('[어원] ', '').replace('\n', '<br>')
					else:
						print('CHECK_THIS')

					if len(strResult) != 0:
						strResult += '<br>' + parseText
					else:
						strResult = parseText
	
		#print('strResult: [' + strResult + ']')

		example = get_example(soup)

		if len(example) != 0:
			strResult += "\t " + example
			
	except Exception as exptn:
		print("search_daum_dic_3 exception")
		print(type(exptn))
		print(exptn.args)
		print(exptn)
		print('exptn: ', traceback.format_exc())
	else:
		#print("search_daum_dic_3 Ok")
		pass

	#print("search_daum_dic_3 End")
	
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

def doWork(wordList, workIdx):

	resultList = []
	
	wordListLen = len(wordList)
	
	#for word in wordList:	
	for i in range(0, len(wordList)):
		word = wordList[i]
		print("workIdx: ", str(workIdx + 1), " | wordIdx: ", str(i + 1) + "/" + str(wordListLen), " | word: ", word)
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
		wordList = [
			'footage', \
			'bond', \
			'precise', \
			'fisher', \
			'fisherman', \
			'entertainment', \
			'entertain', \
			'curious', \
			'curiosity', \
			'soar', \
			'route', \
			'bait', \
			'go through', \
			'crisis', \
			'ify', \
			'janitor', \
			'strict'
			]
		
		#wordList = ['inspire']

		wordListLen = len(wordList)

		I_IDX= wordListLen
		J_IDX = 5
		totalResult = [[0]*J_IDX for _ in range(I_IDX)]
		finalResult = [[0]*J_IDX for _ in range(I_IDX)]

		for j in range(0, J_IDX):
			
			print("Work Index: ", j + 1)

			result = doWork(wordList, j)
			
			for i in range(0, wordListLen):
				totalResult[i][j] = result[i]

		for i in range(0, wordListLen):
			
			IsSame = True
			for j in range(0, J_IDX):
				if totalResult[i][0] != totalResult[i][j]:
					IsSame = False
					break

			if IsSame == True:
				finalResult[i][0] = wordList[i]
				finalResult[i][1] = totalResult[i][0][1]
			else:
				print("Is Not Same: totalResult[i]: ", totalResult[i])
				finalResult[i][0] = wordList[i]
				sortedResult = sorted(totalResult[i], reverse = True, key = lambda x:x[2])
				#print('sortedResult: ', sortedResult)
				finalResult[i][1] = sortedResult[0][1]

				pass
				

		driver.close()

		saveWork(finalResult)

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