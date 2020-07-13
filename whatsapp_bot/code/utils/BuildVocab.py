try:
    import re
    import os
    import sys
    import pickle
    import random
    import string
    import utils.CreateData as CreateData
except Exception as e:
    package = str(e).split()[-1]
    print("ERROR")
    print("{} package not found" .format(package))
    print("Please install the module", package)
    

## Function to remove digits, punctuation and extra space
def processed(text):
    # Removs digits
    def removeDigits(text): 
        result = re.sub(r'\d+', '', text) 
        return result 
    # Removes punctuation 
    def removePunctuation(text): 
        translator = str.maketrans('', '', string.punctuation.replace(":", "").replace("'","")) 
        return text.translate(translator) 
    # Removes whitespace from text 
    def removeSpaces(text): 
        return  " ".join(text.split())
    # Main function
#     if __name__=="__main__":
    text = text.replace("<Media omitted>", " ")
    text = text.lower()
    #text = removeDigits(text)
    text = removePunctuation(text)
    text = removeSpaces(text)
    return text
def performprocess(ListOfMsg):
    output = []
    for text in ListOfMsg:
        output.append(processed(text))
    return(output)

## Function to count unique word occurences
def getWordCount(corpus):
    WordCount = {}
    for text in corpus:
        for word in text.split():
            try:
                WordCount[word] += 1
            except:
                WordCount[word] = 1 
    return WordCount

## Function to get messages index and in out mapping
def getIndexDicMap(inProcessed, outProcessed):
    inDic = {}
    outDic = {}
    for i in range(len(inProcessed)):
        if inProcessed[i] not in inDic.keys():
            inDic[inProcessed[i]] = i
    for i in range(len(outProcessed)):
        if outProcessed[i] not in outDic.keys():
            outDic[outProcessed[i]] = i
    mappingDic = {}
    for index in range(len(outProcessed)):
        try:
            mappingDic[inDic[inProcessed[index]]].append(outDic[outProcessed[index]])
        except:
            mappingDic[inDic[inProcessed[index]]] = [outDic[outProcessed[index]]]
    return inDic, outDic, mappingDic




def main():
    inputPath = "../lib/Output/"
    outputPath = "../lib/Output/vocab/"
    
    if not os.path.exists(os.path.dirname(inputPath)):
        print("Generating dataset from raw data...")
        CreateData.createdata()
    else:
        print("Dataset found \nLoading....")
    with open(inputPath + "incoming.txt", encoding = "utf8") as f:
        incoming = f.read()
    incoming = incoming.split("\n")        
    with open(inputPath + "outgoing.txt", encoding = "utf8") as f:
        outgoing = f.read()
    outgoing = outgoing.split("\n")
    
    inProcessed = performprocess(incoming) # List of list of messages as whole string
    outProcessed = performprocess(outgoing) # List of list of messages as whole string
    
    inWordCount = getWordCount(incoming) # Counting number of unique word occurences
    
    inDic, outDic, mappingDic = getIndexDicMap(inProcessed, outProcessed) # Getting messages index and mapping
    outDicMap = dict([(value, key) for key, value in outDic.items()]) 
    
    # writting those files 
    if not os.path.exists(os.path.dirname(outputPath)):
        try:
            os.makedirs(os.path.dirname(outputPath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise            

    with open(outputPath + "inProcessed.p", 'wb') as f:
        pickle.dump(inProcessed, f)
    with open(outputPath + "outProcessed.p", 'wb') as f:
        pickle.dump(outProcessed, f)
    with open(outputPath + "inWordCount.p", 'wb') as f:
        pickle.dump(inWordCount, f)
    with open(outputPath + "inDic.p", 'wb') as f:
        pickle.dump(inDic, f)
    with open(outputPath + "mappingDic.p", 'wb') as f:
        pickle.dump(mappingDic, f)
    with open(outputPath + "outDicMap.p", 'wb') as f:
        pickle.dump(outDicMap, f)

if __name__ == "__main__":
    main()






