# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
df = pd.read_csv(os.getcwd()+os.sep+'/Desktop/subway.csv')
list(df.route)[-1].split('\xe2\x80\x94\xe2\x80\x94')

#===============得到相邻站台===================
allStations = []
for i in list(df.route):
    allStations.append(i.split('\xe2\x80\x94\xe2\x80\x94'))
df2 = pd.DataFrame(allStations)
#================得到相邻站台及间距==================

df3  = pd.concat([df2,df],axis = 1)
del df3['route']
#==============站台名及其索引的映射====================
allStations = []
for i in list(df.route):
    allStations.extend(i.split('\xe2\x80\x94\xe2\x80\x94'))
dic1 = {}
dic2 = {}
allStations = list(set(allStations))
for i, station in enumerate(allStations):
    dic1[i] = station
    dic2[station] = i + 1
graph  = pd.DataFrame(columns=range(1,len(allStations)+1),\
            index = range(1,len(allStations)+1),data = np.Inf)
#================站台名及其索引的映射==================
chufa = map(lambda x:dic2[x],list(df3[0]))
daoda = map(lambda x:dic2[x],list(df3[1]))
dis = list(df3['dis'])
#================除去重复边==================
dfw = pd.DataFrame([chufa,daoda,dis]).T
dfw = dfw.sort_values(2)
dfw = dfw.drop(list(dfw[dfw[[0,1]].duplicated()].index))
chufa = list(dfw[0])
daoda = list(dfw[1])
dis = list(dfw[2])

#==========================================
#with open(os.getcwd()+os.sep+'sub.txt','wb') as f:
#    f.write('s=[')
#    for i in chufa:
#        f.write('{:.2f}'.format(i))
#        f.write(',')
#    f.write('];')
#    f.write('\n')
#    f.write('t=[')
#    for i in daoda:
#        f.write('{:.2f}'.format(i))
#        f.write(',')
#    f.write('];')
#    f.write('\n')
#    f.write('weights=[')
#    for i in dis:
#        f.write('{:.2f}'.format(i))
#        f.write(',')
#    f.write('];')

#===============距离矩阵========================
for i in range(len(dis)):
    from_ =  chufa[i]
    to_ = daoda[i]
    dis_ = dis[i]
    graph.ix[from_,to_] = dis_
    graph.ix[to_,from_] = dis_
    graph.ix[i,i] = 0
#graph.to_excel(os.getcwd()+os.sep+'dis.xlsx')















