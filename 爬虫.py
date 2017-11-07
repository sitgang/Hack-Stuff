# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import pandas as pd

l = []

for i in range(1,400):
    #print 'http://tieba.baidu.com/sign/index?kw=%CB%CE%DC%E7&type=3&pn={}'.format(i)
    
    m = urllib2.urlopen('http://tieba.baidu.com/sign/index?kw=%CB%CE%DC%E7&type=3&pn={}'.format(i)).read()
    
    soup = BeautifulSoup(m, 'html.parser', from_encoding='utf-8')
    
    for tr in soup.findAll('tr'):
        for td in tr.findAll('td'):
            l.append(td.get_text())



def div_list(ls,n): 
    '''均分列表''' 
    if not isinstance(ls,list) or not isinstance(n,int):  
        return []  
    ls_len = len(ls)  
    if n<=0 or 0==ls_len:  
        return []  
    if n > ls_len:  
        return []  
    elif n == ls_len:  
        return [[i] for i in ls]  
    else:  
        j = ls_len/n  
        k = ls_len%n  
        ### j,j,j,...(前面有n-1个j),j+k  
        #步长j,次数n-1  
        ls_return = []  
        for i in xrange(0,(n-1)*j,j):  
            ls_return.append(ls[i:i+j])  
        #算上末尾的j+k  
        ls_return.append(ls[(n-1)*j:])  
        return ls_return  
        
         
          
           
m = div_list(l,len(l)/6)
df = pd.DataFrame(m) 
df.set_index(0)
df.to_excel('/Users/xuegeng/Desktop/stat.xlsx')
