import os, sys
from pathlib import Path
for filename in os.listdir('/Users/ismailbreiwish/project-zayd-data/project-zayd-data'):
	if filename.endswith(".json") :
		readFile = open(filename)

		lines = readFile.readlines()

		readFile.close()
		w = open(filename,'w')

		w.writelines([item for item in lines[1:-2]])


		w.close()

		w = open(filename, 'a')
		w.write(']')