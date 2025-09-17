import re
import time
import linecache as lc
import array
import os.path

rawFilePath = []
filePath1 = []
filePath2 = []
filePath3 = []
filePath4 = []
filePath5 = []
countFile1 = "./data/wordcount_1"
countFile2 = "./data/wordcount_2"


#setup files/paths
def path_setup():        
    for i in range(0,8):    
        rawFilePath.append("./data/raw1-0000"+ str(i) + "-of-00008")
        filePath1.append("./data/data-cleaning1_0"+ str(i))
        filePath2.append("./data/data-cleaning2_0"+ str(i))
        filePath3.append("./data/data-sort1_0"+ str(i))
        filePath4.append("./data/data-sortlist_0"+ str(i))


#positive regex hits
posConstraint = r'^[\w]+'                       # :=[A-Za-z0-9_]
posConstraintStrict = r'^[a-zA-Z]+$'            # matches words that are only letters
posConstraintUppercase = r'^[A-Z]+$'
posConstraintLowercase = r'^[a-z]+$'
posConstraintNoun = r'^[A-Z][a-z]*$'

#negative regex hits
negConstraintsLower = r'[_]'                    # removes _adj, _noun, and other unwanted characters
negConstraintsNumber = r'[0-9]'                 # removes numbers
negConstraintsSingleLetter = r'^[\w]$'          # one letter words

def regex_check(word: str):
    if re.search(posConstraintStrict, word):    # regex search but only start of line
        if len(word) <= 1: return False         # exclude one letter words
        return True


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
            if regex_check(word):
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
        w2 = open(filePath2[i], 'a+', encoding= "utf-8")
        

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
    with open(countFile1, 'w+') as c:
        for i in range(0, 8):
            count = 0
            overflowCount = 1
            while os.path.exists(f'{filePath1[i]}_{overflowCount}'):
                with open(f'{filePath1[i]}_{overflowCount}', 'r') as f:
                    while f.readline() != '':
                        count = count +1
                c.write(f'{count}  ')
                count = 0
                overflowCount = overflowCount + 1

            c.write('\n')
        
def bubble_sort():
    # bubble sort or hash table sort?
    with open(countFile1, 'r') as c:
        
        for i in range(0,1):
            #timer start
            timeStart = time.time()
            wordOffset = array.array('I',range(0, int(c.readline())))
            wordList = []
            
                
            #itterate over file to get words
            with open(filePath1[i], 'r') as f:
                for j in wordOffset:
                    wordList.append(f.readline())
            
            # Bubble sort implementation
            print(f'start bubble sort for file #{i}')
            counting = 0
            change = True 
            while change:       #change detection    # supposed worst-case O(n) loops
                change = False
                counting = counting +1
                if (counting % 1000) == 0: print(f'loop number {counting}')
                for j in range(0, len(wordOffset)-1):            # O(n)
                    if wordList[j] > wordList[j+1]:
                        change = True
                        wordList[j], wordList[j+1] = wordList[j+1], wordList[j]
                        wordOffset[j], wordOffset[j+1] = wordOffset[j+1], wordOffset[j]
                        
            timeEnd = time.time()
            print(f"time elapsed to sort file {filePath1[i]}: {timeEnd - timeStart}")
            print(f'start using placement to fill file #{i}')
                    
            # no the wordOffset entry for [0] should be the number of the line where the word is stored in the file
            with open(filePath3[i],'a+', encoding= "utf-8") as sf:
                for j in wordOffset:
                    # change between filepath1 and filepath2 for every data, or only the words
                    sf.write(filePath1[i], j - 1)       # use linecache to read only the desired words
                    
            timeEnd2 = time.time()
            print(f"time elapsed writing new file {filePath3[i]}: {timeEnd2 - timeEnd}")
            print(f'finished sorting file #{i}')
            


            #timer end
            timeEnd = time.time()
            print(f"time elapsed to sort and create file {filePath3[i]}: {timeEnd - timeStart}")

    pass

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
                with open(f'./data/excel_exports/data-cleaning_excelsort_0{i}_{overflowCount}.csv', 'r') as f:
                    tmpOffset = 0
                    for j in range(0, int(fileOffset[overflowCount])):
                        # sort on merge
                        data = f.readline().split(";")
                        
                        #search for fitting spot and insert the new word before reading the next
                        while(tmpOffset< len(wordList) and data[0] != '' and data[0].lower() > wordList[tmpOffset].lower()):
                            #enter loop when new word is larger than current selected word out of list
                            tmpOffset = tmpOffset +1
                            if tmpOffset % 100000 == 0: print(f'file {i}; subfile {overflowCount}; offset check: {tmpOffset}')
                        #per loop invariant (data[0] =< wordList[tmpOffset]) is true now
                        #
                        wordList.insert(tmpOffset, data[0])                    #word
                        wordOffset.insert(tmpOffset, int(data[1]) + int(fileOffset[overflowCount-1]))             #offset
                            
                                
                overflowCount = overflowCount + 1
            #print(wordOffset)
            
            ## Bubble sort implementation
            #print(f'start bubble sort for file #{i}')
            #counting = 0
            #change = True 
            #while change:       #change detection    # supposed worst-case O(n) loops
            #    change = False
            #    counting = counting +1
            #    if (counting % 100) == 0: print(f'loop number {counting}')
            #    for j in range(0, len(wordOffset)-1):            # O(n)
            #        if wordList[j] > wordList[j+1]:
            #            change = True
            #            wordList[j], wordList[j+1] = wordList[j+1], wordList[j]
            #            wordOffset[j], wordOffset[j+1] = wordOffset[j+1], wordOffset[j]
            #            
            timeEnd = time.time()
            print(f"time elapsed to sort file {filePath1[i]}: {timeEnd - timeStart}")
            print(f'start using placement to fill file #{i}')
                    
            # no the wordOffset entry for [0] should be the number of the line where the word is stored in the file
            tmp = 0
            with open(filePath3[i],'w+', encoding= "utf-8") as sf:
                for j in wordOffset:
                    tmp = tmp +1 
                    if tmp % 100000 == 0:
                        print(f'this is the {tmp}th loop through {filePath1[i]}')
                    # change between filepath1 and filepath2 for every data, or only the words
                    txt = lc.getline("./data/data-cleaning1_00_1", j)
                    sf.write(lc.getline(str(filePath2[i]), j))       # use linecache to read only the desired line)
                    
            timeEnd = time.time()
            print(f"time elapsed writing new file {filePath3[i]}: {timeEnd - timeStart}")
            print(f'finished sorting file #{i}')
            


            #timer end
            timeEnd = time.time()
            print(f"time elapsed to sort and create file {filePath3[i]}: {timeEnd - timeStart}")

    

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
    ## look for convertion errors from utf-8 to excel
    
cleanupSort()

##bubble_sort()