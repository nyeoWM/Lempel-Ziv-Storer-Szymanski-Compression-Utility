# Lempel-Ziv-Storer-Szymanski-Compression-Utility
Compression utility implementing the Lempel-Ziv-Storer-Szymanski algorithm, which relies on Huffman coding and elias-omega coding to compress and decompress files efficiently

## Running the program

### Compressing files
Run
```
encoder lzss.py <input text file> <W> <L>
```
Where \<W\> is the search window size and \<L\> is the lookahead buffer size.
  
### Decompressing files
Run
```
decoder lzss.py <compressed file name>
```
