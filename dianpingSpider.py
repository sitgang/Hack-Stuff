# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import optparse,os
import pandas as pd
import time



head1 = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'_hc.v=1ab2c409-dc29-f1a5-e08d-9c6e2689a281.1480398303; __utma=1.1563952025.1480398303.1480398303.1480398303.1; __utmz=1.1480398303.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID=C4AA416773586D3C4FE08E52ED5E48DA; aburl=1; cy=2; cye=beijing',
        'Host':'www.dianping.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
head2 = {"Remote Address":'103.18.208.171:80',
        'Request Method':'GET',
        'Status Code':'200 OK (from cache)',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.4.2000 Chrome/39.0.2146.0 Safari/537.36',}
head3 = {"accept":"*/*",
        "accept-encoding":"gzip, deflate, sdch",
        "accept-language":"zh-CN,zh;q=0.8",
        "cache-control":"max-age=0",
        "if-modified-since":"Tue, 17 May 2016 05:52:11 GMT",
        "referer":"https://www.baidu.com/s?wd=%E5%BE%AE%E4%BF%A1%E7%BD%91%E9%A1%B5%E7%89%88&rsv_spt=1&rsv_iqid=0xc9cb40200001e0fd&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=1&rsv_sug1=1&rsv_sug7=001",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
recordList = []
headList = [head1]#,head2,head3]
HEADNUM = len(headList)
HEADTURN = 50

def gethtml(url, headers):
    html = requests.get(url, headers = headers)
    html.encoding = 'utf-8'
    return html.text

def html2df(url,head):
    html = gethtml(url, head )
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    try:
        sa = soup.find(class_ = "comment-list").find('ul')
    except AttributeError:
        print("[-] Page Content Error")
        return False
    lis = sa.findAll('li')
        
    #count = 0
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
        try:
            tit = content.find(class_ = "tit")
            p = tit.parent
            shopReplyComment = p.getText()[6:]
        except AttributeError:
            shopReplyComment = ''
        
        name = pic.find(class_ = 'name').get_text()
        rank = ranks.attrs['class'][1][8:-1]
        try:
            tasteRank = oranks[0].getText()[2]
            envRank = oranks[1].getText()[2]
            servRank = oranks[2].getText()[2]
        except IndexError:
            print("[-] Missed One Comment")
            continue
        
        comment = content.find(class_="J_brief-cont").getText()
        commentTime= content.find(class_="time").getText()
        if len(commentTime)>5:
            commentTime = commentTime[:5]
        
        dict_ = {'name': name,'rank':int(rank),'tasteRank':int(tasteRank),'envRank':int(envRank),
                'servRank':int(servRank),'comment':comment,'commentTime':commentTime,
                'shopReplyComment':shopReplyComment}
        
        recordList.append(dict_)
        return True


def main():  
    parser = optparse.OptionParser('usage %prog -N'+\
        '<shop id> -p <pages>')
    parser.add_option('-N',dest='shopId',type='string',\
        help='specify shop id')
    parser.add_option('-p',dest='pages',type='int',\
        help='specify pages to crawl')
    (options,args) = parser.parse_args()
    shopId = options.shopId
    pages = options.pages
    if (pages ==None) | (shopId == None):
        print('[-] You must specify a shop id and pages to crawl.')
        exit(0)
  
    url = 'http://www.dianping.com/shop/' + shopId + '/review_all?pageno=%d'
    head = head1
    listId = 0
    urls = [url%i for i in range(pages)]
    for index , url in enumerate(urls):
        
        i = (index/HEADTURN)%HEADNUM
        if index%HEADTURN == HEADTURN - 1:
            print("[:|] Let me rest for a while")
            listId = i
            head = headList[listId]
            time.sleep(10)
        
        result = html2df(url,head)
        if result:
            print("[+] Page %d saved..."%(index+1))
    df = pd.DataFrame(recordList) 
    df = df.drop_duplicates()
    df['comment'] = df['comment'].apply(lambda x:x.strip(' ').strip('\n').strip(' ').strip('\t'))
    filename = os.getcwd() + os.sep + 'DianpingShop%s.xlsx'%shopId
    if os.path.exists(filename):
        os.remove(filename)
    df.to_excel(filename)
    print("[:)] Complete !")
    print("[!] Saved to %s"%filename)

if __name__  == '__main__':
    main()
