# BasicOptimization
This program performs a brute-force search for parameters "a" and "c" of the structure. To run the program, you need:
- Code for the structure simulator (https://github.com/pedrogil1919/Structure)
- OpenCV (python-opencv)
- matplotlib.

In main.py, you have to specify the path where the structure code was downloaded (see line 16 or 17 in main.py).

To run the program, type:

$ python3 main.py

The program configuration is in file settings.xml. Read the instruction of each parameter to understand its meaning. If you prefer to use other configuration xml, add the new file to the first argument:

$ python3 main.py /path/to/file/settings.xml

The program generate colormap graphs in the directory specified in xml file, one for each dimension L_H.
