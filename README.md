# Attendance ENSAF
This is an application that controls attendance of students using fingerprint, and a part of my Last Year's Project PFA (2020).
(This is a beta version, dedicated just to the National School of Applied Sciences of Fez, Morocco, 2019-2020 Embedded Systems stream 4th year. I will try to universalize it in the future)

The application is divided into 3 main parts:
- Hardware.
- Server.
- Android Application.

## Hardware
Packages to install:
```Linux
$ sudo apt-get update && sudo apt-get upgrade
$ sudo raspi-config
  (Interfacing Options --> I2C --> Enable)
$ sudo apt-get install python3 i2c-tools python-smbus
$ pip3 install termcolor pyfingerprint RPi.GPIO mysql-connector-python
```
Based on a **Raspberry Pi 3, Raspbian OS, and Python3** alongside the following components:

### FMP10A Fingerprint Sensor:
The fingerprint sensor is connected to the Raspberry Pi with the **TTL-to-USB** connector. Since it is a **3.3V** module, we will have it power on from the 3.3V pin and **NOT** from the 5V pin of TTL-to-USB cable.

<p align="center">
<img src="img/img01.png" width="700">
</p>

### 16x02 LCD I2C:

<p align="center">
<img src="img/img02.png" height="400">
</p>

After connecting the LCD, one of the following command gives the **i2c address** *(0x27 generally)* and **the i2c bus** *(1 generally)*:
```Linux
$ i2cdetect -y 0
$ i2cdetect -y 1
```
The one that contains the address is the i2c bus.
We will use the code provided by [circuitbasics](https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/) found in `3rd_parties/lcd_i2c_driver.py`. **Edit the i2c address `ADDRESS` and i2c bus `I2CBUS` in the code and copy it to the python libraries**:
```Linux
$ sudo cp -r 3rd_parties/lcd_i2c_driver.py /usr/lib/python3.*
```
### 2 Leds (Red and Green) with resistors and an active buzzer:
Red Led is connected to **GPIO 23** *(Pin 16)*.
Green Led is connected to **GPIO 18** *(Pin 12)*.
Buzzer is connected to **GPIO 22** *(Pin 15)*.

<p align="center">
<img src="img/img03.png" height="400">
</p>

At the end of the hardware part, we will create a cron job to execute the script automatically *(may prompt to select preferred editor in first use)* :
```Linux
$ crontab -e
```
Add the following line at the end of the file *(replace `python3` and path to `Main_Program.py` if different)*:
```Linux
30 8,10,14,16 * 9-5 1-6 /usr/bin/python3 /home/pi/Projects/attendance/hardware/Main_Program.py
```
The script will be executed from **September to May, From Monday to Saturday, at *08:30*, *10:30*, *14:30*, *16:30*** and will be ignored if there is no class at the given time. 
