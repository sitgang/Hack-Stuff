# -*- coding: utf-8 -*-
import urllib2,json,requests
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import Fore 
def getLocation(la,lo):  
    #发送http请求获取具体位置信息  
    #import urllib  
    url = 'http://api.map.baidu.com/geocoder/v2/'  
    ak = 'ak=1aZ2PQG7OXlk9E41QPvB9WjEgq5WO8Do'  
    back='&location='  
    location=str(la) + ',' + str(lo)  
    output = '&output=json&pois=0'  
    url = url + '?' + ak + back + location + output  
  
    temp = urllib2.urlopen(url) 
    #temp = requests.post(url)
    hjson = json.loads(temp.read())  
    locate = hjson["result"]["formatted_address"] #省，市，县  
    mapinfo = hjson["result"]["sematic_description"]  #详细描述  
    return " ".join([locate.encode('utf8') , mapinfo.encode('utf8')])
   
#loc = getLocation(39.90,116.5)
#print loc

def testForExif(imgFileName):
    
    """to get the exif information"""
    
    try:
	exifData = {}
	imgFile = Image.open(imgFileName)
	info = imgFile._getexif()
	if info:
	    la = info[34853][2][0][0] + info[34853][2][1][0] / 60.0 + info[34853][2][2][0] / 360000.0
	    lo = info[34853][4][0][0] + info[34853][4][1][0] / 60.0 + info[34853][4][2][0] / 360000.0
	    for (tag,value) in info.items():
		decoded = TAGS.get(tag,tag)
		exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print u" ".join([Fore.RED,"[+] ",imgFileName,Fore.GREEN," located at"])
                print getLocation(la,lo)

    except :
	pass


def printLoc(string):
    l = string.split(' ')
    la = eval(l[0]) + eval(l[2][:-1]) / 60.0 + eval(l[3][:-1])/ 3600.0
    lo = eval(l[5]) + eval(l[7][:-1]) / 60.0 + eval(l[8][:-1])/ 3600.0
    print la,lo
    print getLocation(la,lo)
    
#testForExif(u'/Users/xuegeng/Downloads/IMG_5950.JPG')
#use exif-tool in command line in macOS with the path of a gif or pic, you can get
#a GPS location. Then using this script, one can obtain other's location.

#printLoc('''39 deg 56' 0.60" N, 116 deg 27' 54.00" E''')#gigi辜辜健身房




