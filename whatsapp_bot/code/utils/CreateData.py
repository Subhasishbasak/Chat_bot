import re
import os

def createdata():
    ## Reading path of the data and user name
    Rawpath = "../lib/"
    whatsappName = input("Whatsapp User id: ")

    ## Reading data
    data = ""
    inputPath = Rawpath
    for file in os.listdir(inputPath):
        filePath = os.path.join(inputPath, file)
        with open(filePath, encoding = "utf8") as f:
            temp = f.read()
        data += " " + temp

    ## Creaitng output folder
    outputPath = Rawpath + ("Output/")
    if not os.path.exists(os.path.dirname(outputPath)):
        try:
            os.makedirs(os.path.dirname(outputPath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    ## Splitting data as new message as #brk#
    data = re.sub("\n[0-9]*/[0-9]*/[0-9]*, [0-9]*:[0-9]* [ap][m] - ", " #brk# ", data)
    data = data.split(" #brk# ")[1:]

    ## Creating in and out messages
    dataList = []
    for line in data:
        line = line.replace("\n", " ")
        dataList.append(line.split(": "))

    flag_0 = True
    flag_1 = True
    incoming = []
    outgoing = []
    temp = ""
    for item in dataList:
        try:
            name = item[0]
            txt = item[1]
        except:
            continue
        if name == whatsappName:
            if flag_0:
                if not flag_1:
                    incoming.append(temp)
                temp = txt
                flag_1 = True
                flag_0 = False
            else:
                temp += " " + txt
        else:
            if flag_1:
                if not flag_0:
                    outgoing.append(temp)
                temp = txt
                flag_0 = True
                flag_1 = False
            else:
                temp += " " + txt


    ## Writting created dataset
    with open(outputPath + 'incoming.txt', 'w', encoding = "utf8") as f:
        for item in incoming:
            f.write("%s\n" % item)
    with open(outputPath + 'outgoing.txt', 'w', encoding = "utf8") as f:
        for item in outgoing:
            f.write("%s\n" % item)

if __name__ == "__main__":
    createdata()