import time
import datetime

# time1 = datetime.now()



def loadOffsetValues(filename,indexTime):
    # Time values being compared should be UTC value in seconds
    # Examples: indexTime = time.time()



    filestream = open(filename, 'r')  # Open specified uncertainty file
    filestreamLines = filestream.readlines()  # Create a list of all lines from the uncertainty file
    filestream.close()
    print(filestreamLines)

    # # Remove any blank lines from the list of file lines
    # j = 0
    # for i in filestreamLines:                           # Enumerate through each line in the line list
    #     if i == "\n":                                   # If line only contains newline character
    #         del filestreamLines[j]                      # then delete the line
    #     j += 1


    offsetList = []
    for i in filestreamLines:                           # Enumerate through each line in the line list
        currentLine = i.split(",")                      # Split out the currently enumerated line according to CSV
        print(currentLine)
        lineTimestamp = float(currentLine[1])           # Get the column that should contain the UTC value

        aTime = lineTimestamp
        bTime = indexTime
        deltaSeconds = (bTime - aTime)                  # Find the difference between the index'd value and the file value
        print(deltaSeconds)

        if deltaSeconds <= 86400:                       # if the difference is less than or equal to 24 hours
            currentOffsetVal = str(currentLine[4])      # Get column that should contain the offset value
            try:
                offsetList.append(float(currentOffsetVal))
            except:
                print("\"{}\" was not a number".format(currentOffsetVal))


    return offsetList

time2 = time.time()

listVals = loadOffsetValues("C:\\Users\\Micah\\Downloads\\1245620-2.csv",time2)

print(listVals)
print(len(listVals))