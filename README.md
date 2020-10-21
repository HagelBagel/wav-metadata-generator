# Wav Metadata Generator

## The problem:
Audio professionals working in digital media often use special database-apps to search for the right sounds. Wav-files can have metadata embedded, which then allows for searching for sounds by text fields, rather than having to listen through thousands of files for the right sound.

The process of embedding metadata requires attention to detail, and can be extremely tedious, if doing it file by file. Good metadata apps are often very expensive and batch-editing capabilities are often a bit too manual and confusing. Some free options, such as [BWF-Metaedit](http://bwfmetaedit.sourceforge.net/), leave much to be desired in terms of usability (in my opinion).

I built these two scripts for my personal needs, which are as follows:
1. Partially automate the process of embedding metadata into wav-files using BWF-Metaedit. This makes sense, because I often work on files which have data in common (same recording session, same subject, etc).
2. Generate a human-readable CSV to bundle with those audio files, for users to ingest into whatever audio database apps they use. This allows users to relate more metadata to wav-files than can normally be embedded.

## How to use: 
There are two Python scripts, `filesToCSV3.py` and `metaDataToBWF.py` (Python 3.8).
These are command-line tools, which means you have to run them from a command prompt of some kind. You can also open them in something like VSCode and run them from there.

1. Run `filesToCSV3.py` to generate a CSV-file containing basic metadata
2. If needed, manually edit any field which are unique to each file (description and tags come to mind, but there could be others). You now have a data-rich file to import into a database-app.
3. Run `metaDataToBWF.py` to generate a new CSV, which is strictly for use with BWF-Metaedit. 
4. Open your files in BWF-Metaedit, import the CSV and save changes.

## Notes:

I suggest you read through the code before using.

Rememeber that these scripts are set up for my personal preferences, so if you need your CSV to look different; have different fields, etc, you'll have to modify those sections in the code. The code is full of comments for my own use, but hopefully will help you understand what is going on. 

Do a test run and see what comes out. Then modify to your liking.

Note that this version is designed to take files named according to the [Universal Category System](https://www.universalcategorysystem.com) (UCS) and use the file names as basis for any metadata generated. If you do not have UCS-compliant files, you may need to modify `filesToCSV3.py`.

## Dependecies:
Nothing but standard core Python 3.8 modules...