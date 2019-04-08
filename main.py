#!/usr/bin/env python3.7

BASE_URL='https://thenounproject.com/browse/?i='

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import re
import base64
import logging

def substring_after(s, delim):
	return s.partition(delim)[2]

def get_logger(    
		LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
		LOG_NAME       = '',
		LOG_FILE_INFO  = 'file.log',
		LOG_FILE_ERROR = 'file.err'):

	log           = logging.getLogger(LOG_NAME)
	log_formatter = logging.Formatter(LOG_FORMAT)

	# comment this to suppress console output
	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(log_formatter)
	log.addHandler(stream_handler)

	file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
	file_handler_info.setFormatter(log_formatter)
	file_handler_info.setLevel(logging.INFO)
	log.addHandler(file_handler_info)

	file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
	file_handler_error.setFormatter(log_formatter)
	file_handler_error.setLevel(logging.ERROR)
	log.addHandler(file_handler_error)

	log.setLevel(logging.INFO)

	return log

my_logger = get_logger()
options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)

for pic_num in range(1,100):
	print('working on id', pic_num)
	driver.get(BASE_URL+str(pic_num))
	delay = 6
	t = time.time()
	try:
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'iconPreview')))
		html = driver.page_source
		soup = BeautifulSoup(html, features='lxml')

		name = soup.select_one('.main-term').string.lower().replace(' ','_')
		tag = soup.select_one('.iconPreview')
		pic = substring_after(tag['style'], 'base64,')[:-3]

		svg = base64.b64decode(pic).decode('utf-8')

		with open("pics/{:07d}_{}.svg".format(pic_num, name), 'w') as f:
			f.write(svg)
		print("Page for {} with id {} was ready in {:.2f} seconds".format(name,pic_num,time.time()-t))
		my_logger.info("Page for {} with id {} was ready in {:.2f} seconds".format(name,pic_num,time.time()-t))
	except TimeoutException:
		print("Loading {} took too much time!".format(pic_num))
		my_logger.info("Loading {} took too much time!".format(pic_num))
driver.quit()

#print(p_element.text)