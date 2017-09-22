import uart_lib as u
import serial
import math
import binascii
import random
import time
#import decimal
from decimal import *

from array import array

import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
print sys.argv[1]

port = '/dev/ttyUSB1'
rate = 230400

s = u.ser_open(port, rate)

fpr = open('python_output_log.txt', 'w')
fpr.close()
u.cmd_interpreter(s,sys.argv[1], "100g_address_map.txt")
#u.cmd_interpreter(s,sys.argv[1], "adc_address_map.txt")

print 'Bye'
s.flush()
s.close()             # close port


