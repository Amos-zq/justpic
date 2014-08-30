import random
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')

#picture object
#get similiarity words
def word2another(key,picindex):
    index = key.keyid - 1
    linelist = []
    if picindex == 0:
        for line in open("WordsRelation"):
            line = line[:-1]
            linelist.append(line)
    elif picindex == 1:
        for line in open("WordsRelation1"):
            line = line[:-1]
            linelist.append(line)
    if index > len(linelist):
        return []
    wordslist = linelist[index]
    wordslist = wordslist.split()
    indexlist = []

    wordslist.pop(index)
    index = wordslist.index(max(wordslist))
    indexlist.append(index)

    wordslist.pop(index)
    index = wordslist.index(max(wordslist))
    indexlist.append(index)

    wordslist.pop(index)
    index = wordslist.index(max(wordslist))
    indexlist.append(index)
    return indexlist