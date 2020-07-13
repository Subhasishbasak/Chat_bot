## Import pre-requisites

from bs4 import BeautifulSoup
import sys
from time import *


def read_last_msg(driver):
    """
    Reading the last message that you got in from the chatter
    """
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    htmlcode=(driver.page_source).encode('utf-8')
    soup = BeautifulSoup(htmlcode,features="html.parser")

    d = soup.find_all('div', class_ = 'copyable-text')
    messages = []
    for i in range(0,len(d)):
        s = d[i].find('span', class_ = '_3Whw5 selectable-text invisible-space copyable-text')
        if not d[i].get('data-pre-plain-text') is None:
            #print(" \n",d[i].get('data-pre-plain-text'))
            if not s is None:
                #print(s.span.text)
                messages.append([d[i].get('data-pre-plain-text'), s.span.text])
    return messages[-1]
