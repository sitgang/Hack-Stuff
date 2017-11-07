import pygeoip
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')
def printRecord(tgt):
	rec = gi.record_by_name(tgt)
	print rec.keys()
	city = rec['city']
	region = rec['region_code']
	country = rec['country_name']
	long_ = rec['longitude']
	lat = rec['latitude']
	print "[*] Target: " + tgt + " Geo-located. "
	print "[+] " + str(city) + ", " + str(region) + ", " + str(country)
	print "[+] Latitude: " + str(lat) + ", " + str(long_)
#tgt = '173.255.226.98'
#tgt = '192.168.1.101'
tgt = '220.160.166.131'

printRecord(tgt)