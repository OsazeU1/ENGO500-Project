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


# Takes the Split off Header and breaks it down into all components as listed on NovAtel website
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


def GetMessage(hex, dict):
    binary = "{0:08b}".format(int(str(hex), 16))
    binary = str(binary)
    binary_message = ""
    bit = 7
    for i in range(0, 7):
        if binary[bit] == str(1):
            temp = dict[str(7-bit)]
            binary_message = binary_message + temp + ", "
            bit = bit - 1
    return binary_message

# Full process that takes in a file and turns it into an array of GNSSFiles
# each with their consistant header objects and varying body objects depending on the log/command of the header


def ParseFile(filename):
    GNSSLines = []
    file = open(filename, 'r', encoding="mbcs")
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
        elif log_name == "GPGSA":
            newBody = GPGSA()
        elif log_name == "GPGGA":
            newBody = GPGGA()
        elif log_name == "PASHR":
            newBody = PASHR()
        elif log_name == "GPGST":
            newBody = GPGST()
        elif log_name == "GPVTG":
            newBody = GPVTG()
        elif log_name == "GPHDT":
            newBody = GPHDT()
        elif log_name == "GPZDA":
            newBody = GPZDA()
        elif log_name == "GPGSV":
            newBody = GPGSV()
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
              "numberofmultisats", "lat", "latsigma", "lon", "lonsigma", "hgt", 'hgtsigma', 'und', "GPS and GLONASS Signals Used", "Galileo and BeiDou Signals Used"]
    Data = []
    Data.append(header)

    if filename == None:
        return

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
            gpsglo_message = GNSSLine.body.gpsglo_message
            galbei_message = GNSSLine.body.galbei_message
            textline = [week, seconds, stnid, numberofsatsinsol,
                        numberofL1, numberofmultisats, lat, latsigma, lon, lonsigma, hgt, hgtsigma, und, gpsglo_message, galbei_message]
            Data.append(textline)

    WriteData("Positioning Data for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("Positioning Data csv for " + name + " created!")
    return


def GetBESTGNSSPOS(filename, GNSSLines):
    header = ["week", "seconds", "solstat_message", "position type_message", "lat", "lon", "hgt", "undulation", "datum", "latsigma", "lonsigma", "hgtsigma", "stationid", "differential_age",
              "solution_age", "numberoftrackedsats", "numberofL1sats", "numberofmultisats", "reserved", "Extended solution status ", "GPS and GLONASS Signals Used", "Galileo and BeiDou Signals Used", "32 Bit crc"]
    Data = []
    Data.append(header)
    if filename == None:
        return

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
            gpsglo_message = GNSSLine.body.gpsglo_message
            crc = GNSSLine.body.crc

            textline = [week, seconds, solstat_message, postype_message, lat, lon, hgt, undulation, datum, latsigma, lonsigma, hgtsigma, stnid, diff_age,
                        sol_age, numberoftrackedsats, numberofL1sats, numberofmultisats, reserved, extsolstat_message,  gpsglo_message, galbei_message, crc]
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
    header = ['week', 'seconds', 'port', 'numberofbytes', 'data']
    Data.append(header)
    if filename == None:
        return

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


def GetGPGSA(filename, GNSSLines):
    header = ["modema", "mode123", "prn1", "prn2", "prn3", "prn4", "prn5",
              "prn6", "prn7", "prn8", "prn9", "prn10", "prn11", "prn12", "pdop", "hdop", "vdop"]
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPGSA":
            modema = GNSSLine.body.modema
            mode123 = GNSSLine.body.mode123
            prn1 = GNSSLine.body.prn1
            prn2 = GNSSLine.body.prn2
            prn3 = GNSSLine.body.prn3
            prn4 = GNSSLine.body.prn4
            prn5 = GNSSLine.body.prn5
            prn6 = GNSSLine.body.prn6
            prn7 = GNSSLine.body.prn7
            prn8 = GNSSLine.body.prn8
            prn9 = GNSSLine.body.prn9
            prn10 = GNSSLine.body.prn10
            prn11 = GNSSLine.body.prn11
            prn12 = GNSSLine.body.prn12
            pdop = GNSSLine.body.pdop
            hdop = GNSSLine.body.hdop
            vdop = GNSSLine.body.vdop

            textline = [modema, mode123, prn1, prn2, prn3, prn4, prn5,
                        prn6, prn7, prn8, prn9, prn10, prn11, prn12, pdop, hdop, vdop]
            Data.append(textline)

    WriteData("GPGSA for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPGSA .csv file for " + name + " created!")
    return


def GetGPGGA(filename, GNSSLines):
    header = ["utc", "lat", "latdir", "lon", "londir", "quality", "numofsats", "hdop",
              "antennaalt", "antennaunits", "und", "undunits", "correctiondataage", "stnid"]
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPGGA":
            utc = GNSSLine.body.utc
            lat = GNSSLine.body.lat
            latdir = GNSSLine.body.latdir
            lon = GNSSLine.body.lon
            londir = GNSSLine.body.londir
            quality = GNSSLine.body.quality
            numofsats = GNSSLine.body.numofsats
            hdop = GNSSLine.body.hdop
            antennaalt = GNSSLine.body.antennaalt
            antennaunits = GNSSLine.body.antennaunits
            und = GNSSLine.body.und
            undunits = GNSSLine.body.undunits
            correctiondataage = GNSSLine.body.correctiondataage
            stnid = GNSSLine.body.stnid

            textline = [utc, lat, latdir, lon, londir, quality, numofsats, hdop,
                        antennaalt, antennaunits, und, undunits, correctiondataage, stnid]
            Data.append(textline)

    WriteData("GPGGA for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPGGA .csv file for " + name + " created!")
    return


def GetGPZDA(filename, GNSSLines):
    header = ['utc', 'day', 'month', 'year']
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPZDA":
            utc = GNSSLine.body.utc
            day = GNSSLine.body.day
            month = GNSSLine.body.month
            year = GNSSLine.body.year

            textline = [utc, day, month, year]
            Data.append(textline)

    WriteData("GPZDA for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPZDA .csv file for " + name + " created!")
    return


def GetPASHR(filename, GNSSLines):
    header = ['time', 'heading', 'trueheading', 'roll', 'pitch', 'heave', 'rollaccuracy',
              'pitchaccuracy', 'headingaccuracy', 'gpsupqual', 'instatflag', 'checksum']
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "PASHR":
            time = GNSSLine.body.time
            heading = GNSSLine.body.heading
            trueheading = GNSSLine.body.trueheading
            roll = GNSSLine.body.roll
            pitch = GNSSLine.body.pitch
            heave = GNSSLine.body.heave
            rollaccuracy = GNSSLine.body.rollaccuracy
            pitchaccuracy = GNSSLine.body.pitchaccuracy
            headingaccuracy = GNSSLine.body.headingaccuracy
            gpsupqual = GNSSLine.body.gpsupqual
            instatflag = GNSSLine.body.instatflag
            checksum = GNSSLine.body.checksum

            textline = [time, heading, trueheading, roll, pitch, heave, rollaccuracy,
                        pitchaccuracy, headingaccuracy, gpsupqual, instatflag, checksum]
            Data.append(textline)

    WriteData("PASHR for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("PASHR .csv file for " + name + " created!")
    return


def GetGPGST(filename, GNSSLines):
    header = ['utc', 'rms', 'semimjrstd', 'semimnrstd',
              'orient', 'latstd', 'lonstd', 'altitudestd', 'checksum']
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPGST":
            utc = GNSSLine.body.utc
            rms = GNSSLine.body.rms
            semimjrstd = GNSSLine.body.semimjrstd
            semimnrstd = GNSSLine.body.semimnrstd
            orient = GNSSLine.body.orient
            latstd = GNSSLine.body.latstd
            lonstd = GNSSLine.body.lonstd
            altstd = GNSSLine.body.altstd
            checksum = GNSSLine.body.checksum

            textline = [utc, rms, semimjrstd, semimnrstd,
                        orient, latstd, lonstd, altstd, checksum]
            Data.append(textline)

    WriteData("GPGST for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPGST Data for " + name + " created!")
    return


def GetGPVTG(filename, GNSSLines):
    header = ['tracktrue', 'T', 'trackmag', 'M', 'speedoverground',
              'nauticalspeedunits (N = knots)', 'speed', 'speedindicator (K = km/h)', 'nmeaposmode']
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPVTG":
            tracktrue = GNSSLine.body.tracktrue
            T = GNSSLine.body.T
            trackmag = GNSSLine.body.trackmag
            M = GNSSLine.body.M
            speedoverground = GNSSLine.body.speedoverground
            nauticalspeedunits = GNSSLine.body.nauticalspeedunits
            speed = GNSSLine.body.speed
            speedindicator = GNSSLine.body.speedindicator
            nmeaposmode = GNSSLine.body.nmeaposmode
            textline = [tracktrue, T, trackmag, M, speedoverground,
                        nauticalspeedunits, speed, speedindicator, nmeaposmode]
            Data.append(textline)

    WriteData("GPVTG for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPVTG .csv file for " + name + " created!")
    return


def GetGPGSV(filename, GNSSLines):
    header = ['prn', 'elev', 'azimuth', 'snr', 'gnsssystem', 'signaltype']
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPGSV":
            satinfo = GNSSLine.body.satinfo
            sysname = GNSSLine.body.sysname
            syssignal = GNSSLine.body.syssignal

            for i in range(0, len(satinfo)):
                textline = satinfo[i]
                textline.append(sysname)
                textline.append(syssignal)
                Data.append(textline)

    WriteData("GPGSV for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPGSV .csv file for " + name + " created!")
    return


def GetGPHDT(filename, GNSSLines):
    header = ["Heading in degrees", "Degrees True"]
    Data = []
    Data.append(header)

    if filename == None:
        return

    for GNSSLine in GNSSLines:
        textline = []
        if GNSSLine.header.command == "GPHDT":
            headingdeg = GNSSLine.body.headingdeg
            degtrue = GNSSLine.body.degtrue

            textline = [headingdeg, degtrue]
            Data.append(textline)

    WriteData("GPHDT for ", filename, Data)
    name = getName(filename, ".asc")
    # print(Data)
    print("GPHDT .csv file for " + name + " created!")
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
    directoryname = filename.split('/')
    temp = ""
    for i in range(0, len(directoryname) - 1):
        temp = temp + directoryname[i] + "/"
    directoryname = temp
    name = getName(filename, ".csv")
    newfilename = prefix + name
    #print("TESTING THIS: " + directoryname + newfilename)
    mycsv = open(directoryname + newfilename, 'w',
                 encoding="utf-8", newline='')
    csvWriter = c.writer(mycsv, delimiter=',')
    csvWriter.writerows(Data)
    return


if __name__ == "__main__":
    print("Running functions.py")
