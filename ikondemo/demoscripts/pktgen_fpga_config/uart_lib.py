import serial
import math
import binascii
import random
import time
#import decimal
from decimal import *

from array import array
def ser_open(port, rate):
    ser = serial.Serial(port, baudrate=rate, timeout=1)  # open serial port
    print(ser.name)
    return ser
    
def header_decode(value):
    rtn_value = ""
    if ord(value) == vhdl_pkg_to_var("CMD_HEADER_MSB"):
      rtn_value = "CMD_HEADER_MSB"
    else:
      if ord(value) == vhdl_pkg_to_var("CMD_HEADER_LSB"):
        rtn_value = "CMD_HEADER_LSB"
      else:
          if ord(value) == vhdl_pkg_to_var("RSP_HEADER_MSB"):
            rtn_value = "RSP_HEADER_MSB"
          else:
            if ord(value) == vhdl_pkg_to_var("RSP_HEADER_LSB"):
              rtn_value = "RSP_HEADER_LSB"
            else:
              rtn_value = str(ord(value))
    return rtn_value

def command_decode_lsb(value):
    rtn_value = ""
    if ord(value) == vhdl_pkg_to_var("CMD_LSB_ERROR_MS"):
      rtn_value = "CMD_LSB_ERROR_MS"
    else:
      if ord(value) == vhdl_pkg_to_var("CMD_LSB_ERROR_DS"):
        rtn_value = "CMD_LSB_ERROR_DS"
      else:
        if ord(value) == vhdl_pkg_to_var("CMD_LSB_ERROR_EB"):
          rtn_value = "CMD_LSB_ERROR_EB"
        else:
          if ord(value) == vhdl_pkg_to_var("CMD_LSB_BLOCK_READ_DATA"):
            rtn_value = "CMD_LSB_BLOCK_READ_DATA"
          else:
            if ord(value) == vhdl_pkg_to_var("CMD_LSB_BLOCK_WRITE_INIT"):
              rtn_value = "CMD_LSB_BLOCK_WRITE_INIT"
            else:
              if ord(value) == vhdl_pkg_to_var("CMD_LSB_TERMINATE_BLOCK_READ"):
                rtn_value = "CMD_LSB_TERMINATE_BLOCK_READ"
              else:
                if ord(value) == vhdl_pkg_to_var("CMD_LSB_TERMINATE_BLOCK_WRITE"):
                  rtn_value = "CMD_LSB_TERMINATE_BLOCK_WRITE"
                else:
                  if ord(value) == vhdl_pkg_to_var("RSP_LSB_ACKR"):
                    rtn_value = "RSP_LSB_ACKR"
                  else:
                    if ord(value) == vhdl_pkg_to_var("CMD_LSB_ACKW"):
                      rtn_value = "CMD_LSB_ACKW"
                    else:
                      if ord(value) == vhdl_pkg_to_var("CMD_LSB_BLOCK_WRITE_DATA"):
                        rtn_value = "CMD_LSB_BLOCK_WRITE_DATA"
                      else:
                        if ord(value) == vhdl_pkg_to_var("CMD_LSB_BLOCK_READ_INIT"):
                          rtn_value = "CMD_LSB_BLOCK_READ_INIT"
                        else:
                          if ord(value) == vhdl_pkg_to_var("CMD_LSB_TERMINATE_WRITE_ACK"):
                            rtn_value = "CMD_LSB_TERMINATE_WRITE_ACK"
                          else:
                            if ord(value) == vhdl_pkg_to_var("RSP_LSB_TERMINATE_WRITE_ACK"):
                              rtn_value = "RSP_LSB_TERMINATE_WRITE_ACK"
                            else:
                              if ord(value) == vhdl_pkg_to_var("RSP_LSB_IERR"):
                                rtn_value = "RSP_LSB_IERR"
                              else:
                                if ord(value) == vhdl_pkg_to_var("RSP_LSB_TERMINATE_BLOCK_READ"):
                                  rtn_value = "RSP_LSB_TERMINATE_BLOCK_READ"
                                else:
                                  if ord(value) == vhdl_pkg_to_var("RSP_LSB_TERMINATE_BLOCK_WRITE"):
                                    rtn_value = "RSP_LSB_TERMINATE_BLOCK_WRITE"
                                  else:
                                    if ord(value) == vhdl_pkg_to_var("RSP_HEADER_LSB"):
                                      rtn_value = "RSP_HEADER_LSB"
                                    else:
                                      if ord(value) == vhdl_pkg_to_var("CMD_LSB_LOAD_TIMESTAMP"):
                                        rtn_value = "CMD_LSB_LOAD_TIMESTAMP"
                                      else:
                                        if ord(value) == vhdl_pkg_to_var("CMD_LSB_READ_TIMESTAMP"):
                                          rtn_value = "CMD_LSB_READ_TIMESTAMP"
                                        else:
                                          if ord(value) == vhdl_pkg_to_var("RSP_LSB_IERR_MS"):
                                            rtn_value = "RSP_LSB_IERR_MS"
                                          else:
                                            if ord(value) == vhdl_pkg_to_var("CMD_LSB_READ_DRP"):
                                              rtn_value = "CMD_LSB_READ_DRP"
                                            else:
                                              if ord(value) == vhdl_pkg_to_var("CMD_LSB_WRITE_DRP"):
                                                rtn_value = "CMD_LSB_WRITE_DRP"
                                              else:
                                                if ord(value) == vhdl_pkg_to_var("CMD_LSB_DRP_DONE"):
                                                  rtn_value = "CMD_LSB_DRP_DONE"
                                                else:
                                                  rtn_value = str(ord(value))
    return rtn_value

def command_decode_msb(value):
    rtn_value = ""
    if ord(value) == vhdl_pkg_to_var("RSP_HEADER_MSB"):
      rtn_value = "RSP_HEADER_MSB"
    else:
      if ord(value) == vhdl_pkg_to_var("CMD_MSB_ERROR"):
        rtn_value = "CMD_MSB_ERROR"
      else:
        if ord(value) == vhdl_pkg_to_var("CMD_MSB_MEMORY"):
          rtn_value = "CMD_MSB_MEMORY"
        else:
          if ord(value) == vhdl_pkg_to_var("CMD_MSB_GLOBAL_CLOCK"):
            rtn_value = "CMD_MSB_GLOBAL_CLOCK"
          else:
            rtn_value = str(ord(value))
    return rtn_value


def packet_decipher(data):
   if len(data) == 16:
     fpr = open('python_output_log.txt', 'a')
     if ord(data[2]) == vhdl_pkg_to_var("CMD_MSB_GLOBAL_CLOCK") and ord(data[3]) == vhdl_pkg_to_var("CMD_LSB_LOAD_TIMESTAMP"):
       fpr.write (header_decode(data[0]) + " " + header_decode(data[1]) + " " + command_decode_msb(data[2]) + " " + "CMD_LSB_LOAD_TIMESTAMP" + " " + str(ord(data[4])) + " " + str(ord(data[5])) + " " + str(ord(data[6])) + " " + str(ord(data[7])) + " " + str(ord(data[8])) + " " + str(ord(data[9])) + " " + str(ord(data[10])) + " " + str(ord(data[11])) + " " + str(ord(data[12])) + " " + str(ord(data[13])) + " " + str(ord(data[14])) + " " + str(ord(data[15])) + " " + "\n")
     else:
       if ord(data[2]) == vhdl_pkg_to_var("CMD_MSB_GLOBAL_CLOCK") and ord(data[3]) == vhdl_pkg_to_var("CMD_LSB_READ_TIMESTAMP"):
         fpr.write (header_decode(data[0]) + " " + header_decode(data[1]) + " " + command_decode_msb(data[2]) + " " + "CMD_LSB_READ_TIMESTAMP" + " " + str(ord(data[4])) + " " + str(ord(data[5])) + " " + str(ord(data[6])) + " " + str(ord(data[7])) + " " + str(ord(data[8])) + " " + str(ord(data[9])) + " " + str(ord(data[10])) + " " + str(ord(data[11])) + " " + str(ord(data[12])) + " " + str(ord(data[13])) + " " + str(ord(data[14])) + " " + str(ord(data[15])) + " " + "\n")
       else:
         fpr.write (header_decode(data[0]) + " " + header_decode(data[1]) + " " + command_decode_msb(data[2]) + " " + command_decode_lsb(data[3]) + " " + str(ord(data[4])) + " " + str(ord(data[5])) + " " + str(ord(data[6])) + " " + str(ord(data[7])) + " " + str(ord(data[8])) + " " + str(ord(data[9])) + " " + str(ord(data[10])) + " " + str(ord(data[11])) + " " + str(ord(data[12])) + " " + str(ord(data[13])) + " " + str(ord(data[14])) + " " + str(ord(data[15])) + " " + "\n")
     fpr.close()
             
def vhdl_pkg_to_var(search_var):
   return_int = -1
   fpr = open('ess_constants_pkg.vhd', 'r')
   for line in fpr:
     find_var = line.find (search_var)
     if find_var > 0 :
       find_space = line.find(" " , find_var)
       var_name = line[9:find_space]
       find_var_start = line.find(":= \"" , find_space)
       if find_var_start > 0 :
         find_var_end = line.find("\";" , find_var_start)
         var_value = line[find_var_start+4:find_var_end]
         return_int = int( var_value , 2)
   fpr.close()

   return return_int

def addr_map_search(search_var,map_file):
   return_int = -1
   var_type = "X"
   map_path = map_file
   fpr = open(map_path, 'r')
   for line in fpr:
     find_var = line.find (search_var)
     #print find_var
     if find_var >= 0 :
       find_space = line.find(" " , find_var)
       #print find_space
       var_name = line[0:find_space]
       #print var_name
       find_space1 = line.find(" " , find_space+1)
       #print find_space1
       var_addr = line[find_space+1:find_space1]
       find_space2 = line.find(" " , find_space1+1)
       #print var_addr
       return_int = int(var_addr,10)
       if find_space2 < 0 :
         var_type = line[find_space1+1:len(line)-1]
       else:
         #print "SPACE2" , find_space2
         #print "LINE LENGTH" , len(line)
         var_type = line[find_space1+1:find_space2]
       #print var_type
       #find_var_start = line.find(":= \"" , find_space)
       #if find_var_start > 0 :
         #find_var_end = line.find("\";" , find_var_start)
         #var_value = line[find_var_start+4:find_var_end]
         #return_int = int( var_value , 2)
   fpr.close()

   return return_int , var_type


def address_handler(input_address):
   q, r = divmod(input_address, 16777216)
   if  q == 0:
      string_out = chr(0)
   else:
      string_out = chr(q)

   q, r = divmod(r, 65536)
   if  q == 0:
      string_out = string_out + chr(0)
   else:
      string_out = string_out + chr(q)
      
   q, r = divmod(r, 256)
   if  q == 0:
      string_out = string_out + chr(0)
   else:
      string_out = string_out + chr(q)
      
   string_out = string_out + chr(r)   
   
   return string_out

def bytes_to_integer(data):
  int_out = 0
  #for value in data:
  for index in range(len(data)):
    int_out = int_out + ( ord(data[index])*math.pow(256, 3-index) )
  return int_out

def block_read(ser,start_addr,number_of_reads,seq):
  index_msb = 0
  index_lsb = 0
  true_write = 1
  #reset_index()
  local_index = 0
  return_data = [1.3] * (number_of_reads+1)
  while true_write == 1:
    #local_index = inc_index()
    index_msb = local_index/256
    index_lsb = local_index%256
    local_index = local_index + 1
    true_write = 0    
    chk_sum = 0
    str_addr = address_handler(start_addr)
    end_addr = address_handler(start_addr+number_of_reads-1)
    new_string = chr(vhdl_pkg_to_var("CMD_HEADER_MSB"))
    new_string = new_string + chr(vhdl_pkg_to_var("CMD_HEADER_LSB"))
    new_string = new_string + chr(vhdl_pkg_to_var("CMD_MSB_MEMORY"))
    new_string = new_string + chr(vhdl_pkg_to_var("CMD_LSB_BLOCK_READ_INIT"))
    #new_string = new_string + chr(0)
    new_string = new_string + str_addr[0]
    new_string = new_string + str_addr[1]
    new_string = new_string + str_addr[2] 
    new_string = new_string + str_addr[3] 
    new_string = new_string + end_addr[0] 
    new_string = new_string + end_addr[1] 
    new_string = new_string + end_addr[2] 
    new_string = new_string + end_addr[3] 
    new_string = new_string + chr(index_msb)
    new_string = new_string + chr(index_lsb)
    new_string = new_string + chr(seq)
    #new_string = new_string + chr(inc_seq())
    for index in range(len(new_string)):
      chk_sum = chk_sum + ord(new_string[index])
      if chk_sum > 255:
        chk_sum = chk_sum - 256
    new_string = new_string + chr(chk_sum)

    ser.write(new_string)     # write a string
    ser.flush()
    packet_decipher(new_string)
    pck_cnt = 0
    true_read = 1
    if ord(str_addr[0]) > 15:
      #true_read = 0
      print ('DOWNSTREAM READ')
    check_index = 0       
    while true_read == 1:
      data = ser.read(16)
      if len(data) == 16:
        packet_decipher(data)
        if ord(data[2]) == vhdl_pkg_to_var("CMD_MSB_MEMORY"):
          if ord(data[3]) == vhdl_pkg_to_var("RSP_LSB_ACKR"):
            check_index = ord(data[13])
          chk_sum = 0
          for index in range(len(data)-1):
            chk_sum = chk_sum + ord(data[index])
            if chk_sum > 255:
              chk_sum = chk_sum - 256
          pck_cnt = pck_cnt + 1
          check_index = check_index + 1
          if pck_cnt == number_of_reads+2:
             true_read = 0
          if chk_sum == ord(data[15]):
             datas = data[4] + data[5] + data[6] + data[7]
             return_data[pck_cnt-2] = bytes_to_integer(datas)
             #print ('SEQ')
             #print ord(data[14])
      else:
        #print ('NO DATA')
        true_read = 0
        number_of_reads = pck_cnt - 2
  return return_data[0:number_of_reads];
                                                       
def block_write(ser,start_addr,write_data,seq):
  number_of_writes = len(write_data)
  #index_msb = 0
  #index_lsb = 0
  true_write = 1
  #local_seq = inc_seq()
  #reset_index()
  local_index = 0
  while true_write == 1:
    #local_index = inc_index()
    index_msb = local_index/256
    index_lsb = local_index%256
    local_index = local_index + 1
    #print index_lsb
    chk_sum = 0
    str_addr = address_handler(start_addr)
    new_string = chr(vhdl_pkg_to_var("CMD_HEADER_MSB"))
    new_string = new_string + chr(vhdl_pkg_to_var("CMD_HEADER_LSB"))
    new_string = new_string + chr(vhdl_pkg_to_var("CMD_MSB_MEMORY"))
    if index_lsb == 0:
      new_string = new_string + chr(vhdl_pkg_to_var("CMD_LSB_BLOCK_WRITE_INIT"))
      new_string = new_string + str_addr[0] 
      new_string = new_string + str_addr[1] 
      new_string = new_string + str_addr[2] 
      new_string = new_string + str_addr[3] 
      new_string = new_string + chr(0)
      new_string = new_string + chr(0)
      new_string = new_string + chr(0)
      new_string = new_string + chr(0)
    else:
      new_string = new_string + chr(vhdl_pkg_to_var("CMD_LSB_BLOCK_WRITE_DATA"))
      str_data = address_handler(write_data[index_lsb-1])
      new_string = new_string + chr(0)
      new_string = new_string + chr(0)
      new_string = new_string + chr(0)
      new_string = new_string + chr(0)
      new_string = new_string + str_data[0]
      new_string = new_string + str_data[1]
      new_string = new_string + str_data[2]
      new_string = new_string + str_data[3]
    new_string = new_string + chr(index_msb)
    #if index_lsb == number_of_writes+1:
    #  new_string = new_string + chr(10)
    #  print 'Sent Incorrect Index'
    #else:
    #if index_lsb == 3:
    #  new_string = new_string + chr(7)
    #else:
    new_string = new_string + chr(index_lsb)
    new_string = new_string + chr(seq)
    for index in range(len(new_string)):
      chk_sum = chk_sum + ord(new_string[index])
      if chk_sum > 255:
        chk_sum = chk_sum - 256
    new_string = new_string + chr(chk_sum)
    ser.write(new_string)     # write a string
    ser.flush()
    #print "Sending Index - " , ord(new_string[12]) , ord(new_string[13])
    packet_decipher(new_string)
    #if index_lsb == 255:
    #  index_lsb = 0
    #else:
    #  index_lsb = index_lsb + 1
    
    if index_lsb == number_of_writes:
      true_write = 0
    #if index_lsb == 1:
    #  data = ser.read(16)
    #  packet_decipher(data)

    #else:
      data = ser.read(16)
      if len(data) == 16:
        packet_decipher(data)
  mem_terminate(ser,vhdl_pkg_to_var("CMD_LSB_TERMINATE_BLOCK_WRITE"),seq,local_index)
      
def mem_terminate(ser,cmd,seq,local_index):
  #local_index = inc_index()
  index_msb = local_index/256
  index_lsb = local_index%256
  #index_msb = 0
  #index_lsb = 0
  true_write = 1
  while true_write == 1:
    chk_sum = 0
    new_stringx = chr(vhdl_pkg_to_var("CMD_HEADER_MSB"))
    new_stringx = new_stringx + chr(vhdl_pkg_to_var("CMD_HEADER_LSB"))
    new_stringx = new_stringx + chr(vhdl_pkg_to_var("CMD_MSB_MEMORY"))
    new_stringx = new_stringx + chr(cmd)
    new_stringx = new_stringx + chr(0)
    new_stringx = new_stringx + chr(0) 
    new_stringx = new_stringx + chr(0) 
    new_stringx = new_stringx + chr(0) 
    new_stringx = new_stringx + chr(0) 
    new_stringx = new_stringx + chr(0) 
    new_stringx = new_stringx + chr(0)
    new_stringx = new_stringx + chr(0)
    new_stringx = new_stringx + chr(index_msb)
    new_stringx = new_stringx + chr(index_lsb)
    new_stringx = new_stringx + chr(seq)
    #new_stringx = new_stringx + chr(ret_seq())
    for index in range(len(new_stringx)):
      chk_sum = chk_sum + ord(new_stringx[index])
      if chk_sum > 255:
        chk_sum = chk_sum - 256
    new_stringx = new_stringx + chr(chk_sum)
    #if index_lsb == 255:
    #  index_lsb = 0
    #else:
    #  index_lsb = index_lsb + 1
    ser.write(new_stringx)     # write a string
    ser.flush()
    packet_decipher(new_stringx)
    

    #if index_lsb == 1:
    true_write = 0

  data = ser.read(16)
  packet_decipher(data)

def set_timestamp(ser,timevalue_sec,timevalue_nano,cmd):
   index_msb = 0
   index_lsb = 0
   str_data_sec = address_handler(timevalue_sec)
   str_data_nano = address_handler(timevalue_nano)
   chk_sum = 0
   new_string = chr(vhdl_pkg_to_var("CMD_HEADER_MSB"))
   new_string = new_string + chr(vhdl_pkg_to_var("CMD_HEADER_LSB"))
   new_string = new_string + chr(vhdl_pkg_to_var("CMD_MSB_GLOBAL_CLOCK"))
   #new_string = new_string + chr(vhdl_pkg_to_var("CMD_LSB_LOAD_TIMESTAMP"))
   new_string = new_string + chr(cmd)
   new_string = new_string + str_data_sec[0] 
   new_string = new_string + str_data_sec[1] 
   new_string = new_string + str_data_sec[2] 
   new_string = new_string + str_data_sec[3]  
   new_string = new_string + str_data_nano[0] 
   new_string = new_string + str_data_nano[1] 
   new_string = new_string + str_data_nano[2] 
   new_string = new_string + str_data_nano[3]  
   new_string = new_string + chr(index_msb)
   new_string = new_string + chr(index_lsb)
   new_string = new_string + chr(inc_seq())

   for index in range(len(new_string)):
    chk_sum = chk_sum + ord(new_string[index])
    if chk_sum > 255:
      chk_sum = chk_sum - 256
   new_string = new_string + chr(chk_sum)
   if index_lsb == 255:
    index_lsb = 0
   else:
    index_lsb = index_lsb + 1
   ser.write(new_string)     # write a string
   ser.flush()
   packet_decipher(new_string)

   data = ser.read(16)
   chk_sum = 0
   for index in range(len(data)-1):
    chk_sum = chk_sum + ord(data[index])
    if chk_sum > 255:
      chk_sum = chk_sum - 256
   if chk_sum == ord(data[15]):
    packet_decipher(data)
   else:
    print ('Timestamp CheckSum WRONG')
    #print "Expected :- " , chk_sum
    #print "Received :- " , ord(data[15])	

def poll_data(ser):
    pck_cnt = 0
    true_read = 1
    while true_read == 1:
      data = ser.read(16)
      #packet_decipher(data)
      if len(data) == 16:
        packet_decipher(data)
      else:
        print ('NO DATA')
        #true_read = 0

def cmd_interpreter(s,script_var,address_map):
   seq_number = random.randint(1, 255)
   a = array("L", [0, 1])
   b = array("L", [0])
   ret_d = array("L", [0, 1])
   base = 1024
   return_int = -1
   #script_path = '/u/jpe87/hardware/ESS/ess_timing_demonstrator/test/' + script_var
   script_path = script_var
   fpr = open(script_path, 'r')
   #fpr = open('/u/jpe87/hardware/ESS/ess_timing_demonstrator/test/cmd_script.txt', 'r')
   for line in fpr:
     find_var = line.find (" ")
     if find_var > 0 :
       find_space1 = line.find(" " , find_var)
       arg1 = line[0:find_space1]
       #print arg1
       find_space2 = line.find( " " , find_space1+1 )
       if find_space2 >= 0 :
         arg2 = line[find_space1+1:find_space2]
       else:
         arg2 = line[find_space1+1:len(line)-1]
       #print find_space2
       #print arg2
       #print 'Hello'
       if arg2 == "BASE":
         my_addr = 1
         my_type = "AD"
       else:
         my_addr , my_type = addr_map_search(arg2,address_map)
       if my_addr >= 0 :
         if seq_number < 255:
	   seq_number = seq_number + 1
         else:
           seq_number = 1
         #print my_addr
         #print my_type
         #print len(my_type)
         if arg1 == "SET" and my_type == "MAC" :
           #print "Setting MAC Address"
           find_space_dot1 = line.find( "." , find_space2+1 )
           find_space_dot2 = line.find( "." , find_space_dot1+1 )
           find_space_dot3 = line.find( "." , find_space_dot2+1 )
           find_space_dot4 = line.find( "." , find_space_dot3+1 )
           find_space_dot5 = line.find( "." , find_space_dot4+1 )
           mac1 = line[find_space2+1 : find_space_dot1]
           mac2 = line[find_space_dot1+1 : find_space_dot2]
           mac3 = line[find_space_dot2+1 : find_space_dot3]
           mac4 = line[find_space_dot3+1 : find_space_dot4]
           mac5 = line[find_space_dot4+1 : find_space_dot5]
           mac6 = line[find_space_dot5+1 : len(line)-1]
           #print mac1
           #print mac2
           #print mac3
           #print mac4
           #print mac5
           #print mac6
           ip_mac_top = int ( 256*int(mac1,16) + int(mac2,16) )
           #print ip_mac_top
           ip_mac_bot = int ( 16777216*int(mac3,16) + 65536*int(mac4,16) + 256*int(mac5,16) + int(mac6,16) )
           #print ip_mac_bot
           a[0] = ip_mac_top
           a[1] = ip_mac_bot
           block_write(s,base+my_addr,a,seq_number)
           print "Setting MAC Address" , arg2 , "-" , mac1 , ":" , mac2 , ":" , mac3 , ":" , mac4 , ":" , mac5 , ":" , mac6 
         else:
           if arg1 == "SET" and my_type == "IP" :
             #print "Setting IP Address"
             find_space_dot1 = line.find( "." , find_space2+1 )
             find_space_dot2 = line.find( "." , find_space_dot1+1 )
             find_space_dot3 = line.find( "." , find_space_dot2+1 )
             ip1 = line[find_space2+1 : find_space_dot1]
             ip2 = line[find_space_dot1+1 : find_space_dot2]
             ip3 = line[find_space_dot2+1 : find_space_dot3]
             ip4 = line[find_space_dot3+1 : len(line)-1]
             #print ip1
             #print ip2
             #print ip3
             #print ip4
             ip_addr = 16777216*int(ip1,10) + 65536*int(ip2,10) + 256*int(ip3,10) + int(ip4,10)
             b[0] = ip_addr
             block_write(s,base+my_addr,b,seq_number)
             print "Setting IP Address" , arg2 , "-" , ip1 , "." ,ip2 , "." , ip3 , "." , ip4 
           else:
             if arg1 == "SET" and my_type == "LW":
               #print "Setting Register"
               port = line[find_space2+1 : len(line)]
               #print port
               ip_port = int(port,10)
               #print ip_port
               b[0] = ip_port
               block_write(s,base+my_addr,b,seq_number)  
               print "Setting Register" , arg2 , ip_port
             else:  
              if arg1 == "SET" and arg2 == "BASE" :
                #print "Setting Base Address"
                baddr = line[find_space2+1 : len(line)]
                base  = int(baddr,10)
                print "Setting Base Address" , base
              else:
                if arg1 == "READ" and my_type == "LW":
                  #print "Reading Register"
                  #print arg1
                  #print my_type
                  ret_d = block_read(s,base+my_addr,1,seq_number) 
                  print "Reading Register" , arg2 , "-" , int(ret_d[0])
                else:
                  if arg1 == "READ" and my_type == "IP":
                    #print "Reading IP Address"
                    #print arg1
                    #print my_type
                    ret_d = block_read(s,base+my_addr,1,seq_number) 
                    #print ret_d[0]
                    str_addr = address_handler(int(ret_d[0]))
                    ip1 = ord(str_addr[0])
                    ip2 = ord(str_addr[1])
                    ip3 = ord(str_addr[2])
                    ip4 = ord(str_addr[3])
                    print "Reading IP Address" , arg2 , "-" ,  ip1 , "." , ip2 , "." , ip3 , "." , ip4
                  else:
                    if arg1 == "READ" and my_type == "MAC":
                      #print "Reading MAC Address"
                      #print arg1
                      #print my_type
                      ret_d = block_read(s,base+my_addr,2,seq_number) 
                      #print ret_d[0]
                      str_addr = address_handler(int(ret_d[0]))
                      str_addr = str_addr + address_handler(int(ret_d[1]))
                      mac1 = hex(ord(str_addr[2]))[2:4]
                      mac2 = hex(ord(str_addr[3]))[2:4]
                      mac3 = hex(ord(str_addr[4]))[2:4]
                      mac4 = hex(ord(str_addr[5]))[2:4]
                      mac5 = hex(ord(str_addr[6]))[2:4]
                      mac6 = hex(ord(str_addr[7]))[2:4]
                      mac_st = mac1 + ":" + mac2 + ":" + mac3 + ":" + mac4 + ":" + mac5 + ":" + mac6
                      print "Reading MAC Address" , arg2 , "-" , mac_st
                    else:
                      if arg1 == "SET" and my_type == "GAIN":
                        #print "SETTING GAIN"
                        port = line[find_space2+1 : len(line)-1]
                        #print port,'x'
                        #ip_port = int(port,10)
                        #print ip_port
                        #b[0] = ip_port
                        if port == "C_100mV":
                          b[0] = 35
                        else:
                          if port == "C_1V":
                            b[0] = 17
                          else:
                            if port == "C_10V":
                              b[0] = 69
                            else:
                              if port == "C_100mV_cal":
                                b[0] = 66
                              else:
                                if port == "C_1V_cal":
                                  b[0] = 64
                                else:
                                  if port == "C_10V_cal":
                                    b[0] = 68
                                  else:
                                    if port == "C_100mV_50ohm":
                                      b[0] = 43
                                    else:
                                      if port == "C_1V_50ohm":
                                        b[0] = 25
                                      else:
                                        if port == "C_10V_50ohm":
                                          b[0] = 77
                        print 'SETTING GAIN' , arg2 , "-" , b
                        #print my_addr
                        #print b
                        block_write(s,base+my_addr,b,seq_number) 
                      else:
                        if arg1 == "SET" and my_type == "OFFSET":
                          #print "SETTING OFFSET"
                          #print my_addr
                          port = line[find_space2+1 : len(line)-1]
                          #print port,'x'
                          ip_port = float(port)
                          #print ip_port
                          if ip_port >= 0:
                            b[0] = 524288 + (my_addr-28)*65536 + 32768 + int(32767*ip_port/5)
                            #print b[0]
                            block_write(s,base+my_addr,b,seq_number) 
                            #print "Offset Done Positively"
                          else:
                            b[0] = 524288 + (my_addr-28)*65536 + 32767 - int(32767*ip_port/5)
                            #print b[0]
                            block_write(s,base+my_addr,b,inc_seq()) 
                            #print "Offset Done Negitively"
                            print "SETTING OFFSET" , arg2 , "-" , b[0]
                        else:
                          if arg1 == "READ" and my_type == "OFFSET":
                            #print "Reading OFFSET"
                            ret_d = block_read(s,base+my_addr,1,seq_number) 
                            #print ret_d[0]
                            if ret_d[0] >= 524288:
                              #print "Channel Enabled"
                              ret_d[0] = ret_d[0] - 524288
                            else:
                              #print "Channel Disabled"
                              ch_number = int(ret_d[0] / 458752 )
                              #print "Channel " , ch_number + 1
                            print "Reading OFFSET" , arg2 , ret_d[0]
                          else:
                            if arg1 == "READ" and my_type == "GAIN":
                              #print "Reading GAIN"
                              ret_d = block_read(s,base+my_addr,1,seq_number) 
                              print "Reading GAIN" , arg2 , "-" , ret_d[0]
                         
   fpr.close()

   return return_int
