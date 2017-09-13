# -*- coding: utf-8 -*-
import sys
import string

output = {}
n = -1
body = False
bodyText = True
printline = ''

for line in sys.stdin:
	line = line.replace('\n','')
	n += 1
	if len(line.split()) > 0:
		if '</text>' in line:
			body = False
			# print line
			# print n
		elif '</body>' in line:
			body = False
			# print line
			# print n
		elif '<text>' in line:
			# print line
			# print n
			body = True
		elif '<body>' in line:
			# print line
			# print n
			body = True
	if body == True and '<body>' not in line and '<text>' not in line:
		last3 = ''
		for chr in line:
			if chr == '<':
				bodyText = False
			if bodyText == True:
				printline += chr
			elif chr == 'v' and last3 == 'di':
				if len(printline.split()) > 0:
					printline2 = printline.split()[0]
					if len(printline.split()) > 1:
						for w in printline.split()[1:]:
							printline2 += ' '+w
					print printline2
					print
					printline = ''
				last3 = ''
			if chr == '>':
				bodyText = True
			if chr == 'd':
				last3 = 'd'
			elif last3 == 'd' and chr == 'i':
				last3 = 'di'
			else:
				last3 = ''
	if body == True and '/head' in line and len(printline.split()) > 0:
		printline2 = printline.split()[0]
		if len(printline.split()) > 1:
			for w in printline.split()[1:]:
				printline2 += ' '+w
		print printline2
		print
		printline = ''
	if printline != '' and printline[-1] != ' ':
		printline += ' '