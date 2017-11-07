# -*- coding: utf-8 -*-
import urllib2,optparse,json,os
from urlparse import urlsplit
from os.path import basename,isfile
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import Fore
def findImages(url):
    
    """find all the source url in a certain page"""
    
    print "[+] Finding images on " + url
    urlContent = urllib2.urlopen(url).read()
    soup = BeautifulSoup(urlContent)
    imgTags = soup.findAll('img')
    return imgTags

def downloadImage(imgTag):
    
    """download a pic to current folder"""
    
    try:
        print "[+] Downloading image..."
	imgSrc = imgTag['src']
	imgContent = urllib2.urlopen(imgSrc).read()
	imgFileName = basename(urlsplit(imgSrc)[2])
	imgFile = open(imgFileName,'wb')
	imgFile.write(imgContent)
	imgFile.close()
	return imgFileName
    except:
	return ''
def findImagePaths(folderPath):
    
    """return all the file paths in a folder"""
    allPaths = []
    
    for root,dirs,files in os.walk(folderPath):
        for f in files:
            f = root + os.sep + f
            if isfile(f):
                allPaths.append(f)
    
    return allPaths
    
def testForExif(imgFileName):
    
    """to get the exif information"""
    
    try:
	exifData = {}
	imgFile = Image.open(imgFileName)
	info = imgFile._getexif()
	if info:
	    #la = info[34853][2][0][0] + info[34853][2][1][0] / 60.0 + info[34853][2][2][0] / 360000.0
     #       lo = info[34853][4][0][0] + info[34853][4][1][0] / 60.0 + info[34853][4][2][0] / 360000.0
	    for (tag,value) in info.items():
		decoded = TAGS.get(tag,tag)
		exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print "[+] " + imgFileName +Fore.RED + " has GPS location " #+ Getlocation(la,lo)

    except :
	pass
		
		
def Getlocation(la,lo):  
    
    """发送http请求获取具体位置信息  """
    
    url = 'http://api.map.baidu.com/geocoder/v2/'  
    ak = 'ak=1aZ2PQG7OXlk9E41QPvB9WjEgq5WO8Do'  
    back='&location='  
    location=str(la) + ',' + str(lo)  
    output = '&output=json&pois=0'  
    url = url + '?' + ak + back + location + output  
  
    temp = urllib2.urlopen(url)  
    hjson = json.loads(temp.read())  
    locate = hjson["result"]["formatted_address"] #省，市，县  
    mapinfo = hjson["result"]["sematic_description"]  #详细描述  
    return " ".join([locate.encode('utf8') , mapinfo.encode('utf8')])
    
def main():
	parser = optparse.OptionParser("usage%prog " + "-u <target url> -f <target folder>")
	parser.add_option('-u',dest = 'url',type = 'string',help = 'specify url address')
	parser.add_option('-f',dest = 'folder',type = 'string',help = 'specify folder path')
	(options,args) = parser.parse_args()
	url = options.url
	folder = options.folder
	if not url and not folder :
	    print parser.usage
	    exit(0)
	if url and folder :
	    print parser.usage
	    exit(0)
	if url :
	    imgTags = findImages(url)
	    for imgTag in imgTags:
		imgFileName = downloadImage(imgTag)
		testForExif(imgFileName)
        elif folder :
            imgPaths = findImagePaths(folder)
	    for imgPath in imgPaths:
		testForExif(imgPath)

if __name__ == "__main__":
	main()
