from bitstring import *
from pandas import *
import openpyxl
import dictonaries as d
from tkinter import *
from tkinter import filedialog
from classes import *
import csv

## REMEMBER FUNCTIONS IN THE APPLICATION ARE DIFFERENT THAN THE ONES HERE" 

def exceltodict(filename):
    xls = ExcelFile(filename)
    df = xls.parse(xls.sheet_names[0])
    print(df.to_dict())
    return


# Splits long line from ASCII file into the header and body
def GetHeaderBody(line):
    splitline = line.split(";")
    header = []
    # array of headers incase of rxconfig
    numofheaders = len(splitline) - 1
    for i in range(0, numofheaders):
        header.append(splitline[i])
    body = splitline[numofheaders]
    return [header, body]



# Takes the Split off Header and breaks it down into all components as listen on NovAtel website
def ParseHeader(header):
    parsedheader = []
    for i in range(0, len(header)):
        splitheader = header[i].split(",")
        fullcommand = splitheader[0]

        # Takes the sync "#" for ASCII
        sync = fullcommand[fullcommand.index("#")]

        # Ex. full_command = "#BestPosA", command = "BestPos"
        command = fullcommand[:-1]
        command = command[1:]

        port = splitheader[1]
        sequence = splitheader[2]
        idletime = splitheader[3]
        timestatus = splitheader[4]
        week = splitheader[5]
        seconds = splitheader[6]
        recieverstatus = splitheader[7]
        reserved = splitheader[8]
        recieversw = splitheader[9]

        # Translating Codes to messages using disctonary
        timestatus_message = d.gpsref_timestatus[timestatus]

        parsedheader.append([sync, command, port, sequence, idletime,
                            timestatus_message, week, seconds, recieverstatus, reserved, recieversw])

    return parsedheader

# Splits the crc end code from the main body
def SplitBodyMessage(line):
    split = line.split("*")
    crc = split[1]
    mainbody = split[0]
    return[mainbody, crc]

# Unfinished: Hex to Binary Conversion
def BytesToBinary(bytes_str):
    binary_str = BitArray(hex=bytes_str)
    binary_str.bin[2:]
    return binary_str

# Full process that takes in a file and turns it into an array of GNSSFiles
# each with their consistant header objects and varying body objects depending on the log/command of the header
def ParseFile(filename):
    GNSSLines = []
    file = open(filename, 'r')
    lines = file.readlines()
    numberoflines = 0

    for line in lines:
        numberoflines += 1

        [header, body] = GetHeaderBody(line)
        parsedheader = ParseHeader(header)
        newHeader = Header()
        newHeader.Parse(parsedheader)
        log_name = newHeader.command
        # Checks for the command and creates object accordingly
        if log_name == "BESTPOS":
            newBody = BESTPOS()
        else:
            newBody = None

        newBody.Parse(body)

        newGNSSLine = GNSSLine(newHeader, newBody)
        GNSSLines.append(newGNSSLine)
        return GNSSLines


def GetPositioningData(filename, GNSSLines):
    Data = []

    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "BESTPOS":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds
            stnid = GNSSLine.body.stnid
            numberofsatsinsol = GNSSLine.body.numberofsatsinsol
            numberofL1 = GNSSLine.body.numberofL1sats
            numberofmultisats = GNSSLine.body.numberofmultisats
            lat = GNSSLine.body.lat
            latsigma = GNSSLine.body.latsigma
            lon = GNSSLine.body.lon
            lonsigma = GNSSLine.body.lonsigma
            hgt = GNSSLine.body.hgt
            hgtsigma = GNSSLine.body.hgtsigma
            und = GNSSLine.body.undulation

            textline = [week, seconds, stnid, numberofsatsinsol,
                        numberofL1, numberofmultisats, lat, latsigma, lon, lonsigma, hgt, hgtsigma, und]
            Data.append(textline)
        else:
            continue
    WriteData("PositioningDatafor", filename, Data)
    return


def WriteData(prefix, filename, Data):
    newfilename = prefix + filename
    mycsv = open(newfilename, "w+")
    csvWriter = csv.writer(mycsv, delimiter=',')
    csvWriter.writerows(Data)
    return


if __name__ == "__main__":
    print("Running functions.py")
