import requests
from bs4 import BeautifulSoup
import urllib2,optparse
import pandas as pd

def gethtml(url, headers):
    html = requests.get(url, headers = headers)
    html.encoding = 'utf-8'
    return html.text

head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'_hc.v=1ab2c409-dc29-f1a5-e08d-9c6e2689a281.1480398303; __utma=1.1563952025.1480398303.1480398303.1480398303.1; __utmz=1.1480398303.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID=C4AA416773586D3C4FE08E52ED5E48DA; aburl=1; cy=2; cye=beijing',
        'Host':'www.dianping.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}



recordList = []

def html2df(url= 'http://www.dianping.com/shop/6232395/review_all?pageno=1'):
    global recordList
    html = gethtml(url, head)
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    sa = soup.find(class_ = "comment-list").find('ul')
    lis = sa.findAll('li')
    
    
    count = 0
    for li in lis:
    
        pic = li.find(class_ = 'pic')
        content = li.find(class_ = 'content')
        
        try:
            name = pic.find(class_ = 'name').get_text()
        except AttributeError:
            continue 

        ranks = content.find('span')
        orank = content.find(class_ = 'user-info')
        oranks = orank.findAll(class_ = 'rst')
        
        name = pic.find(class_ = 'name').get_text()
        rank = ranks.attrs['class'][1][8:-1]
        tasteRank = oranks[0].getText()[2]
        envRank = oranks[1].getText()[2]
        servRank = oranks[2].getText()[2]
        comment = content.find(class_="J_brief-cont").getText()
        commentTime= content.find(class_="time").getText()
        
        dict_ = {'name': name,'rank':int(rank),'tasteRank':int(tasteRank),'envRank':int(envRank),
                'servRank':int(servRank),'comment':comment,'commentTime':commentTime}
        for value in dict_.values():
            print value
        count += 1
        #print "count ==> " + str(count)
        recordList.append(dict_)

if __name__  == '__main__':
    
    parser = optparse.OptionParser('usage %prog -N'+\
        '<shop id> -p <pages>')
    parser.add_option('-N',dest='shopId',type='string',\
        help='specify shop id')
    parser.add_option('-p',dest='pages',type='int',\
        help='specify pages to crawl')
    (options,args) = parser.parse_args()
    shopId = options.shopId
    pages = int(options.pages)
    if (pages ==None) | (shopId == None):
        print '[-] You must specify a target host and port[s].'
        exit(0)
    print shopId , type(shopId)
    print pages, type(pages)
    
    #url = 'http://www.dianping.com/shop/6232395/review_all?pageno=%d'
    #urls = [url%i for i in range(3)]
    #for url in urls:
    #    html2df(url)
    #df = pd.DataFrame(recordList) 
    #df.set_index(0)
    #df.to_excel('/Users/xuegeng/Desktop/sasat.xx')
