#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys
import string

titleStmt = False
TG = False
Tgo = False
AG = False
Ago = False
author = 'UNKNOWN'
title = 'UNKNOWN'

for line in sys.stdin:
	if '/titleStmt' in line:
		break
	if titleStmt == True:
		if '</title' in line:
			n = -1
			for chr in line:
				n += 1
				if chr == '<':
					Tgo = False
					if line[n+1:n+8] == '/title>':
						TG = False
						break
				if Tgo == True:
					if title == 'UNKNOWN':
						title = ''
					title += chr
				if chr == 'e' and line[n-5:n] == '<titl':
					TG = True
				if TG == True and chr == '>':
					Tgo = True

		if '</author' in line:
			n = -1
			for chr in line:
				n += 1
				if chr == '<':
					Ago = False
					if line[n+1:n+9] == '/author>':
						AG = False
						break
				if Ago == True:
					if author == 'UNKNOWN':
						author = ''
					author += chr
				if chr == 'r' and line[n-6:n] == '<autho':
					AG = True
				if AG == True and chr == '>':
					Ago = True

	if 'titleStmt' in line:
		titleStmt = True

title = title.replace(' ','_').replace('Machine_readable_text','')
author = author.replace(' ','_')
while title[-1] == '_':
	title = title[0:-1]
while author[-1] == '_':
	author = author[0:-1]
if len(title) > 50:
	title = title[0:50]
if len(author) > 50:
	author = author[0:50]

print title
