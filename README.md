# Attendance ENSAF
This is an application that controls attendance of students using fingerprint, and a part of my Last Year's Project PFA (2020).
(This is a beta version, dedicated just to the National School of Applied Sciences of Fez, Morocco, 2019-2020 Embedded Systems stream 4th year. I will try to universalize it in the future.)

The application is divided into 3 main parts:
- Hardware.
- Server.
- Android Application.

## Hardware
Based on a Raspberry Pi 3 with Raspbian OS alongside the following components:
- FMP10A Fingerprint Sensor.
- 16x02 LCD.

The fingerprint sensor is connected to the Raspberry Pi with the TTL-to-USB connector. Since it is a 3.3V module, we will have it power on from the 3.3V pin and not from the 5V pin of TTL-to-USB cable.
