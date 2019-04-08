#!/usr/bin/env python3.7
"""
create a csv with number and name
"""
import glob
import os

ignore_duplicates = True
files = glob.glob('pics/*.svg')

vals = []

for file in files:
	name = os.path.basename(file)[:-4]
	parts = name.split('_')
	num = parts[0]
	noun = ' '.join(parts[1:])
	vals.append((num,noun))

vals.sort(key=lambda x: x[0])

if not ignore_duplicates:
	for val in vals:
		num, noun = val
		print(f'{num},{noun}')
else:
	nouns = [noun for _,noun in vals]
	no_duplicates = set(nouns)

	for noun in no_duplicates:
		print(f'{noun}')
