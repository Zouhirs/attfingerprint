# Attendance ENSAF
This is an application that controls attendance of students using fingerprint, and a part of my Last Year's Project PFA (2020).
(This is a beta version, dedicated just to the National School of Applied Sciences of Fez, Morocco, 2019-2020 Embedded Systems stream 4th year. I will try to universalize it in the future)

Packages to install:
```Linux
$ sudo apt-get update && sudo apt-get upgrade
$ sudo raspi-config
  (Interfacing Options --> I2C --> Enable)
$ sudo apt-get install i2c-tools python-smbus
$ sudo apt-get install python3
$ pip3 install termcolor
$ pip3 install pyfingerprint
```

The application is divided into 3 main parts:
- Hardware.
- Server.
- Android Application.

## Hardware
Based on a Raspberry Pi 3 with Raspbian OS alongside the following components:

### FMP10A Fingerprint Sensor:
The fingerprint sensor is connected to the Raspberry Pi with the TTL-to-USB connector. Since it is a 3.3V module, we will have it power on from the 3.3V pin and not from the 5V pin of TTL-to-USB cable.
<p align="center">
<img src="img/img01.png" width="700">
</p>

### 16x02 LCD I2C:
<p align="center">
<img src="img/img02.png" width="700">
</p>
After connecting the LCD, use one of the following command to find i2c address (0x27 generally) and i2c bus (1 generally):
```Linux
$ i2cdetect -y 0
$ i2cdetect -y 1
```
The one that contains the address is the i2c bus.
We will use the code provided by [circuitbasics](https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/) found in `3rd_parties/lcd_i2c_driver.py`. Edit the i2c address and i2c bus and copy it to the python libraries:
```Linux
$ sudo cp -r 3rd_parties/lcd_i2c_driver.py /usr/lib/python3.*
```
