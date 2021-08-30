from PIL import Image
import os
def search_photos (dir):
	aarray=[]
	aarray.append (0)
	allDirs=os.listdir (dir)
	for i in range (len(allDirs)):
		if not os.path.isdir (allDirs[i]) and get_extension (allDirs[i])=="jpg" or get_extension (allDirs[i])=="png": aarray.append (os.path.join (dir, allDirs[i]))
	aarray[0]=len(aarray)
	aarray[0]=aarray[0]-1
	return aarray

def get_extension (param):
	return param.split('.')[-1].lower()

def valid_arg (param):
	if get_extension (param)!="jpg" or get_extension (param)!="png":
		return None
	param=os.path.abspath(param)
	if os.path.isfile (param):
		return param
	else:
		return None

def get_date_taken(path):
	date=""
	try:
		# get from file tag
		date=Image.open(path).getexif()[306]
	except:
		# if exif is empty, get from file properties
		timestamp=os.path.getctime(path)
		date = datetime.fromtimestamp(timestamp).strftime ('%Y:%m:%d %H:%M:%S')
	return date
