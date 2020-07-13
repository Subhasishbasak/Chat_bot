try:
    import re
    import os
    import scipy
    import random
    import pickle
    import warnings
    import utils.BuildVocab as BuildVocab
    import numpy as np
    warnings.filterwarnings("ignore")
    from gensim.models import Word2Vec
    from gensim.models.keyedvectors import KeyedVectors
except Exception as e:
    package = str(e).split()[-1]
    print("ERROR")
    print("{} package not found" .format(package))
    print("Please install the module", package)


class Model():
    def __init__(self):
        self.SIZE = 100
        self.WINDOW = 5
        self.ALPHA = 0.001
        self.Method = 1

        self.inputPath = "../lib/Output/vocab/"
        self.outputPath = "../lib/Output/weights/"
        if not os.path.exists(os.path.dirname(self.inputPath)):
            print("Generating vocabulary..")
            BuildVocab.main()
        else:
            print("Vocabulary found\nLoading...")
        with open(self.inputPath + "inProcessed.p", 'rb') as f:
            self.inProcessed = pickle.load(f)
#         with open(self.inputPath + "outProcessed.p", 'rb') as f:
#             self.outProcessed = pickle.load(f)
        with open(self.inputPath + "inWordCount.p", 'rb') as f:
            self.inWordCount = pickle.load(f)
        with open(self.inputPath + "inDic.p", 'rb') as f:
            self.inDic = pickle.load(f)
        with open(self.inputPath + "mappingDic.p", 'rb') as f:
            self.mappingDic = pickle.load(f)
        with open(self.inputPath + "outDicMap.p", 'rb') as f:
            self.outDicMap = pickle.load(f)

        if not os.path.exists(os.path.dirname(self.outputPath)): 
            try:
                os.makedirs(os.path.dirname(self.outputPath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            print("Model training under process...")
            self.model = self.trainModel()
            self.model.wv.save_word2vec_format(self.outputPath + "word2vecWeights.txt", binary=False)  
        else:
            print("Trained weights found\nLoading..")
            self.model = KeyedVectors.load_word2vec_format(self.outputPath + "word2vecWeights.txt", binary=False)
            print("Weights loaded successfully")
    ## Function to training a word2vec model    
    def trainModel(self):
        trainData = list(i.split() for i in self.inProcessed)
        model = Word2Vec(trainData, size = self.SIZE, window = self.WINDOW, min_count = 1, workers = 4)
        return model  
    
    ## Function to return the word embedding of the word, zeros if the wor is unknown
    def Vec(self, word):
        try:
            return self.model[word]
        except:
            return np.zeros(self.SIZE)
        
    ## Function to return the count of the word in the corpus   
    def Count(self, word):
        try:
            return self.inWordCount[word]
        except:
            return 0
        
    ## Function to return the similarity distance (cosine) between two senetnce.
    ## 0 implies they are totally similar and 1 implies they are way apart
    def CosSifDist(self, sentence_1, sentence_2):
        vector_1 = np.sum([self.Vec(word)*(self.ALPHA / (self.ALPHA + self.Count(word))) for word in BuildVocab.processed(sentence_1).split()], axis = 0)
        vector_2 = np.sum([self.Vec(word)*(self.ALPHA / (self.ALPHA + self.Count(word))) for word in BuildVocab.processed(sentence_2).split()], axis = 0)
        cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
        #print('Word Embedding method with a cosine distance method, sentences are similar to',round((1-cosine)*100,2),'%')
        return cosine  
    
    ## Function tto return the similarity distance (word mover) between two senetnce.
    def WMDist(self, sentence_1, sentence_2):
        sentence_1 = BuildVocab.processed(sentence_1)
        sentence_2 = BuildVocab.processed(sentence_2)
        return self.model.wmdistance(sentence_1, sentence_2)    
    
    ## Function to return the closest messages given a raw text
    def getCloseMsg(self, RawText):
        if self.Method == 1:
            temp = np.inf
            closestMsg = None
            for oldmsg in self.inProcessed:
                similarity = self.CosSifDist(RawText, oldmsg)
                if similarity < temp:
                    temp = similarity
                    closestMsg = oldmsg
        elif self.Method == 2:
            temp = np.inf
            closestMsg = None
            for oldmsg in self.inProcessed:
                similarity = self.WMDist(RawText, oldmsg)
                if similarity < temp:
                    temp = similarity
                    closestMsg = oldmsg
        return closestMsg 
    
    ## Function to return the reply of a message
    def getReply(self, newMsg):
        botimoji = " ¯\_(ツ)_/¯ -> "
        replies = []
        closestMsg = self.getCloseMsg(newMsg)
        if closestMsg == None:
            return(botimoji + "Sorry, I didnot get you..")
        index = self.inDic[closestMsg]
        repliesindex = self.mappingDic[index]
        for i in repliesindex:
            replies.append(self.outDicMap[i])
        
        return(botimoji + random.choice(replies))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
