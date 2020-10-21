#! python3
# Writes metadata to CSV, based on filename, user inputs and file properties
# This version: - changed for UCS compliant naming
# See individual functions for required change notes
import os, re, csv, sys, wave, glob

def timeFormat(time):
    # seconds (ints) to hh:mm:ss formatter
    # this takes an int and formats it to the time format of hh:mm:ss
    # first calculate minutes and seconds
    time = int(time)  # round off any floats to ints
    hours = time // 3600
    time = time % 3600    # subtract whole hours from time
    minutes = time // 60  # returns whole minutes as remainder of time
    seconds = time % 60   # returns whole seconds as remainder of minutes

    hrStr = ''
    minStr = ''
    secStr = ''

    # format as hh:mm:ss string
    if hours < 10:
        hrStr = f'{hours:02d}'
    else:
        hrStr = str(hours)
        
    if minutes < 10:
        minStr = f'{minutes:02d}' # using f-strings to add one leading zero
    else:
        minStr = str(minutes)
        
    if seconds < 10:
        secStr = f'{seconds:02d}'
    else:
        secStr = str(seconds)
        
    duration = hrStr + ':' + minStr + ':' + secStr
    return duration

# Sanitize keywords, removing numbers, special chars, sentences
# and whitespace, making sure all words are capitalized
# see kwdSanitize.py for details

def kwdSanitize(kws):     
    kws = kws.replace(' ', ',') 
    kws = re.sub('[\d+!#¤%&]', '', kws) 
    kws = re.sub(',{2,}', ',', kws) 
    
    kws = kws.split(',')
    for i in range(len(kws)):
        kws[i] = kws[i].capitalize()
    kws = ','.join(kws)
    keywords = kws.strip(',-')
    return keywords
    

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

# initializing various variables
num = 0                         # set in for loop
bitDepth = ''                   # get from file metadata
sampleRate = ''                 # get from file metadata
channels = ''                   # get from file metadata
duration = 0                    # get from file metadata
looping = ''                    # set with regex

# regex object to check if file is a loop
loopRegex = re.compile(r'\,Loop$') 

# get name of parent folder and create namestring for the csv to be generated
folderName = os.path.basename(path)
outFileName = folderName + '-Metadata.csv' 

# enter data for column headers - change these strings to your own liking
print('Enter base description:')
desc = input()
desc = ' Add prefix in script if relevant ' + desc 

print('Enter recording location:')
location = input()             # set in CLI

print('Date of recording: Enter in preferred format:')
dateTime = input()              

recordist = 'Set recordist name in script'  # default
rights = 'Set your org name in script'      # default

print('Enter mics used')    # can get this from filename in future
mics = input()               # set in CLI

print('Recording device: Enter device name:')
recorder = input()       

print('Getting other file data...')


# create a csv file to hold the filenames and open it at path
outputFile = open(os.path.normpath(path) + '\\' + outFileName, 'w', newline='')
outputWriter = csv.writer(outputFile)
outputWriter.writerow(['Num', 'FileName', 'Description', 'Keywords', 'Bit Depth', 'Sample Rate', 'Channels', 'Duration', 'Looping Y/N', 'Location', 'Date/Time', 'Creator/Recordist', 'Copyright', 'Microphone', 'Recorder' ])

# Loop over the files at path. 
# any vars that get their values from the individual files must be assigned inside the loop
# get only specific file type, should be wav. Regex is avoided by using: os.path.join(path, '*.wav')
for file in glob.glob(os.path.join(path, '*.wav')):     # On the files that match     
    filename = os.path.basename(file)
    num = num + 1                               # ...give the file a number
    keywords = os.path.splitext(filename)[0]    # ...strip away file extension to get tags
    
    # Remove UCS name prefix and suffix: 
    # split by underscore
    name_elements = keywords.split('_')
    # then convert [1] back to string & save to keywords
    keywords = str(name_elements[1])
    
    # Sanitize keywords
    keywords = kwdSanitize(keywords)
    
    if loopRegex.search(keywords):              # mark if file is looping (checks if the word "loop" is in the file name)
        looping = 'Y'        
    else:
        looping = 'N'    
        
    
    # Get file properties using wave module...
    waveFile = wave.open(file, 'r')
    bitDepth = 8 * waveFile.getsampwidth()
    sampleRate = waveFile.getframerate()
    channels = waveFile.getnchannels()
    frames = waveFile.getnframes()
    frameRate = waveFile.getframerate()
    duration = frames / frameRate
    duration = timeFormat(duration)     
    waveFile.close()
    
    # This is where the CSV rows are written, using the variables above. Change/add/remove these to change your rows.
    outputWriter.writerow([num, str(filename), str(desc), str(keywords), str(bitDepth), sampleRate, channels, duration, looping, location, dateTime, recordist, rights, mics, recorder])
outputFile.close()

print(' ')
print('Done. Type "o" + ENTER to open CSV or type any key to exit.')
endCommand = input()
if endCommand == 'o':
    os.startfile(os.path.normpath(path) + '\\' + outFileName) # using normpath to avoid escaping backslashes in the path name
else:
    exit()    

    
