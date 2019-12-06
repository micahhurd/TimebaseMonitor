# Program Info
programName = "Timebase Monitor Program"
# By Micah Hurd
version = 1

import serial
import time
from os import system, name
import time
import statistics
import math
import pyvisa as visa
import datetime
import csv
from win32com import client
from PyPDF2 import PdfFileMerger
import xlwings as xw
import os
from pathlib import Path
import shutil

def create_log(logFile):

    f= open(logFile,"w+")

    f.close()
    return 0

def writeLog(entry,logFile):
    write_mode = "a"

    currentDT = datetime.datetime.now()

    date_time = currentDT.strftime("%Y-%m-%d %H:%M:%S")

    with open(logFile, mode=write_mode, newline='') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        result_writer.writerow([date_time, entry])

    result_file.close()

    return 0

def createSerial(port, rate, tOut):
    global ser
    ser = serial.Serial()
    ser.baudrate = rate
    ser.timeout = tOut
    # ser.port = '/dev/ttyUSB0'
    ser.port = port
    # print("serial parameters: " + str(ser))
    ser.open()
    # print("Serial open status: " + str(ser.is_open))
    return ser.is_open

def readTxtFile(filename,searchTag,index, sFunc=""):
    searchTag = searchTag.lower()
    # print("Search Tag: ",searchTag)

    # Open the file
    with open(filename, "r") as filestream:
        # Loop through each line in the file
        for line in filestream:
            # Split each line into separated elements based upon comma delimiter
            currentLine = line.split(",")
            # select the first comma seperated value
            search = str(currentLine[0])
            # Set the value to all lowercase for comparison
            search = search.lower()

            # Remove the newline symbol from the list, if present
            lineLength = len(currentLine)
            lastElement = lineLength - 1
            if currentLine[lastElement] == "\n":
                currentLine.remove("\n")
            lineLength = len(currentLine)
            lastElement = lineLength - 1

            # Output the line which matches the search
            # If index is populated then output the indexed field
            if search == searchTag:
                if index == "":
                    output = currentLine
                    # break
                    # return currentLine

                if type(index) is int:
                    if index > lineLength:
                        output = "Index out of range"
                        # break
                    else:
                        output = currentLine[index]
                        # break
                        # return currentLine[index]

                if type(index) is str and index.find(":"):
                    index = index.split(":")
                    index[0] = int(index[0])

                    if index[0] > lineLength:
                        output = "Index out of range"
                        # break
                        # return "Index out of range"

                    if index[1] != "" and index[1] != " ":
                        index[1] = int(index[1])
                        if index[1] > lineLength:
                            output = "Index out of range"
                            # break
                            # return "Index out of range"

                    if index[1] == "" or index[1] == " ":
                        index[1] = lastElement

                    parsedLine = []
                    while index[0] <= index[1]:
                        x = currentLine[index[0]]
                        parsedLine.append(x)
                        index[0] += 1
                    output = parsedLine
                    # break
                    #return parsedLine.

                # Apply string manipulation functions, if requested (optional argument)
                if sFunc != "":
                    sFunc = sFunc.lower()

                    if sFunc == "strip":
                        output = output.strip()

                return output

        return "Searched term could not be found"


    filestream.close()
    return "Searched term could not be found"

def userInterfaceHeader(program,version,cwd,logFile,msg=""):
    print(program + ", Version " + str(version))
    print("Current Working Directory: " + str(cwd))
    print("Log file located at working directory: " + str(logFile))
    print("=======================================================================")
    if msg != "":
        print(msg)
        print("_______________________________________________________________________")
    return 0

def dataConv(unknownVal):
    # This data conversion program is really only applicable to the output of the Fluke 910 because
    # the 910 outputs hex values starting with \x instead of the normal 0x. Otherwise this works for
    # any form of byte to string conversion

    # Determine if value is byte or string; in either case strip remove formatting to make "normal" string
    if type(unknownVal) is bytes:
        # print("unknown value is bytes")
        # convert = decode.convert
        unknownVal = str(unknownVal)
        # print(unknownVal)
        length = len(unknownVal)
        stop = length - 1
        start = 2
        unknownVal = unknownVal[start:stop]
        # print("Sliced: ", unknownVal)
    elif type(unknownVal) is str:
        # print("unknown value is string")
        if unknownVal.find("b") == True:
            unknownVal = unknownVal.replace(str("b"), str(""))
            # print(unknownVal)
        if unknownVal.find("'") == True:
            unknownVal = unknownVal.replace(str("'"), str(""))
            # print(unknownVal)
        if unknownVal.find("\\x") == True:
            unknownVal = unknownVal.replace(str("\\x"), str(""))
            # print(unknownVal)
            unknownVal = int(unknownVal, 16)
        # print("Stripped: ", unknownVal)

    # Determine if unkown value is hexedecimal; convert to base 10 if so
    if unknownVal.find("x") == True:
        stop = len(unknownVal)
        start = 2
        unknownVal = unknownVal[start:stop]
        # print(unknownVal)
        unknownVal = int(unknownVal, 16)

    # Try to convert value to int, float, or string (whichever is applicable)
    try:
        # print(1)
        unknownVal = int(unknownVal)
    except:
        try:
            # print(2)
            unknownVal = float(unknownVal)
        except:
            try:
                # print(3)
                unknownVal = str(unknownVal)
            except:
                print("Not a int, float, or string")
    return unknownVal

def serialIO(cmd,dType=""):
    global ser
    output = cmd
    if output == 'exit':
        ser.close()
        exit()
    else:
        output = "\r" + output + "\r"
        bytes = str.encode(output)
        ser.write(bytes)
        time.sleep(1)
        quantity = ser.inWaiting()
        print("Quantity waiting in buffer: " + str(quantity))


        if dType == "" or dType == "string":
            input = ""
            while ser.inWaiting() > 0:
                serInput = ser.read(1)
                # print("RAW SERIAL RXd: ",serInput)
                typeCheck = type(serInput)
                # print("RAW SERIAL TYPE: %s"%(typeCheck))

                converted = dataConv(serInput)					# Convert from byte or hex, as applicable

                converted = str(converted)						# Force to string type prior to concatenation
                input = input + converted


        elif dType == "list":
            input = []
            while ser.inWaiting() > 0:
                serInput = ser.read(1)
                # print("RAW SERIAL RXd: ", serInput)
                typeCheck = type(serInput)
                # print("RAW SERIAL TYPE: %s"%(typeCheck))
                converted = dataConv(serInput)
                # if decode == "yes":
                # 	converted = serInput.decode("utf-8")
                # 	input.append(converted)
                # else:
                input.append(converted)

        return input

global ser


logFile = "TBMLog.txt"
templateFile = "TBMconfig.ini"
create_log(logFile)

writeLog("New Program Instance -------------------------------",logFile)
writeLog("Program Name: " + str(programName),logFile)
writeLog("Program Version: " + str(version),logFile)
writeLog("Current Working Directory: "+str(cwd),logFile)

clear()
userInterfaceHeader(programName,version,cwd,logFile)

# Import values from configuration file ------------------------------
print("Importing parameters from the template file...")
writeLog("Importing parameters from measurement template file: {}".format(str(templateFile)), logFile)
time.sleep(0.5)

# Iterate through up to 4 configurable instruments from the timebase file
i = 1
while i < 5:
    lookup = "timeBase" + str(i)
    tbDevice = readTxtFile(templateFile, lookup, 1, sFunc="strip")

    if tbDevice != "Searched term could not be found":
        if i == 1:
            list = tbDevice.split(",")
            dev1ID = tbDevice
            print(dev1ID)


    i += 1


# Load Configuration Information
