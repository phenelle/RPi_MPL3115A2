# **************************************************************************
#
#  @file     MPL3115A2.py
#  @author   P. Henelle (Cubitux)
#  @license  BSD (see license.txt)
#
#  A port of the excelent Adafruit_MPL3115A2_Library made by K.Townsend,
#  written in python, for all Raspberry Pi users. 
#  (The original Adafruit library is C++ for Arduino)
#
#  This code is also inspired of the python code (MPL3115A2) from 
#  ControlEverythingCommunity
#
#  @section  HISTORY
#  v1.0 - Initial commit
#
# **************************************************************************

from __future__ import division
import smbus
import time

# Delay between calls (200ms)
SLEEP = 1 / 5

# I2C Bus Identifier (Default: 1)
I2C_BUS_ID = 1

######################
# Various registers  #
######################

# Device Address
MPL3115A2_ADDRESS= 0x60

# Device Identifier (int 196)
MPL3115A2_WHOAMI = 0x0C


MPL3115A2_CTRL_REG1 = 0x26
MPL3115A2_CTRL_REG1_SBYB = 0x01
MPL3115A2_CTRL_REG1_OS128 = 0x38
MPL3115A2_CTRL_REG1_ALT = 0x80
MPL3115A2_CTRL_REG1_BAR = 0x00

MPL3115A2_PT_DATA_CFG = 0x13
MPL3115A2_PT_DATA_CFG_TDEFE = 0x01
MPL3115A2_PT_DATA_CFG_PDEFE = 0x02
MPL3115A2_PT_DATA_CFG_DREM = 0x04

MPL3115A2_REGISTER_STATUS_TDR = 0x02
MPL3115A2_REGISTER_PRESSURE_MSB = 0x01
MPL3115A2_REGISTER_TEMP_MSB = 0x04


# Get I2C bus
bus = smbus.SMBus(I2C_BUS_ID)

# Check device identifier (also check that the wire are correctly plugged)
whoami = bus.read_i2c_block_data(MPL3115A2_ADDRESS, MPL3115A2_WHOAMI, 1)
if (whoami[0] != 196):
	exit("Not Adafruit_MPL3115A2")

# Initialize device capabilities 
bus.write_byte_data(MPL3115A2_ADDRESS, MPL3115A2_CTRL_REG1, MPL3115A2_CTRL_REG1_SBYB | MPL3115A2_CTRL_REG1_OS128 | MPL3115A2_CTRL_REG1_ALT)

# Delay
time.sleep(SLEEP)

# Initialize device capabilities 
bus.write_byte_data(MPL3115A2_ADDRESS, MPL3115A2_PT_DATA_CFG, MPL3115A2_PT_DATA_CFG_TDEFE | MPL3115A2_PT_DATA_CFG_PDEFE | MPL3115A2_PT_DATA_CFG_DREM)

# Delay
time.sleep(SLEEP)

###############
# TEMPERATURE #
###############

# Read 2 bytes from MPL3115A2_ADDRESS at MPL3115A2_REGISTER_TEMP_MSB (temperature sensor)
data = bus.read_i2c_block_data(MPL3115A2_ADDRESS, MPL3115A2_REGISTER_TEMP_MSB, 2)
#print data 		# Debug output


temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
cTemp = temp / 16.0
fTemp = cTemp * 1.8 + 32
print "Temperature in Celsius  : %.2f C" %cTemp
print "Temperature in Fahrenheit  : %.2f F" %fTemp



############
# ALTITUDE #
############

# Prepare sensor to read atmospheric pressure
bus.write_byte_data(MPL3115A2_ADDRESS, MPL3115A2_CTRL_REG1, MPL3115A2_CTRL_REG1_SBYB | MPL3115A2_CTRL_REG1_OS128 | MPL3115A2_CTRL_REG1_BAR)

# Delay
time.sleep(SLEEP)

# Reads 3 bytes from MPL3115A2_ADDRESS at MPL3115A2_REGISTER_PRESSURE_MSB (atmospheric sensor)
data = bus.read_i2c_block_data(MPL3115A2_ADDRESS, MPL3115A2_REGISTER_PRESSURE_MSB, 3)
#print data 		# Debug output

# Original ControlEverythingCommunity convertion to 20 bits
# tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16   
# @See https://forums.adafruit.com/viewtopic.php?f=8&t=123890&p=618560

# Somehow, this calculation gives better result than the code of ControlEverythingCommunity that tells my altitude is 60km
# Best would be to exact bitshift on 20bits, like the Adafruit Lbirary does... 
# (but it's midnight and those <== / != / >== operators hurts my head off...)
tHeight = (((data[0] * 256) + (data[1] * 16) + (data[2])) & 0xF0) / 16
altitude = tHeight / 16.0
print "Altitude : %.2f m" %altitude

# Delay
time.sleep(SLEEP)



###########
# PRESURE #
###########

# Reads 4 bytes from MPL3115A2_ADDRESS at MPL3115A2_CTRL_REG1_BAR
data = bus.read_i2c_block_data(MPL3115A2_ADDRESS, MPL3115A2_CTRL_REG1_BAR, 4)

# Convert the data to 20-bits
pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
pressure = (pres / 4.0) / 1000.0
print "Pressure : %.2f kPa" %pressure
