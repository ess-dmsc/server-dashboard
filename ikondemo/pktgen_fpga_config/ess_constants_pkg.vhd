----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/05/2016 01:32:33 PM
-- Design Name: 
-- Module Name: ess_constants_pkg - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:--



-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.all;
library ess_lib;
use ess_lib.ess_datestamp.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

package ess_constants is

  constant TMR_CNTR_MAX        : std_logic_vector(26 downto 0) := "101111101011110000100000000";  --100,000,000 = clk cycles per second
--constant TMR_CNTR_MAX_88MHZ : std_logic_vector(26 downto 0)        := "101001111101100011000000000"; --88,000,000 = clk cycles per second
  constant TMR_CNTR_MAX_88MHZ  : std_logic_vector(26 downto 0) := "101010001011101001010110000";  --88,462,000 = clk cycles per second--
  constant TMR_CNTR_MAX_100MHZ : std_logic_vector(26 downto 0) := "101111101011110000100000000";  --100,000,000 = clk cycles per second
  constant STROBE_14HZ_100MHZ  : std_logic_vector(26 downto 0) := "000011011001111110111001001";
--constant STROBE_14HZ_88MHZ : std_logic_vector(26 downto 0) :=  "000010111111110100110010010"; --88,000,000 = clk cycles per second
  constant STROBE_14HZ_88MHZ   : std_logic_vector(26 downto 0) := "000011000000110101001111010";  --88,462,000 = clk cycles per second
  constant TMR_VAL_MAX         : std_logic_vector(3 downto 0)  := "1111";  --15
  constant RESET_CNTR_MAX      : std_logic_vector(17 downto 0) := "110000110101000000";  -- 100,000,000 * 0.002 = 200,000 = clk cycles per 2 ms
  constant TMR_2ms             : std_logic_vector(17 downto 0) := "110000110101000000";  --2,000,000 = clk cycles per second

  type CHAR_ARRAY is array (integer range<>) of std_logic_vector(7 downto 0);

  constant MAX_STR_LEN : integer := 27;

  constant WELCOME_STR_LEN : natural := 27;
  constant BTN_STR_LEN     : natural := 24;

-- constant BIT_TMR_MAX : std_logic_vector(13 downto 0) := "10100010110000"; --10416 = (round(100MHz / 9600)) - 1
  constant BIT_TMR_MAX      : std_logic_vector(13 downto 0) := "00001101100011";  --867 = (round(100MHz / 115200)) - 1
  constant BIT_INDEX_MAX    : natural                       := 10;
  constant BIT_INDEX_MAX_RX : natural                       := 9;

--  constant BAUD_9600   : std_logic_vector(13 downto 0) := "10100010110000";  --10416 = (round(100MHz / 9600)) - 1
--  constant BAUD_14400  : std_logic_vector(13 downto 0) := "01101100011111";  --6943 = (round(100MHz / 14400)) - 1
--  constant BAUD_19200  : std_logic_vector(13 downto 0) := "01010001010111";  --5207 = (round(100MHz / 19200)) - 1
--  constant BAUD_28800  : std_logic_vector(13 downto 0) := "00110110001111";  --3471 = (round(100MHz / 28800)) - 1
--  constant BAUD_38400  : std_logic_vector(13 downto 0) := "00101000101011";  --2603 = (round(100MHz / 38400)) - 1
--  constant BAUD_57600  : std_logic_vector(13 downto 0) := "00011011000111";  --1735 = (round(100MHz / 57600)) - 1
--  constant BAUD_115200 : std_logic_vector(13 downto 0) := "00001101100011";  --867 = (round(100MHz / 115200)) - 1
--  constant BAUD_230400 : std_logic_vector(13 downto 0) := "00000110110001";  --433 = (round(100MHz / 230400)) - 1

  constant SEG7_BAUD_9600   : std_logic_vector(31 downto 0) := "10111101000000001001011000000000";  --10416 = (round(100MHz / 9600)) - 1
  constant SEG7_BAUD_14400  : std_logic_vector(31 downto 0) := "10111101000000010100010000000000";  --6943 = (round(100MHz / 14400)) - 1
  constant SEG7_BAUD_19200  : std_logic_vector(31 downto 0) := "10111101000000011001001000000000";  --5207 = (round(100MHz / 19200)) - 1
  constant SEG7_BAUD_28800  : std_logic_vector(31 downto 0) := "10111101000000101000100000000000";  --3471 = (round(100MHz / 28800)) - 1
  constant SEG7_BAUD_38400  : std_logic_vector(31 downto 0) := "10111101000000111000010000000000";  --2603 = (round(100MHz / 38400)) - 1
  constant SEG7_BAUD_57600  : std_logic_vector(31 downto 0) := "10111101000001010111011000000000";  --1735 = (round(100MHz / 57600)) - 1
  constant SEG7_BAUD_115200 : std_logic_vector(31 downto 0) := "10111101000100010101001000000000";  --867 = (round(100MHz / 115200)) - 1
  constant SEG7_BAUD_230400 : std_logic_vector(31 downto 0) := "10111101001000110000010000000000";  --433 = (round(100MHz / 230400)) - 1

  constant CMD_HEADER_MSB : std_logic_vector(7 downto 0) := "11001010";  -- 0xCA
  constant CMD_HEADER_LSB : std_logic_vector(7 downto 0) := "11111110";  -- OxFE

  constant RSP_HEADER_MSB : std_logic_vector(7 downto 0) := "10111010";  -- 0xBA
  constant RSP_HEADER_LSB : std_logic_vector(7 downto 0) := "10111110";  -- OxBE

  constant CMD_MSB_GLOBAL_CLOCK : std_logic_vector(7 downto 0) := "01000000";
  constant CMD_MSB_MEMORY       : std_logic_vector(7 downto 0) := "10000000";
  constant CMD_MSB_ERROR        : std_logic_vector(7 downto 0) := "11111111";
  constant RSP_MSB_MEMORY       : std_logic_vector(7 downto 0) := "10000000";
  constant RSP_MSB_ERROR        : std_logic_vector(7 downto 0) := "11111111";

  constant CMD_LSB_LOAD_TIMESTAMP        : std_logic_vector(7 downto 0) := "00000000";  -- Set Timestamp counter        
  constant CMD_LSB_READ_TIMESTAMP        : std_logic_vector(7 downto 0) := "00001001";  -- Set Timestamp counter        
  constant CMD_LSB_BLOCK_READ_INIT       : std_logic_vector(7 downto 0) := "00000000";  -- Initiate Block Read                           
  constant CMD_LSB_BLOCK_READ_DATA       : std_logic_vector(7 downto 0) := "10100000";  -- Initiate Block Read                           
  constant CMD_LSB_BLOCK_WRITE_INIT      : std_logic_vector(7 downto 0) := "00000010";  -- Initiate Block Write                            
  constant CMD_LSB_BLOCK_WRITE_DATA      : std_logic_vector(7 downto 0) := "11110010";  -- Initiate Block Write                            
  constant CMD_LSB_TERMINATE_BLOCK_READ  : std_logic_vector(7 downto 0) := "11000000";  -- Terminate Block Read     
  constant CMD_LSB_TERMINATE_BLOCK_WRITE : std_logic_vector(7 downto 0) := "11000001";  -- Terminate Block Write  
  constant CMD_LSB_TERMINATE_WRITE_ACK   : std_logic_vector(7 downto 0) := "11010001";  -- Terminate Block Write                                         
  constant CMD_LSB_ERROR_MS              : std_logic_vector(7 downto 0) := "00000001";
  constant CMD_LSB_ERROR_DS              : std_logic_vector(7 downto 0) := "00000011";
  constant CMD_LSB_ERROR_EB              : std_logic_vector(7 downto 0) := "00000111";
  
  constant CMD_LSB_READ_DRP              : std_logic_vector(7 downto 0) := "00001111";
  constant CMD_LSB_WRITE_DRP             : std_logic_vector(7 downto 0) := "00011111";
  constant RSP_LSB_DRP_DONE              : std_logic_vector(7 downto 0) := "00111111";
      
  constant RSP_LSB_IERR_MS               : std_logic_vector(7 downto 0) := "11110001";  -- Respond to Read received index error
  constant RSP_LSB_IERR_DS               : std_logic_vector(7 downto 0) := "11110010";  -- Respond to Read received index error
  constant RSP_LSB_TERMINATE_BLOCK_READ  : std_logic_vector(7 downto 0) := "11100000";  -- Terminate Block Read     
  constant RSP_LSB_TERMINATE_BLOCK_WRITE : std_logic_vector(7 downto 0) := "11100001";  -- Terminate Block Write  
  constant RSP_LSB_TERMINATE_WRITE_ACK   : std_logic_vector(7 downto 0) := "11010101";  -- Terminate Block Write                                         

  constant RSP_LSB_ACKR : std_logic_vector(7 downto 0) := "10000000";  -- Acknowledge Block Read command
  constant CMD_LSB_ACKW : std_logic_vector(7 downto 0) := "10000001";  -- Acknowledge Block Write command

--Welcome string definition. Note that the values stored at each index
--are the ASCII values of the indicated character.
  constant WELCOME_STR : CHAR_ARRAY(0 to 26) := (X"0A",   --\n
                                                 X"0D",   --\r
                                                 X"4E",   --N
                                                 X"45",   --E
                                                 X"58",   --X
                                                 X"59",   --Y
                                                 X"53",   --S
                                                 X"34",   --4
                                                 X"20",   -- 
                                                 X"47",   --G
                                                 X"50",   --P
                                                 X"49",   --I
                                                 X"4F",   --O
                                                 X"2F",   --/
                                                 X"55",   --U
                                                 X"41",   --A
                                                 X"52",   --R
                                                 X"54",   --T
                                                 X"20",   -- 
                                                 X"44",   --D
                                                 X"45",   --E
                                                 X"4D",   --M
                                                 X"4F",   --O
                                                 X"21",   --!
                                                 X"0A",   --\n
                                                 X"0A",   --\n
                                                 X"0D");  --\r

--Button press string definition.
  constant BTN_STR : CHAR_ARRAY(0 to 23) := (X"42",       --B
                                                 X"75",   --u
                                                 X"74",   --t
                                                 X"74",   --t
                                                 X"6F",   --o
                                                 X"6E",   --n
                                                 X"20",   -- 
                                                 X"70",   --p
                                                 X"72",   --r
                                                 X"65",   --e
                                                 X"73",   --s
                                                 X"73",   --s
                                                 X"20",   --
                                                 X"64",   --d
                                                 X"65",   --e
                                                 X"74",   --t
                                                 X"65",   --e
                                                 X"63",   --c
                                                 X"74",   --t
                                                 X"65",   --e
                                                 X"64",   --d
                                                 X"21",   --!
                                                 X"0A",   --\n
                                                 X"0D");  --\r

  constant TX_STR_LEN : natural := 16;
  constant TX_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                            RSP_HEADER_LSB,
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",   -- Index MSB
                                            X"00",   -- Index LSB
                                            X"FF",   -- Sequence Byte
                                            X"00");  -- Checksum

  constant TM_STR_LEN : natural := 16;
  constant TM_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                            RSP_HEADER_LSB,
                                            CMD_MSB_GLOBAL_CLOCK,
                                            CMD_LSB_READ_TIMESTAMP,
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",
                                            X"00",   -- Index MSB
                                            X"00",   -- Index LSB
                                            X"FF",   -- Sequence Byte
                                            X"00");  -- Checksum

  constant BLOCK_RD_LEN : natural := 16;
  constant BLOCK_RD_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                                  RSP_HEADER_LSB,
                                                  CMD_MSB_MEMORY,
                                                  CMD_LSB_BLOCK_READ_DATA,
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",   -- Index MSB
                                                  X"00",   -- Index LSB
                                                  X"FF",   -- Sequence Byte
                                                  X"00");  -- Checksum

  constant ACKW_STR_LEN : natural := 16;
  constant ACKW_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                              RSP_HEADER_LSB,
                                              CMD_MSB_MEMORY,
                                              CMD_LSB_ACKW,
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",   -- Index MSB
                                              X"00",   -- Index LSB
                                              X"FF",   -- Sequence Byte
                                              X"00");  -- Checksum

  constant ACKR_STR_LEN : natural := 16;
  constant ACKR_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                              RSP_HEADER_LSB,
                                              CMD_MSB_MEMORY,
                                              RSP_LSB_ACKR,
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",   -- Index MSB
                                              X"00",   -- Index LSB
                                              X"FF",   -- Sequence Byte
                                              X"00");  -- Checksum

  constant ACKR_TER_STR_LEN : natural := 16;
  constant ACKR_TER_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                                  RSP_HEADER_LSB,
                                                  RSP_MSB_MEMORY,
                                                  RSP_LSB_TERMINATE_BLOCK_READ,
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",   -- Index MSB
                                                  X"00",   -- Index LSB
                                                  X"FF",   -- Sequence Byte
                                                  X"00");  -- Checksum

  constant ACKW_TER_STR_LEN : natural := 16;
  constant ACKW_TER_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                                  RSP_HEADER_LSB,
                                                  RSP_MSB_MEMORY,
                                                  RSP_LSB_TERMINATE_WRITE_ACK,
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",
                                                  X"00",   -- Index MSB
                                                  X"00",   -- Index LSB
                                                  X"FF",   -- Sequence Byte
                                                  X"00");  -- Checksum

  constant IERR_STR_LEN : natural := 16;
  constant IERR_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                              RSP_HEADER_LSB,
                                              CMD_MSB_ERROR,
                                              RSP_LSB_IERR_MS,
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",
                                              X"00",   -- Index MSB
                                              X"00",   -- Index LSB
                                              X"FF",   -- Sequence Byte
                                              X"00");  -- Checksum


  constant ERR_STR_LEN : natural := 16;
  constant ERR_STR : CHAR_ARRAY(0 to 15) := (RSP_HEADER_MSB,
                                             RSP_HEADER_LSB,
                                             CMD_MSB_ERROR,
                                             CMD_LSB_ERROR_MS,
                                             X"00",
                                             X"00",
                                             X"00",
                                             X"00",
                                             X"00",
                                             X"00",
                                             X"00",
                                             X"00",
                                             X"00",   -- Index MSB
                                             X"00",   -- Index LSB
                                             X"FF",   -- Sequence Byte
                                             X"00");  -- Checksum                                                                               

end ess_constants;

package body ess_constants is
end ess_constants;
