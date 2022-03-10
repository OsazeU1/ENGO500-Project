from functions import *

app = Application(tk.Tk())
app.mainloop()
filename = app.filename
print(test)

# filename = "testfile.txt"

# test = ParseFile(filename)
# print(test[0].header.command)
# GetPositioningData(filename, test)
# file = open(filename, 'r')
# lines = file.readlines()

numberoflines = 0

#test = BytesToBinary("0x0300")
# print(test)
# Debugging
# for line in lines:
#     numberoflines += 1
#     print("Full Line: " + line.strip() + '\n')

#     [header, body] = GetHeaderBody(line)
#     print("Original Header: ")
#     print(header[0])
#     print("Body: " + body + '\n')
#     parsedheader = ParseHeader(header)
#     print("Header: ")
#     print(parsedheader[0])
#     print('\n')
#     [mainbody, crc] = SplitBodyMessage(body)
#     print("mainbody: " + mainbody + '\n' + "crc: " +
#           crc + '\n')

#     newHeader = Header()
#     newHeader.Parse(parsedheader)
#     # print(newHeader.timestatus_message)

#     # print(newGNSSLine.header.sync)
#     log_name = newHeader.command

#     if log_name == "BESTPOS":
#         newBody = BESTPOS()
#     elif log_name == "RANGE":
#         a = 0

#     newBody.Parse(body)

#     newGNSSLine = GNSSLine(newHeader, newBody)
#     print(newGNSSLine.body.latsigma)
