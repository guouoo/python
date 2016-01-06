import datetime;
weekDay = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
monthDay = [31,28,31,30,31,30,31,31,30,31,30,31]
month=[1,2,3,4,5,6,7,8,9,10,11,12]
for m in range (0,2):
    for d in range(1,monthDay[m]+1):
        week = int(datetime.datetime(2015,m+1,d).strftime('%w'))
        print('2015-%02d-%02d'%(m+1,d),'is',weekDay[week],'\t',end=' ')

