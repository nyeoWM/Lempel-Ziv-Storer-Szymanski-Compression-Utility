import os
import sys
from os import listdir
from os.path import isfile, join
import time
import filecmp

dir_path = os.path.dirname(os.path.realpath(__file__))
onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
L = []
for x in onlyfiles:
    if x[-2:] != "py" and  x[-3:] != "bin" and x[-5:] != "Store":
        print("Encoding file " + x)
        start = time.time()
        os.system("python3 " + "encoder_lzss.py " + x + " 3" + " 2")
        end = time.time()
        print("Encoding Time :" + str(end - start))

        print("Decoding output for " + x)
        start = time.time()
        os.system("python3 " + "decoder_lzss.py output_encoder_lzss.bin")
        end = time.time()
        print("Decoding Time :" + str(end - start))

        # try:
        if filecmp.cmp(x,'output_decoder_lzss.txt') == False:
            print("!!!!!!!!!!!!!Warning Error When processing file " + x)
            os.rename("output_encoder_lzss.bin", "f_en_" + x + ".bin")
            os.rename("output_decoder_lzss.txt", "f_de_" + x)
            L.append(x)
        else:
            print("Test passed, files similiar")
        print("\n")
        # except FileNotFoundError:
            # print("Cant encode file")

for x in onlyfiles:
    if x[-3:] == "bin":
        start = time.time()
        os.system("python3 " + dir_path + "/decoder_lzss.py " + dir_path + "/" + x)
        print("Decoding file " + x)
        end = time.time()
        print("Decoding Time :" + str(end - start))
        print("\n")

print("Files that Failed Similarities Check")
for i in L:
    print(i)



