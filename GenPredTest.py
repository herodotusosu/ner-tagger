from __future__ import division
import sys
import re
import os
import string
import operator
from model import *

Test = (open(sys.argv[1]).read().splitlines())
Pred  = (open(sys.argv[2]).read().splitlines())

for i in range(0, len(Test)):
	if len(Test[i].split()) == 0:
		print
	else:
		print 'P:', Pred[i], 'A:', Test[i]