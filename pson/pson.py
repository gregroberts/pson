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

def fp(pson, target, path = ''):
	if isinstance(pson, list) or isinstance(pson, set):
		return [a for a in not_none([fp(b,target, path = path+'.'+str(a)) for a,b in enumerate(pson)])]
	elif isinstance(pson, dict):
		return [a for a in not_none([fp(b,target, path = path+'.'+str(a)) for a,b in pson.items()])]
	else:
		if pson == target:
			if isinstance(path,str):
				return path[1:]
			else:
				return path
				
def findpath(pson,target):
	return list(flatten(fp(pson,target)))



def replace_path(pson, target, new_val, seperator):
	#no idea if this is stable!!! let's hope so!!!!!
	if isinstance(target, str) or isinstance(target, unicode):
		target = pathparser(target, separator =seperator)
	if isinstance(pson, list):
		return [replace_path(a,target[1:], new_val, seperator) for a in pson]
	elif isinstance(pson, dict):
		if len(target) > 1:
			res = {}
			for a, b in pson.items():
				if a == target[0]:
					res[a] = replace_path(b,target[1:], new_val, seperator)
				else:
					res[a] = b
			return res
		elif len(target) == 1:
			res = {}
			for a, b in pson.items():
				if a == target[0]:
					res[a] = new_val
				else: 
					res[a] = b
			return res
	elif isinstance(pson, str) or isinstance(pson, unicode):
		return pson



if __name__ == '__main__':
	a= {
		'b':{
			'c':{
				'd':1
			},
			'e':[{'f':1},{'f':1}]

		}
	}
	print replace(a,'b.e.f', 'REPLACE!!', '.')