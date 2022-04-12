import dictonaries as d
import functions as func
import tkinter as tk
from tkinter import filedialog
from time import sleep
import math
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

        # DEBUGING #
        # print(header)
        # print('\n')
        # print(header[0])
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
            [sync, command, week, seconds] = header[0]
            self.sync = sync
            self.command = command
            self.week = week
            self.seconds = seconds
        elif temp[0] == "$":
            [sync, command] = header[0]
            self.sync = sync
            self.command = command
        else:
            self.sync = "ERROR"
            self.command = "ERROR"
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
        # print(datumid)
        if datumid == "WGS84" or datumid == "USER":
            datum = datumid
            # print("here")
        else:
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

        galbei_message = func.GetMessage(
            galbei_sigmask, d.bestpos_galbei_sigmask)
    
        

        gpsglo_message = func.GetMessage(
            gpsglo_sigmask, d.bestpos_gpsglo_sigmask)
            
        extsolstat_message = "WIP"
        #extsolstat_message = d.bestpos_ess[extsolstat]
        
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
        self.gpsglo_message = gpsglo_message
        self.crc = crc
        return


class NoBody:
    def __init__(self):
        return

    def Parse(self, body_message):
        self.type = None
        return


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
        # print(datumid)
        if datumid == "WGS84" or datumid == "USER":
            datum = datumid
            # print("here")
        else:
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

        extsolstat_message = "WIP"
        #extsolstat_message = d.bestpos_ess[extsolstat]
        galbei_message = func.GetMessage(
            galbei_sigmask, d.bestpos_galbei_sigmask)

        gpsglo_message = func.GetMessage(
            gpsglo_sigmask, d.bestpos_gpsglo_sigmask)
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
        self.gpsglo_message = gpsglo_message
        self.crc = crc
        return


class INSPVAX:
    def __init__(self):
        return

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        [insstatus, postype, self.lat, self.lon, self.hgt, self.undulation, self.northvel, self.eastvel, self.upvel, self.roll, self.pitch, self.azimuth, self.latsigma,
            self.lonsigma, self.hgtsigma, self.northvelsigma, self.eastvelsigma, self.upvelsigma, self.rollsigma, self.pitchsigma, self.azimuthsigma, extsolstat, self.tsu] = mainbody

        self.instatus_message = d.interial_solution_status[insstatus]
        self.postype_message = d.bestpos_posveltype[postype]
        self.extsolstat_message = "WIP"
        #self.extsolstat_message = d.bestpos_ess[extsolstat]

        # Assigning Local Variables


class RANGE:
    def __init__(self):
        return
    # takes the split off body message (after ";")

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        # print(mainbody)
        # assigning variables and translating codes to messages
        # Number of observations
        self.numberofobs = int(mainbody[0])
        #print (self.numberofobs)
        index = 1
        self.PRNobs = []
        # print(mainbody[540])
        for i in range(0, self.numberofobs):
            temp = []
            for j in range(0, 10):
                if index <= self.numberofobs*10:
                    temp.append(mainbody[index])
                    index = index + 1
            # print(temp)
            self.PRNobs.append(temp)

        # print(len(self.PRNobs))
        return


class TRACKSTAT:

    def __init__(self):
        return

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        # print(mainbody)
        # assigning variables and translating codes to messages

        solstat = mainbody[0]
        self.solstat_message = d.bestpos_solutionsstatus[solstat]
        postype = mainbody[1]
        self.postype_message = d.bestpos_posveltype[postype]

        self.cutoff = mainbody[2]
        # Number of hardware channels with information to follow
        self.numberofchans = int(mainbody[3])
        #print (self.numberofobs)
        index = 4
        self.PRNobs = []
        # print(mainbody[540])
        for i in range(0, self.numberofchans):
            temp = []
            for j in range(0, 10):
                if index <= self.numberofchans*10 + 3:
                    temp.append(mainbody[index])
                    index = index + 1
            # print(temp)
            self.PRNobs.append(temp)

        # print(len(self.PRNobs))
        return


class SATVIS2:

    def __init__(self):
        return

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        self.satvis_message = "TRUE"
        self.almanacflag_message = "TRUE"

        self.satsystem = mainbody[0]
        satvis = mainbody[1]
        if satvis == "0":
            self.satvis_message = "FALSE"

        almanacflag = mainbody[2]
        if almanacflag == "0":
            self.almanacflag_message = "FALSE"

        # Number of satellites
        self.numberofsats = int(mainbody[3])
        #print (self.numberofsats)
        index = 4
        self.SATobs = []
        # print(mainbody[540])
        for i in range(0, self.numberofsats):
            temp = []
            for j in range(0, 6):
                if index <= self.numberofsats*6 + 3:
                    temp.append(mainbody[index])
                    index = index + 1
            # print(temp)
            self.SATobs.append(temp)

        # print(len(self.SATobs))
        return


class RAWIMUSX:
    def __init__(self):
        return

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        # print(mainbody)
        [self.imuinfo, imutype, self.gnssweek, self.gnssweekseconds, imustatus, self.zaccel,
            self.yaccel, self.xaccel, self.zgyro, self.ygyro, self.xgyro] = mainbody

        self.imu = d.imutypes[imutype]
        self.imustatus_message = "WIP"
        #self.imustatus_message = maybenotneeded
        return


class HEADING2:

    def __init__(self):
        return

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        [solstat, postype, self.length, self.heading, self.pitch, self.reserved, self.hdgsigma, self.pitchdigma, self.roverid, self.masterstnid,
            self.numberofsats, self.numberofsatsinsol, self.numberofobs, self.numberofmultisats, solsource, ess, galbei, gpsglo] = mainbody

        self.solstat_message = d.bestpos_solutionsstatus[solstat]
        self.postype_message = d.bestpos_posveltype[postype]
        self.solsource = "WIP"
        self.extsolstat_message = "WIP"
        self.galbei_message = "WIP"
        self.gpsglo_message = "WIP"
        #self.solsource = mightnotneed
        #self.extsolstat_message = d.bestpos_ess[extsolstat]
        #self.galbei_message = d.bestpos_galbei_sigmask[galbei_sigmask]
        #self.gpsglo_message = d.bestpos_gpsglo_sigmask[gpsglo_sigmask]

        return


class PASSTHROUGH:
    def __init__(self):
        return

    def Parse(self, body_message):
        # splits into the crc end message and the main body of the log
        [mainbody, crc] = func.SplitBodyMessage(body_message)

        # makes an array with each of the fields being an index (allstrings)
        mainbody = mainbody.split(",")
        [self.port, self.numberofbytes, self.data] = mainbody
        return


class GPGSA:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        [self.vdop, check] = finalbody[16].split('*')
        if finalbody[0] == "M":
            finalbody[0] = "Manual, forced to operate in 2D or 3D"
        else:
            finalbody[0] = " Automatic 2D/3D"

        if finalbody[0] == "1":
            finalbody[0] = "Fix not available"
        elif finalbody[0] == "2":
            finalbody[0] = "2D"
        else:
            finalbody[0] = "3D"

        for i in range(2, 13):
            if finalbody[i] == '':
                finalbody[i] = " "
            elif int(finalbody[i]) <= 32:
                finalbody[i] = "GPS"
            elif int(finalbody[i]) <= 64 or finalbody[i] == 87:
                finalbody[i] = "SBAS"
            elif int(finalbody[i]) <= 96 and int(finalbody[i]) != 87:
                finalbody[i] = "GLO"

        [self.modema, self.mode123, self.prn1, self.prn2, self.prn3, self.prn4, self.prn5,
            self.prn6, self.prn7, self.prn8, self.prn9, self.prn10, self.prn11, self.prn12, self.pdop, self.hdop, fullend] = finalbody
        return


class GPGGA:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message

        finalbody[5] = d.gps_qual_indicators[finalbody[5]]

        [self.utc, self.lat, self.latdir, self.lon, self.londir, self.quality, self.numofsats, self.hdop,
            self.antennaalt, self.antennaunits, self.und, self.undunits, self.correctiondataage, self.stnid] = finalbody

        return


class PASHR:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        [self.time, self.heading, self.trueheading, self.roll, self.pitch, self.heave, self.rollaccuracy, self.pitchaccuracy,
         self.headingaccuracy, gpsupqual, message] = finalbody

        [instatflag, self.checksum] = message.split('*')
        self.gpsupqual = d.gps_udpate_qual[gpsupqual]
        self.instatflag = d.ins_status_flag[instatflag]

        return


class GPGST:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        [self.utc, self.rms, self.semimjrstd, self.semimnrstd, self.orient,
            self.latstd, self.lonstd, message] = finalbody

        [self.altstd, self.checksum] = message.split('*')
        return


class GPVTG:
    def __init__(self):
        return

    def Parse(self, body_message):

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        [self.tracktrue, self.T, self.trackmag, self.M, self.speedoverground,
            self.nauticalspeedunits, self.speed, self.speedindicator, message] = finalbody

        [i, self.checksum] = message.split('*')

        self.nmeaposmode = d.nmea_posmode[i]


class GPHDT:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        [self.headingdeg, message] = finalbody
        [self.degtrue, self.checksum] = message.split('*')
        return


class GPZDA:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        [self.utc, self.day, self.month, self.year, null1, message] = finalbody
# Unfinished


class GPGSV:
    def __init__(self):
        return

    def Parse(self, body_message):
        # print(body_message)

        # makes an array with each of the fields being an index (allstrings)
        finalbody = body_message
        numofsatsinline = (len(finalbody)- 3)/4
        
        #print(numofsatsinline)
        self.totalnumofmessages = finalbody[0]
        self.currentmessagenum = finalbody[1]
        self.totalnumofsatsinview = finalbody[2]
        message = finalbody[len(finalbody) - 1]
        #print(message)
        [systemid, self.checksum] = message.split('*')
        if systemid == "": 
            self.sysname = 'unavailable'
            self.syssignal = 'unavailable'
        else:
            num1 = systemid[0]
            num2 = systemid[1]

            self.sysname = d.gnss_system_names[num1]
            self.syssignal = d.gnss_systems_sigids[num1][num2]

        counter = 3
       
        self.satinfo = []
        for i in range(0, int(numofsatsinline)-1):
            temp = []

            for j in range(0, 4):
                if finalbody[counter] == "":
                    temp.append(" ")
                else:
                    temp.append(finalbody[counter])
                counter = counter+1

            self.satinfo.append(temp)
        # account for missing snr at the end
        temp = []
        temp.append(finalbody[counter])
        temp.append(finalbody[counter + 1])
        temp.append(finalbody[counter + 2])
        temp.append(" ")
        return


# Windows Application (.exe)
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        space = tk.Label(master, text=" ")
        space.config(font=("Courier", 14))
        space.pack()

        instructionsbox = tk.Text(master, height=3, width=40)
        instructionstitle = tk.Label(master, text="Instructions")
        instructionstitle.config(font=("Courier", 14))

        instructionsmessage = "1. Open ASCII File" + '\n' + \
            "2. Parse GNSS Logs" + '\n' + "3. Output CSV Files for Logs of Interest"

        instructionstitle.pack()
        instructionsbox.pack()

        instructionsbox.insert(tk.END, instructionsmessage)

        space2 = tk.Label(master, text=" ")
        space2.config(font=("Courier", 14))
        space2.pack()

        self.openbutton = tk.Button(
            master, text="Open ASCII File", command=self.openFile)
        master.geometry("600x900")
        master.title("GNSS Log Parser")
        self.openbutton.pack()
        self.filename = None

        self.printbutton = tk.Button(
            master, text="Display Current File", command=self.printFilename)
        self.printbutton.pack()

        self.parsebutton = tk.Button(
            master, text="Parse Data", command=self.ParseFile)
        self.parsebutton.pack()

        # Create text widget and specify size.

        # Create label

        space3 = tk.Label(master, text=" ")
        space3.config(font=("Courier", 14))
        space3.pack()

        GNSStitle = tk.Label(master, text="Set One of Available GNSS Logs")
        GNSStitle.config(font=("Courier", 14))
        GNSStitle.pack()

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
            text="Get INSPVAX Information", command=self.GetINSPVAX)
        self.bbutton.pack()

        self.cbutton = tk.Button(
            text="Get RANGE Information", command=self.GetRANGE)
        self.cbutton.pack()

        self.dbutton = tk.Button(
            text="Get TRACKSTAT Information", command=self.GetTRACKSTAT)
        self.dbutton.pack()

        self.ebutton = tk.Button(
            master, text="Display Galileo and BeiDou Signals", command=None)
        self.ebutton.pack()

        self.fbutton = tk.Button(
            text="Get SATVIS2 Information", command=self.GetSATVIS2)
        self.fbutton.pack()

        self.gbutton = tk.Button(
            text="Get RAWIMUSX Information", command=self.GetRAWIMUSX)
        self.gbutton.pack()

        self.hbutton = tk.Button(
            text="Get HEADING2 Information", command=self.GetHEADING2)
        self.hbutton.pack()

        self.ibutton = tk.Button(
            text="Get PASSTHROUGH Information", command=self.GetPASSTHROUGH)
        self.ibutton.pack()

        space4 = tk.Label(master, text=" ")
        space4.config(font=("Courier", 14))
        space4.pack()

        INStitle = tk.Label(master, text="Set Two of Available GNSS Logs")
        INStitle.config(font=("Courier", 14))
        INStitle.pack()

        self.gpgsabutton = tk.Button(
            text="Get GPGSA Information", command=self.GetGPGSA)
        self.gpgsabutton.pack()

        self.gpggabutton = tk.Button(
            text="Get GPGGA Information", command=self.GetGPGGA)
        self.gpggabutton.pack()

        self.gpzdabutton = tk.Button(
            text="Get GPZDA Information", command=self.GetGPZDA)
        self.gpzdabutton.pack()

        self.pashrbutton = tk.Button(
            text="Get PASHR Information", command=self.GetPASHR)
        self.pashrbutton.pack()

        self.gpgstbutton = tk.Button(
            text="Get GPGST Information", command=self.GetGPGST)
        self.gpgstbutton.pack()

        self.gpvtgbutton = tk.Button(
            text="Get GPVTG Information", command=self.GetGPVTG)
        self.gpvtgbutton.pack()

        self.gpgsvbutton = tk.Button(
            text="Get GPGSV Information", command=self.GetGPGSV)
        self.gpgsvbutton.pack()

        self.gphdtbutton = tk.Button(
            text="Get GPHDT Information", command=self.GetGPHDT)
        self.gphdtbutton.pack()

        self.gpzdabutton = tk.Button(
            text="Get GPZDA Information", command=self.GetGPZDA)
        self.gphdtbutton.pack()

    def openFile(self):
        self.filename = filedialog.askopenfilename(initialdir="C:\\",
                                                   title="Select ASCII File",
                                                   filetypes=(("text files", "*.asc"),
                                                              ("all files", "*.*")))
        return

    def printFilename(self):
        name = self.filename
        print("Current File: " + name)
        return

    def getName(self, ext):
        name = func.getName(self.filename, ext)
        # name = self.filename.split('/')
        # name = name[-1]
        # # removes the extention (ex. ".asc", ".txt", etc.)
        # tempname = name[:-4]
        # name = tempname
        # name = name + ext
        return name

    def ParseFile(self):
        self.GNSSLines = func.ParseFile(self.filename)
        # print(self.filename)
        # GNSSLines = []

        # if self.filename == None:
        #     self.GNSSLines = GNSSLines
        #     return
        # else:
        #     file = open(self.filename, 'r')
        #     lines = file.readlines()
        #     numberoflines = 0

        #     for line in lines:
        #         numberoflines += 1

        #         [header, body] = func.GetHeaderBody(line)

        #         # ~~~~ DEBUGING ~~~~~~#
        #         #print("header: ")
        #         #print(header)
        #         #print('\n')
        #         #print("body: ")
        #         #print(body)
        #         parsedheader = func.ParseHeader(header)
        #         newHeader = Header()
        #         #print(numberoflines)
        #         #print('\n')
        #         newHeader.Parse(parsedheader)
        #         log_name = newHeader.command
        #         #print (parsedheader)
        #         # Checks for the command and creates object accordingly
        #         if log_name == "BESTPOS":
        #             newBody = BESTPOS()
        #         elif log_name == "BESTGNSSPOS":
        #             newBody = BESTGNSSPOS()
        #         elif log_name == "INSPVAX":
        #             newBody = INSPVAX()
        #         else:
        #             newBody = NoBody()

        #         newBody.Parse(body)

        #         newGNSSLine = GNSSLine(newHeader, newBody)
        #         GNSSLines.append(newGNSSLine)

        # self.GNSSLines = GNSSLines

        # name = self.getName(".asc")
        # print("Parse of " + name + " Successful!")
        return

    def GetPositioningData(self):
        func.GetPositioningData(self.filename, self.GNSSLines)
        # header = ["week", "seconds", "stnid", "numberofsatsinsol", "numberofL1",
        #           "numberofmultisats", "lat", "latsigma", "lon", "lonsigma", "hgt", 'hgtsigma', 'und']
        # Data = []
        # Data.append(header)

        # if self.filename == None:
        #     return
        # for GNSSLine in self.GNSSLines:
        #     textline = []
        #     if GNSSLine.header.command == "BESTPOS":
        #         week = GNSSLine.header.week
        #         seconds = GNSSLine.header.seconds
        #         stnid = GNSSLine.body.stnid
        #         numberofsatsinsol = GNSSLine.body.numberofsatsinsol
        #         numberofL1 = GNSSLine.body.numberofL1sats
        #         numberofmultisats = GNSSLine.body.numberofmultisats
        #         lat = GNSSLine.body.lat
        #         latsigma = GNSSLine.body.latsigma
        #         lon = GNSSLine.body.lon
        #         lonsigma = GNSSLine.body.lonsigma
        #         hgt = GNSSLine.body.hgt
        #         hgtsigma = GNSSLine.body.hgtsigma
        #         und = GNSSLine.body.undulation

        #         textline = [week, seconds, stnid, numberofsatsinsol,
        #                     numberofL1, numberofmultisats, lat, latsigma, lon, lonsigma, hgt, hgtsigma, und]
        #         Data.append(textline)
        #     else:
        #         continue

        # self.WriteData("PositioningDatafor ", Data)
        # name = self.getName(".asc")
        # print("Positioning Data csv for " + name + " created!")
        return

    def GetBESTGNSSPOS(self):
        func.GetBESTGNSSPOS(self.filename, self.GNSSLines)
        return

    def GetINSPVAX(self):
        func.GetINSPVAX(self.filename, self.GNSSLines)
        return

    def GetRANGE(self):
        func.GetRANGE(self.filename, self.GNSSLines)
        return

    def GetTRACKSTAT(self):
        func.GetTRACKSTAT(self.filename, self.GNSSLines)
        return

    def GetSATVIS2(self):
        func.GetSATVIS2(self.filename, self.GNSSLines)
        return

    def GetRAWIMUSX(self):
        func.GetRAWIMUSX(self.filename, self.GNSSLines)
        return

    def GetHEADING2(self):
        func.GetHEADING2(self.filename, self.GNSSLines)
        return

    def GetPASSTHROUGH(self):
        func.GetPASSTHROUGH(self.filename, self.GNSSLines)
        return

    def GetGPGSA(self):
        func.GetGPGSA(self.filename, self.GNSSLines)
        return

    def GetGPGGA(self):
        func.GetGPGGA(self.filename, self.GNSSLines)
        return

    def GetGPZDA(self):
        func.GetGPZDA(self.filename, self.GNSSLines)
        return

    def GetPASHR(self):
        func.GetPASHR(self.filename, self.GNSSLines)
        return

    def GetGPGST(self):
        func.GetGPGST(self.filename, self.GNSSLines)
        return

    def GetGPVTG(self):
        func.GetGPVTG(self.filename, self.GNSSLines)
        return

    def GetGPGSV(self):
        func.GetGPGSV(self.filename, self.GNSSLines)
        return

    def GetGPHDT(self):
        func.GetGPHDT(self.filename, self.GNSSLines)
        return

    def GetGPZDA(self):
        func.GetGPZDA(self.filename, self.GNSSLines)
        return

    def WriteData(self, prefix, Data):
        func.WriteData(prefix, self.filename, Data)
        # if self.filename == None:
        #     return

        # name = self.getName(".csv")
        # newfilename = prefix + name
        # mycsv = open(newfilename, "w+")
        # csvWriter = c.writer(mycsv, delimiter=',')
        # csvWriter.writerows(Data)
        return
