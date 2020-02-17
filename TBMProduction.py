# Program Info
programName = "Timebase Monitor Program"
# By Micah Hurd
version = 1

# exec(open("C:\\Users\\Micah\\PycharmProjects\\Libraries\\ReadTxtFile.py").read())
def readTxtFile(filename, searchTag, index, sFunc=""):
    # Example Useage:
    # emailList = readTxtFile(templateFile, "emails", "1:", sFunc="list")
    # Returns values as a list

    indexing = False
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
                    indexing = True
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
                    # return parsedLine.

                # Apply string manipulation functions, if requested (optional argument)
                if sFunc != "":
                    sFunc = sFunc.lower()

                    if sFunc == "strip" and indexing == False:
                        output = output.strip()

                if (type(output) is list) and sFunc != "list":
                    output2 = ""
                    for i in output:
                        output2 += str(i) + ","
                    length = len(output2)
                    output2 = output2[0:(length - 1)]
                    output = ""
                    output = output2

                if (type(output) is str) and sFunc == "list":
                    output = output.split(",")

                return output

        return "Searched term could not be found"

    filestream.close()
    return "Searched term could not be found"


# exec(open("C:\\Users\\Micah\\PycharmProjects\\Libraries\\userPrompt.py").read())
def userPrompt(message,inType="",range=""):
    # requires import os
    # Example usage:
    # evalMethod = userPrompt("Please enter an option.","num","1:4:whole")
    # userPrompt("Set the step attenuator to {} dB".format(nominal),"")

    def stringInput(prompt):
        a = False
        b = False
        while a == False:
            string = input(" > " + str(prompt) + " ")
            while b == False:
                check = input(" > Please verify that \"{}\" is correct. Enter (y)es or (n)o: ".format(string))
                # print("entered: ",check)
                check = check.lower()
                # print("lowered: ", check)
                if check != "y" and check != "n":
                    print("!! You must enter \"y\" for Yes or \"n\" for No !!")
                elif check == "y" or check == "n":
                    b = True
            if check == "y":
                a = True
            else:
                b = False
        string = string.strip()
        return string

    def yesNoPrompt(prompt):
        b = False
        while b == False:
            check = input(" > "+ str(prompt) + " - Enter (y)es or (n)o: ")
            # print("entered: ",check)
            check = check.lower()
            # print("lowered: ", check)
            if check != "y" and check != "n":
                print("!! You must enter \"y\" for Yes or \"n\" for No !!")
            elif check == "y" or check == "n":
                b = True
        if check == "y":
            return True
        else:
            return False

    def checkFileExists(prompt):
        string = input(" > " + str(prompt) + " ")
        b = os.path.isfile(string)
        while b == False:
            string = input(" > File \"{}\" does not exist. Please re-enter: ".format(string))
            b = os.path.isfile(string)

        string = string.strip()
        return string

    def numberInput(prompt,range=""):
        if range != "":
            range = str(range)
            range = range.split(":")
            numType = str(range[2])
            if numType == "whole":
                lower = int(range[0])
                upper = int(range[1])
            else:
                lower = float(range[0])
                upper = float(range[1])

            number = lower - 1
            while (number < lower) or (number > upper):
                number = input(
                    " > " + prompt + " (" + str(lower) + " through " + str(upper) + "): ")
                try:
                    if numType == "float":
                        number = float(number)
                    elif numType == "whole":
                        number = int(number)
                except:
                    print("No valid number entered! Please try again...")
                    number = lower - 1
                else:
                    if numType == "float" and type(number) is float:
                        if number < lower or number > upper:
                            print("Allowed values are " + float(lower) + " through " + float(upper) + ". Please try again.")
                        else:
                            return number
                    elif numType == "whole" and type(number) is int:
                        if number < lower or number > upper:
                            print("Allowed values are " + str(lower) + " through " + str(upper) + ". Please try again.")
                        else:
                            return number
        else:
            while 1:
                number = input(" > " + prompt + " (numeric entry): ")
                try:
                    number = float(number)
                except:
                    print("No valid number entered! Please try again...")
                else:
                    return number


    if inType != "":
        inType = inType.lower()

    if inType == "":
        input(" > " + str(message) + " ")
        return 0
    elif inType == "yn":
        return yesNoPrompt(message)
    elif inType == "string":
        return stringInput(message)
    elif inType == "file":
        return checkFileExists(message)
    elif inType == "num":
        return numberInput(message,range)

import serial
import platform
import statistics
import math
import os
import datetime
import csv
from os import system, name
from os import path
import time
# import pyvisa as visa
# from win32com import client
# from PyPDF2 import PdfFileMerger
# import xlwings as xw

from pathlib import Path
import shutil

def create_log(logFile):
    checkExists = path.exists(logFile)

    if checkExists == False:
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

def writeLogCSV(listToFile,logFile):
    import time
    import datetime

    utcTime = str(time.time())
    write_mode = "a"

    currentDT = datetime.datetime.now()

    date_time = currentDT.strftime("%Y-%m-%d_%H:%M:%S")

    # Convert list to CSV string
    stringToFile = ""
    for i in listToFile:
        stringToFile += str(i) + ","
    # Chop the trailing comma off the end of the string
    length = len(stringToFile)
    stringToFile = stringToFile[0:(length - 1)]

    # Incorporate time stamp into the string and add the newline character
    stringToFile = str(date_time) + "," + utcTime + "," + stringToFile + "\n"

    # Open the file and write the output string
    result_file = open(logFile, write_mode)
    result_file.writelines(stringToFile)

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

def serialIO(cmd,dType="",timeout=1):
    global ser

    output = cmd
    if output == 'exit':
        ser.close()
        # exit()
    elif output == 'buffer?':
        quantity = ser.inWaiting()
        # print("Quantity waiting in buffer: " + str(quantity))
    else:
        # The magic thing to get this to work was to add "\r" before and after the command...
        output = "\r" + output + "\r"
        bytes = str.encode(output)
        ser.write(bytes)

        if "?" in output:
            for i in range(timeout):
                time.sleep(1)
                quantity = ser.inWaiting()
                # print("Quantity waiting in buffer: " + str(quantity))
                if quantity > 0:
                    break

        if dType == "" or dType == "string":
            inputRx = ""
            while ser.inWaiting() > 0:
                serInput = ser.read(1)
                # print("RAW SERIAL RXd: ",serInput)
                typeCheck = type(serInput)
                # print("RAW SERIAL TYPE: %s"%(typeCheck))

                converted = dataConv(serInput)					# Convert from byte or hex, as applicable

                converted = str(converted)						# Force to string type prior to concatenation
                inputRx = inputRx + converted

                inputRx = inputRx.replace("\\n","")

                inputRx = inputRx.strip()


        elif dType == "list":
            inputRx = []
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
                inputRx.append(converted)

        return inputRx

# def isMidnight():
#     import time
#     import datetime
#
#     currentDT = datetime.datetime.now()
#
#     date_time = currentDT.strftime("%H:%M:%S")
#
#     date_time = date_time.split(":")
#
#     hour = int(date_time[0])
#
#     if hour == 0:
#         return True
#     else:
#         return False

def timeDeltaSecondsUTC(startTime, endTime=""):
    if endTime == "":
        endTime = time.time()

    return endTime - startTime

def waitTime(interval):
    # Input time is in minutes and output time is in seconds
    # Consistency is overrated...
    import datetime
    import math

    currentDT = datetime.datetime.now()
    date_time = currentDT.strftime("%H:%M:%S")
    date_time = date_time.split(":")
    minutesTime = float(date_time[1])
    secondsTime = float(date_time[2])

    seconds = (minutesTime * 60) + secondsTime

    intervalSeconds = interval * 60

    secondsInHour = 60 * 60

    qtyElapsedSoFar = seconds / intervalSeconds
    nextInterval = math.ceil(qtyElapsedSoFar)

    if nextInterval == qtyElapsedSoFar:
        nextInterval += 1

    seconds1 = qtyElapsedSoFar * intervalSeconds
    seconds2 = nextInterval * intervalSeconds

    secondsToWait = math.ceil(seconds2 - seconds1)

    if seconds2 > secondsInHour:
        diff = seconds2 - secondsInHour
        secondsToWait -= diff

    return secondsToWait

def sendEmail(recipeintList,subjectStr,msgStr,smtpURLstr,smtpPortInt,smtpFromStr,smtpPassStr):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()

    if type(recipeintList) is list:
        print("List address detected")
        addressList = ""
        for index, i in enumerate(recipeintList):
            address = str(i).strip()
            # addressList += str(address) + "; "
            recipeintList[index] = address

        # # Chop the trailing ; off the end of the string
        # length = len(addressList)
        # addressList = addressList[0:(length - 2)]
    else:
        addressList = recipeintList

    MY_ADDRESS = smtpFromStr
    PASSWORD = smtpPassStr

    msg['From'] = MY_ADDRESS
    msg['To'] = addressList
    msg['Subject'] = subjectStr

    part1 = MIMEText(msgStr, 'plain')
    msg.attach(part1)

    print(recipeintList)
    try:
        server = smtplib.SMTP_SSL(smtpURLstr, smtpPortInt)
        server.ehlo()
        server.login(MY_ADDRESS, PASSWORD)
        server.sendmail(MY_ADDRESS, recipeintList, msg.as_string())
        server.close()
        return 0
    except:
        return 1

def loadOffsetValues(filename,indexTime):
    # Time values being compared should be UTC value in seconds
    # Examples: indexTime = time.time()

    print("***************************************************************************************************")
    print("")



    filestream = open(filename, 'r')  # Open specified uncertainty file
    filestreamLines = filestream.readlines()  # Create a list of all lines from the uncertainty file
    filestream.close()
    print(filestreamLines)

    # Remove any blank lines from the list of file lines
    j = 0
    for i in filestreamLines:                           # Enumerate through each line in the line list
        if i == "\n":                                   # If line only contains newline character
            del filestreamLines[j]                      # then delete the line
        j += 1


    offsetList = []
    for i in filestreamLines:                           # Enumerate through each line in the line list
        currentLine = i.split(",")                      # Split out the currently enumerated line according to CSV
        print(currentLine)
        try:
            lineTimestamp = float(currentLine[1])           # Get the column that should contain the UTC value
        except:
            print("\"{}\" was not a number".format(currentLine[1]))

        aTime = lineTimestamp
        bTime = indexTime
        deltaSeconds = (bTime - aTime)                  # Find the difference between the index'd value and the file value
        print(deltaSeconds)

        if deltaSeconds <= 86400:                       # if the difference is less than or equal to 24 hours
            currentOffsetVal = str(currentLine[4])      # Get column that should contain the offset value
            print("Found Offset Value: \"{}\"".format(currentOffsetVal))
            try:
                offsetList.append(float(currentOffsetVal))
            except:
                print("Offset value \"{}\" was not a number".format(currentOffsetVal))
    print("offsetList: {}".format(offsetList))
    print("")
    print("***************************************************************************************************")
    return offsetList

# def cullLogFile(filename,maxLines):
#     fileLines = []
#     with open(filename, "r") as filestream:
#         # print(len(filestream))
#
#         lineCount = 0
#         for indx, line in enumerate(filestream):
#             fileLines.append(line)
#             lineCount = indx
#
#         print(lineCount)
#
#     if lineCount > maxLines:
#         qtyToDelete = lineCount - maxLines
#     else:
#         return 0
#
#
#     f = open(filename, "w+")
#     f.close()
#
#     with open(filename, "a") as result_file:
#         for indx, line in enumerate(fileLines):
#             if indx >= qtyToDelete:
#                 result_file.writelines(line)
#
#     return 1

def cullLogFile(filename,maxSize):
    # Size is in bytes (one character per byte)
    char_list = [ch for ch in open(filename).read()]
    fileSize = len(char_list)

    if fileSize > maxSize:
        qtyToDelete = fileSize - maxSize
    else:
        return 0


    f = open(filename, "w+")
    f.close()

    with open(filename, "a") as result_file:
        for indx, char in enumerate(char_list):
            if indx >= qtyToDelete:
                result_file.writelines(char)

    return 1

def getFileSize(file):

    statinfo = os.stat(file)
    fileSize = statinfo.st_size

    return fileSize

# =====================================================================================================
# Start of program
# =====================================================================================================

# In windows testing this will be different than in linux testing
# Place this here so that this can be easily change when moved to a linux environment

opSystem = platform.system()
if opSystem == "Linux":
    fileSlash = "/"
elif opSystem == "Windows":
    fileSlash = "\\"
else:
    print("Unkown OS")
    sys.exit()

debug = userPrompt("Debug Mode?","yn")

if debug == True:
    if userPrompt("Terminal Mode?","yn"):
        port = userPrompt("Enter the serial port resource string:","string")
        rate = userPrompt("Enter the baud rate of the serial port:","num")
        tOut = userPrompt("Enter the timeout (seconds):", "num")
        createSerial(port, rate, tOut)
        escape = False
        while escape == False:
            cmd = str(input("TX: "))
            if cmd == "exit":
                escape = True
            response = serialIO(cmd, dType="string", timeout=30)
            print("RX: {}".format(response))



# Program Required constants and variables ---------------------------
cwd = os.getcwd()
dailyTimeStamp = time.time()
logFile = "TBMLog.txt"
templateFile = "TBMconfig.ini"
timeProgramStarted = time.time()
tieValue1 = 0
tieTimeStamp1 = 0
logFileMaxSize = 50_000_000
deviceList = []
freqOffsetList = []
duplicateTieList = []
pastTieValList = []
pastTimeValList = []
ErrorList = []
templateFile = cwd + fileSlash + templateFile
freqOffset24HR = ""
deltaTimeLastSelftest = 0
deltaTimeLastDailyMail = 0
timeLastErrorEmail = 0
commRetryInterval = 5
dailyEmailAlreadySentList = []
# tieValue24HR1 = 0
# tieTimeStamp24HR1 = 0


# Create or append or cull the program log file ----------------------------------------------------------------
create_log(logFile)                 # Create the program log file (if not exists already)
print("Culling log file. This may take some time, depending on the size of the file...")
tempResult = cullLogFile(logFile, logFileMaxSize)   # Reduce the size of the log file to value in bytes

writeLog("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ New Program Instance \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/",logFile)
writeLog("Program Name: " + str(programName),logFile)
writeLog("Program Version: " + str(version),logFile)
writeLog("Current Working Directory: "+str(cwd),logFile)

if tempResult == 1:
    writeLog("Log file was culled at program start.", logFile)
else:
    writeLog("Log file was less than {} at program start.".format(logFileMaxSize), logFile)

userInterfaceHeader(programName,version,cwd,logFile)

# Import values from configuration file ------------------------------
print("Importing parameters from the template file...")
writeLog("Importing parameters from measurement template file: {}".format(str(templateFile)), logFile)
time.sleep(0.5)

# Iterate through configured instruments from the timebase ini file --------------------------------------
# Also initializes various lists which will hold a list per instrument
i = 0
searchComplete = False
while searchComplete == False:
    lookup = "timeBase" + str(i + 1)
    tbDevice = readTxtFile(templateFile, lookup, "1:", sFunc="strip")

    if tbDevice == "Searched term could not be found":
        searchComplete = True
        break
    else:
        writeLog("Timebase Device: {}".format(str(tbDevice)), logFile)
        device = tbDevice.split(",")
        deviceList.append(device)
        freqOffsetList.append([])
        duplicateTieList.append([])
        dailyEmailAlreadySentList.append(False)
        pastTieValList.append(0)
        pastTimeValList.append(0)
    i += 1

# Load previous offset error values from any existing measurement logs -------------------------------------
indexTime = time.time()
deviceCounter = 0
writeLog("Attempting to load hsitorical offset error values from log files...", logFile)
for i in deviceList:
    currentDevice = i
    assetNum = currentDevice[0]
    # Create the output directory name and log output file for the monitored device --------------------
    outputDir = str(readTxtFile(templateFile, "logDirectory", 1, sFunc="strip"))
    outputFile = outputDir + fileSlash + str(assetNum) + ".csv"
    writeLog("Checking if log exists at: {}".format(str(outputFile)), logFile)

    if os.path.exists(outputFile) == True:
        print("Found a historical log file")
        listFromFile = loadOffsetValues(outputFile, indexTime)
        writeLog("Found the following historical offset values: {}".format(str(listFromFile)), logFile)
        tempLength = len(listFromFile)
        if tempLength > 0:
            try:
                for i in listFromFile:
                    freqOffsetList[deviceCounter].append(i)
                writeLog("Saved historical offset values successfully", logFile)
                writeLog("freqOffsetList: {}".format(freqOffsetList), logFile)
                print("Saved historical offset values successfully")
            except:
                print("Failed to load historical offset values!")
                writeLog("Failed to load historical offset values!", logFile)
        else:
            print("No historical offset values found within the 24 hour window.")
            writeLog("No historical offset values found within the 24 hour window.", logFile)

    deviceCounter += 1

# Main program loop ===========================================================================
# This loop is programmed to repeat every 20 minutes, starting at the top of each hour
monitor = True
while monitor == True:

    # Device Iteration Loop =======================================================================
    writeLog("------------------------------- Started device iteration loop -------------------------------", logFile)
    deviceCounter = 0
    for i in deviceList:
        # Add in some white space just to make the program output look cleaner --------
        print()
        print(" _____________________________________________________________________ ")
        print("|                       Time Base Monitor Application                 |")
        print("|_____________________________________________________________________|")
        print()
        currentDT = datetime.datetime.now()
        date_time = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        print("Timestamp: {}".format(date_time))

        # Cull log file if necessary ------------------------------------------
        logFileSize = getFileSize(logFile)
        if logFileSize >= 100_000_000:
            cullLogFile(logFile, 50_000_000)

        # Load in device information and configuration information ------------
        # print(i)
        smtpUrl = readTxtFile(templateFile, "smtpUrl", 1, sFunc="strip")
        smtpPort = int(readTxtFile(templateFile, "smtpPort", 1))
        smtpEmail = readTxtFile(templateFile, "smtpEmail", 1)
        smtpPassword = readTxtFile(templateFile, "smtpPassword", 1)
        currentDevice = i
        writeLog("currentDevice: {}".format(str(currentDevice)), logFile)
        print("Device Parameters:")
        print(currentDevice)
        assetNum = str(currentDevice[0])
        writeLog("assetNum: {}".format(str(assetNum)), logFile)
        resourceStr = currentDevice[1]
        writeLog("resourceStr: {}".format(str(resourceStr)), logFile)
        baudRate = currentDevice[2]
        writeLog("baudRate: {}".format(str(baudRate)), logFile)
        timeOut = 10
        writeLog("timeOut: {}".format(str(timeOut)), logFile)
        diffLimit = float(currentDevice[3])
        writeLog("diffLimit: {}".format(str(diffLimit)), logFile)
        emailList = readTxtFile(templateFile, "emails", "1:", sFunc="list")
        writeLog("emailList: {}".format(str(emailList)), logFile)
        monitoringInterval = float(readTxtFile(templateFile, "monitoringInterval", 1))
        commErrorTimeout = float(readTxtFile(templateFile, "commErrorTimeout", 1))
        commRetryCnt = commErrorTimeout / commRetryInterval
        commRetryCnt = round(commRetryCnt)
        commRetryCnt = int(commRetryCnt)

        # Variables to keep track of the hour and minutes; for making sure events happen at midnight -------
        currentTime = currentDT.strftime("%H:%M:%S")
        currentTime = currentTime.split(":")
        timeHour = int(currentTime[0])
        timeMinute = int(currentTime[1])
        tbError = False
        tbErrorType = 999

        # Create the output directory name and log output file for the monitored device --------------------
        outputDir = str(readTxtFile(templateFile, "logDirectory", 1, sFunc="strip"))
        writeLog("outputDir: {}".format(str(outputDir)), logFile)
        outputFile = outputDir + fileSlash + str(assetNum) + ".csv"
        writeLog("outputFile: {}".format(str(outputFile)), logFile)

        # Look to see if a log file already exists for the device being monitored
        # if not then create it ----------------------------------------------------------------------------
        if os.path.exists(outputFile) == False:
            if os.path.isdir(outputDir) == False:
                os.mkdir(outputDir)
            create_log(outputFile)
            toFile = ["DeviceID", "IDN", "freqOffset_Current", "freqOffset_24HR", "Misc."]
            writeLogCSV(toFile, outputFile)
            writeLog("Created device log: {}".format(str(outputFile)), logFile)


        # Determine if it is midnight, and if it is the first monitoring interval of the hour
        # If these are both true then the program should run self-test and send
        # the daily status e-mail ---------------------------------------------------------------------------
        if timeHour == 0:
            isMidnight = True
        else:
            isMidnight = False

        # Once the daily email is sent, dailyEmailAlreadySent is set to True, and the daily e-mail cannot be
        # re-sent. If the variable flag is set to True, AND the hour is past 1 AM, then set the already sent
        # flag back to false, so that an e-mail can be sent at the next midnight hour time segment
        dailyEmailAlreadySent = dailyEmailAlreadySentList[deviceCounter]
        if dailyEmailAlreadySent == True and timeHour > 1:
            dailyEmailAlreadySent = False
            dailyEmailAlreadySentList[deviceCounter] = dailyEmailAlreadySent

        # Set Send Daily E-mail and self-test Flag ----------------------------------------------------------
        if isMidnight == True:
            writeLog("isMidnight = True", logFile)
            tempCurrentTime = time.time()
            temporaryFloatValue = abs(tempCurrentTime - deltaTimeLastSelftest)
            if temporaryFloatValue > 3600:
                performSelfTest = True
                deltaTimeLastSelftest = time.time()
                dailyEmail = True
                deltaTimeLastDailyMail = time.time()
                writeLog("Set flags to run self-test and send daily e-mail notification", logFile)
                writeLog("Performing operation to cull the length of the log file", logFile)
                cullLogFile(logFile, 100_000_000)
        else:
            writeLog("isMidnight = False", logFile)
            dailyEmail = False
            performSelfTest = False

        # Create serial communication instance --------------------------------------------------------------
        if debug == False:
            try:
                createSerial(resourceStr, baudRate, timeOut)
                writeLog("Created serial resource at: {}".format(str(resourceStr)), logFile)
            except:
                writeLog("Failed to create serial resource at: {}".format(str(resourceStr)), logFile)

        # Get device information ----------------------------------------------------------------------------
        if debug == False:
            serialCmd = "*IDN?"
            devIDN = serialIO(serialCmd, dType="string", timeout=10)

            tbError = False
            if devIDN == "":
                for i in range(commRetryCnt):
                    print("Communication Retry {}".format(i + 1))
                    time.sleep(commRetryInterval)
                    serialCmd = "*IDN?"
                    devIDN = serialIO(serialCmd, dType="string", timeout=10)
                    if devIDN != "":
                        break

                if devIDN == "":
                    tbError = True
                    ErrorList.append(assetNum)
                    tbErrorType = 0
                else:
                    tbError = False


        else:
            devIDN = "manf,model,SN,version"
        devIDN = devIDN.replace(",", "_")
        print("Device IDN: {}".format(devIDN))
        writeLog("devIDN: {}".format(str(devIDN)), logFile)

        # Run self-test and set Self-Test failure Flag ------------------------------------------------------
        selfTestParam = ["ALL", "RAM", "ROM", "NONV", "GPS"]
        writeLog("performSelfTest: {}".format(str(performSelfTest)), logFile)
        selfTestRegister = []
        if performSelfTest == True and dailyEmailAlreadySent == False:
            string = "Selftest:"
            writeLog("Self-test initiated...", logFile)
            for i in selfTestParam:
                serialCmd = "TEST:SEL " + str(i)
                print("SerialCmd: {}".format(serialCmd))

                if debug == False:
                    serialIO(serialCmd, "string")
                    serialCmd = "*TST?"
                    serialRcvd = serialIO(serialCmd, "string", timeout=30)
                    print("serialRcvd: {}".format(serialRcvd))

                    if serialRcvd != "0":
                        selfTestFail = True
                    else:
                        selfTestFail = False

                    string += str(i) + ":" + str(serialRcvd) + "_"
                    try:
                        selfTestRegister.append(int(serialRcvd))
                    except:
                        selfTestRegister.append(0)
                else:
                    string = "ALL:0_RAM:0_ROM:0_NONV:0_GPS:0_"
                    selfTestRegister = [0,0,0,0,0]
                    selfTestFail = False

            selfTestResults = string
            writeLog("Self-test Results: {}".format(str(selfTestResults)), logFile)
        else:
            selfTestResults = "null"
            selfTestRegister = [2, 2, 2, 2, 2]
            selfTestFail = False

        # Parse Self-Test Register to string variant for e-mail use -----------------------------------------
        selfTestStringRegister = []
        for i in selfTestRegister:
            if i == 0:
                selfTestStringRegister.append("Pass")
            elif i == 1:
                selfTestStringRegister.append("Fail")
            elif i == 2:
                selfTestStringRegister.append("Not Run")
            else:
                selfTestStringRegister.append("unk.")

        # Confirm that the GPS is still locked:
        string = True
        tempCounter = 0
        while string == True:
            status = serialIO("SYNC:STAT?", "string", timeout=10)
            status = status.strip()
            if status != "":
                print("GPS Receiver Status: {}".format(status))
                string = False
            else:
                tempCounter += 1
                string = True
            if tempCounter >= 10:
                string = False
        writeLog("GPS Receiver Status: {}".format(status), logFile)

        if status != "LOCK" and status != "POW" and status != "":
            tbError = True
            ErrorList.append(assetNum)
            tbErrorType = 2

        if status == "POW":
            deviceMeasHold = True
        else:
            deviceMeasHold = False
        # print("deviceMeasHold: {}".format(deviceMeasHold))


        # Get the Frequency Figure of Merit
        string = True
        tempCounter = 0
        while string == True:
            FFOM = serialIO("SYNC:FFOM?", "string", timeout=10)
            if status != "":
                if FFOM == "1":
                    description = "Frequency output is locked to GPS"
                elif FFOM == "2":
                    description = "Frequency output is in hold-over mode and of good quality"
                elif FFOM == "3":
                    description = "Frequency output is poor, possibly due to startup, or other"
                else:
                    description = "Unknown status"
                print("Frequency Figure of Merit: {} ({})".format(FFOM,description))
                string = False
            else:
                tempCounter += 1
                string = True
            if tempCounter >= 10:
                string = False
        writeLog("FFOM: {}".format(FFOM), logFile)

        # Fetch the current TIE value and timestamp ---------------------------------------------------------
        if debug == False:
            tempList = []
            for i in range(1):
                string = True
                tempCounter = 0
                while string == True:
                    try:
                        tieValue2 = serialIO("FETC?", "string", timeout=10)
                        print("Current Time Interval Error Reported by Timebase: {}".format(tieValue2))
                        tieValue2 = float(tieValue2)
                        tempList.append(tieValue2)
                        string = False
                    except:
                        tempCounter += 1
                        print("Could not convert {} to float".format(tieValue2))
                        string = True
                        if tempCounter >= 10:
                            string = False
                            tempList.append(0)
            tieTimeStamp2 = time.time()
            tieValue2 = statistics.mean(tempList)
            # print("Averaged TIE Value: {}".format(tieValue2))

        else:
            tieValue2 = 3E-7
            tieTimeStamp2 = time.time()

        writeLog("Recorded TieValue2: {}".format(str(tieValue2)), logFile)
        writeLog("Recorded tieTimeStamp2: {}".format(str(tieTimeStamp2)), logFile)

        # Calculate 20 Minute Freq. Diff --------------------------------------------------------------------
        # Pull the past tie value out of the tie value list based on device counter
        writeLog("pastTieValList: {}".format(pastTieValList), logFile)
        tieValue1 = pastTieValList[deviceCounter]
        tieTimeStamp1 = pastTimeValList[deviceCounter]
        intervalPer24Hr = float(24 * 60 / monitoringInterval)
        intervalPer24Hr = round(intervalPer24Hr)
        writeLog("Quantity of time base averages per 24 hours (monitoring interval of {} minuteds): {}".format(monitoringInterval,intervalPer24Hr), logFile)
        if tieValue1 == 0:
            # No TIE1 value to calculate against, so the results of the calculation is null
            freqOffset = "null"
            # Load the initial TIE and Time values into the list
            pastTieValList[deviceCounter] = tieValue2
            pastTimeValList[deviceCounter] = tieTimeStamp2
        else:
            # Code to check for duplicate TIE values and note them as such if so
            # Receiving duplicate TIE values indicates that the timebase is unlocked from the GPS
            if tieValue2 == tieValue1:
                duplicateTieList[deviceCounter].append(tieValue2)
            else:
                # If Tie values are not duplicate then remove one
                tempLength = len(duplicateTieList[deviceCounter])
                if tempLength > 0:
                    duplicateTieList[deviceCounter].pop(0)



            tempLength = len(duplicateTieList[deviceCounter])
            if tempLength > 10:
                ErrorList.append(assetNum)
                tbError = True
                tbErrorType = 1
                # Allow no more than 15 entries
                while tempLength > 15:
                    duplicateTieList[deviceCounter].pop(0)
                    tempLength = len(duplicateTieList[deviceCounter])

            # Perfrom the frequency offset calculation, which takes the form:
            # Freq Offset = (TIE2 - TIE1)/(TIME2 - TIME1)
            freqOffset = (tieValue2 - tieValue1) / (tieTimeStamp2 - tieTimeStamp1)
            # print("tbError: {}".format(tbError))
            if tbError == False and deviceMeasHold == False:
                freqOffsetList[deviceCounter].append(freqOffset)
                length = len(freqOffsetList[deviceCounter])
                # print("Performed Freq Offset Archival")
                while length > intervalPer24Hr:
                    freqOffsetList[deviceCounter].pop(0)
                    length = len(freqOffsetList[deviceCounter])
            else:
                print("Withheld Freq Offset Archival")


            # Place the new most recent TIE value and time into the associated value lists
            # the TIE and Time 2 values should go into the past register because, for the next
            # offset calculation they will be the new TIE and Time 1 values.
            pastTieValList[deviceCounter] = tieValue2
            pastTimeValList[deviceCounter] = tieTimeStamp2
        writeLog("freqOffset: {}".format(str(freqOffset)), logFile)
        tempLength = len(duplicateTieList[deviceCounter])
        writeLog("Qty Duplicate TIE Vals for AN{}: {}".format(assetNum,tempLength), logFile)


        # Calculate 24 Hr Avg. Freq. Diff --------------------------------------------------------------------
        length = len(freqOffsetList[deviceCounter])
        writeLog("freqOffsetList: {}".format(freqOffsetList), logFile)
        writeLog("length: {}".format(length), logFile)
        if length >= intervalPer24Hr or length >= 2:
            writeLog("==== Performing 24 Hour Average Calculation ====", logFile)
            # writeLog("freqOffsetList: {}".format(freqOffsetList),logFile)
            # writeLog("freqOffsetList for device {} is: {}".format(deviceCounter,freqOffsetList[deviceCounter]), logFile)
            list24hrVals = []
            for i in freqOffsetList[deviceCounter]:
                list24hrVals.append(i)

            freqOffset24HR = statistics.mean(list24hrVals)
            print("Current 24 Hour Mean Deviation: {}".format(freqOffset24HR))
            writeLog("freqOffset24HR: {}".format(str(freqOffset24HR)), logFile)
        else:
            freqOffset24HR = "null"

        # Set TIE Flag if it exceeds the limit --------------------------------------------------------------
        if freqOffset != "null" and diffLimit != "":
            if abs(freqOffset) > diffLimit:
                diffLimitMet = True
                print("Send e-mail warning Tie Limit is exceeded")
            else:
                diffLimitMet = False
        else:
            diffLimitMet = False


        if (freqOffset24HR != "null") and (diffLimitMet != True):
            if abs(freqOffset24HR) > diffLimit:
                diffLimitMet = True
        writeLog("diffLimitMet: {}".format(str(diffLimitMet)), logFile)

        # Place results into string to be written to monitoring log ----------------------------------------
        # toFile = ["DeviceID","IDN","freqOffset_Current","freqOffset_24HR","Misc."]
        toFile = ["", "", "", "", ""]
        toFile[0] = assetNum
        toFile[1] = devIDN
        toFile[2] = freqOffset
        toFile[3] = freqOffset24HR
        toFile[4] = selfTestResults

        # Logic to keep the program from writing when the timebase device is not working properly
        if tbError == False and deviceMeasHold == False:
            writeLogCSV(toFile, outputFile)
            writeLog("Wrote to instrument monitoring log: {}".format(str(toFile)), logFile)
            writeLog("Instrument monitoring log at: {}".format(str(outputFile)), logFile)
        else:
            writeLog("Withheld writing values to monitoring log because error flag is true.", logFile)

        tempCurrentTime = time.time()
        deltaLastErrorEmail = tempCurrentTime - timeLastErrorEmail

        # Send E-mail If Flagged To Do So ----------------------------------------------------------------
        tempCheckInList = assetNum in ErrorList
        if (tbError == True) and (deltaLastErrorEmail > 3600) and (tempCheckInList == True):
            if tbErrorType == 0:
                errorMsg = "During routine monitoring the TBM program could not communicate with one or more devices.\n\n"
            elif tbErrorType == 1:
                errorMsg = "During routine monitoring the TBM program observed more than 10 consecutive instances of"
                errorMsg += " the same TIE value. This indicates that the device is not locked to a satellite.\n\n"
            elif tbErrorType == 2:
                errorMsg = "During routine monitoring the TBM program found a device with an unlocked GPS receiver. "
                errorMsg += "The instrument SYNC:STAT is reported as \"{}\".\n\n".format(status)
            else:
                errorMsg = "During routine monitoring the TBM program found a device which experienced an unknown error.\n\n"

            subjectStr = "AN {} GPS Timebase Warning Message".format(assetNum)
            msgStr = ""
            msgStr += errorMsg
            msgStr += "Device Asset Number(s): {}\n\n".format(ErrorList)
            msgStr += "Please check the listed device(s).\n\n".format(diffLimit)
            msgStr += "{}, Version {}\n".format(programName, version)

            test = sendEmail(emailList, subjectStr, msgStr, smtpUrl, smtpPort, smtpEmail, smtpPassword)

            print("Error Type {}".format(tbErrorType))
            print("Warning Email sent? (0 = yes): {}".format(test))
            # Remove the device from the error list
            list(filter(lambda a: a != assetNum, ErrorList))
            timeLastErrorEmail = time.time()
            tbErrorType = 999




        if diffLimitMet == True or debug == True:
            subjectStr = "AN {} GPS Timebase Warning Message".format(assetNum)
            msgStr = ""
            msgStr += "During routine monitoring the TBM program found a device which exceeded its frequency offset error limit.\n\n"
            msgStr += "Device Asset Number: {}\n".format(assetNum)
            msgStr += "Specified Frequency Offset Error Limit: {}\n".format(diffLimit)
            msgStr += "Most Recent Offset Error: {}\n".format(freqOffset)
            msgStr += "24 Hour Average Offset Error: {}\n\n".format(freqOffset24HR)
            msgStr += "{}, Version {}\n".format(programName, version)

            test = sendEmail(emailList, subjectStr, msgStr, smtpUrl, smtpPort, smtpEmail, smtpPassword)

            print("Warning Email sent? (0 = yes): {}".format(test))

        if dailyEmail == True or debug == True:
            dailyEmailAlreadySent = dailyEmailAlreadySentList[deviceCounter]
            if dailyEmailAlreadySent == False:
                msgStr = ""
                if selfTestFail == True:
                    subjectStr = "AN {} GPS Timebase Self-Test Failure".format(assetNum)
                    msgStr += "During the daily self-test routine, the TBM program found a device which failed self-test.\n\n"
                else:
                    subjectStr = "AN {} GPS Timebase Daily Status Update".format(assetNum)
                    msgStr += "Daily Status Update for Timebase Device AN {}.\n\n".format(assetNum)

                msgStr += "Device *IDN? Response: {}\n".format(devIDN)
                msgStr += "All Self-Test Result: {}\n".format(selfTestStringRegister[0])
                msgStr += "RAM Self-Test Result: {}\n".format(selfTestStringRegister[1])
                msgStr += "ROM Self-Test Result: {}\n".format(selfTestStringRegister[2])
                msgStr += "Non-Volatile Memory Self-Test Result: {}\n".format(selfTestStringRegister[3])
                msgStr += "GPS Receiver Self-Test Result: {}\n".format(selfTestStringRegister[4])
                msgStr += "Specified Frequency Offset Error Limit: {}\n".format(diffLimit)
                msgStr += "Most Recent Offset Error: {}\n".format(freqOffset)
                msgStr += "24 Hour Average Offset Error: {}\n\n".format(freqOffset24HR)
                msgStr += "{}, Version {}\n".format(programName, version)

                test = sendEmail(emailList, subjectStr, msgStr, smtpUrl, smtpPort, smtpEmail, smtpPassword)

                print("Daily Email sent? (0 = yes): {}".format(test))

                dailyEmailAlreadySent = True
                dailyEmailAlreadySentList[deviceCounter] = dailyEmailAlreadySent



            # Increment the device counter for the next instrument being monitored
            deviceCounter += 1

        # End of device monitoring iteration loop =========================================================

    writeLog("------------------------------- Ended Device Iteration Loop ---------------------------------", logFile)
    # write the program total run time to the program log
    upTime = timeDeltaSecondsUTC(timeProgramStarted)
    upTime = upTime / 60 / 60 / 24
    upTime = round(upTime)
    writeLog("Program up time: {} days".format(str(upTime)), logFile)

    # Place status into log file to indicate that the program is still running ---
    writeLog("Program Running = True", logFile)

    print("")
    print("")
    print("")
    print("Program Uptime: {} Days".format(upTime))
    print("============")

    userInterfaceHeader(programName, version, cwd, logFile, msg="Waiting for next monitoring event...")

    if debug == True:
        input("...")

    # Determine the time to the next 20 minute interval and wait that long
    secondsWait = float(waitTime(monitoringInterval))
    # print("secondsWait: {}".format(secondsWait))
    writeLog("Seconds to next monitoring event: {}".format(str(secondsWait)), logFile)
    writeLog("Minutes to next monitoring event: {}".format(str(secondsWait/60)), logFile)
    while secondsWait >= 0:
        minutes = secondsWait / 60
        wholeMinutes = math.floor(minutes)
        seconds = secondsWait - (wholeMinutes * 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
            seconds = seconds.replace(".0", "")
        else:
            seconds = str(seconds)
            seconds = seconds.replace(".0", "")
        if wholeMinutes < 10:
            wholeMinutes = "0" + str(wholeMinutes)
        if debug == True:
            print("Minutes Remaining: {}:{}".format(wholeMinutes,seconds))
        else:
            print("Minutes Remaining: {}:{}    \r".format(wholeMinutes,seconds), end="")
        secondsWait -= 1
        time.sleep(1)
    print()





# Divide by zero error on the 24 hour interval error average; check that the correct values are being stored
# Place TIE value and Timestamp into log file
# Setup program to pull the last TIE value and calculate an offset off that, if it was less than a day ago
# Setup the program to run multiple intervals (figure out how to designate what the interval is)
# Run full self-test only once per month

