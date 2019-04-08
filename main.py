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
	page = await browser.newPage()
	try:
		await page.goto(BASE_URL+str(num), timeout=6*1000)
		raw_content = await page.content()
		matches = re.findall("<h1>Page Not Found</h1>", raw_content)
		if not matches:
			await page.waitForSelector('.iconPreview', timeout=6*1000)
			content = await page.content()
			await extract_image(content, num)
		else:
			raise Exception(f'Page not found for {num}')
	except Exception as e:
		print(e)
		logger.info(f'{num} _timeout_')
	finally:
		await page.close()

async def worker(name, browser, queue):
	while True:
		idx = await queue.get()
		await fetch_page(browser, idx)
		queue.task_done()
		#print(f'{name} completed {idx}')
		await asyncio.sleep(1.8)
	
async def main():
	n_calls=6
	s = 6286
	q = asyncio.Queue()
	browser = await launch()
	await asyncio.sleep(2)
	for i in range(s,8000):
		q.put_nowait(i)

	tasks = [asyncio.create_task(worker(f'{_}',browser, q)) for _ in range(n_calls)]

	await q.join()

	for task in tasks:
		task.cancel()
	await asyncio.gather(*tasks, return_exceptions=True)
	await browser.close()

logger = get_logger()
loop = asyncio.get_event_loop()

loop.run_until_complete(main())
