import dictonaries as d
import functions as func
import tkinter as tk
from tkinter import filedialog
from time import sleep
# for application to not freakout
import csv as c

# GNSS header class, always the same for all messages


class Header:
    def __init__(self):
        return

    def Parse(self, header):
        rxconfig = False
        # checks if its an rxconfig header which has the header then the subseqent log header
        if len(header) > 2:
            # takes the next log header as the main header
            header = [header[1]]
            rxconfig = True


        # assigning variables
        print(header)
        print('\n')
        temp = header[0]
        if temp[0] == "#":
            [sync, command, port, sequence, idletime,
            timestatus_message, week, seconds, recieverstatus, reserved, recieversw] = header[0]
            self.sync = sync
            self.command = command
            self.port = port
            self.sequence = sequence
            self.idletime = idletime
            self.timestatus_message = timestatus_message
            self.week = week
            self.seconds = seconds
            self.recieverstatus = recieverstatus
            self.reserved = reserved
            self.recieversw = recieversw
            self.rxconfig = rxconfig
        elif temp[0] == "%":
            [sync, command] = header[0]
            self.sync = sync
            self.command = command
        elif temp[0] == "$":
            [sync, command] = header[0]
            self.sync = sync
            self.command = command
        return

# Fully parsed gnss line


class GNSSLine:
    def __init__(self, header, body):
        # always the same
        self.header = header
        # varies depending on log command (header.command)
        self.body = body

# Types of Bodys


class BESTPOS:
    def __init__(self):
        return
    # takes the split off body message (after ";")

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")

        # assigning variables and translating codes to messages
        solstat = mainbody[0]
        solstat_message = d.bestpos_solutionsstatus[solstat]

        postype = mainbody[1]
        postype_message = d.bestpos_posveltype[postype]

        lat = mainbody[2]
        lon = mainbody[3]
        hgt = mainbody[4]
        undulation = mainbody[5]

        datumid = mainbody[6]
        if (datumid == 61):
            datum = "WGS84"
        elif (datumid == 63):
            datum = "USER"
        else:
            datum = "ERROR"

        latsigma = mainbody[7]
        lonsigma = mainbody[8]
        hgtsigma = mainbody[9]
        stnid = mainbody[10]
        diff_age = mainbody[11]
        sol_age = mainbody[12]
        numberoftrackedsats = mainbody[13]
        numberofsatsinsol = mainbody[14]
        numberofL1sats = mainbody[15]
        numberofmultisats = mainbody[16]
        reserved = mainbody[17]
        extsolstat = mainbody[18]
        galbei_sigmask = mainbody[19]
        gpsglo_sigmask = mainbody[20]

        extsolstat_message = d.bestpos_ess[extsolstat]
        galbei_message = "WIP"
        gpsglo_message = "WIP"
        #galbei_message = d.bestpos_galbei_sigmask[galbei_sigmask]
        #gpsglo_message = d.bestpos_gpsglo_sigmask[gpsglo_sigmask]

        # Assigning Local Variables
        self.solstat_message = solstat_message
        self.postype_message = postype_message
        self.lat = lat
        self.lon = lon
        self.hgt = hgt
        self.undulation = undulation
        self.datum = datum
        self.latsigma = latsigma
        self.lonsigma = lonsigma
        self.hgtsigma = hgtsigma
        self.stnid = stnid
        self.diff_age = diff_age
        self.sol_age = sol_age
        self.numberoftrackedsats = numberoftrackedsats
        self.numberofsatsinsol = numberofsatsinsol
        self.numberofL1sats = numberofL1sats
        self.numberofmultisats = numberofmultisats
        self.reserved = reserved
        self.extsolstat_message = extsolstat_message
        self.galbei_message = galbei_message
        self.gpsglo_sigmask = gpsglo_sigmask
        self.crc = crc
        return


class NoBody:
    def __init__(self):
        return

    def Parse(self, body_message):
        self.type = None
        return

# Unfinished


class BESTGNSSPOS:
    def __init__(self):
        return

    # takes the split off body message (after ";")
    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")

        # assigning variables and translating codes to messages
        solstat = mainbody[0]
        solstat_message = d.bestpos_solutionsstatus[solstat]

        postype = mainbody[1]
        postype_message = d.bestpos_posveltype[postype]

        lat = mainbody[2]
        lon = mainbody[3]
        hgt = mainbody[4]
        undulation = mainbody[5]

        datumid = mainbody[6]
        if (datumid == 61):
            datum = "WGS84"
        elif (datumid == 63):
            datum = "USER"
        else:
            datum = "ERROR"

        latsigma = mainbody[7]
        lonsigma = mainbody[8]
        hgtsigma = mainbody[9]
        stnid = mainbody[10]
        diff_age = mainbody[11]
        sol_age = mainbody[12]
        numberoftrackedsats = mainbody[13]
        numberofsatsinsol = mainbody[14]
        numberofL1sats = mainbody[15]
        numberofmultisats = mainbody[16]
        reserved = mainbody[17]
        extsolstat = mainbody[18]
        galbei_sigmask = mainbody[19]
        gpsglo_sigmask = mainbody[20]

        extsolstat_message = d.bestpos_ess[extsolstat]
        galbei_message = "WIP"
        gpsglo_message = "WIP"
        #galbei_message = d.bestpos_galbei_sigmask[galbei_sigmask]
        #gpsglo_message = d.bestpos_gpsglo_sigmask[gpsglo_sigmask]

        # Assigning Local Variables
        self.solstat_message = solstat_message
        self.postype_message = postype_message
        self.lat = lat
        self.lon = lon
        self.hgt = hgt
        self.undulation = undulation
        self.datum = datum
        self.latsigma = latsigma
        self.lonsigma = lonsigma
        self.hgtsigma = hgtsigma
        self.stnid = stnid
        self.diff_age = diff_age
        self.sol_age = sol_age
        self.numberoftrackedsats = numberoftrackedsats
        self.numberofsatsinsol = numberofsatsinsol
        self.numberofL1sats = numberofL1sats
        self.numberofmultisats = numberofmultisats
        self.reserved = reserved
        self.extsolstat_message = extsolstat_message
        self.galbei_message = galbei_message
        self.gpsglo_sigmask = gpsglo_sigmask
        self.crc = crc
        return


# Unfinished
class TRACKSTAT:
    def __init__(self):
        return

# Unfinished


class LBANDBEAMTABLE:
    def __init__(self, message):
        self.message = message

        def Parse(message):
            [mainbody, crc] = func.SplitBodyMessage(message)
            mainbody = mainbody.split(",")
            numberofentries = mainbody[0]
            entries = [[]]
            counter = 0
            temp = []
            # Start a 1 to ignore number of entries
            for i in range(1, numberofentries*8):
                temp.append(mainbody[i])
                counter += 1
                if counter % 8 == 0:
                    entries.append(temp)
                    temp = []
                    counter = 0

            self.numberofentries = numberofentries
            self.entries = entries


# Windows Application (.exe)
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.openbutton = tk.Button(
            master, text="Open ASCII File", command=self.openFile)
        master.geometry("600x600")
        master.title("GNSS Data Parser")
        self.openbutton.pack()
        self.filename = None

        self.printbutton = tk.Button(
            master, text="Display Current File", command=self.printFilename)
        self.printbutton.pack()

        self.parsebutton = tk.Button(
            master, text="Parse Data", command=self.ParseFile)
        self.parsebutton.pack()

        self.ebutton = tk.Button(
            master, text="Display Galileo and BeiDou Signals", command=None)
        self.ebutton.pack()

        self.fbutton = tk.Button(
            master, text="Display GPS and GLONASS Signals", command=None)
        self.fbutton.pack()

        self.GNSSLines = []
        self.getpositionsbutton = tk.Button(
            text="Get Positioning Information", command=self.GetPositioningData)
        self.getpositionsbutton.pack()

        self.abutton = tk.Button(
            text="Get BESTGNSSPOS Information", command=self.GetBESTGNSSPOS)
        self.abutton.pack()

        self.bbutton = tk.Button(
            text="Get Satellite Information", command=None)
        self.bbutton.pack()

        self.cbutton = tk.Button(
            text="Get Frequency Information", command=None)
        self.cbutton.pack()

        self.dbutton = tk.Button(
            text="Get Device Position Information", command=None)
        self.dbutton.pack()

    def openFile(self):
        self.filename = filedialog.askopenfilename(initialdir="C:\\",
                                                   title="Select ASCII File",
                                                   filetypes=(("text files", "*.asc"),
                                                              ("all files", "*.*")))
        return

    def printFilename(self):
        name = self.getName(".asc")
        print("Current File: " + name)
        return

    def getName(self, ext):
        name = self.filename.split('/')
        name = name[-1]
        # removes the extention (ex. ".asc", ".txt", etc.)
        tempname = name[:-4]
        name = tempname
        name = name + ext
        return name

    def ParseFile(self):
        print(self.filename)
        GNSSLines = []

        if self.filename == None:
            self.GNSSLines = GNSSLines
            return
        else:
            file = open(self.filename, 'r')
            lines = file.readlines()
            numberoflines = 0

            for line in lines:
                numberoflines += 1

                [header, body] = func.GetHeaderBody(line)
                print(header)
                parsedheader = func.ParseHeader(header)
                newHeader = Header()
                print(numberoflines)
                print('\n')
                newHeader.Parse(parsedheader)
                log_name = newHeader.command
                #print (parsedheader)

                if log_name == "BESTPOS":
                    newBody = BESTPOS()
                else:
                    newBody = NoBody()

                newBody.Parse(body)

                newGNSSLine = GNSSLine(newHeader, newBody)
                GNSSLines.append(newGNSSLine)

        self.GNSSLines = GNSSLines

        name = self.getName(".asc")
        print("Parse of " + name + " Successful!")
        return

    def GetPositioningData(self):
        header = ["week", "seconds", "stnid", "numberofsatsinsol", "numberofL1",
                  "numberofmultisats", "lat", "latsigma", "lon", "lonsigma", "hgt", 'hgtsigma', 'und']
        Data = [[header]]

        if self.filename == None:
            returnma
        for GNSSLine in self.GNSSLines:
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

        self.WriteData("PositioningDatafor ", Data)
        name = self.getName(".asc")
        print("Positioning Data csv for " + name + " created!")
        return

    def GetBESTGNSSPOS(self):
        func.GetBESTGNSSPOS(self.filename, self.GNSSLines)
        return

    def WriteData(self, prefix, Data):
        if self.filename == None:
            return

        name = self.getName(".csv")
        newfilename = prefix + name
        mycsv = open(newfilename, "w+")
        csvWriter = c.writer(mycsv, delimiter=',')
        csvWriter.writerows(Data)
        return
