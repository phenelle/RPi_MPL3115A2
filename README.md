RPi_MPL3115A2
==

A simple port of the Adafruit MPL3115A2 barometric/altitude pressure sensor to the RPi

This code is based on both https://github.com/ControlEverythingCommunity/MPL3115A2/ and https://raw.githubusercontent.com/adafruit/Adafruit_MPL3115A2_Library

**Note: The code is not complete. Feel free to use, modify, and pull update**

Example
==
![MPL3115A2_raspberry](https://www.cubitux.ca/img/github/MPL3115A2_raspberry.jpg)

Setup
==

## Wiring to the Pi

Adafruit MPL3115A2 uses I2C to communicate with the Pi.

| Rpi Pin              | MPL3115A2     |
| -------------------- | ------------- |
| PIN #1 (3.3v)        | 3V            |
| PIN #3 (SDA1 / I2C)  | SDA           |
| PIN #3 (SDL1 / I2C)  | SDL           |
| PIN #6 (GND)         | GND           |

I have attached picture of the wiring
![wiring_MPL3115A2_raspberry](https://www.cubitux.ca/img/github/wiring_MPL3115A2_raspberry.jpg)


## Enable I2C on your Raspberry Pi

Basically, all your have to do is enable I2C communication.

### Step1
Log in to your pi, and run:
```{r, engine='bash', raspi-config}
sudo raspi-config
```
### Step2

Navigate to the "Interfacing Options"

![Interfacing Options](https://www.cubitux.ca/img/github/step1.jpg)



### Step3
Choose "I2C"

![I2C](https://www.cubitux.ca/img/github/step2.jpg)



### Step4
Enable "I2C"

![Enable I2C](https://www.cubitux.ca/img/github/step3.jpg)



### Step5
Reboot
```{r, engine='bash', raspi-config}
sudo reboot
```





## Execute RPi_MPL3115A2
Login to the Pi, and execute the following:
```{r, engine='bash', raspi-config}
sudo apt-get install git python-smbus 
git clone https://github.com/phenelle/RPi_MPL3115A2
cd RPi_MPL3115A2
python RPi_MPL3115A2.py
```
![MPL3115A2_raspberry](https://www.cubitux.ca/img/github/MPL3115A2_raspberry.jpg)
