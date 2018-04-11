#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ConfigParser
import logging
import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("runtime")

# 第三方 SMTP 服务
class Mail():
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("config.private")
        self.mail_host = self.cf.get("mail", "mail_host")
        self.mail_user = self.cf.get("mail", "mail_user")
        self.mail_pass = self.cf.get("mail", "mail_pass")
        self.mail_to = self.cf.get("mail", "mail_to").split()
        self.subject = self.cf.get("mail", "subject")

    def sendEmail(self, content):
        message = MIMEText(str(content), 'plain', 'utf-8')
        message['From'] = Header(self.mail_user, 'utf-8')
        message['To'] =  Header("who", 'utf-8')
        message['Subject'] = Header(self.subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect(self.mail_host, 25)    # 25 为 SMTP 端口号
            logger.info("connect success")        
            smtpObj.login(self.mail_user, self.mail_pass)  
            logger.info("login success")
            logger.info(message.as_string())
            smtpObj.sendmail(self.mail_user, self.mail_to, message.as_string())
            logger.info("send success")
        except  Exception, e:
            logger.error("send fail")
            logger.error(e)

if __name__ == "__main__":
    #sendEmail(content="ai")
    mail = Mail()
