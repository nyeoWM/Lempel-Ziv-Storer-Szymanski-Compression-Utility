"""
Algorithm to decode lzss encoded file into ascii characters. Algorithm makes use of the bit
arry and bytearray modules
General approach:
Takes the binary as a list, and iterates through it, passing each of the functions the binary 
representation and a currentIndex. Each function will return the value required and the index
for the next undecoded bit
@complexity :O(n log n) where n is the number of bits because for the worst case we would have 
to run elias and huffman for every bit. Complexity of elias and huffman are n log n being in 
the worst case.
"""
import sys
from bitarray import bitarray

def processArgs():
    """
    Reads the input from the terminal and returns the filename, window, and lookahead
    @returns bitList :bitarray
    @complexity :O(n)
    """
    fileName = sys.argv[1]
    bitList = bitarray()
    with open(fileName,'rb') as f:
        bitList.fromfile(f)
    return bitList


def writeFile(outputList):
    """
    Reads the input from the terminal and returns the filename, window, and lookahead
    @param outputList :bytearray
    @complexity :O(n)
    """
    with open("output_decoder_lzss.txt", "wb") as file:
        file.write(outputList)


class huffNode():
    # class store huffman code for decoding
    def __init__(self, char=None):
        self.char = char
        self.child = [None, None]


class HuffSearchTree():
    """
    class that implements huffman search trees
    """
    def __init__(self):
        self.root = huffNode()


    def addHuffCode(self, huffCode, includedCharacters):
        """
        making a tree by adding character code and character
        @param huffCode :list of bitarrays
        @param includedCharacters :list of bytes
        @complexity :O(log n)
        """
        for char in includedCharacters:
            self.addChar(huffCode[char], char)

    # adding individual huffman codes to t
    def addChar(self, charHuffCode, char):
        # inserting charHuffCode for char
        current = self.root
        for i in range(len(charHuffCode)):
            # checking if children exist, else make new node
            if charHuffCode[i] == 1:
                if current.child[1] == None:
                    current.child[1] = huffNode()
                    current = current.child[1]
                else:
                    current = current.child[1]
            if charHuffCode[i] == 0:
                if current.child[0] == None:
                    current.child[0] = huffNode()
                    current = current.child[0]
                else:
                    current = current.child[0]
        # add new char if at leaf
        current.char = char

    
    def decode(self, searchString, currentIndex):
        """
        decoding a single character based on index in  
        @param searchString :bytearray
        @param currentIndex :integer
        @returns current.child :byte
        @returns currentIndex :integer
            index in the bytearray
        @complexity :overall O(n log n)
        """
        current = self.root
        # using index to iterate through the string
        while True:
            if current.char is not None:
                # reached child, outputting character
                return current.char, currentIndex
                # starting from node again
            else:
                # not at child
                huffPosition = int(searchString[currentIndex])
                current = current.child[huffPosition]
                currentIndex += 1


def decodeElias4(bitStr, currentIndex):
    """
    @param string :bitarray
    @param integer :currentIndex
        the current index the is being decodeded
    @returns decodedNumber :integer
    @returns currentIndex :integer
    @complexity :O(n log n)

    """
    # Initialize: readlen = (1)dec, component = <EMPTY>, pos = 1
    readlen = 1
    component = None
    currentIndex += 1
    while True:
        #  component = bitStr[pos . . . pos - 1 + readlen − 1].
        next = currentIndex + readlen - 1
        component = bitarray()
        for i in range(currentIndex - 1, next):
            component.append(bitStr[i])
        # If the most-significant bit of component is 1, then N = (component)dec. STOP.
        if component[0] == 1:
            decodedNumber = 0
            numDigits = len(component)
            calcDigits = numDigits - 1
            # value of current component 
            for i in range(numDigits):
                if component[i] == 1:
                    decodedNumber += 2**(calcDigits - i)
            currentIndex = next
            return decodedNumber, currentIndex

        # Else, if the most-significant bit of component is 0, 
        else:
            # then flip 0 → 1  
            component[0] = 1
            # and reset pos = pos + readlen,
            currentIndex = currentIndex + readlen
            # readlen = (component)dec + 1.
            decodedNumber = 0
            numDigits = len(component)
            calcDigits = numDigits - 1
            # length of next component 
            for i in range(numDigits):
                if component[i] == 1:
                    decodedNumber += 2**(calcDigits - i)
            readlen = decodedNumber + 1 


def getDecimal(binaryNum):
    """
    @param binaryNum :bitarray
        decimal number
    @returns deci :integer
    @complexity :O(n log n)
    """
    deci = 0
    numDigits = len(binaryNum)
    calcDigits = numDigits - 1
    for i in range(numDigits):
        if binaryNum[i] == 1:
            deci += pow(2, calcDigits - i)
    return deci


def decodeData(inputBin, huffCode, charList, currentIndex):
    """
    Seperate function to decode the data portion of the text
    @param inputBin :bitarray
    @param huffCode :list of bitarray
    @param charList :list
    @param currentIndex :integer
    @returns outputlist :bytearray
    @complexity :O(n log n)
    """
    outputList = bytearray()
    formatNumber = 0
    writeIndex = 0
    newHuffTree = HuffSearchTree()
    newHuffTree.addHuffCode(huffCode, charList)
    totalFormat, currentIndex = decodeElias4(inputBin, currentIndex)
    # only decode totalFormat number of characters
    while formatNumber < totalFormat:

        # if its 1 just write the current char
        if inputBin[currentIndex] == 1:
            formatNumber += 1
            currentIndex += 1
            # char obtained from huffman tree
            cucurrentChar, currentIndex =  newHuffTree.decode(inputBin, currentIndex)
            outputList.append(cucurrentChar)
            writeIndex += 1

        # if i is 0
        elif inputBin[currentIndex] == 0:
            formatNumber += 1
            currentIndex += 1
            # getting the offset
            offSet, currentIndex = decodeElias4(inputBin, currentIndex)
            # start from current position - offset
            copyIndex = writeIndex - offSet
            # getting the length of the string
            stringLength, currentIndex = decodeElias4(inputBin, currentIndex)
            endCopy = copyIndex + stringLength
            # copying characters for earlier in the output list
            while copyIndex < endCopy:
                outputList.append(outputList[copyIndex])
                copyIndex += 1
                writeIndex += 1
    return outputList


def decodeLzss(bitStr):
    """
    function to decode the header and pass the information to decode data
    @param bitStr :bitarray
    @returns outputlist :bytearray
    @complexity :including inner function calls O(n log n)
    """

    # decoding the header
    huffCode = [bitarray() for i in range(128)]
    currentIndex = 0
    numStrings, currentIndex = decodeElias4(bitStr, currentIndex)
    charList = bytearray()

    #decoding individual ascii characters and their representations
    for i in range(numStrings):
        # obtaining 7 bit ascii character
        asciiChar = []
        charHuff = bitarray()
        for x in range(7): 
            asciiChar.append(bitStr[currentIndex])
            currentIndex += 1
        char = getDecimal(asciiChar)
        charList.append(char)

        # obtaining the length of the huffman code
        length, currentIndex = decodeElias4(bitStr, currentIndex)

        # saving huffman code into charHuff
        for i in range(length):
            charHuff.append(bitStr[currentIndex])
            currentIndex += 1
        # saving huffman code
        huffCode[char] = charHuff
    #decoding data using seperate function
    outputList = decodeData(bitStr, huffCode, charList, currentIndex)
    return outputList



if __name__ == "__main__":
    # getting file
    inputFile = processArgs()
    # decoding file
    outputList = decodeLzss(inputFile)
    # writing output to file
    writeFile(outputList)  


