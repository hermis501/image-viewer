import base64, urllib.request, urllib.parse, time, json

def cloudvis(filename, lang = "en", target = "all", qr = 0, translate = 0):
	with open(filename, "rb") as f:
		body = base64.b64encode(f.read())
	
	try: r1 = urllib.request.urlopen("https://visionbot.ru/apiv2/in.php", data = urllib.parse.urlencode({
			"body": body,
			"lang": lang,
			"target": target,
			"qr": qr,
			"translate": translate
		}).encode()
	)
	except: return ""
	j1 = json.loads(r1.read())
	r1.close()
	del body
	if j1["status"] != "ok":
		return (j1["status"])
	
	for i in range(1000):
		r2 = urllib.request.urlopen("https://visionbot.ru/apiv2/res.php",
			data = urllib.parse.urlencode({"id": j1["id"]}).encode())
		j2 = json.loads(r2.read())
		r2.close()
		if j2["status"] == "error":
			return(j2["status"])
		
		if j2["status"] == "ok":
			return j2['text']
		
		if j2["status"] == "notready":
			time.sleep(0.2)
			continue
