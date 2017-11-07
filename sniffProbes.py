#import logging
#logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import pcapy
interface = 'en0'
probeReq = []
def sniffProbe(p):
	if p.haslayer(Dot11ProbeReq):
		netName = p.getlayer(Dot11ProbeReq).info
		if netName not in probeReqs:
			probeReqs.append(netName)
			print "[+] Detected New Probe Request: " + netName

sniff(iface = interface,prn = sniffProbe)
