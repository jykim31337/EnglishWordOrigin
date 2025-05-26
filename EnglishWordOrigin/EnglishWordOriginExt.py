# -*- coding: cp949 -*-
import traceback

import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd

import xlrd
from xlutils.copy import copy

urlBase = """https://dic.daum.net/search.do?q={0}&dic=eng"""
urlDetail = """https://dic.daum.net/word/view.do?wordid={0}"""

workPath = "d:\\DaumDic\\"
sourceExcelFileName = "wordbook.xls"
targetExcelFileName = "workbook_result.xls"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

def returnSoup(getUrl):
	driver.get(getUrl)
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	return soup

def search_daum_dic_1(getUrl):
	soup = returnSoup(getUrl)
	tit_cleansch = soup.find(attrs={'class':'tit_cleansch'})
	
	if tit_cleansch != None:
		data_tiara_id = tit_cleansch.attrs.get('data-tiara-id')
		sendUrl = urlDetail.format(data_tiara_id)
		soup = returnSoup(sendUrl)
		return search_daum_dic_3(soup)
	else:
		return search_daum_dic_3(soup)	

	
def get_example(soup):
	
	try:
		'''
		$('.list_example')[0].children[0]
		$('.list_example')[3].children.length
		'''
		txt_example = soup.find_all(attrs={'class':'list_example'})
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
		pass
	
	return examples

def search_daum_dic_3(soup):
	
	strResult = ''
	
	try:
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
		pass

	return strResult

def readXlsFile(fileName):
	
	df = pd.read_excel(fileName, usecols=['단어'])
	result = df['단어'].tolist()
	
	return result

def doWork(wordList, workIdx):

	resultList = []
	
	wordListLen = len(wordList)
	
	for i in range(0, len(wordList)):
		word = wordList[i]
		print("workIdx: ", str(workIdx + 1), " | wordIdx: ", str(i + 1) + "/" + str(wordListLen), " | word: ", word)
		urlBaseFormat = urlBase.format(word)
		result = search_daum_dic_1(urlBaseFormat)
		writeLine = word + "\t" + result + "\n"
		resultList.append([word, result, len(result)])
		
	return resultList

def saveWorkXls(list):
	sourceFile = workPath + sourceExcelFileName
	targetFile = workPath + targetExcelFileName
	
	rb = xlrd.open_workbook(sourceFile, formatting_info=True)
	sheet = rb.sheet_by_index(0)
	wb = copy(rb)
	ws = wb.get_sheet(0)

	ws.write(0, 7, '어원')
	ws.write(0, 8, '예제')

	row = 1

	for item in list:
		ws.write(row, 7, item[0])
		ws.write(row, 8, item[1])
		row = row + 1
		
	wb.save(targetFile)


def main(args=None):
	
	print("main: Start")
	
	wordList = readXlsFile(workPath + sourceExcelFileName)
	
	try:
		# if simple list work
		#wordList = [
		#	'rupture', 
		#	'wander', 
		#	'terrain', 
		#	'debris', 
		#	'flaw', 
		#	'tip', 
		#	'hurl', 
		#	'refined', 
		#	'subtle', 
		#	'leverage', 
		#	'airborne', 
		#	'experiment', 
		#	'bunk', 
		#	'sublimate', 
		#	]
		
		# or only single word
		#wordList = ['inspire']

		wordListLen = len(wordList)

		I_IDX= wordListLen
		J_IDX = 3
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
				finalResult[i][1] = sortedResult[0][1]

				pass
				

		driver.close()

		saveWorkXls(finalResult)

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