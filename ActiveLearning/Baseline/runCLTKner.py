# !/usr/bin/env python
# -*- coding: ascii -*-

import sys
# import cltk
# from cltk.corpus.utils.importer import CorpusImporter
# corpus_importer = CorpusImporter('latin')
# corpus_importer.list_corpora
## remote corpus 
# corpus_importer.import_corpus('latin_text_latin_library')
# from cltk.tag import ner

import cltk
from cltk.corpus.utils.importer import CorpusImporter
CorpusImporter('latin').import_corpus('latin_text_latin_library')
from cltk.tag import ner

n = 0
for line in sys.stdin:
	if len(line.split()) > 0:
		#line = line.replace('\n','')
		# print(line)
		# print()
		list = ner.tag_ner('latin', input_text=line)#, output_type=list)
		for item in list:
			word = item[0]
			if len(item) > 1:
				label = item[1]
			else:
				label = '0'
			if len(word.split()) != 0:
				print(label, '\t'+word)
	else:
		# print('_____________________________________________')
		print()