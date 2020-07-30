import os,sys,inspect
currentdir = os.getcwd()
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import utils.bot as bot

def lets_chat():
    
    model = bot.Model()
    prevMsg = None 

    try:
        
        while True:    
                question = input('\nask : ')
                reply_m = str(model.getReply_m(question, prevMsg))
                reply = str(model.getReply(question))
                print('\n')
                print(reply_m + '\n')
                print(reply)
                prevMsg = question
                
    except KeyboardInterrupt:
        
        print("Exiting")
        sys.exit()

if __name__ == '__main__':

    lets_chat()



