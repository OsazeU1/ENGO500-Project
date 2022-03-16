from bitstring import *
from pandas import *
import openpyxl
import dictonaries as d
from tkinter import *
from tkinter import filedialog
from classes import *
import csv

# REMEMBER FUNCTIONS IN THE APPLICATION ARE DIFFERENT THAN THE ONES HERE"


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
        #print("fullcommand: ")
        # print(fullcommand)
        # print('\n')
        # Takes the sync "#" for ASCII
        sync = fullcommand[0]
        print("sync: " + sync)

        # Ex. full_command = "#BestPosA", command = "BestPos"
        command = fullcommand[:-1]
        command = command[1:]

        if sync == "#":
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
        elif sync == "%":
            parsedheader.append([sync, command])
            #print (parsedheader)
            # print('\n')
        elif sync == "$":
            parsedheader.append([sync, command])

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
        elif log_name == "BESTGNSSPOS":
            newBody = BESTGNSSPOS()
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


def GetBESTGNSSPOS(filename, GNSSLines):
    Data = []

    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "BESTGNSSPOS":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds
            solstat_message = GNSSLine.body.solstat_message
            postype_message = GNSSLine.body.postype_message
            lat = GNSSLine.body.lat
            lon = GNSSLine.body.lon
            hgt = GNSSLine.body.hgt
            undulation = GNSSLine.body.undulation
            datum = GNSSLine.body.datum
            latsigma = GNSSLine.body.latsigma
            lonsigma = GNSSLine.body.lonsigma
            hgtsigma = GNSSLine.body.hgtsigma
            stnid = GNSSLine.body.stnid
            diff_age = GNSSLine.body.diff_age
            sol_age = GNSSLine.body.sol_age
            numberoftrackedsats = GNSSLine.body.numberoftrackedsats
            numberofsatsinsol = GNSSLine.body.numberofsatsinsol
            numberofL1sats = GNSSLine.body.numberofL1sats
            numberofmultisats = GNSSLine.body.numberofmultisats
            reserved = GNSSLine.body.reserved
            extsolstat_message = GNSSLine.body.extsolstat_message
            galbei_message = GNSSLine.body.galbei_message
            gpsglo_sigmask = GNSSLine.body.gpsglo_sigmask
            crc = GNSSLine.body.crc

            textline = [week, seconds, solstat_message, postype_message, lat, lon, hgt, undulation, datum, latsigma, lonsigma, stnid, diff_age,
                        sol_age, numberoftrackedsats, numberofL1sats, numberofmultisats, reserved, extsolstat_message, galbei_message, gpsglo_sigmask, crc]
            Data.append(textline)
        else:
            continue
    WriteData("BESTGNSSPOS for ", filename, Data)
    name = getName(filename, ".asc")
    print("BESTGNSSPOS csv file for " + name + " created!")
    return


def getName(filename, ext):
    name = filename.split('/')
    name = name[-1]
    # removes the extention (ex. ".asc", ".txt", etc.)
    tempname = name[:-4]
    name = tempname
    name = name + ext
    return name


def WriteData(prefix, filename, Data):
    name = getName(filename, ".csv")
    newfilename = prefix + name
    mycsv = open(newfilename, "w+")
    csvWriter = c.writer(mycsv, delimiter=',')
    csvWriter.writerows(Data)
    return


if __name__ == "__main__":
    print("Running functions.py")
