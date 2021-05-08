'''
This is a tool to extract member code check results produced by framework into 
excel format. The framework results should be printed on LANDSCAPE format

fwmemcodex.py <control_file.inp>

		control_file.inp
		[0] 1st line -- <XXX.lis>   <XXX.xlsx>
		[1] 2nd line -- <XXX.lis>   <XXX.xlsx>
		[2] 3rd line -- <XXX.lis>   <XXX.xlsx>
		[..] ..th line -- <XXX.lis>   <XXX.xlsx>
        Extension should be included!!

'''


import os
import sys
import sesamutil



def checkargv() :
	''' Checking argument '''
	res = 0
	if len(sys.argv) == 1:
		print('Please input the control file name with its extension')
	elif len(sys.argv) > 2:
		print('Only accept 1 argument')
	elif len(sys.argv) == 2:
		if os.path.exists(sys.argv[1]): #Check if the path is valid
			res = 1
		else :
			print('File does not exists')

	return res

def to_list(nameoffile, stripstatus):
	''' Function to read lines into a list '''
	with open(nameoffile, 'r') as f:
        #llist = [line.strip() for line in f] 
		if stripstatus == True :
			llist = [line.strip() for line in f]
		else :
			llist = [line for line in f]
	return llist


''' Execute Program '''

resargv = checkargv()

if resargv ==1:
	# echoing the name of the control file
	print('reading control file : ' , sys.argv[1] )
else:
	# spit this when control file not found and stop the program
	sys.exit('ERROR -- Oops! Control file not found')

# Reading the control file 
ctrlpar = [ line.split() for line in to_list(sys.argv[1], True) ]

# Check validity of the control file
if len(ctrlpar) == 0 :
    sys.exit('ERROR -- Please put your source and output file names')

for item in ctrlpar :
    if len(item) == 2 :
        print( 'source : ' + item[0] + '--->' + item[1])
    else :
        sys.exit('ERROR -- Please check again your control file')

# Runnning the extraction
count = 0
for item in ctrlpar :
    memcodechecklist = sesamutil.getmemcheck360(item[0])
    sesamutil.list_to_excel(memcodechecklist, item[1])
    count += 1

print(f"A total of {count} file(s) have been extracted!!")

