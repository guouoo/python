# coding=UTF-8
# Created by GuoJun

import time
import os
import random
import re

class OperationList:
    def clist(self,clist):
        self.clist = clist
    def rlist(self,rlist):
        self.rlist =  rlist
    def path(self,path):
        self.path =  path

def pathverify():
    running = True
    while running:
        temppath = input("请输入要修改的文件夹目录(例如 d:\pictures)，然后回车: ")
        if len(temppath) <= 3:
            print('路径（'+ str(temppath) + "）不正确，请重新输入")

        elif os.path.isdir(temppath) == False:
            print('路径（'+ str(temppath) + "）不存在，请重新输入")

        elif any(re.findall('Program Files|program files|Windows|windows|Users|users', temppath)) == True:
            print('路径（'+ str(temppath) + "）非法，请重新输入")

        elif any(re.findall('reverse|Reverse|REVERSE', temppath)) == True:
            reverse()
            running = False
            operationlist.path=[]
        else:
            operationlist.path = temppath
            running = False

def confirm():
    running = True
    while running:
        if any(operationlist.path) == False:
            print('Done!')
            running =False
            break
        yesno = input('您确定要将文件夹目录(' + operationlist.path +')下的所有文件名改为时间戳吗？（y/n) ')
        if (yesno == 'n' or yesno == 'N' or yesno == 'no' or yesno == 'NO' or yesno == 'No'):
            print('任务终止。')
            running = False
        elif len(yesno) > 1 and  (yesno != 'yes' and yesno != 'YES'  and yesno != 'Yes') :
            print('输入不正确，请重新输入')
        else:
            print('开始修改文件名...')
            getlist(operationlist.path)
            changename(operationlist.clist)
            running = False

def getlist(path):
    changelist = {}
    reversedlist = {}
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            filelist = os.path.join(parent,filename)
            filetypetemp = filelist.split('.')
            filetype = filetypetemp[-1]
            statinfo=os.stat(filelist)
            timestamp = min(statinfo.st_mtime,statinfo.st_ctime)
            newname = str(time.strftime('%Y-%m-%d %H%M%S_',time.localtime(timestamp)))  +str(random.randint(100, 999))+' .' + filetype
            newfilelist = os.path.join(parent,newname)
            changelist[filelist] = newfilelist
            reversedlist[newfilelist]=filelist
            operationlist.clist = changelist
            operationlist.rlist = reversedlist

def changename(list):
    changelist = list
    if not os.path.isdir('Log'):
        os.makedirs('Log')
    if not os.path.isdir('Reverse'):
        os.makedirs('Reverse')
    filename  = 'Log/' + str(time.strftime("%Y%m%d %H%M%S",time.localtime(time.time()))) + '.txt'
    f = open(filename, 'w')
    for i in changelist:
        os.rename(i,changelist[i])
        print(str(i) + '  >>>  ' + str(changelist[i]))
        f.write(str(i) + '  >>>  ' + str(changelist[i]) + '\n')
    f.close()
    print('...完成！')

def reverse():
    reverselist = {}
    filelist = os.listdir(r'./Reverse/')
    filelist.sort(reverse=True)
    for filename in filelist:
        f = open('./Reverse/'+filename, mode='r')
        content = f.readlines()
        for i in content:
            valuename = re.match(r'^.*?.>>>',i).group(0).replace('  >>>','')
            listname = re.search(r'>>>.*',i).group(0).replace('>>>  ','').strip()
            reverselist[listname] = valuename
        f.close()
        os.remove('./Reverse/'+filename)

    filename  = 'Log/R_' + str(time.strftime("%Y%m%d %H%M%S",time.localtime(time.time()))) + '.txt'
    f = open(filename, 'w')
    for i in reverselist:
        os.rename(i,reverselist[i])
        print(str(i) + '  >>>  ' + str(reverselist[i]))
        f.write(str(i) + '  >>>  ' + str(reverselist[i]) + '\n')
    f.close()

if __name__ == "__main__":
    operationlist = OperationList()
    pathverify()
    confirm()