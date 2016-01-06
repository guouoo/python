"""
print(2,end=' ')
for n in range(3,1000,2):
    b='true'
    for m in range(3,int(n**0.5)+1):
        #print (str(n)+'%'+ str(m)+'='+str(n%m))
        if n%m == 0:
            b='false'
            break
    if b=='true': print(n,end=' ')
"""
#print ([2]+(lambda n,s=set():[i for i in range(3,n+1,2) if ([j for j in range(i*3,n+1,i*2) if s.add(j)] or i not in s)])(1000))


maxNum=1000

numList =[]

for i in range (1, maxNum+1):
    numList.append ('false')

for a in range(2,int(maxNum**0.5)+1):
    n=a
    for n in range(n,maxNum+1,n):
        if n%a==0 and numList[n-1] == 'false' and n>a   :
                numList[n-1]='true'
              
   
for i in range (1, maxNum-1):
    if numList[i] =='false':
        print(i+1,end=', ')

   
"""
def allPrime(maxNum):
    aList = [x for x in range(0,maxNum)]
    prime = []
    for i in range(2,len(aList)):
        if aList[i] != 0:
            prime.append(aList[i])
            clear(aList[i],aList,maxNum)
    print (prime)     
 
def clear(aPrime,aList,maxNum):
    for i in range(2,int((maxNum/aPrime)+1)):
        if not aPrime*i>maxNum-1:
            aList[i*aPrime]=0
 
allPrime(1000)
"""
