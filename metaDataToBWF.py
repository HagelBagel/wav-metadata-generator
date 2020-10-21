#! python3
# This takes the finished metadata CSV, loads it and saves a modified version
# as a new CSV, to be imported into BWF metaedit.

# maybe not all of this is needed
import os, re, csv, sys

# Code to let the user input a folder path and check that it is valid and exists
pathRegex = re.compile(r'[A-Z]:\\[a-zA-Z0-9]+')
toggle = False  # Toggle to break out of while loop

while toggle == False:
    print('Enter folder path')   #  or press "c" + ENTER for CWD (maybe implement this)
    path = input()

    if pathRegex.match(path) and os.path.isdir(path):            
        print('Using ' + path)
        toggle = True
    else:
        print('Path is invalid or doesn\'t exist...')
        print('Use current working directory - y/n?')
        cwdVal = input()
        if cwdVal == 'y':
            path = os.getcwd()  # overwrite path with cwd
            print('Using CWD ' + path)
            toggle = True      
# end of path-checker code

# get name of parent folder and create namestring for the csv to be generated
folderName = os.path.basename(path)
outFileName = folderName + '-bwf.csv'

# create a csv file to hold the filenames and open it at path
outputFile = open(os.path.normpath(path) + '\\' + outFileName, 'w', newline='')
outputWriter = csv.writer(outputFile)
outputWriter.writerow(['FileName', 'Description', 'IKEY', 'BitsPerSample', 'SampleRate', 'Channels', 'Duration', 'IARL', 'ICRD', 'IART', 'ICOP'])

# open finished metadata CSV and save some of the columns, with modified headings, to bwf CSV
# this could be improved by comparing column names and including only matches, like bitDepth = bitsPerSample, IARL = location, etc
# maybe comparing two lists and removing the diff?
print('Input source CSV file (file name with extension):')
sourceCSV = input()

metadata = open(path + '\\' +  sourceCSV) # build the correct full path.
metaReader = csv.reader(metadata) #save it as an object
metaList = list(metaReader) # turn it into a list
metaList = metaList[1:] # leave out the first row of the list

for i in range(len(metaList)):   # all the rows except the first
    for j in range(11):             # just as many cols as we want to keep
        filename = path + '\\' +  metaList[i][1] #index 0 of each row is 1st col, plus file path also
        description = metaList[i][2]     #index 2 is 2nd col
        ikey = metaList[i][3]
        bitspersample = metaList[i][4]
        samplerate = metaList[i][5]
        channels = metaList[i][6]
        duration = metaList[i][7]
        iarl = metaList[i][9]
        icrd = metaList[i][10]
        iart = metaList[i][11]
        icop = metaList[i][12]
    # This is where the CSV rows are written, using the variables above. Change/add/remove these to change your rows.
    outputWriter.writerow([str(filename), str(description), str(ikey), str(bitspersample), str(samplerate), str(channels), str(duration), str(iarl), str(icrd), str(iart), str(icop)])
outputFile.close()

# closing everything down...
print('Current path is: ' + path)
print('Done. Type "o" + ENTER to open CSV or type any key to exit.')
endCommand = input()
if endCommand == 'o':
    os.startfile(os.path.normpath(path) + '\\' + outFileName) # using normpath to avoid escaping backslashes in the path name.
    
