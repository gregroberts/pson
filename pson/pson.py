import json
from pprint import pprint
from collections import Iterable




def pathparser(path, separator="."):
		return path.split(separator)

def pathquery(pson, path, separator=".", missing=None, iterate=True):
	if isinstance(path,str) or isinstance(path, unicode):
		path = pathparser(path, separator=separator)
	counter = 0
	for token in path:
		if type(pson) == dict and pson.has_key(token): # step one level deeper into the pson with our token
			pson = pson[token]
		elif type(pson) == list: 
	# if we hit an array see if the token is a number else assume we 
	# want the rest of the path applied to every element in the array
			try:
				if int(token)<len(pson):
					pson = pson[int(token)]
				else: #handle a number longer than list len
					return missing
			except ValueError: 
				if iterate:
					return [pathquery(x, path[counter:]) for x in pson]
				return missing
		else:
			return missing
		counter += 1
	return pson


def not_none(list):
	for a in list:
		if a is not None:
			yield a

def flatten(lis):
	for item in lis:
		if isinstance(item, list):
			for x in flatten(item):
				yield x
		else:        
			yield item	

def findpath(pson, target, path = ''):
	if isinstance(pson, list) or isinstance(pson, set):
		return [a for a in not_none([findpath(b,target, path = path+'.'+str(a)) for a,b in enumerate(pson)])]
	elif isinstance(pson, dict):
		return [a for a in not_none([findpath(b,target, path = path+'.'+str(a)) for a,b in pson.items()])]
	else:
		if pson == target:
			if isinstance(path,str):
				return path[1:]
			else:
				return path


a = ['a',{'c':{'b':'b'}},{'c':['a','b','b']},'d']

if __name__ == '__main__':
	print list(flatten(findpath(a,'b')))
	#returns ['1.c.b', '2.c.1', '2.c.2']