#!/usr/bin/env python3.7

BASE_URL='https://thenounproject.com/browse/?i='

import time

from bs4 import BeautifulSoup
import re
import base64
import logging
import asyncio
from pyppeteer import launch
import xml.dom.minidom
import random


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


def substring_after(s, delim):
	return s.partition(delim)[2]

async def extract_image(content, num):
	soup = BeautifulSoup(content, "html5lib")
	name = soup.select_one('.main-term').string.lower().strip().replace(' ','_')
	tag = soup.select_one('.iconPreview')
	pic = substring_after(tag['style'], 'base64,')[:-3]

	svg = base64.b64decode(pic).decode('utf-8')
	xml_svg = xml.dom.minidom.parseString(svg)
	pretty_svg = xml_svg.toprettyxml()
	with open("pics/{:07d}_{}.svg".format(num, name), 'w') as f:
		f.write(pretty_svg)
	logger.info(f'{num} {name}')

async def fetch_page(browser, num):
	print(f'fetching {num}')
	try:
		page = await browser.newPage()
		await page.goto(BASE_URL+str(num), timeout=6*1000)
		await page.waitForSelector('.iconPreview', timeout=6*1000)
		content = await page.content()
		await extract_image(content, num)
	except:
		logger.info(f'{num} _timeout_')

async def main():
	n_calls=6
	for start in range(163,1000,n_calls):
		browser = await launch()
		await asyncio.gather(*[fetch_page(browser, pic_num) for pic_num in range(start,start+n_calls)])
		await asyncio.sleep(4)
		await browser.close()
logger = get_logger()
loop = asyncio.get_event_loop()

loop.run_until_complete(main())
