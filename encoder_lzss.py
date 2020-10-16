"""
Algorithm to encode a ascii file using lzss algorithm using both bitarray and bytearray
Complexity :worst case O(n log n) 
"""
import heapq
import sys
from bitarray import bitarray



def processArgs():
    """
    Reads the input from standard input and returns the filename, window, and lookahead
    @returns txtFile :bytearray
    @returns windowSize :integer
    @returns lookAheadSize :integer
    @complexity :O(n) 
    """
    fileName = sys.argv[1]
    srchSize = int(sys.argv[2])
    lkSize = int(sys.argv[3])
    with open(fileName,'rb') as f:
        txtFile = f.read()
    return txtFile, srchSize, lkSize


def writeBinary(header, data, fileName):
    """
    @param header :bitarray
    @param data :bitarray
    @filename :string
    @compexity :O(n)
    """
    # appending data to header
    header.extend(data)
    n = 8 - (len(header) % 8)
    # pad with 0 if required
    for i in range(n):
        header.append(0)
    with open(fileName, "wb") as file:
        header.tofile(file)


def findingFrequencies(someString):
    """
    Finds the frequencies of characters in the text file using a count list. 
    @param someString :bytearray
    @returns charList :bytearray 
        unsorted list of every unique byte in the file, each item has len == 1
    @returns frequencyList :list of triples
        triples are [<frequency of bytes>, <length of strings>, <byte array>]
        frequecy is stored as a triple so that the heap breaks ties on frequency
        of bytes on length of string
    @complexity :O(n)
    """
    # list of lenght 128 for frequency list
    asList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    charList = bytearray()
    freqencyList = []
    # iterating through the list and 
    # incrementing the count of each 
    for i in someString:
        asList[i] += 1
    # forming the frequencylist O(n)
    for i in range(len(asList)):
        if asList[i] != 0:
            charList.append(i)
            newByte = [i]
            freqencyList.append([asList[i], 1, bytearray(newByte)])
    return charList, freqencyList


def createHuffCode(charList, freqList):
    '''
    @param charList :bytearray
        unsorted list of every unique characters in the file, each item has len == 1
    @param frequencyList :list of triples
        triples are [<frequency of bytes>, <length of strings>, <byte array>]
        length of list is 128, one for every basic ascii code
        frequecy is stored as a triple so that the heap breaks ties on frequency
        of bytes on length of string
    @returns huffcode :bitarray
        length of list is 128, one list for every basic ascii code. 
    @complexity :worst case in O(n log n) at worst sink and rise operations would be
    conducted for every item. Adding items to heap makes use of heapify, which 
    keeps the complexity bounded by O(n log n)
    '''
    # create freqency list
    # other necessary variables
    huffCode = [bitarray() for i in range(128)]
    if len(freqList) == 0:
        raise Exception("There are no frequencies found")
    # case when size is 1
    if len(freqList) == 1:
        # serve 1 element from list
        huffCode[freqList[0][2][0]].append(0)
        # first item receives 0
        return huffCode
    heapq.heapify(freqList)
    # case when size is 2:
    if len(freqList) == 2:
    # serve 1 element from list
        item1 = heapq.heappop(freqList)
        # serve 1 element from list
        item2 = heapq.heappop(freqList)
        # first item receives 0, second serve receives 1 as code
        huffCode[item1[2][0]].append(0)
        huffCode[item2[2][0]].append(1)
        return huffCode
    else:
        # serve 1 element from list
        item1 = heapq.heappop(freqList)
        # serve 1 element from list
        item2 = heapq.heappop(freqList)
        # first item receives 0, second serve receives 1 as code
        huffCode[item1[2][0]].append(0)
        huffCode[item2[2][0]].append(1)
        # summing the frequency of the two elements and concatenating them to form a new element
        while len(freqList) != 0:
            # summing the frequency of the two elements and concatenating them to form a new element
            itemNew = [(item1[0] + item2[0]), (item1[1] + item2[1]), (item1[2] + (item2[2]))] # chance to make more efficient
            # pushing the new element to the list and serving 1 element using heapq.heappushpop which is more efficient
            item1 = heapq.heappushpop(freqList, itemNew)
            # serve 1 more item
            item2 = item2 = heapq.heappop(freqList)
            # again first serve receives 0, 
            for i in range(len(item1[2])):
                huffCode[item1[2][i]].append(0)
            # second serve receives 1 as code (append to the end)
            for i in range(len(item2[2])):
                huffCode[item2[2][i]].append(1)

        for number in range(len(charList)):  
            huffCode[charList[number]] = huffCode[charList[number]][::-1]
    return huffCode


def encodeElias(n):
    """
    encode number n using elias encoding
    @param n :integer
    @returns encodedNum :bitarray
    @complexity :O(n log n)
    """
    # convert to binary (if needed)
    returnList = []
    encodedNum = bitarray(format(n, 'b'))
    returnList.append(encodedNum)
    currentLength = len(encodedNum)
    currentNumber = encodedNum
    # to prevent recopying of list (can remove if proven to be slower)
    # loop until lenght component is 1
    while currentLength != 1:
        # produce the lenght of the last lenght string in bits
        currentLength = len(currentNumber) - 1
        currentNumber = bitarray(format(currentLength, 'b'))
        # change the first item to zero
        currentNumber[0] = 0
        returnList.append(currentNumber)
    # reversing the list in O(n)
    returnList.reverse()
    # copying all the list in O(n)
    outputBitArray = returnList[0]
    for x in range(1, len(returnList)):
        outputBitArray.extend(returnList[x])
    return outputBitArray


def zAlgo(string, currentIndex, window, lookAhead):
    """
    Algorithm to return the longest matching prefix of lookahead in window 
    @param string :bytearray
    @param currentIndex :integer
    @param window :integer
    @param lookahead :integer
    @returns maxFreq :integer
        the length of the longest substring
    @returns position :integer
        the position of the longest matching substring
    @complexity O(n)
    """
    # ensure that window does not overshoot the start
    if currentIndex - window < 0:
        window -= (window - currentIndex)

    # ensure that lookAhead does not overshoot the string
    if currentIndex + lookAhead >= len(string):
        lookAhead -= (currentIndex + lookAhead - len(string))

    # your z string is lookAhead|(somerandombit)|window|lookAhead
    searchString = [None] * (lookAhead + window + lookAhead + 1)
    distanceToSecondLookAhead = lookAhead + window + 1
    for i in range(lookAhead):
        searchString[i] = string[currentIndex + i]
        searchString[distanceToSecondLookAhead + i] = string[currentIndex + i]
        # print(string[currentIndex + i])
    for i in range(window):
        searchString[lookAhead + i + 1] = string[currentIndex - window + i]
        # print(string[currentIndex - window + i])
    # adding string as delimiter
    searchString[lookAhead] = '€'

    # z algorithm variables
    zboxStart, zboxEnd, k = 0, 0, 0
    strSize = len(searchString)
    zArr = [None] * strSize

    # get z array
    for index in range(1, strSize):

        # case 1 where there is no z box
        if index > zboxEnd:
            # start naive method
            m = 0
            while m < strSize - index + 1:
                # at the last character
                if m == strSize - index:
                    zboxEnd = m + index - 1
                    zboxStart = index
                    zArr[index] = zboxEnd - zboxStart + 1
                    break 
                # no memoization, lazy method to find match
                elif searchString[m] != searchString[m + index]:
                    zboxEnd = m + index - 1
                    zboxStart = index
                    zArr[index] = zboxEnd - zboxStart + 1
                    break 
                m += 1

        else:
            # assigning k variables only when needed
            k = index - zboxStart
            remaining = (zboxEnd - index + 1)

            # case 2 where k is less than remaining
            if zArr[k] < remaining:
                zArr[index] = zArr[k]

            # case 3 where k is equal to remaining, compare all additional characters
            elif zArr[k] == remaining:
                zboxStart = index
                while zboxEnd < strSize and searchString[zboxEnd - zboxStart] == searchString[zboxEnd]: 
                    zboxEnd += 1
                zArr[index] = zboxEnd - zboxStart
                zboxEnd -= 1

            # case 4 when k is more than remaining 
            elif zArr[k] > remaining:
                zArr[index] = remaining

    # finding maximum value from z array
    maxFreq = 0
    position = None
    for i in range(lookAhead + 1, (window + lookAhead + 1)):
        if zArr[i] >= maxFreq:
            maxFreq = zArr[i]
            # generating position 
            position = (currentIndex - window + (i - (lookAhead + 1)))
    return maxFreq, position


def generateHeader(inputAscii):
    """
    code to generate the header portion of the code containing the huffman code
    @param inputAscii :bytearray
        input text to encode
    @returns charList :bytearray
        list of unique characters
    @returns huffCode :list of list of integers
        huffman code for the file
    @returns header :list of strings
        header of the file
    @complexity :worst case in O(n)
    """

    outputList = bitarray('')
    # get all unique characters from the text
    charList, frequencyList = findingFrequencies(inputAscii)
    numberOfCharacters = len(charList)
    # making the huffman code
    huffCode = createHuffCode(charList, frequencyList)
    # Encode the number of unique ASCII characters in the input text using elias code
    outputList.extend(encodeElias(numberOfCharacters))
    # iterate for each unique character in the text:
    for charIndex in range(numberOfCharacters):
        asciiNum = charList[charIndex]
        # Encode the unique character using the fixed-length 7-bit ASCII code
        # (All input characters will have ASCII values < 128.)
        binary = bin(asciiNum)
        binaryLength = len(binary)
        if binaryLength < 9:
            for i in range(9 - binaryLength):
                outputList.append(0)   
        for i in range(len(binary) - 2):
            outputList.append(int(binary[i + 2]))
        # encode the length of the Huffman code assigned to that unique
        # character using variable-length Elias ω code.
        outputList.extend(encodeElias(len(huffCode[asciiNum])))
        # appending the variable-length Huffman codeword assigned
        # to that unique character.
        outputList.extend(huffCode[asciiNum])
 
    return outputList, huffCode, charList


def encodeData(inputString, huffCode, window, lookAhead):
    """ 
    encode the data portion of file using lzss, huffman, and elias encoding

    @param inputString :bytearray
    @param huffCode :list of bitarray
    @param window :integer
    @param lookAhead :integer
    @returns finalList :bitarray
    @complexity :O(n log n)
    """
    outputList = bitarray()
    lenInputString = len(inputString)
    # while there are still chars to encode in lookahead buffer
    # current index keep track of position on the data that we are encoding
    currentIndex = 0
    # numfields tracks the number of the number of 0 and 1 fields
    numFields = 0
    while currentIndex < lenInputString:
        # use z algorithm here
            # find the largest matched substring from the lookahead buffer that matches a string in the dictionary
            # always pick the smallest offset
        matchLength, position = zAlgo(inputString, currentIndex, window, lookAhead)
        
        # not worth it to use elias code if length is less than 3, so only encoding only huffman code
        if matchLength < 3:
            outputList.append(1)
            numFields += 1
            # use huffman code to write the character
            outputList.extend(huffCode[inputString[currentIndex]])
            currentIndex += 1

        # length of match is more than or equal to 3, so encoding offset length 
        else:
            outputList.append(0)
            numFields += 1
            offset = currentIndex - position
            outputList.extend(encodeElias(offset))
            outputList.extend(encodeElias(matchLength))
            currentIndex += matchLength
    # adding the number of fields in the output 
    finalList = encodeElias(numFields)
    # adding the data to the output list
    finalList.extend(outputList)

    return finalList 


if __name__ == "__main__":
    txtFile, window, lookAhead = processArgs()
    # Generate header
    header, huffCode, charList = generateHeader(txtFile)
    # Generate data section
    data = encodeData(txtFile, huffCode, window, lookAhead)
    # Write to file
    writeBinary(header, data, "output_encoder_lzss.bin")
