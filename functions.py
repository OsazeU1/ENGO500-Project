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
    check = line.split(",")
    first_string = check[0]
    # print(first_string[0])
    header = []
    # In the cases of "#" and "%" sync's the body variable is a long string with ","
    if first_string[0] != "$":
        splitline = line.split(";")
        # array of headers incase of rxconfig (usually numofheaders is 1)
        numofheaders = len(splitline) - 1
        for i in range(0, numofheaders):
            header.append(splitline[i])
        body = splitline[numofheaders]
    # In the cases of "$" the body variable is an already separated array
    else:
        body = []
        header.append(first_string)
        for i in range(1, len(check)):
            body.append(check[i])

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
        #print("sync: " + sync)

        if sync == "#":
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
        elif sync == "%":
            # Ex. full_command = "#BestPosA", command = "BestPos"
            command = fullcommand[:-1]
            command = command[1:]
            week = splitheader[1]
            seconds = splitheader[2]
            parsedheader.append([sync, command, week, seconds])
            #print (parsedheader)
            # print('\n')
        elif sync == "$":
            command = fullcommand[1:]
            #print("test: ")
            # print(command)
            # print('\n')
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
        # ~~~~ DEBUGING ~~~~~~#
        #print("header: ")
        # print(header)
        # print('\n')
        #print("body: ")
        # print(body)
        parsedheader = ParseHeader(header)
        newHeader = Header()
        # print(numberoflines)
        # print('\n')
        newHeader.Parse(parsedheader)
        log_name = newHeader.command
        #print (parsedheader)
        # Checks for the command and creates object accordingly
        if log_name == "BESTPOS":
            newBody = BESTPOS()
        elif log_name == "BESTGNSSPOS":
            newBody = BESTGNSSPOS()
        elif log_name == "INSPVAX":
            newBody = INSPVAX()
        elif log_name == "RANGE":
            newBody = RANGE()
        elif log_name == "TRACKSTAT":
            newBody = TRACKSTAT()
        elif log_name == "SATVIS2":
            newBody = SATVIS2()
        elif log_name == "RAWIMUSX":
            newBody = RAWIMUSX()
        elif log_name == "HEADING2":
            newBody = HEADING2()
        elif log_name == "PASSTHROUGH":
            newBody = PASSTHROUGH()
        else:
            newBody = NoBody()

        newBody.Parse(body)

        newGNSSLine = GNSSLine(newHeader, newBody)
        GNSSLines.append(newGNSSLine)

    name = getName(filename, ".asc")
    print("Parse of " + name + " Successful!")
    return GNSSLines


def GetPositioningData(filename, GNSSLines):
    header = ["week", "seconds", "stnid", "numberofsatsinsol", "numberofL1",
              "numberofmultisats", "lat", "latsigma", "lon", "lonsigma", "hgt", 'hgtsigma', 'und']
    Data = []
    Data.append(header)

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

    WriteData("Positioning Data for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("Positioning Data csv for " + name + " created!")
    return


def GetBESTGNSSPOS(filename, GNSSLines):
    header = ["week", "seconds", "solstat_message", "position type_message", "lat", "lon", "hgt", "undulation", "datum", "latsigma", "lonsigma", "hgtsigma", "stationid", "differential_age",
              "solution_age", "numberoftrackedsats", "numberofL1sats", "numberofmultisats", "reserved", "Extended solution status ", "Galileo and BeiDou sig mask", "GPS and GLONASS sig mask", "32 Bit crc"]
    Data = []
    Data.append(header)
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

            textline = [week, seconds, solstat_message, postype_message, lat, lon, hgt, undulation, datum, latsigma, lonsigma, hgtsigma, stnid, diff_age,
                        sol_age, numberoftrackedsats, numberofL1sats, numberofmultisats, reserved, extsolstat_message, galbei_message, gpsglo_sigmask, crc]
            Data.append(textline)
        else:
            continue
    WriteData("BESTGNSSPOS for ", filename, Data)
    name = getName(filename, ".asc")
    print("BESTGNSSPOS csv file for " + name + " created!")
    return


def GetINSPVAX(filename, GNSSLines):
    header = ['week', 'seconds', 'INSstatus_message', 'postype_message', 'lat', 'lon', 'hgt', 'undulation', 'northvel', 'eastvel', 'upvel', 'roll', 'pitch', 'azimuth', 'latsigma',
              'lonsigma', 'hgtsigma', 'northvelsigma', 'eastvelsigma', 'upvelsigma', 'rollsigma', 'pitchsigma', 'azimuthsigma', 'Extended solution status', 'Time Since Update']
    Data = []
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "INSPVAX":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds

            instatus_message = GNSSLine.body.instatus_message
            postype_message = GNSSLine.body.postype_message
            lat = GNSSLine.body.lat
            lon = GNSSLine.body.lon
            hgt = GNSSLine.body.hgt
            undulation = GNSSLine.body.undulation

            northvel = GNSSLine.body.northvel
            eastvel = GNSSLine.body.eastvel
            upvel = GNSSLine.body.upvel
            roll = GNSSLine.body.roll
            pitch = GNSSLine.body.pitch
            azimuth = GNSSLine.body.azimuth

            latsigma = GNSSLine.body.latsigma
            lonsigma = GNSSLine.body.lonsigma
            hgtsigma = GNSSLine.body.hgtsigma
            northvelsigma = GNSSLine.body.northvelsigma
            eastvelsigma = GNSSLine.body.eastvelsigma
            upvelsigma = GNSSLine.body.upvelsigma
            rollsigma = GNSSLine.body.rollsigma
            pitchsigma = GNSSLine.body.pitchsigma
            azimuthsigma = GNSSLine.body.azimuthsigma
            extsolstat_message = GNSSLine.body.extsolstat_message
            tsu = GNSSLine.body.tsu

            textline = [week, seconds, instatus_message, postype_message, lat, lon, hgt, undulation, northvel, eastvel, upvel, roll, pitch, azimuth, latsigma,
                        lonsigma, hgtsigma, northvelsigma, eastvelsigma, upvelsigma, rollsigma, pitchsigma, azimuthsigma, extsolstat_message, tsu]
            Data.append(textline)
        else:
            continue
    WriteData("INSPVAX for ", filename, Data)
    name = getName(filename, ".asc")
    print("INSPVAX csv file for " + name + " created!")
    return


def GetRANGE(filename, GNSSLines):
    header = ["PRN", "glofreq", "pseudorange measurement", "pseudorange sigma", "carrier phase",
              "carrier phase sigma", "soppler freq", "Carrier to noise density ratio", "locktime", "tracking status"]
    Data = []
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "RANGE":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds
            PRNobs = GNSSLine.body.PRNobs
            for i in range(0, len(PRNobs)):
                textline = PRNobs[i]
                Data.append(textline)

    WriteData("RANGE for ", filename, Data)
    name = getName(filename, ".asc")
    print("RANGE csv file for " + name + " created!")
    return


def GetTRACKSTAT(filename, GNSSLines):

    Data = []
    header = ["solution status", "position type", "GPS tracking elevation cut-off angle", "PRN", "glofreq", "tracking status", "pseudorange measurement",
              "doppler freq", "Carrier to noise density ratio", "locktime", "pseudorange residual", "range reject code", "pseudorange filter weighting"]
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "TRACKSTAT":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds
            solstat_message = GNSSLine.body.solstat_message
            postype_message = GNSSLine.body.postype_message
            cutoff = GNSSLine.body.cutoff
            PRNobs = GNSSLine.body.PRNobs
            for i in range(0, len(PRNobs)):
                textline = PRNobs[i]

                textline.insert(0, solstat_message)
                textline.insert(1, postype_message)
                textline.insert(2, cutoff)

                Data.append(textline)

    WriteData("TRACKSTAT for ", filename, Data)
    name = getName(filename, ".asc")
    print("TRACKSTAT csv file for " + name + " created!")
    return


def GetSATVIS2(filename, GNSSLines):
    Data = []
    header = ["Satellite System", "satellite visibility", "complete almanac ", "Satellite ID", "Satellite health", "Elevation(degrees)", "Azimuth (degrees)",
              "doppler freq", "Theoretical Doppler", "Apparent Doppler"]
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "SATVIS2":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds

            satsystem = GNSSLine.body.satsystem
            satvis_message = GNSSLine.body.satvis_message
            almanacflag_message = GNSSLine.body.almanacflag_message

            SATobs = GNSSLine.body.SATobs
            for i in range(0, len(SATobs)):
                textline = SATobs[i]

                textline.insert(0, satsystem)
                textline.insert(1, satvis_message)
                textline.insert(2, almanacflag_message)

                Data.append(textline)

    WriteData("SATVIS2 for ", filename, Data)
    name = getName(filename, ".asc")
    print("SATVIS2 csv file for " + name + " created!")
    return


def GetRAWIMUSX(filename, GNSSLines):
    Data = []
    header = ['IMU Info Bits', 'imutype', 'gnssweek', 'gnssweekseconds', 'imustatus',
              'zaccel', 'yaccel', 'xaccel', 'zgyro', 'ygyro', 'xgyro']
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "RAWIMUSX":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds

            imuinfo = GNSSLine.body.imuinfo
            imutype = GNSSLine.body.imu
            gnssweek = GNSSLine.body.gnssweek
            gnssweekseconds = GNSSLine.body.gnssweekseconds
            imustatus = GNSSLine.body.imustatus_message
            zaccel = GNSSLine.body.zaccel
            yaccel = GNSSLine.body.yaccel
            xaccel = GNSSLine.body.xaccel
            zgyro = GNSSLine.body.zgyro
            ygyro = GNSSLine.body.ygyro
            xgyro = GNSSLine.body.xgyro

            textline = [imuinfo, imutype, gnssweek, gnssweekseconds, imustatus,
                        zaccel, yaccel, xaccel, zgyro, ygyro, xgyro]
            Data.append(textline)
    WriteData("RAWIMUSX for ", filename, Data)
    name = getName(filename, ".asc")
    print("RAWIMUSX csv file for " + name + " created!")
    return


def GetHEADING2(filename, GNSSLines):
    Data = []
    header = ['solstat', 'postype', 'length', 'heading', 'pitch', 'reserved', 'hdgsigma', 'pitchdigma', 'roverid', 'masterstnid',
              'numberofsats', 'numberofsatsinsol', 'numberofobs', 'numberofmultisats', 'solsource', 'ess', 'galbei', 'gpsglo']
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "HEADING2":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds

            solstat = GNSSLine.body.solstat_message
            postype = GNSSLine.body.postype_message
            length = GNSSLine.body.length
            heading = GNSSLine.body.heading
            pitch = GNSSLine.body.pitch
            reserved = GNSSLine.body.reserved
            hdgsigma = GNSSLine.body.hdgsigma
            pitchdigma = GNSSLine.body.pitchdigma
            roverid = GNSSLine.body.roverid
            masterstnid = GNSSLine.body.masterstnid
            numberofsats = GNSSLine.body.numberofsats
            numberofsatsinsol = GNSSLine.body.numberofsatsinsol
            numberofobs = GNSSLine.body.numberofobs
            numberofmultisats = GNSSLine.body.numberofmultisats
            solsource = GNSSLine.body.solsource
            ess = GNSSLine.body.extsolstat_message
            galbei = GNSSLine.body.galbei_message
            gpsglo = GNSSLine.body.gpsglo_message

            textline = [solstat, postype, length, heading, pitch, reserved, hdgsigma, pitchdigma, roverid, masterstnid,
                        numberofsats, numberofsatsinsol, numberofobs, numberofmultisats, solsource, ess, galbei, gpsglo]
            Data.append(textline)

    WriteData("HEADING2 for ", filename, Data)
    name = getName(filename, ".asc")
    print("HEADING2 csv file for " + name + " created!")
    return


def GetPASSTHROUGH(filename, GNSSLines):
    Data = []
    header = ['week','seconds', 'port', 'numberofbytes', 'data']
    Data.append(header)
    if filename == None:
        return

    print("InGPD: " + filename)
    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "PASSTHROUGH":
            week = GNSSLine.header.week
            seconds = GNSSLine.header.seconds

            port = GNSSLine.body.port
            numberofbytes = GNSSLine.body.numberofbytes
            data = GNSSLine.body.data

            textline = [week, seconds, port, numberofbytes, data]
            Data.append(textline)

    WriteData("PASSTHROUGH for ", filename, Data)
    name = getName(filename, ".asc")
    print("PASSTHROUGH csv file for " + name + " created!")
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
    mycsv = open(newfilename, 'w', newline='')
    csvWriter = c.writer(mycsv, delimiter=',')
    csvWriter.writerows(Data)
    return


if __name__ == "__main__":
    print("Running functions.py")
