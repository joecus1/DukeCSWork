'''
Created on Feb 26, 2018

@author: ola
'''
import os
lowerwords = []
novowels = []

def isVowel(ch):
    """
    Return True if ch is a vowel and False otherwise
    """
    return "aeiouAEIOU".count(ch) > 0

def encrypt(word):
    """
    Return a string that is word
    with all vowels removed, other letters/chars
    in original order as in word
    """
    nv = [ch for ch in word if not isVowel(ch)]
    return ''.join(nv)

def loadlower():
    """
    Set global variables so that 
    lowerwords is all the words from a file of words
    and novowels is the list of these words with
    all vowels removed. This means that
    novowels[k] is the encrypted form of lowerwords[k]
    
    Returns the 
    """
    global lowerwords, novowels
    #f = open("data/lowerwords.txt")
    f = open(os.path.join("data", "lowerwords.txt"))
    lowerwords = [w.strip() for w in f.read().split()]
    novowels = [encrypt(w) for w in lowerwords]
    f.close()
    return lowerwords

def decrypt(word):
    """
    String word has no vowels
    Find a match for word formed
    by finding a word that could have vowels
    removed to yield word. If more than one
    such word, choose one. If no such word found
    then return "NT_WORD"
    
    Note: this code depends on global variables
    lowerwords and novowels. These are initialized
    once and then the values used on all other calls 
    after initialization
    """
    global lowerwords, novowels
    if len(lowerwords) == 0:
        lowerwords = loadlower()
        print("read words in Vowelizer")
    
    word = word.lower()
    matches = [dex for dex in range(len(novowels)) if novowels[dex] == word]
    #print("%d number of matches for %s" % (len(matches),word))
    if len(matches) > 0:
        return lowerwords[matches[0]]
    return "NT_WORD"
    

if __name__ == '__main__':
    words = ["vowels", "strength", "oasis", "elephant"]
    ewords = []
    for w in words:
        ew = encrypt(w)
        ewords.append(ew)
        print(w,ew)
    
    print("decrypting")
    for w in ewords:
        dw = decrypt(w)
        print(w,dw)