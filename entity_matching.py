import filter as fil
import compare as comp
import sygus
import random
import time
import datetime

wordlenClean = []
posexampleDataPath: str = './data/examples/posexampledata'
posPath: str = './data/examples/posexamples'
negexampleDataPath: str = './data/examples/negexampledata'
negPath: str = './data/examples/negexamples'
examplepaths = []

foundexBlueprint = './data/functions/'
foundexamples = './data/functions/NO_DATE_found'
foundFuncBlueprint = './data/functions/'
foundFunctions = './data/functions/NO_DATE_foundfunctions'

validWordSet = frozenset({})
validWordPath = './data/german_words_from_wiktionary.txt'

charlist = []

#charlist with all starting letters
for k in range(ord('A'), ord('Z')):
    charlist.append(chr(k))
for k in range(ord('a'), ord('z')):
    charlist.append(chr(k))
for k in ['Ä', 'Ö', 'Ü', 'ä', 'ö', 'ü', 'ß']:
    charlist.append(k)
    
# for faster testruns and Benchmarks:
#charlist = ['S']

# Solver
solver = None
# Function
fun = None


#path setup for length + prefix letter seperation
def getletterpath(wordlen:str , letter:str):
    fix = wordlen
    if len(wordlen) == 1: fix = '0' + fix
    return f'./data/wordlensort/len{fix}/{letter}_words'

#setup files/paths
def path_setup():        
    #files for each word lenght
    for i in range(0, 26):
        tmp = ""
        if i < 10: tmp = "0"
        wordlenClean.append(f'./data/wordlen/word_length_reduced_{tmp}{i}')
        
    exampleDataPath = ''
    examplepaths.append(f'./data/example/examples')
    
    tmpset = set()
    with open(validWordPath, 'r', encoding= "utf-8") as f:
        line = f.readline()
        
        while line != '':
            line = line.replace('\n', '')
            tmpset.add(line)
            
            line = f.readline()
            
        global validWordSet
        validWordSet = frozenset(tmpset)
    
    
    
path_setup()

# adjust number of functions and value of threshholds
compareOnValueFunctions = [
    (comp.relativeChangeFlip, []),
    (comp.compareMaxima, []),
    (comp.compareExtremaSymm, ['add']), 
    (comp.compareExtremaSymm, ['sub'])
]

compareOnWordFunctions = [
    #(fil.filterLength,),
    #(fil.filterPrefix,),
    #(fil.filterSuffix,),
    (comp.levenshteinDistance, [])
]

# find the actual data of a word
def findWordData(w1):
    d1 = ''
    #d2 = ''
    #if fil.filterLength(w1, w2, 0):  #this is only for avoiding double file searches
    with open(wordlenClean[len(w1)], 'r', encoding= "utf-8") as f:
        loop = True
        while loop:
            line = f.readline()
            if line == '': 
                loop = False
                continue
            word = line.split()[0]
            if word == w1:
                d1 = line
                return line
                break
            #elif word == w2:
            #    d2 = line
        else: 
            raise AssertionError(f'Word {w1} has not been found in file {comp.wordlenClean[len(w1)]}. Check examples input')
            
# UNUSED
#def applyFunction(d1, d2, f, var):
#    return float(f(d1, d2, *var))

# apply all currently selected functions and return the calculated values 
# input: [word1, data11, data12, ...], [word2, data21, data22, ...]#
# output: [word1, word2, valueF1, valueF2, ....]
def applyFunctions(data1, data2):
    #starttime = time.time()
    pairValues = [data1[0], data2[0]]
    
    totalWords = float(data1[1]) + float(data2[1])
    #pairValues.append(totalWords)
    
    # word functions
    for f, arr in compareOnWordFunctions:
        pairValues.append(float(f(data1[0], data2[0], *arr)))
    
    data1.append("2001,0,0")
    d1 = comp.fillData(data1)
    data2.append("2001,0,0")
    d2 = comp.fillData(data2)
    

    # data functions
    for f, arr in compareOnValueFunctions:
        pairValues.append(float(f(d1, d2, *arr)))
        
    #endtime = time.time()
    #print(f'calculating values for {pairValues[0]};{pairValues[1]} took {round(endtime - starttime, 6)} seconds')
    return pairValues


# this function asumes, that the example pairs are provided in file [path] in the format:
# w1v1;w1v2
# w2v1;w2v2
# w3v1;w3v2
def exampleLoadNew(path):
    exampleValues = []
    with open(path,  'r', encoding= "utf-8") as e:
        
        # parse over all the examples
        while(True):
            ex = e.readline()
            if ex == '': break
            if ex.find('#') != -1: continue
            if ex.find(';') == -1: continue
            pair = ex.split(';')
            w1, w2 = pair[0], pair[1]
            #remove \n from second word
            if w2.find('\n') != -1: w2 = w2[:-1]
            pairValues = [w1, w2]
            
            d1 = findWordData(w1).split()
            d2 = findWordData(w2).split()
        
            ## filter functions:
            exampleValues.append(applyFunctions(d1, d2))
    
    return exampleValues
            
   
def exampleLoadOld(path):
    exampleValues = []
    with open(path,  'r', encoding= "utf-8") as e:
        while True:
            line = e.readline()
            if line == '': break
            
            # the first two words are the compared pair
            tmp = [*line.split()[:2]]
            
            # the rest are comparison values
            for elem in line.split()[2:]:
                tmp.append(float(elem))
            
            exampleValues.append(tmp)
            
            
    return exampleValues
    
# return True if this pair passes the filter
def checkToCompare(word1, word2, total):
    comp = False
    # the structure of the comparison calls already blocks any words that are above a length difference of 4 (may vary depending on usage) 
    # so there is no need to check for length difference
    
    
    if not fil.filterPrefix(word1, word2, 3): return False
    if not fil.filterSuffix(word1, word2, 1): return False
    
    
    # especially in the first runs, it is better to compare less to cauge if the matching produces good results
    if random.randint(1, 100) != 1: return False
    
    # if there is just too little total usage, ignore the pair
    if total < 400: return False
    
    
    return True           
         
# the main compare for two words and their data            
def WordCompare(solver, fun, d1, d2):
    
    w1 = d1[0]
    w2 = d2[0]
    
    wordcount = int(d1[1]) + int(d2[1])
    # early check for validity of the compare based on the preffixi
    if not checkToCompare(word1= w1, word2= w2, total= wordcount): return
    
    # calculate values
    pairValues = applyFunctions(data1= d1, data2= d2)
            
    # verify against the current function
    valid = sygus.verify(solver= solver, fun= fun, vars= pairValues[2:])
    if not valid: return
    
    # add entry to existing file
    with open(foundexamples, 'a', encoding= "utf-8") as f:
        f.write(f'{'\t'.join(map(str, pairValues))}\n')

    
    

    
#PSEUDOCODE implementation from Entity Matching paper
#!!!!!!!!!   PHI != phi   !!!!!!!!!
# E union of M and D; the set of examples; split in this implementation
    # M Matching        ;= posEx
    # D Not Matching    ;= negEx
# Ggbf; grammar defined by the combination of AND OR and NOT combination of elements
# F; Library of functions
# müh; optimality metric
# K
def EMOPT(posEx, negEx, Kransac, Kcegis):
    r = 0
    phi = None              # will be of form: [solver, function]
    phieval = len(posEx) + len(negEx)   # current least amount of misses
    print(f'#total examples: {phieval}\t#pos-examples: {len(posEx)}\t#neg-examples: {len(negEx)}')
    
    while r < Kransac:
        i = 0
        e_syn = []
        # the paper makes a point of the chance that the example is pos/neg beeing 50/50
        # BUT cvc5 needs a positive and a negative example to synthesize a formular
        #if not random.getrandbits(1):       #positive example
        e_syn.append([True, *posEx[random.randint(0, len(posEx) -1)]])
        #else:                               #negative example
        e_syn.append([False, *negEx[random.randint(0, len(negEx) -1)]])
            
        #Esyn = List(e[0])
        while i < Kcegis:
            newphi = sygus.synth(e_syn)
            if newphi == None: break   # no solution found -> restart Kcegis
            
            # add efficiency
            inval = sygus.VerifyExamples(*newphi, posEx, negEx)   # counter-examples
            if inval == []: #no non-fitting examples -> perfect function found. further examination is ALMOST unneeded
                return newphi
            else:
                e_syn.append(inval[random.randint(0, len(inval) -1)]) #randomly add a non.fitting example
                
            #phi = argmax (with Phi out of (phi,PHI[i]) müh(PHI, M D))
            #keep the better of the two current
            if len(inval) < phieval:
                phi = newphi
                phieval = len(inval)
                print(f'the better function is {phi[1]} with {phieval} misses')
            
            i = i + 1
        r = r + 1
    
    # update current function
    solver = phi[0]
    fun = phi[0]
    
    
    return phi


class FileEnd(Exception): pass           
    
def searchEM(solver, fun):
    blockinglength = 2      # how big is the difference between word length that we still want to compare
    random.seed(1234)       # setseed to get compareable results from sampling in the filter

    ## second variation with tell and seek (deleted first version)
    totalwords = 0
    #over all files
    for i in range(6, len(wordlenClean)):
        print(f'start comparing words with length {i}')
        wordlengthtimestart = time.time()
        try:
            # get a word, then compare against all later words
            wordIndex = 0
            while True:     # thsi will break if every word from wordlenClean[i] has been compared from 'raise FileEnd'
                
                currentWord = []           # out of file f1 to compare against other files
                
                with open(wordlenClean[i], 'r', encoding= "utf-8") as f1:
                    tmp = -1    #-1 to ensure that at least one line is read
                    line = ''
                    # find next word in file
                    f1.seek(wordIndex)
                    line = f1.readline()
                    if line == '': raise FileEnd    # raise to start with the next file
                    wordIndex = f1.tell()
                    
                    # now the earliest word that hasnt been compared is in line
                    currentWord = line.split()
                    
                    # check if the current word is even worth looking at
                    # compare against the existing valid word list
                    # THIS DOES EXCLUDE MOST COMPOUND WORDS
                    if currentWord[0] not in validWordSet: 
                        continue         # if the word is not valid, get new
                    
                    
                    # OLD implementation that didnt validate the current word 
                    # to bring back also adjust 'i -2' to 'i +1' in the below for-loop
                    # # compare to the next words in the same file
                    # line2 = f1.readline()
                    # while line2 != '':
                    #     WordCompare(solver, fun, currentWord, line2.split())
                    #     line2 = f1.readline()
                    
                # get the words from the next file in blockinglength
                for j in range(max(2, i -blockinglength), min(i+ blockinglength +1, len(wordlenClean))):
                    with open(wordlenClean[j], 'r', encoding= "utf-8") as f2:
                        # get the words
                        line2 = f2.readline()
                        while line2 != '':
                            WordCompare(solver, fun, currentWord, line2.split())
                            line2 = f2.readline()

                # completed wordLoop
                totalwords = totalwords +1
                if totalwords % 1000000 == 0:
                    print(f'completed comparing word #{totalwords}')
                    
        # catch to end current file and start new 
        except FileEnd:
            # according to stackoverflow this is a correct and usable option to handle br4eaking multiple loops
            fileduration = time.time()- wordlengthtimestart
            print(f'finished comparing all of {wordlenClean[i]} in {fileduration / 60} minutes')
                
    print(f'Finished loop')
    


# variation with blocking per file -size
def searchEM2(solver, fun):
    blockinglength = 2      # how big is the difference between word length that we still want to compare
    random.seed(1234)       # setseed to get compareable results from sampling in the filter
    

    ## second variation with tell and seek (deleted first version)
    totalwords = 0
    #over word length
    for i in range(10, 11):#len(wordlenClean)):
        print(f'start comparing words with length {i}')
        wordlengthtimestart = time.time()
        
        #over letter
        for c in charlist:
            filepath = getletterpath(str(i), c)
            try:
                # get a word, then compare against all later words
                wordIndex = 0
                while True:     # thsi will break if every word from wordlenClean[i] has been compared from 'raise FileEnd'

                    currentWord = []           # out of file f1 to compare against other files

                    with open(filepath, 'r', encoding= "utf-8") as f1:
                        tmp = -1    #-1 to ensure that at least one line is read
                        line = ''
                        # find next word in file
                        f1.seek(wordIndex)
                        line = f1.readline()
                        if line == '': raise FileEnd    # raise to start with the next file
                        wordIndex = f1.tell()

                        # now the earliest word that hasnt been compared is in line
                        currentWord = line.split()

                        # check if the current word is even worth looking at
                        # compare against the existing valid word list
                        # THIS DOES EXCLUDE MOST COMPOUND WORDS
                        if currentWord[0] not in validWordSet: 
                            continue         # if the word is not valid, get new
                        
                        
                        # OLD implementation that didnt validate the current word 
                        # to bring back also adjust 'i -2' to 'i +1' in the below for-loop
                        # # compare to the next words in the same file
                        # line2 = f1.readline()
                        # while line2 != '':
                        #     WordCompare(solver, fun, currentWord, line2.split())
                        #     line2 = f1.readline()

                    ##old non-cached version
                    ## get the words from the next file in blockinglength
                    #for j in range(max(2, i -blockinglength), min(i+ blockinglength +1, len(wordlenClean))):
                    #    with open(getletterpath(str(j), c), 'r', encoding= "utf-8") as f2:
                    #        # get the words
                    #        line2 = f2.readline()
                    #        while line2 != '':
                    #            WordCompare(solver, fun, currentWord, line2.split())
                    #            line2 = f2.readline()
                    
                    
                    # get the words from the next file and load all in cache
                    for j in range(max(2, i -blockinglength), min(i+ blockinglength +1, len(wordlenClean))):
                        with open(getletterpath(str(j), c), 'r', encoding= "utf-8") as f2:
                            # get the words (and cut off the last '\n' character)
                            file2 = f2.read()[:-1].split('\n')
                        for line in file2:
                            WordCompare(solver, fun, currentWord, line.split())

                    # completed wordLoop
                    totalwords = totalwords +1
                    if totalwords % 1000000 == 0:
                        print(f'completed comparing word #{totalwords}')
                    
            # catch to end current file and start new 
            except FileEnd:
                # according to stackoverflow this is a correct and usable option to handle br4eaking multiple loops
                fileduration = time.time()- wordlengthtimestart
                print(f'finished comparing all of {getletterpath(str(i), c)} in {fileduration / 60} minutes')
                
    print(f'Finished loop')
    
    
# variation with blocking per file -size
# test with all cached Words
def searchEM2test(solver, fun):
    blockinglength = 2      # how big is the difference between word length that we still want to compare
    random.seed(1234)       # setseed to get compareable results from sampling in the filter

    ## second variation with tell and seek (deleted first version)
    totalwords = 0
    #over word length
    for i in range(13, 14):#len(wordlenClean)):
        print(f'start comparing words with length {i}')
        wordlengthtimestart = time.time()
        
        #over letter
        for c in charlist:
            filepath = getletterpath(str(i), c)
        
            # get a word, then compare against all later words
            wordIndex = 0

            currentWords = []           # all valid words from the current file
            with open(getletterpath(str(i), c), 'r', encoding= "utf-8") as f2:
                    # get the words (and cut off the last '\n' character)
                    allcurrentWords = f2.read()[:-1].split('\n')
            
            # sort out all invalid words, as they should not be compared against everything
            for line in allcurrentWords:
                currentWord = line.split()
                # sort out words that are NOT in validwords and thus should not be compared
                if currentWord[0] in validWordSet: 
                    currentWords.append(currentWord)

            ## Version 1
            ## iterrate over all current Words
            #for currentWord in currentWords:
            #    # get the words from the next file and load all in cache
            #    for j in range(max(2, i -blockinglength), min(i+ blockinglength +1, len(wordlenClean))):
            #        with open(getletterpath(str(j), c), 'r', encoding= "utf-8") as f2:
            #            # get the words (and cut off the last '\n' character)
            #            file2 = f2.read()[:-1].split('\n')
            #        for line in file2:
            #            WordCompare(solver, fun, currentWord, line.split())
                        
            # Version 2
            #get all file content of the files used with this process
            files = []
            tmptime = time.time()
            for j in range(max(2, i -blockinglength), min(i+ blockinglength +1, len(wordlenClean))):
                with open(getletterpath(str(j), c), 'r', encoding= "utf-8") as f2:
                        # get the words (and cut off the last '\n' character)
                        files.append(f2.read()[:-1].split('\n'))
            print(f'time to load {min(i+ blockinglength +1, len(wordlenClean)) - max(2, i -blockinglength)} files was {time.time() - tmptime}')
            
            # iterrate over all current Words
            for currentWord in currentWords:
                # get the words from the next file and load all in cache
                for j in range(max(2, i -blockinglength), min(i+ blockinglength +1, len(wordlenClean))):
                    with open(getletterpath(str(j), c), 'r', encoding= "utf-8") as f2:
                        # get the words (and cut off the last '\n' character)
                        file2 = f2.read()[:-1].split('\n')
                    for line in file2:
                        WordCompare(solver, fun, currentWord, line.split())

            # completed wordLoop
            totalwords = totalwords +1
            if totalwords % 1000000 == 0:
                print(f'completed comparing word #{totalwords}')
                
        
            # time
            fileduration = time.time()- wordlengthtimestart
            print(f'finished comparing all of {getletterpath(str(i), c)} in {fileduration / 60} minutes')
                
    print(f'Finished loop')
    
def loopcheck():
    pass
        
# CENTRAL FUNCTION
def main(new):
    posexampleData = []
    negexampleData = []
    if new:
        # load new modified examples
        posexampleData = exampleLoadNew(posPath)
        negexampleData = exampleLoadNew(negPath)
        with open(posexampleDataPath, 'w', encoding= "utf-8") as f:
            #print(f'lengthDiff\tPref\tSuff\tLevDis\trelChange\tcompMaxi')
            for e in posexampleData:
                f.write(f'{'\t'.join(map(str, e))}\n')
                #print(line)

        with open(negexampleDataPath, 'w', encoding= "utf-8") as f:
            #print(f'lengthDiff\tPref\tSuff\tLevDis\trelChange\tcompMaxi')
            for e in negexampleData:
                f.write(f'{'\t'.join(map(str, e))}\n')
                #print(line)
    else:
        posexampleData = exampleLoadOld(posexampleDataPath)
        negexampleData = exampleLoadOld(negexampleDataPath)
    
    kran = 30       # nr of restarts for the whole process; Random sample consensus
    kceg = 50       # max number of samples per attempt
    
    
    for i in range(0, 1):
        # curFun:= [solver, function]
        global foundexamples
        global foundFuncBlueprint
        timestamp = str(datetime.datetime.now())[:-7].replace(':', '-').replace(' ', '_')
        foundexamples = f'{foundexBlueprint}{timestamp}_found'
        foundFunctions = f'{foundFuncBlueprint}{timestamp}_foundFunctions'
        curFun = EMOPT(posEx= posexampleData, negEx= negexampleData, Kransac= kran, Kcegis= kceg)
        with open(foundFunctions,  'a', encoding= "utf-8") as e:
            e.write(f'loop #{i}: {curFun[1]}\n')
        searchEM2(*curFun)
        #searchEM2test(*curFun)
        
        loopcheck()
        #TODO: find load new examples in the respective pos/neg example-sets
    
    
    
    
    

#for path in examplepaths:
#    exampleData = exampleLoad(path)
#    print(exampleData)
#    print('seperator')
#    with open(exampleDataPath, 'w', encoding= "utf-8") as f:
#        print(f'lengthDiff\tPref\tSuff\tLevDis\trelChange\tcompMaxi')
#        for e in exampleData:
#            line = ''
#            for l in e:
#                line = line + f'{l}\t'
#            f.write(f'{line[:len(line)-1]}\n')
#            print(line)
#    
#    #for example in exampleData:
#    #    print(example)





print(time.time())
print(datetime.datetime.now())
tmp = 0



newData = False
#newData = True
main(newData)