
import sys, os
sys.path.append(os.path.dirname('C:\\Users\\Livery35\\Documents\\GitHub\\pson\\pson'))
from streams import Github
from pson import pathparser, pathquery, findpath

def partial_path(pson, path):
	'''when you have a partial path, returns closest pson path'''
	if isinstance(pson, list):
		return partial_path(pson[0], path) 
	path = pathparser(path)
	for i in range(len(path)):
		j = len(path) - i
		ppath = '.'.join(path[:j])
		npath = '.'.join(path[j:])
		res = pathquery(pson, ppath)
		if res is not None:
			return ppath, npath
	else:
		return path
	
def crawler(query, start,handler=lambda x: x):
	'''crawls through a network of objects. 
		How to crawl is determined by handler'''
	pp = partial_path(start,query)
	goto, remains = pp
	if remains != '':
		end = pathquery(start,goto)
		if isinstance(end,str) or isinstance(end, unicode):
			return crawler(remains, handler(end), handler)
	elif remains == '':
		return pathquery(start, goto)

class query(object):
	def __init__(self,query, obj):
		self.obj = obj
		self.query = query


class crawlobjector:
	def __init__(self,handler=lambda x: x):
		self.handler = handler
	def query(self,query_obj):
		if isinstance(query_obj,list):
			print 'list!'
			return [self.query(query) for query in query_obj]	
		elif isinstance(query_obj,dict):
			print 'dict!'
			res = {}
			for kquery,vquery in query_obj.items():
				res[self.query(kquery)] = self.query(vquery)
			return res
		elif query_obj.__class__.__name__ == 'query':
			print 'query!'
			return crawler(query_obj.query,self.handler(query_obj.obj),self.handler)
		else:
			return query_obj


if __name__=='__main__':
	b={'a':'f'}	
	a={'a':{'b':'c','d':b}}
	q ={query('a.d.a',a):query('a.d.a',b),'other':query('a.b', a)}
	r = crawlobjector()
	#print r.query(q)


