import os
def search_photos (dir):
	aarray=[]
	aarray.append (0)
	allDirs=os.listdir (dir)
		for i in range (len(allDirs):
			if not os.path.isdir (allDirs[i]) and get_extension (allDirs[i])=="jpg" or get_extension (allDirs[i])=="png": aarray.append (allDirs[i])
	aarray[0]=len(aarray)
	return aarray

def get_extension (param):
	return param.split('.')[-1]
