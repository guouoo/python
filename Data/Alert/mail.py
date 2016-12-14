#! /usr/bin/env python

import smtplib
from email.mime.text import MIMEText
mailto_list=['taff.guo@morningstar.com']           #收件人(列表)
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址
mail_user="guouoo"                           #用户名
mail_pass="ggjj.66199916"                             #密码
mail_postfix="163.com"                     #邮箱的后缀
def send_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print (str(e))
        return False

for i in range(2):                             #发送五封，不过会被拦截的。。。
    if send_mail(mailto_list,"hello","haha!"):  #邮件主题和邮件内容
        print ("done!")
    else:
        print ("failed!")