import random
import time
import linecache as lc
import Levenshtein as lev

rawFilePath = []
filePath1 = []
filePath2 = []
filePath3 = []
filePath4 = []
filePath5 = []
wordlenClean = []
countFile1 = "./data/wordcount_1"
countFile2 = "./data/wordcount_2"

# way faster than loading the file every time
wordCountPerYear = "1800,72711918,642619,4039	1801,73637691,606919,3453	1802,70324882,636532,3968	1803,74977221,664339,3764	1804,82305130,712429,3972	1805,83109241,711789,3967	1806,85622393,720463,3469	1807,68092435,534472,3148	1808,77014840,625152,3384	1809,76622885,621900,2868	1810,89079881,749505,3559	1811,85438578,676564,3262	1812,84600290,647378,3050	1813,77826652,568141,3097	1814,73305376,552534,3441	1815,88981289,712435,3425	1816,98164886,733014,3864	1817,116055413,840400,4445	1818,108921112,798397,4232	1819,126596541,903907,4729	1820,141857340,1004820,4879	1821,151740414,1086564,4755	1822,158806080,1131093,5077	1823,158472227,1101249,4923	1824,172229586,1229844,5661	1825,190736675,1350523,6136	1826,203597396,1413155,6289	1827,218009545,1479786,6409	1828,269310602,1816802,7049	1829,263814471,1735229,6386	1830,298362737,1933951,7027	1831,298595295,1881065,6597	1832,300447104,1845367,6484	1833,317307083,1960803,6773	1834,341503819,2031565,7106	1835,364017924,2174026,7517	1836,384974173,2322379,7805	1837,410454044,2465622,8025	1838,453746287,2675756,8450	1839,450054139,2667921,8617	1840,487429485,2877748,9706	1841,457862116,2718236,8784	1842,492985141,2839346,8873	1843,529526486,3044418,9820	1844,581934428,3382262,10420	1845,607667959,3535308,10803	1846,633872576,3704370,11149	1847,581683427,3245694,10156	1848,503248997,2784313,10632	1849,400078264,2186850,7822	1850,557947071,3133273,10406	1851,673135486,3736016,10421	1852,664041038,3606320,10928	1853,739700463,3949844,11855	1854,756904959,4035741,12425	1855,769101656,4070637,12344	1856,784833876,4216393,12360	1857,809699866,4284997,12278	1858,830170776,4405018,12876	1859,786088944,4080937,11904	1860,907355988,4687105,13868	1861,879738736,4641387,13585	1862,903344103,4782112,13783	1863,967374132,5061927,14023	1864,935700200,4767184,13363	1865,1009511990,5282082,14365	1866,953559921,4890837,13358	1867,1066622808,5490608,14710	1868,1081645864,5551516,15804	1869,1118322317,5675713,15895	1870,985800158,4979170,15083	1871,924444880,4608711,14043	1872,1016551796,5084460,15070	1873,1024496226,5140956,15122	1874,1140094162,5775249,15503	1875,1084072525,5455250,15155	1876,1154737476,5794174,16090	1877,1130838698,5704863,15763	1878,1127491747,5599565,14501	1879,1087221070,5439396,12606	1880,919739694,4454145,7696	1881,934720576,4545569,7791	1882,1029838374,5024438,8898	1883,972884407,4720792,8536	1884,975098545,4738362,8613	1885,1014644028,4918072,8580	1886,1024710004,4905050,8790	1887,1068902257,5136302,9013	1888,1064397580,5075886,9358	1889,1092431959,5247455,9528	1890,1150024192,5507635,10025	1891,1171854954,5592450,10357	1892,1227556287,5862161,10596	1893,1284716957,6128620,11168	1894,1248619709,5934672,10828	1895,1322069939,6221823,11260	1896,1388536136,6558178,11816	1897,1441811694,6798776,12327	1898,1478780755,7019794,12708	1899,1530177965,7189692,13053	1900,1606392383,7696308,14824	1901,1702564550,8061526,14768	1902,1790336205,8496387,15727	1903,1829232512,8767732,16462	1904,2006111892,9565412,18006	1905,2047867899,9735053,18385	1906,2214492392,10400954,19470	1907,2230352585,10672846,20149	1908,2360032889,11230231,21422	1909,2105244191,10006330,19103	1910,2102373500,10092907,19655	1911,2125823164,10179685,19811	1912,2156352842,10355710,20499	1913,2294067635,10825295,21030	1914,1926513254,9088194,18086	1915,1303297330,6133527,12567	1916,1171078225,5438216,11201	1917,1085432860,5122978,10517	1918,1016934305,4768437,9924	1919,1081374156,5277858,11923	1920,1287235915,6288733,13004	1921,1320510989,6355327,12967	1922,1414708644,6858213,14132	1923,871344263,4243591,8034	1924,710986072,3505620,6870	1925,945628634,4665930,9442	1926,936510052,4540052,9838	1927,980687841,4753627,10308	1928,1039957984,5005245,10786	1929,1013045045,4876174,10600	1930,1048718986,5082833,10978	1931,942931415,4477426,9711	1932,855770833,4096332,9350	1933,830591159,3958578,9797	1934,761519002,3662082,10129	1935,786257382,3762147,9647	1936,761183505,3637798,9250	1937,774678298,3712027,9223	1938,764948782,3654775,8942	1939,703249661,3368228,7941	1940,533032180,2606528,6503	1941,471714406,2301600,5581	1942,401658213,2033650,4868	1943,452617027,2348850,5307	1944,266778995,1423291,3733	1945,168184281,894573,2348	1946,236775908,1298880,3774	1947,364816117,1926228,4860	1948,464752809,2364370,5584	1949,585343547,2898483,6505	1950,730914877,3440557,7141	1951,648782962,3037088,6931	1952,727572159,3424224,7430	1953,800951713,3664781,7863	1954,898127587,4169908,9031	1955,962537969,4433815,9779	1956,1087543078,5029711,10970	1957,1089573279,5055847,10870	1958,1165348441,5420356,11812	1959,1267437554,5986962,12726	1960,1393555013,6631490,14314	1961,1412675823,6675965,14672	1962,1580309482,7600415,17634	1963,1579969762,7681520,17461	1964,1596843959,7699697,17542	1965,1826131535,8913933,18956	1966,1782719873,8637147,19295	1967,1960856651,9496112,20649	1968,2020879425,9782555,22053	1969,1979404592,9498796,20989	1970,2002101091,9716092,22291	1971,1823539299,8806061,19577	1972,1764867278,8613500,19469	1973,1687087779,8325592,19070	1974,1683063492,8240590,18753	1975,1708913611,8406355,18538	1976,1584739011,7801304,17571	1977,1646950672,8071835,18138	1978,1685987816,8316918,18451	1979,1667105426,8306784,19511	1980,1745938039,8603071,19791	1981,1693928581,8412349,19374	1982,1674053298,8376626,19741	1983,1706931529,8385288,19497	1984,1665061391,8110349,18303	1985,1645433635,8073709,18093	1986,1589766701,7666108,17463	1987,1586047783,7666945,16996	1988,1666986583,8076032,18048	1989,1655869369,7855844,17761	1990,1656391844,7925411,17779	1991,1578679740,7624379,17306	1992,1566672746,7451461,17024	1993,1688703959,7944457,17374	1994,1749203788,8263836,18137	1995,1742329745,8245350,17965	1996,1686053587,7947005,17394	1997,1707313100,8095687,17657	1998,1761106604,8287823,17565	1999,1874109252,8945925,19310	2000,2031235259,9786838,21636"
totalWords = wordCountPerYear.split()
totalWordsYear = []
totalWordsFirst = []
totalWordsSecond = []
totalWordsThird = []
for count in totalWords:
    tmp = count.split(',')
    totalWordsFirst.append(int(tmp[1]))
    # totalWordsSecond.append(int(tmp[2]))
    # totalWordsThird.append(int(tmp[3]))

#setup files/paths
def path_setup():        
    for i in range(0,8):    
        rawFilePath.append("./data/words/raw1-0000"+ str(i) + "-of-00008")
        filePath1.append("./data/words/data-cleaning1_0"+ str(i))
        filePath2.append("./data/words/data-cleaning2_0"+ str(i))
        filePath3.append("./data/words/data-sort1_0"+ str(i))
        filePath4.append("./data/words/data-sortclean_0"+ str(i))
        
    #group everything above 25 length together
    for i in range(0, 26):
        tmp = ""
        if i < 10: tmp = "0"
        filePath5.append(f'./data/wordlen/word_length_{tmp}{i}')
        wordlenClean.append(f'./data/wordlen/word_length_clean_{tmp}{i}')
        
path_setup()

# WORD function; needs only the words as input
def levenshteinDistance(word1, word2, limit: int = 0):
    res = lev.distance(word1, word2)
    return res

# count total number of occurances over all the years (1800-2000)
def countSingleWord(data):
    copy = data[:]
    total = 0
    # this line gets rid of the word IF it is still in the list
    if ',' not in copy[0]: copy.pop(0)
    for d in copy:
        total = total + int(d.split(',')[1])
        
    return total
        

def yearDiff(data1, data2):
    result = []
    i, j = 1, 1           # i years from data1; j years from data2
    iMax, jMax = len(data1), len(data2)
    while i < iMax and j < jMax:
        yearData1 = [int(x) for x in data1[i].split(',')]
        yearData2 = [int(x) for x in data2[j].split(',')]
        if yearData1[0] == yearData2[0]:
            result.append((yearData1[0], yearData1[1] - yearData2[1]))
            i, j = i +1, j +1
        elif yearData1[0] < yearData2[0]:
            result.append((yearData1[0], yearData1[1]))
            i = i +1
        elif yearData1[0] > yearData2[0]:
            result.append((yearData2[0], -yearData2[1]))
            j = j +1
    
    return result

def localMaxima(data, local:int = 10):
    data.append("2001,0,0")
    dataYear = []
    dataCount = []
    result = []
        
    timestart = time.time()
    # some words may have no entries in some years
    dataIndex = 1
    for year in range(1800, 2001):
        tmp = data[dataIndex].split(',')
        if int(tmp[0]) == year:
            dataYear.append(int(tmp[0]))
            dataCount.append(int(tmp[1]))
            dataIndex = dataIndex +1
        else:
            dataYear.append(year)
            dataCount.append(0)
    
    # idea 1 nestled for-loops in n* (2 *range)
    for i in range(0,201):
        for j in range(max(0, i -local), min(201, i +local)):
            if i != j and dataCount[i] < dataCount[j]:      # check only for break criteria
                break
        else: result.append(data[i+1])
    timestop = time.time()
    print(f'time for method 1: {timestop - timestart}')
        
        
                

    timestart = time.time()
    # some words may have no entries in some years
    dataIndex = 1
    for year in range(1800, 2001):
        tmp = data[dataIndex].split(',')
        if int(tmp[0]) == year:
            dataYear.append(int(tmp[0]))
            dataCount.append(int(tmp[1]))
            dataIndex = dataIndex +1
        else:
            dataYear.append(year)
            dataCount.append(0)
    # idea 2
    # go through data forwards and backwards
    # then search through both to find maximas
    # 2n + (& operator costs) + n/2 to check for range
    listUp = []
    listDown = []
    isUp = True     # does the usage rise?
    
    # due to the nature of this implemetnation, if following years have the same usage, only the most recent (highest years) is added to the list
    for i in range(0, 200): # check over 200 years
        #d1 = data[i].split(',')
        #d2 = data[i +1].split(',')
        if dataCount[i] < dataCount[i +1]:               # 1 < 2  -> 1 may be minima
            isUp = True
        elif dataCount[i] > dataCount[i +1]:             # 3 > 2  -> 3 may be maxima
            if isUp:
                listUp.append(i)
                isUp = False
    
    #print(listUp)
    # both now contain only respective local peaks
        # find range
    currentGoal = 0 
    
    index = 0
    
    while index != len(listUp) -1:       # maximal n/2 loops, one for each year in listUp
        if abs(dataYear[listUp[index]] - dataYear[listUp[index +1]]) < local:
            if dataCount[listUp[index]] < dataCount[listUp[index +1]]:
                listUp.pop(index)
            else:
                listUp.pop(index +1)
        else:
            index = index +1
            
    result2 = []
    for index in listUp:
        result2.append(f'{dataYear[index]},{dataCount[index]}')
    timestop = time.time()
    print(result)
    print(f'time for method 2: {timestop - timestart}')
    print(result2)
    return result2
        
def localMinima(data, local:int = 10):
    data.append("2001,9099037677")#highest number of total words per year (2013)
    dataYear = []
    dataCount = []
        
    # some words may have no entries in some years
    dataIndex = 1
    for year in range(1800, 2001):
        tmp = data[dataIndex].split(',')
        if int(tmp[0]) == year:
            dataYear.append(int(tmp[0]))
            dataCount.append(int(tmp[1]))
            dataIndex = dataIndex +1
        else:
            dataYear.append(year)
            dataCount.append(0)
            
    # idea 1 nestled for-loops in n* (2 *range)

    
    # idea 2
    # go through data forwards and backwards
    # then search through both to find maximas
    # 2n + (& operator costs) + n/2 to check for range
    listUp = []
    listDown = []
    isDown = True     # does the usage fall?
    
    # due to the nature of this implemetnation, if following years have the same usage, only the most recent (highest years) is added to the list
    for i in range(0, 200): # check over 200 years
        #d1 = data[i].split(',')
        #d2 = data[i +1].split(',')
        if dataCount[i] > dataCount[i +1]:               # 1 < 2  -> 1 may be minima
            if not isDown:
                isDown = True
        elif dataCount[i] < dataCount[i +1]:             # 3 > 2  -> 3 may be maxima
            if isDown:
                listDown.append(i)
                isDown = False
    
    # both now contain only respective local peaks
        # find range
    currentGoal = 0 
    
    index = 0
    
    while index != len(listDown) -1:       # maximal n/2 loops, one for each year in listDown
        if abs(dataYear[listDown[index]] - dataYear[listDown[index +1]]) < local:
            if dataCount[listDown[index]] > dataCount[listDown[index +1]]:
                listDown.pop(index)
            else:
                listDown.pop(index +1)
        else:
            index = index +1
            
    result = []
    for index in listDown:
        result.append(f'{dataYear[index]},{dataCount[index]}')
    return result



#
#   Here begin the functions that factor in the relative word count in respect to the total word count of that year
#   as the total word count follows a common graph that increases with the book count and is not indicating of the actual usage
#   e.g. there is a dip in works created during WW2
#   
#   
#   
#   
#   

def fillData(data):
    newData = []
    
    # some words may have no entries in some years
    dataIndex = 2
    for year in range(1800, 2001):
        tmp = data[dataIndex].split(',')
        if int(tmp[0]) == year:
            newData.append(data[dataIndex])
            dataIndex = dataIndex +1
        else:
            newData.append(f'{year},0')
    
    return newData

# get relative data
def getRelData(data):
    relativeDataCount = []
    
    # some words may have no entries in some years
    dataIndex = 0
    for year in range(1800, 2001):
        tmp = data[dataIndex].split(',')
        if int(tmp[0]) == year:
            relativeDataCount.append((int(tmp[1])) / totalWordsFirst[year - 1800])
            dataIndex = dataIndex +1
        else:
            relativeDataCount.append(0)
            
    return relativeDataCount

# maxima in relation to total word count
def relativeMaxima(data, local:int = 10):
    #roughData.append("2001,0,0")
    #data = fillData(roughData)
    relativeDataCount = getRelData(data= data)
    result = []
        
    timestart = time.time()
    # some words may have no entries in some years
    
    # idea 1 nestled for-loops in n* (2 *range)
    for i in range(0,201):
        if relativeDataCount[i] == 0: continue
        for j in range(max(0, i -local), min(201, i +local)):
            # if there is a larger element, abandon the current value and check the next
            if i != j and relativeDataCount[i] < relativeDataCount[j]:
                break
            # only count maxima if there is no 'empty' year arround it
            if relativeDataCount[j] == 0:
                break
        # if there is no larger element, add to list
        else: result.append(data[i])
    timestop = time.time()
    #print(f'time for relativeMaxima: {timestop - timestart}')
    return result

# minima in relation to total word count
def relativeMinima(data, local:int = 10):
    # roughData.append("2001,0,0")
    # data = fillData(roughData)
    relativeDataCount = getRelData(data= data)
    result = []
        
    #timestart = time.time()
    
    # idea 1 nestled for-loops in n* (2 *range)
    for i in range(0,201):
        for j in range(max(0, i -local), min(201, i +local)):
            # if there is a smaller element, abandon the current value and check the next
            if i != j and relativeDataCount[i] > relativeDataCount[j]:
                break
        # if there is no smaller element, add to list
        else: 
            if data[i] != 0:
                result.append(data[i])
        
    #timestop = time.time()
    #print(f'time for relativeMinima: {timestop - timestart}')
    
    return result

# take stringarray ["word","yeardata", [...], "yeardata"] 
# and return floatarray [yeardiff, [...], yeardiff]
def relativeChange(data):
    #roughData.append("2001,0,0")
    #data = fillData(roughData)
    relativeDataCount = getRelData(data= data)
    result = []
        
    #timestart = time.time()
    
    for i in range(0, len(relativeDataCount)  -1):
        result.append(relativeDataCount[i +1]- relativeDataCount[i])
    
    
    #timestop = time.time()
    #print(f'time for relativeChange: {timestop - timestart}')
    
    return result


# if two words change usage the relation of the usage change should switch
# switches should be reflected by the division flipping to -1
def relativeChangeFlip(data1, data2):
    #data1.append("2001,0,0")
    #data2.append("2001,0,0")
    relData1 = relativeChange(data1)
    relData2 = relativeChange(data2)
    
    perYear = []
    
    for d1, d2 in zip(relData1, relData2):
        if d2 == 0: perYear.append(0.0)
        else :perYear.append(d1/d2)
    
    # assume 1 as standart change in relative usage over the years
    meanError = 0.0
    for x in perYear:
        if x < 0: x = -x
        meanError = meanError + ((1.0 - x) ** 2.0)
    meanError = meanError / len(perYear)
    
    #
    # should some outliners be excluded, like it is done with experimental data?
    # 
    
    return meanError
    

# compare the peaks of two words by the number of similar peaks around timeframe
# OLD possible pitfalls: a patter like [1,3,5,7] [2,4,6,8] would only have hits
# NEW if a value is alone, it counts as a miss. a pair counts as a hit. but the values of the hit get deleted, which can lead to edge cases
def compareMaxima(data1, data2, timeframe: int =3):
    m1 = relativeMaxima(data1)
    m2 = relativeMaxima(data2)
    
    in1, in2 = 0, 0
    comphit = 0
    comptotal = 1
    while(True):
        if in1 >= len(m1) or in2 >= len(m2):
            comptotal = comptotal + len(m1) - in1 + len(m2) - in2       # add the remaining unchecked amount
            break
        if abs(int(m1[in1].split(',')[0]) - int(m2[in2].split(',')[0])) < timeframe:
            comphit = comphit +1
            comptotal = comptotal +1
            in1 = in1 +1
            in2 = in2 +1
        elif int(m1[in1].split(',')[0]) > int(m2[in2].split(',')[0]):
            in2 = in2 +1
            comptotal = comptotal +1
        elif int(m1[in1].split(',')[0]) < int(m2[in2].split(',')[0]):
            in1 = in1 +1
            comptotal = comptotal +1
    
    # comparableValue = comphit / comptotal
    comprel = comphit / comptotal
    return comprel    

# compare the peaks of two words by the number of similar peaks around timeframe
# OLD possible pitfalls: a patter like [1,3,5,7] [2,4,6,8] would only have hits
# NEW if a value is alone, it counts as a miss. a pair counts as a hit. but the values of the hit get deleted, which can lead to edge cases
def compareExtrema(data1, data2, timeframe):
    #print(f'non-symetric function compareExtrema()')
    m1 = relativeMaxima(data1)
    m2 = relativeMinima(data2)
    
    in1, in2 = 0, 0
    comphit = 0
    comptotal = 0
    while(True):
        if in1 >= len(m1) or in2 >= len(m2):
            comptotal = comptotal + len(m1) - in1 + len(m2) - in2       # add the remaining unchecked amount
            break
        if abs(int(m1[in1].split(',')[0]) - int(m2[in2].split(',')[0])) < timeframe:
            comphit = comphit +1
            comptotal = comptotal +1
            in1 = in1 +1
            in2 = in2 +1
        elif int(m1[in1].split(',')[0]) > int(m2[in2].split(',')[0]):
            in2 = in2 +1
            comptotal = comptotal +1
        elif int(m1[in1].split(',')[0]) < int(m2[in2].split(',')[0]):
            in1 = in1 +1
            comptotal = comptotal +1
    
    # comparableValue = comphit / comptotal
    comprel = comphit / comptotal
    return comprel  
    

def compareExtremaSymm(data1, data2, method = 'add', timeframe: int= 3):
    val1 = compareExtrema(data1= data1, data2= data2, timeframe= timeframe)
    val2 = compareExtrema(data1= data2, data2= data1, timeframe= timeframe)
    if method == 'add':
        return val1 + val2
    elif method == 'mul':
        return val1 * val2
    elif method == 'div':
        return val1 / val2
    elif method == 'sub':
        return val1 - val2
    else:
        raise AssertionError(f'operation method {method} has to be one of [add, mul, div]')

####### UNFINISHED #######
def compareRelativeChange(data1, data2):
    #data1.append("2001,0,0")
    #data2.append("2001,0,0")
    relData1 = relativeChange(data1)
    relData2 = relativeChange(data2)
    # what counts as similar change?
    # compare with - or with /
    perYear = []
    
    for d1, d2 in zip(relData1, relData2):
        if d2 == 0: perYear.append(0.0)
        else :perYear.append(d1/d2)
        
    
    # Check for average deviation
    ####### UNFINISHED #######
    
    
# check for relation of change to be either 1 or -1
####### UNFINISHED #######
def findSwitchYears(data1, data2):
    raise Exception("unfinished function")
    data1.append("2001,0,0")
    data2.append("2001,0,0")
    relData1 = relativeChange(fillData(data1))
    relData2 = relativeChange(fillData(data2))
    
    perYear = []
    
    for d1, d2 in zip(relData1, relData2):
        
        perYear.append(d1 - d2)
    
    # change per year
    change1 = []
    change2 = []
    for i in range(0, len(relData1) -1):
        change1.append(relData1[i-1] - relData1[i])
        change2.append(relData2[i-1] - relData2[i])
    
    # compare the changes per year and find counteracting switches
    for i in range(0, len(change1)):
        # direct comparison would almost always be false
        # what value is good to check for proximity without comparing too broad or too narrow
        pass
    ####### UNFINISHED #######
    
    
    
    
    
def compare_main():
    # get example matches
    x, y = random.randrange(0,400000), random.randrange(0,400000)
    #x, y = 10000, 10001    
    l = 5               # change l to the length of the searched words
    ##x = 70730
    l1, l2 = lc.getline(str(wordlenClean[l]), x).split(), lc.getline(str(wordlenClean[l]), y).split()
    w1, w2 = l1[0], l2[0]
    #print(l1)

    print(f"The Levenshtein distance between {w1} and {w2} is : {levenshteinDistance(w1, w2)}")
    #print(yearDiff(l1, l2))
    print("~~~~~~~~~~")
    print(f'peaks of {w1} are:\n{relativeMaxima(l1)}')
    print("~~~~~~~~~~")
    print(f'lows of {w1} are:\n{relativeMinima(l1)}')
    print("~~~~~~~~~~")
    print(f'relative peaks of {w1} are:\n{relativeMaxima(l1)}')
    print("~~~~~~~~~~")
    print(f"The mean sqared error distance between {w1} and {w2} is : {relativeChangeFlip(l1, l2)}")

##compare_main()