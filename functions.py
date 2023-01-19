from exif import Image
import os
import sys
from datetime import datetime
import re
try:
	import universal_speech as unispeech
except:
	import ctypes
	MB_OK = 0x0
	ICON_STOP = 0x10	
	result = ctypes.windll.user32.MessageBoxW(0, "Cannot initialize universal speech library. Please reinstall program.", "System error", MB_OK| ICON_STOP)
	sys.exit (0)

def decode (param):
	param=param[2:-1]
	temp=""
	text=""
	length=len (param)
	i=0
	while (i<=length-1):
		if (param[i]=="\\") and (i!=length) and (param[i+1]=="x"):
			i=i+2
			if temp!="": temp=temp+param[i]+param[i+1]; temp=bytearray.fromhex(temp).decode('utf-8', errors='ignore'); text=text+temp; i=i+1; temp=""
			else: temp=param[i]+param[i+1]; i=i+1
		else: text=text+param[i]
		i=i+1
	return text.replace ("\\", "")

def speak (text):
	unispeech.output (text)

def search_photos (dir):
	aarray=[]
	aarray.append (0)
	allDirs=os.listdir (dir)
	for i in range (len(allDirs)):
		if not os.path.isdir (allDirs[i]) and get_extension (allDirs[i])=="jpg" or get_extension (allDirs[i])=="png": aarray.append (os.path.join (dir, allDirs[i]))
	aarray[0]=len(aarray)
	aarray[0]=aarray[0]-1
	if aarray[0]==0: return None
	return aarray

def get_extension (param):
	return param.split('.')[-1].lower()

def valid_arg (param):
	ext=get_extension (param)
	if ext!="jpg" and ext!="png":
		return None
	param=os.path.abspath(param)
	if os.path.isfile (param):
		return param
	else:
		return None

def get_date_from_file(path):
	date=""
	try:
		# get from file tag
		with open(path, "rb") as f: image = Image(f); date=image.datetime_original
	except:
		# if exif is empty, get from file properties
		timestamp=os.path.getctime(path)
		date = datetime.fromtimestamp(timestamp).strftime ('%Y:%m:%d %H:%M:%S')
		date=str(date)
	date=date.replace (":", "")
	date=date.replace (" ", "-")
	return date

def stringToFileName (param):
	param=param.strip ()
	param=re.sub(' +', ' ', param)
	not_valid='\/:*"<>|?'
	for i in not_valid: param=param.replace (i, "_")
	return param[0:255]

def getImageDescription (path):
	with open(path, "rb") as f: image = Image(f)
	try: desc=image.get ('image_description')
	except: desc=None
	if desc==None: return ""
	desc=str (desc)
	desc=decode (desc)
	return desc

def setImageDescription (path, description):
	with open(path, "rb") as f: image = Image(f)
	description = description.replace('\n', ' ').replace('\r', ' ')
	b = description.encode('utf-8', errors='ignore')
	b=str (b)
	image.image_description=b
	with open (path, 'wb') as f: f.write(image.get_file())

def delImageDescription (path):
	with open(path, "rb") as f:
		image = Image(f)
		try: image.delete ('image_description')
		except: pass
	with open (path, 'wb') as f: f.write(image.get_file())

def get_config_path():
	"""Return user config path.
	Windows = %AppData% + app_name
	Linux   = ~/.config + app_name
	"""
	if os.name == 'nt':
		path = os.getenv('APPDATA')
	else:
		path = os.path.join(os.path.expanduser('~'), '.config')
	return os.path.join(path, "imageviewer".lower())
