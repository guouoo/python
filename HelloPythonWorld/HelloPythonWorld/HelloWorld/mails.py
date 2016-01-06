#! /usr/bin/env python  
import smtplib
from email.mime.text import MIMEText

mailto_list=['guouoo@163.com']        
mail_host="localhost"     
mail_user="guouoo"                         
mail_pass="gj.66199916"                           
mail_postfix="163.com"                   
def send_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='text')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)            
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                       
#         server.login(mail_user,mail_pass)           
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print (str(e))
        return False
for i in range(1):                           
    if send_mail(mailto_list,"hello","haha!"): 
        print ("done!")
    else:
        print ("failed!")
        
# Sending mails failed by socket blocked