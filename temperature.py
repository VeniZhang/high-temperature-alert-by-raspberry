# code from the Internet
import ConfigParser
import logging
import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("record")

import RPi.GPIO as GPIO
import time
class Temperature():
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("config.private")
        self.interval = self.cf.getint("temperature", "interval")

    def check(self):
        channel = 4
        data = []
        j = 0
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(channel, GPIO.HIGH)
        GPIO.setup(channel, GPIO.IN)
        while GPIO.input(channel) == GPIO.LOW:
            continue
        while GPIO.input(channel) == GPIO.HIGH:
            continue
        while j < 40:
            k = 0
            while GPIO.input(channel) == GPIO.LOW:
                continue
            while GPIO.input(channel) == GPIO.HIGH:
                k +=1

                if k > 100:
                    break
            if k < 8: 
                data.append(0)
            else:
                data.append(1) 
            j += 1

        GPIO.cleanup()
        time.sleep(self.interval)

        print "sensor is working "
        print data
        logger.info("data is %s " % data)
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0 
        temperature_point = 0
        check = 0
        for i in range(8):
            humidity += humidity_bit[i] * 2 ** (7-i)
            humidity_point += humidity_point_bit[i] * 2 ** (7-i)
            temperature += temperature_bit[i] * 2 ** (7-i)
            temperature_point += temperature_point_bit[i] * 2 ** (7-i)
            check += check_bit[i] * 2 ** (7-i)
        tmp = humidity + humidity_point + temperature + temperature_point
        if check == tmp :
            logger.info("True temperature: %s *C humidity: %s", temperature,  humidity)
            return True, temperature, humidity
        else:
            logger.info("False temperature: %s *C humidity: %s", temperature,  humidity)
            return False, temperature, humidity

if __name__ == "__main__":
    temp = Temperature()
    while True:
        temp.check()
        print "next"
