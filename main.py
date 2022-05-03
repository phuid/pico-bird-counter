from machine import I2C, Pin
from time import sleep_ms
from DHT22 import DHT22

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
i2c.scan()

import ds1307

ds = ds1307.DS1307(i2c)

dht22 = DHT22(Pin(2,Pin.IN,Pin.PULL_UP),dht11=False)

proximity = Pin(22, Pin.IN)
led = Pin(25, Pin.OUT)

previous = 1 - proximity.value()
counter = 0

while True:
    led.value(0)
    if (1 - proximity.value() > previous):
        dhtdata = None
        dsdata = None
        try:
            dhtdata = dht22.read()
        except Exception as e:
            print(e)
        try:
            dsdata = ds.datetime()
        except Exception as e:
            print(e)
        counter += 1
        f = open("data.csv", "a")
        f.write("{},{},{}".format(counter, dhtdata, dsdata).replace("(", "").replace(")", "").replace(" ", ""))
        #for x in ds.datetime():
        #    f.write("," + str(x))
        f.write("\n")
        f.close()
        print("{},{},{}".format(counter, dhtdata, dsdata).replace("(", "").replace(")", "").replace(" ", ""))
        if dsdata == None or dhtdata == (None,None):
            for x in range(10):
                led.value((x+1) % 2)
                sleep_ms(49)
        else:
            led.value(1)
            sleep_ms(490)
    previous = 1 - proximity.value()
    sleep_ms(5)

