import re
import time
import linecache as lc
import array
import os.path
from os import listdir
from pathlib import Path
import sys
print("Interpreter:", sys.executable)

rawFilePath = []
filePath1 = []
filePath2 = []
filePath3 = []
filePath4 = []
filePath5 = []
filePath6 = []
wordLenUnder100 = []
wordlensort = []
countFile1 = "./data/wordcount_1"
countFile2 = "./data/wordcount_2"

charlist = []

#path setup for length + prefix letter seperation
def getletterpath(wordlen:str , letter:str):
    fix = wordlen
    if len(wordlen) == 1: fix = '0' + fix
    return f'./data/wordlensort/len{fix}/{letter}_words'
    
def getletterdir(wordlen:str , letter:str):
    fix = wordlen
    if len(wordlen) == 1: fix = '0' + fix
    return f'./data/wordlensort/len{fix}'
    
#setup files/paths
def path_setup():        
    for i in range(0,8):    
        rawFilePath.append("./data/words/raw1-0000"+ str(i) + "-of-00008")
        filePath1.append("./data/words/data-cleaning1_0"+ str(i))
        filePath2.append("./data/words/data-cleaning2_0"+ str(i))
        filePath3.append("./data/words/data-sort1_0"+ str(i))
        filePath4.append("./data/words/data-sortclean_0"+ str(i))
        
    #charlist with all starting letters
    for k in range(ord('A'), ord('Z')):
        charlist.append(chr(k))
    for k in range(ord('a'), ord('z')):
        charlist.append(chr(k))
    for k in ['Ä', 'Ö', 'Ü', 'ä', 'ö', 'ü', 'ß']:
        charlist.append(k)
    
    #group everything above 25 length together
    for i in range(0, 26):
        tmp = ""
        if i < 10: tmp = "0"
        filePath5.append(f'./data/wordlen/word_length_{tmp}{i}')
        filePath6.append(f'./data/wordlen/word_length_clean_{tmp}{i}')
        wordLenUnder100.append(f'./data/wordlen/word_length_reduced_{tmp}{i}')
        
        if i <= 1: continue
        # length + letter seperation
        for k in charlist:
            dire =getletterdir(str(i), k)
            path = getletterpath(str(i), k)
            Path(dire).mkdir(parents=True, exist_ok= True)
            with open(path, 'w'): pass

#  ^w+$  wwwwwwwwwwwwww  wwwiwwwww
#positive regex hits
posConstraint = r'^[\w]+'                       # :=[A-Za-z0-9_]
posConstraintStrict = r'^[a-zA-ZÄÖÜäöüß]+$'            # matches german words that are only letters
posConstraintUppercase = r'^[A-Z]+$'
posConstraintLowercase = r'^[a-z]+$'
posConstraintNoun = r'^[A-Z][a-z]*$'
posConstraintGermanWord = r'^[A-Za-zÖÄÜäöüß][a-zäöüß]*$'

#negative regex hits
negConstraintsLower = r'[_]'                    # removes _adj, _noun, and other unwanted characters
negConstraintsNumber = r'[0-9]'                 # removes numbers
negConstraintsSingleLetter = r'^[\w]$'          # one letter words

def regex_check(word: str):
    if re.search(posConstraintStrict, word):    # regex search but only start of line
        if len(word) <= 1: return False         # exclude one letter words
        return True

def regex_check2(word: str):
    return re.search(posConstraintGermanWord, word)
    


def basic_clean():
    for i in range(0,8):
        #timer start
        timeStart = time.time()
        overflowCount = 1
        f = open(rawFilePath[i], 'r', encoding = "utf-8")
        w = open(f'{filePath1[i]}_{overflowCount}', 'w+', encoding= "utf-8")
        w.truncate(0)
        line = f.readline()

        #test area


        #test area end
        x = 1                       # rough count of words, needed to track file sizes
        while line != '':
                                  

            txt = line.split()
            word = txt[0]       #regex search but only start of line
            if regex_check2(word):
                w.write(str(word)+"\n")
                x = x+1         
            #for s in txt:                          #itterate over all parameters
            #    if re.search(constraint, s):        #regex search for letters in the beginning every part
            #        w.write(s+"\n")
            #        #print(s)

            #print(txt[0])
            
            # excel can only display 1048576 rows
            # open new file to store words
            if x % 1000000 == 0:
                overflowCount = overflowCount + 1 
                x = x +1
                w.close()
                w = open(f'{filePath1[i]}_{overflowCount}', 'w+', encoding= "utf-8")
                w.truncate(0)
                


            line = f.readline()

        f.close()
        w.close()

        #timer end
        timeEnd = time.time()
        print(f"time elapsed for file {rawFilePath[i]} in first function: {timeEnd - timeStart}")
        
    
def clean_data():
    
    for i in range(0,8):
        #timer start
        overflowCount = 1
        timeStart = time.time()
        f = open(rawFilePath[i], 'r',encoding = "utf-8")
        w1 = open(f'{filePath1[i]}_{overflowCount}', 'r', encoding= "utf-8")
        w2 = open(filePath2[i], 'w', encoding= "utf-8")

        cmpare = w1.readline()
        line = f.readline()
        while cmpare != '' and line != '':

            txt1 = line.split()[0]
            txt2 = cmpare.split()[0]
            #if txt1 == txt2: print(f'{txt1} = {txt2}')
            #print(txt2)
            #print(txt1 == txt2)
            while txt1 != txt2:         #this should ensure that both have the same word
                line = f.readline()
                if line == '': break
                txt1 = line.split()[0]
            w2.write(line)

            line = f.readline()
            cmpare = w1.readline()
            
            #jump to different file
            if cmpare == '':
                overflowCount = overflowCount + 1
                if os.path.exists(f'{filePath1[i]}_{overflowCount}'):
                    w1.close()
                    w1 = open(f'{filePath1[i]}_{overflowCount}', 'r', encoding= "utf-8")
                    cmpare = w1.readline()
                
                

        f.close()
        w1.close()
        w2.close()

        #timer end
        timeEnd = time.time()
        print(f"time elapsed for file {rawFilePath[i]} in second function: {timeEnd - timeStart}")
        
def countWords():
    maxLen = ''
    with open(countFile1, 'w+') as c:
        for i in range(0, 8):
            count = 0
            overflowCount = 1
            while os.path.exists(f'{filePath1[i]}_{overflowCount}'):
                with open(f'{filePath1[i]}_{overflowCount}', 'r') as f:
                    line = f.readline()
                    
                    while line != '':
                        if len(maxLen) < len(line):  
                            maxLen = line
                            print(f'new longest word with {len(maxLen)} lenght:  {line}')
                        line = f.readline()
                        count = count +1
                        
                c.write(f'{count}  ')
                count = 0
                overflowCount = overflowCount + 1

            c.write('\n')
        c.write(str(maxLen))

def cleanupSort():
    with open(countFile1, 'r') as c:
        
        for i in range(0,8):
            #timer start
            timeStart = time.time()
            wordOffset = []
            wordList = []
            overflowCount = 1
            zeroArray = ['0']
            fileOffset = zeroArray + c.readline().split()
            print(fileOffset)
            size = 0
            for k in fileOffset:
                size = size + int(k)
            
            #itterate over file to get words
        
            while os.path.exists(f'./data/excel_exports/data-cleaning_excelsort_0{i}_{overflowCount}.csv'):
                ##only if there is no second file yet
                #if not os.path.exists(f'./data/excel_exports/data-cleaning_excelsort_0{i}_{overflowCount+1}.csv'):
                #    with open(f'./data/excel_exports/data-cleaning_excelsort_0{i}_{overflowCount}.csv', 'r') as f:
                #        for j in range(0, int(fileOffset[1])):
                #            data = f.readline().split(";")
                #            wordList.append(data[0])                    #word
                #            wordOffset.append(int(data[1]) + int(fileOffset[overflowCount]))             #offset
                
                ## if there is a second file
                #else:
                with open(f'./data/excel_exports/data-cleaning_excelsort_0{i}_{overflowCount}.csv', 'r', encoding = "utf-8") as f:
                    tmpOffset = 0
                    for j in range(0, int(fileOffset[overflowCount])):
                        # sort on merge
                        data = f.readline().split(";")
                        if regex_check2(data[0]):          # sort out only german words/nouns. this should NOT be triggered as false
                            #search for fitting spot and insert the new word before reading the next
                            while(tmpOffset< len(wordList) and data[0] != '' and data[0].lower() > wordList[tmpOffset].lower()):
                                #enter loop when new word is larger than current selected word out of list
                                tmpOffset = tmpOffset +1
                                if tmpOffset % 100000 == 0: print(f'file {i}; subfile {overflowCount}; offset check: {tmpOffset} of {size}')
                            #per loop invariant (data[0] =< wordList[tmpOffset]) is true now
                            #
                            wordList.insert(tmpOffset, data[0])                    #word
                            wordOffset.insert(tmpOffset, int(data[1]) + (int(fileOffset[overflowCount-1]) * (overflowCount -1)))             #offset
                            
                        else: continue
                            
                                
                overflowCount = overflowCount + 1
            #print(wordOffset)
            
            ## check if there are duplicate words;    was NOT the source of error
            #tmp = len(wordOffset)
            #unique_values = list(set(wordOffset))
            #tmp2 = len(unique_values)
            #continue
            
            
            
            #            
            timeEnd = time.time()
            print(f"time elapsed to sort file {filePath1[i]}: {timeEnd - timeStart}")
            print(f'start using placement to fill file #{i}')
                    
            # no the wordOffset entry for [0] should be the number of the line where the word is stored in the file
            tmp = 0
            with open(filePath3[i],'w+', encoding= "utf-8") as sf:
                ##sf.write("test")
                ##sf.close()
                for j in wordOffset:
                    tmp = tmp +1 
                    if tmp % 100000 == 0:
                        print(f'this is loop {tmp} of {size} through {filePath1[i]}')
                    # change between filepath1 and filepath2 for every data, or only the words
                    ##print(lc.getline(str(filePath2[i]), j))
                    sf.write(lc.getline(str(filePath2[i]), j))       # use linecache to read only the desired line)
                    
            timeEnd = time.time()
            print(f"time elapsed writing new file {filePath3[i]}: {timeEnd - timeStart}")
            print(f'finished sorting file #{i}')
            


            #timer end
            timeEnd = time.time()
            print(f"time elapsed to sort and create file {filePath3[i]}: {timeEnd - timeStart}")


def sortLength():
    timeStartMain = time.time()
    for i in range(2, 26):
        # open files in read to empty them
        open(filePath5[i], 'w', encoding= "utf-8")
            
    for i in range(0,8):
        #timer start
        timeStart = time.time()
            
        print(f'start sorting file #{i}')
                
        
        with open(filePath3[i],'r', encoding= "utf-8") as sf:
            
            line = sf.readline()
            sort = 0
            while line != '':
                wlen =  int(len(line.split()[0]))
                sort = sort +1
                if wlen > 25: wlen = 25
                
                with open(filePath5[wlen], 'a', encoding= "utf-8") as f:
                    f.write(line)
                if sort % 100000 == 0: print(f'sorted {sort} words of file #{i}: current word is {line.split()[0]}')
                line = sf.readline()
                
        timeEnd = time.time()
        print(f"time elapsed for sorting file {filePath3[i]}: {timeEnd - timeStart}")
        print(f'finished sorting file #{i}')
        


    #timer end
    timeEnd = time.time()
    print(f"time elapsed to sort and create file {filePath3[i]}: {timeEnd - timeStartMain}")
    pass    


# delete the data that is not in range of 1800-2000
def cleanLenght():
    for i in range(2, 26):
        print(f'start cleaning file {filePath5[i]}')
        # open files in read to empty them
        clean = open(filePath6[i], 'w', encoding= "utf-8")
        dirty = open(filePath5[i], 'r', encoding= "utf-8")
        
        line = dirty.readline()
        while line != '':
            
            data = line.split()
            newLine = data.pop(0)
            word = newLine
            tmpCheck = False
            for d in data:
                number = d.split(',')
                if 1800 <= int(number[0]) <= 2000:
                    tmpCheck = True
                    newLine = f'{newLine}\t{number[0]},{number[1]}'
            newLine = f'{newLine}\n'
            
            if not regex_check2(word= word):tmpCheck = False
            if tmpCheck: clean.write(newLine)
            line = dirty.readline()
        clean.close()
        dirty.close()
        print(f'finished cleaning file {filePath5[i]}')
           
                    
                    
def reducenumeber():
    for i in range(2, len(wordLenUnder100)):
        with open(filePath6[i], 'r', encoding= "utf-8") as f:
            with open(wordLenUnder100[i], 'w', encoding= "utf-8") as e:
                line = f.readline()
                while line != '':
                    data = line.split()
                    tmp = 0
                    for j in range(1, len(data)):
                        tmp = tmp + int(data[j].split(',')[1])
                    
                    if tmp >= 100:
                        e.write('\t'.join([data[0], str(tmp), *data[1:]]) + '\n')
                    line = f.readline()
                
                    
# sort by length and by letter
def sortlenlet():
    for i in range(2, 26):
        print(f'start sorting {wordLenUnder100[i]} by starting letter')
        with open(wordLenUnder100[i], 'r', encoding= "utf-8") as e:
            line = e.readline()
            while(line != ''):
                thischar = line[0]
                curpath = getletterpath(str(i), thischar)
                with open(curpath, 'a', encoding= "utf-8") as f:
                    f.write(line)
                
                line = e.readline()
                
                
                    
                    
totalstart= time.time()
#actual execution
path_setup()

#basic_clean()
#clean_data()
#countWords()

    ## export and sort in excel
    ## files have to contain under 1048576 words to be used in excel
    ## =SEQUENCE(X,1;1;1)           [(row,column;start;steps)]
    ## start numbering in excel at 1, because linecache also uses numbering starting at 1
    ## naming after data-cleaning_excelsort_0{i}_{overflowCount+1}.csv' 
    ## look for convertion errors from utf-8 to excel#
    
#cleanupSort()
#sortLength()
#cleanLenght()
#reducenumeber()
sortlenlet()

totaltime = time.time() - totalstart
print(f'The complete cleaning process took {round(totaltime / 60)} minutes and {round(totaltime) - (round(totaltime/60) *60)}')

##bubble_sort()