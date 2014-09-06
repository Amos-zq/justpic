#!/usr/bin/env python
# encoding: utf-8

input_list=['all','this','happened','more','or','less']

def find_bigrams(input_list):
    bigram_list=[]
    for i in range(len(input_list)-1):
        bigram_list.append((input_list[i],input_list[i+1]))
    return bigram_list

def find_bigrams2(input_list):
    return zip(input_list,input_list[1:])

#Biggrams
zip(input_list,input_list[1:])
#Trigrams
zip(input_list,input_list[1:],input_list[2:])
#and so on
zip(input_list,input_list[1:],input_list[2:],input_list[3:])

def find_ngrams(input_list,n):
    return zip(*[input_list[i:] for i in range(n)])
