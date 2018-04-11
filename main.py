import temperature
import mail
import ConfigParser


if __name__ == "__main__":
    cf = ConfigParser.ConfigParser()
    cf.read("config.private")
    threshold = cf.getint("alert", "threshold")
    eml = mail.Mail()
    temp = temperature.Temperature()
    while True:
        flag, t, h = temp.check()
        if flag and  t >= threshold:
            eml.sendEmail(t)
         
               
	
    #temp.check()
    #eml.sendEmail("nihao")
