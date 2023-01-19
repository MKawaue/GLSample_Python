# coding: UTF-8
"""
This program is for fiber QC.
The connection supports TCP/IP(LAN) connection.

System requirements (software)
    Python 3.8

"""
import time
import pdb
import os
import sys
import string
import datetime
from tcp import Tcp

#GLOBAL CONSTANT
#Timeout(1sec)
Timeout_default = 1
NCH = 64
NSAMP = 60
SAMP_TIME = 1#sec
SH_SCRIPT_NAME = "GL_to_ttree.sh"
#CPP_SCRIPT_NAME = "../GL840_fiberQC"
#PATH_TO_DATA_DIRECTRY = "../GL840_data/"
PATH_TO_DATA_DIRECTRY = "/Users/kawaue/mppctest/GL840_data/"
PATH_TO_SCRIPT_DIRECTRY = "/Users/kawaue/mppctest/"
#sockets
tcp_logger = Tcp(Timeout_default)
tcp_LED = Tcp(Timeout_default)
tcp_MPPC = Tcp(Timeout_default)
IP_logger = "192.168.2.11"
port_logger = 8023
#IP_LED = "192.168.1.12"
IP_LED = "192.168.11.12" #NEW ROUTER
port_LED = 5025
IP_MPPC = "192.168.2.12"
port_MPPC = 5025

def main():
    #Instantiation of the LAN communication class
    """
    tcp_logger = Tcp(Timeout_default)
    tcp_LED = Tcp(Timeout_default)
    IP_logger = "192.168.2.11"
    port_logger = 8023
    IP_LED = "192.168.1.12"
    port_LED = 5025
    #IP_MPPC = "192.168.1.11"
    #port_MPPC = 5025
    """


    print("Connecting with Logger...")
    connect_tcp(tcp_logger,IP_logger,port_logger)
    print("Connecting with LED PS...")
    connect_tcp(tcp_LED,IP_LED,port_LED)
    print("Connecting with MPPC PS...")
    connect_tcp(tcp_MPPC,IP_MPPC,port_MPPC)

    initial_setup()

    running_mode()

    tcp_logger.close()
    tcp_LED.close()
    tcp_MPPC.close()

def connect_tcp(tcp,IP,port):

    if not tcp.open(IP, port):
        print("Connection error")
        return

def initial_setup():
    #tcp_LED.send_command(":VOLT 5")
    #"""
    """
    tcp_LED.send_command(":CURR 1.92")
    msgBuf = tcp_LED.send_read_command(":CURR?", Timeout_default)
    print("LED Current")
    """
    tcp_LED.send_command(":VOLT 5")
    msgBuf = tcp_LED.send_read_command(":VOLT?", Timeout_default)
    print("LED Voltage")
    print(msgBuf)
    tcp_MPPC.send_command(":VOLT 51.5")
    msgBuf = tcp_MPPC.send_read_command(":VOLT?", Timeout_default)
    print("MPPC Voltage")
    print(msgBuf)
    #"""
    tcp_logger.send_command(":DATA:SAMP 100MS")
    msgBuf = tcp_logger.send_read_command(":DATA:SAMP?",Timeout_default)
    print(msgBuf)
    for i in range(0,NCH,1) :
        amp_on = ":AMP:CH%d:INP DC"%int(i+1)
        tcp_logger.send_command(amp_on)
        print(":AMP:CH%d:INP?"%int(i+1))
        msgBuf = tcp_logger.send_read_command(":AMP:CH%d:INP?"%int(i+1), Timeout_default)
        print(msgBuf)
        #amp_range = ":AMP:CH%d:RANG 200MV"%int(i+1)
        amp_range = ":AMP:CH%d:RANG 500MV"%int(i+1)
        tcp_logger.send_command(amp_range)
        print(":AMP:CH%d:RANG?"%int(i+1))
        msgBuf = tcp_logger.send_read_command(":AMP:CH%d:RANG?"%int(i+1), Timeout_default)
        print(msgBuf)

def running_mode():
    while True:
        print("Enter to Start Measurement")
        command = input()
        #Start Measurement when No Input
        if command == "" :
            measurement()
        #Show Status
        if command == "status" :
            show_status()
        #Interactive Mode (for experts)
        #bug : After a few communication, the same message is sent twice.
        if command == "expert" :
            while True:
                print("Welcome to expert mode")
                print("MPPC or LED or logger?")
                mode = input()
                if mode == "MPPC" :
                    ascii_mode(tcp_MPPC)
                if mode == "LED" :
                    ascii_mode(tcp_LED)
                if mode == "logger" :
                    pdb.set_trace()
                    ascii_mode(tcp_logger)
                if mode == "exit" :
                    break
        if command == "exit" :
            print("Bye :)")
            break
        #something meaningless is entered
        else:
            print("Start Measurement : just press Enter key, Show Status : status, Exit : exit")

def measurement():

    planel_id = "hoge"
    first_id = "fuga"
    second_id = "piyo"
    MPPC_id = "hogehoge"
    calib_flag = 0

    #LOOP START
    while True:
        #Panel
        print("Select panel (U or R or L or T)")
        command = input()
        if command.isdigit() or command == "U" or command == "R" or command == "L" or command == "T":
            if command.isdigit() :
                print("calibration mode")
                calib_flag = 1
            planel_id = command
        #1st coordinate
            print("First index")
            command = input()
            if command.isdigit() :
                first_id = command
        #2nd coordinate
                print("Second index")
                command = input()
                if command.isdigit() :
                    second_id = command
        #Concatenate position infomation above and Create file name
                    MPPC_id = planel_id + "-" + first_id + "-" + second_id
                    print("Start measurement for " + MPPC_id)
                    command = input()
                    if command == "" :
                        break
                    else :
                        return 0
                else :
                    print("Invalid Argument")
            else :
                print("Invalid Argument")
        else :
            print("Invalid Argument")
            #print("Enter U (Upstram) or R (Right) or L (Left) or T (Top) ")
    #LOOP END

    print(MPPC_id)
    #"""
    #MPPC ON
    print("Turn On MPPC and LED")
    switch_PS(tcp_MPPC,"ON")
    #"""
    #Start Recording
    #Stop Recording
    #LED ON
    #switch_PS(tcp_LED,"ON")

    file_name = "run_number.txt"
    f_RN = open(file_name,"r")
    run_num = int(f_RN.read())
    f_RN.close()
    f_RN = open(file_name,"w")
    f_RN.write(str(run_num+1))
    f_RN.close()
    #file_name = "../GL840_data/test.csv"
    file_name = PATH_TO_DATA_DIRECTRY + MPPC_id + ".csv"
    f = open(file_name,"w")
    #Buffer Clear
    msgBuf = tcp_logger.send_read_command(":MEAS:OUTP:STAT?",Timeout_default)
    print("Buffer Status")
    print(msgBuf)
    msgBuf = "Cleaning Buffer......"
    print(msgBuf)
    #msgBuf =
    print("############ACK############")
    tcp_logger.send_read_command(":MEAS:OUTP:ACK?", Timeout_default)
    #print(msgBuf)
    #msgBuf = tcp_logger.send_read_command(":MEAS:OUTP:DATAACK?", Timeout_default)
    #print(msgBuf)
    time.sleep(1.0)
    #Start Recording
    msgBuf = "Taking Data ......"
    print(msgBuf)
    for i in range(int(NSAMP)+1):
        #if i % 2 == 0 :
        if i==10 :
            print("!!!!!LED Switch ON!!!!!")
            switch_PS(tcp_LED,"ON")
        data = ""
        data = tcp_logger.send_read_command(":MEAS:OUTP:ONECSV?", Timeout_default)
        #print("kokokara\n")
        #print(data)
        #print("kokomade\n")
        if type(data) == str :
            if data =="":
                print("data empty")
                i = -1
            else:
                f.write(data)
                f.write("\n")
        else :
            print("Initializing ... \n")
            print(data)
            i = i-1
        #print(data)
        time.sleep(SAMP_TIME)
        if not i == -1:
            print("\r","Progress : ",i,"% / 100%",end="")
    #Stop Recording
    print("\nData Taking was done.")
    print("{0} was saved.".format(file_name))
    f.close()
    #sh_script_exe = "source " + " " + SH_SCRIPT_NAME + " " + file_name
    calib_filename_tmp = datetime.date.today()
    calib_filename = PATH_TO_DATA_DIRECTRY + calib_filename_tmp.strftime('%Y-%m-%d') + ".root"
    if calib_flag == 0 :
        sh_script_exe = PATH_TO_SCRIPT_DIRECTRY + SH_SCRIPT_NAME + " " + file_name + " " + calib_filename
        os.system(sh_script_exe)
    else :
        sh_script_exe = PATH_TO_SCRIPT_DIRECTRY + "for_calib_" + SH_SCRIPT_NAME + " " + file_name
        os.system(sh_script_exe)
        calib_flag = 0
    #cpp_script_exe = CPP_SCRIPT_NAME + " " + root_filename + " " + calib_filename
    #os.system(cpp_script_exe)

    #Turn off PSs
    print("Turn Off MPPC and LED")
    switch_PS(tcp_MPPC,"OFF")
    switch_PS(tcp_LED,"OFF")
    """
    data = tcp_logger.send_read_command(":MEAS:OUTP:ACK?", Timeout_default)
    print(data)
    msgBuf = tcp_logger.send_read_command(":MEAS:OUTP:DATAACK?", Timeout_default)
    print(msgBuf)
    """
    #LED OFF
    #switch_PS(tcp_LED,"OFF")
    #MPPC OFF
    #switch_PS(tcp_LED,"OFF")

    """
    #MPPC ON
    tcp_MPPC.send_command("OUTP ON")
    msgBuf = tcp_MPPC.send_read_command("OUTP?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_MPPC.send_read_command("MEAS:VOLT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_MPPC.send_read_command("MEAS:CURR?", Timeout_default)
    print(msgBuf)
    #Start Recording
    #Stop Recording
    #LED ON
    tcp_LED.send_command("OUTP ON")
    msgBuf = tcp_LED.send_read_command("OUTP?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_LED.send_read_command("MEAS:VOLT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_LED.send_read_command("MEAS:CURR?", Timeout_default)
    print(msgBuf)
    time.sleep(0.5)
    #Buffer Clear
    msgBuf = tcp_logger.send_command("MEAS:OUTP:ACK?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_logger.send_command("MEAS:OUTP:DATAACK?", Timeout_default)
    print(msgBuf)
    #Start Recording
    time.sleep(10)
    #Stop Recording
    data = tcp_logger.send_command("MEAS:OUTP:ACK?", Timeout_default)
    print(data)
    msgBuf = tcp_logger.send_command("MEAS:OUTP:DATAACK?", Timeout_default)
    print(msgBuf)
    #LED OFF
    tcp_LED.send_command("OUTP OFF")
    msgBuf = tcp_LED.send_read_command("OUTP?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_LED.send_read_command("MEAS:VOLT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_LED.send_read_command("MEAS:CURR?", Timeout_default)
    print(msgBuf)
    #MPPC OFF
    tcp_MPPC.send_command("OUTP OFF")
    msgBuf = tcp_MPPC.send_read_command("OUTP?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_MPPC.send_read_command("MEAS:VOLT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_MPPC.send_read_command("MEAS:CURR?", Timeout_default)
    print(msgBuf)
    """

#Turn ON/OFF the PS
def switch_PS(tcp_obj,command):
    if command == "ON" :
        tcp_obj.send_command(":OUTP ON")
    if command == "OFF" :
        tcp_obj.send_command(":OUTP OFF")

    msgBuf = tcp_obj.send_read_command(":OUTP?", Timeout_default)
    print("OUTPUT 1:OFF, 0:ON")
    print(msgBuf)
    msgBuf = tcp_obj.send_read_command(":MEAS:VOLT?", Timeout_default)
    print("Voltage")
    print(msgBuf)
    msgBuf = tcp_obj.send_read_command(":MEAS:CURR?", Timeout_default)
    print("Current")
    print(msgBuf)
    time.sleep(0.5)

#Show Status
def show_status():
    #MPPC Status
    print("MPPC Status")
    msgBuf = tcp_MPPC.send_read_command(":OUTP?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_MPPC.send_read_command(":MEAS:VOLT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_MPPC.send_read_command(":MEAS:CURR?", Timeout_default)
    print(msgBuf)
    #LED Status
    print("LED Status")
    msgBuf = tcp_LED.send_read_command(":OUTP?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_LED.send_read_command(":MEAS:VOLT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_LED.send_read_command(":MEAS:CURR?", Timeout_default)
    print(msgBuf)

    print("Logger Status")
    msgBuf = tcp_logger.send_read_command(":MEAS:OUTP:STAT?", Timeout_default)
    print(msgBuf)
    msgBuf = tcp_logger.send_read_command(":DATA:SAMP?", Timeout_default)
    print(msgBuf)

# TCP/IP Connection
def if_tcp():

    IP = "192.168.1.11"
    port = 8023

    tcp = Tcp(Timeout_default)
    if not tcp.open(IP, port):
        print("Connection error")
        return

    ascii_mode(tcp)

    tcp.close()

# Ascii mode
def ascii_mode(obj):
    #Send and receive commands
    while True:
        print("Enter the command (Exit with no input) Ex.*IDN?")
        command = input()
        #Exit if no input
        if command == "":
            break
        #If the command contains "?"
        if "?" in command :
            msgBuf = obj.send_read_command(command, Timeout_default)
            print("pass above")
            print(msgBuf)
            print("pass below")
        if command == "help":
            print("Command List")
            print("*IDN? : ask ID")
        #Send only
        else:
            obj.send_command(command)


if __name__ == '__main__':
  args = sys.argv
  main()
