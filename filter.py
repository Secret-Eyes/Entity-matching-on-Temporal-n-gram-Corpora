
def filterPrefix(w1, w2, lim: int):
    for i in range(0, min(lim, len(w1), len(w2))):
        if w1[i] != w2[i]: return False
    return True

def filterSuffix(w1, w2, lim: int):
    for i in range(0, lim):
        if w1[len(w1) -i -1] != w2[len(w2) -i -1]: return False
    return True

def filterLength(w1, w2, lim: int =2):
    return abs(len(w1) - len(w2)) <= lim

# return False if there are less entries than limit
def filterTotalAmount(d1, limit: int= 100):
    total = 0
    for i in range(1, len(d1)):
        total = total + d1[i].split(',')[1]
    return total >= limit
        
    

# functions to get the differences, usefull in compare and for the initialisation of the examples
def getfilterPrefix(w1, w2):
    for i in range(0, len(w1)):
        if w1[i] != w2[i]: return i
    return w1

def getfilterSuffix(w1, w2):
    for i in range(0, len(w1)):
        if w1[len(w1) -i -1] != w2[len(w2) -i -1]: return i
    return len(w1)

def getfilterLength(w1, w2):
    return abs(len(w1) - len(w2))




# return False if filter is not passed
def filter(w1: str, w2: str):
    print(f'filter Prefix: {filterPrefix(w1, w2)} for {w1} {w2}')
    print(f'filter Suffix: {filterSuffix(w1, w2)} for {w1} {w2}')
    print(f'filter Length: {filterLength(w1, w2)} for {w1} {w2}')