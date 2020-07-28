import re
import os

def createdata_old():
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
    with open(outputPath + 'incoming_old.txt', 'w', encoding = "utf8") as f:
        for item in incoming:
            f.write("%s\n" % item)
    with open(outputPath + 'outgoing_old.txt', 'w', encoding = "utf8") as f:
        for item in outgoing:
            f.write("%s\n" % item)

# New createdata function for splitted, 1-1, incoming-outgoing scheme

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
    # <media omitted> issue addressed here

    dataList = []
    for line in data:
        line = line.replace("\n", " ")
        if line.split(": ")[1] == '<Media omitted>':
            dataList.append([line.split(": ")[0], 'I wish I could send an imgae for this!'])
        else:
            dataList.append(line.split(": "))

    # Code for removing the text messages from the Whastapp user, from the very beginning (if exists)

    index = 0
    current_name = dataList[index][0]    

    while current_name == whatsappName:
        index += 1
        current_name = dataList[index][0]

    #print("Total number of messages deleted at the beginning : ", index)
    dataList = dataList[index:]       


    # code for decomposing the conversations in blocks

    blocks = []
    temp = []
    flag = False
    index = 0

    for i in dataList:
        if i[0] == whatsappName:
            flag = True
            temp.append(i)
        elif (i[0] != whatsappName and not flag):
            index += 1
            temp.append(i)
        else:
            blocks.append(temp + [index])
            temp = []
            index = 1
            temp.append(i)
            flag = False

    # code for generating all possible incoming-outgoing pairs within each block

    final = []

    for block in blocks:
        block_expanded = []
        incoming_num = block[-1]
        outgoing_num = len(block) -1 - incoming_num
        
        incoming_block = block[:incoming_num]
        outgoing_block = block[incoming_num:-1]
        
        for i in incoming_block:
            for j in outgoing_block:
                final.append(i)
                final.append(j)

    # code for generating MODIFIED incoming.txt and outgoing.txt

    incoming = [x[1] for x in final[::2]]
    outgoing = [x[1] for x in final[1:][::2]]

    assert len(incoming) == len(outgoing), 'incoming & outgoing lengths differ'
    
    ## Writting created dataset
    with open(outputPath + 'incoming.txt', 'w', encoding = "utf8") as f:
        for item in incoming:
            f.write("%s\n" % item)
    with open(outputPath + 'outgoing.txt', 'w', encoding = "utf8") as f:
        for item in outgoing:
            f.write("%s\n" % item)




if __name__ == "__main__":
    createdata()
