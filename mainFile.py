"""
movieConverter: Converter for all mkv files to mp4 all at once
Hussein Esmail
Created: 2020 01 21 
Updated: 2020 02 15
Description: Batch converter from mkv to mp4 that checks multiple folders, and all go to the same place
"""

import os                       # To run commands, change directories, delete files, etc.
import time                     # For time delays
from termcolor import colored   # To print colored text in terminal (when run in terminal)
import shutil
import datetime
import re

# VARIABLES
arrayTempConvertedFiles = []
arrayTargetFolders = ["/Users/hussein/Downloads",
                      "/Users/hussein/Downloads/Mipony",
                      "/Users/hussein/MEGA",
                      "/Users/hussein/Movies/Movies/To_Convert"]
# TODO: Integrate srt files if they have the same title as an mkv file in the same directory before conversion
arrayRemoveTheseFilesFromListsIfTheyExist = [".DS_Store",
                                             ".debris",
                                             ".localized"]
boolShowTerminalPrints = False
boolDeleteSourceFileAfterConvert = True
boolShowNonMkvFileNames = False
boolTryToMoveMoviesToHardDriveIfConnected = True
boolDevPrintListDirArrays = False
boolRemoveSpacesInFiles = True
boolRemoveOtherFileKeywords = True
boolTestRename = False

colorIntroPrints = "green"
colorCompleted = "green"
colorMkvExists = "green"
colorFileNotMkv = "red"
colorWarning = "yellow"
colorLoading = "yellow"
colorDenied = "red"
colorUnexpectedError = "red"
colorFilesDeletedNotification = "red"
colorFileNoLongerNeeded = "yellow"
colorFileConverted = "cyan"
colorFileListNotifications = "cyan"
colorFolderDNE = "red"
colorFileRenamed = "cyan"

intTimeDelayBetweenFolderIterations = 2
intTimeDelayBetweenFileIterations = 0.01
intTimeDelayAfterIntro = 2
intTimeDelayIfHardDriveConnected = 1
intDelayMegaLoadInSteps = 0.5
intDelayMegaWaitForConfirmEmpty = 1
intDelayMegaWhileEmptyingTrash = 10
intTimeDelayLoadInSteps = 2

strPathOfMP4s = "/Users/hussein/Movies/Movies/Not_Backed_Up"
strPathOfMP4s2 = strPathOfMP4s.replace(" ", "\\ ")  # For the terminal commands
strPathOfMovieDrive = "/Volumes/Hussein4TB/1 Movies"
strPathOfBackedUpMovies = "/Users/hussein/Movies/Movies/Backed_Up"
strProjectPath = "/Users/hussein/PycharmProjects/movieConverter"
strSmartConverterPath = "/Users/hussein/Movies/SmartConverter"

strPathOfTrash = "/Users/hussein/.Trash/"
strSpaceReplacerInFiles = "."
strUnexpectedError = "UNEXPECTED ERROR - TAKE NOTE: "
strIntro = "Batch Convert MKVs to MP4\nby Hussein Esmail"
strMegaTrashNotEmptied = "Clear Trash button on MEGA not pressed. The text of the empty button has changed."
strHardDriveNotConnectedMovingTo = "Hard drive not connected, files not backed up"
strFileDeleted = "\t\tDELETED "
strFolderIsEmpty = "\tNo files in this folder"
strFoundFileToConvertPrefix = "\tFOUND>>> "
strConvertingMovie = "\t\tConverting..."
strConvertingAlternate = "\t\tConversion failed. Running alternate..."
strFileConverted = "\t\tConversion complete."
strMovingFilesToHardDrive = "Moving files to hard drive..."
strStringsToRemoveInFileNames = ["1080p", "10bit",  "7.1",  "720p",  "AAC5.1", "AAC",  "AAC-RARBG",  "AMIABLE",
                                 "Atmos", "BRRip",  "Blu-ray",  "BluRay",  "CHD", "-CMRG", "CMRG",  "DC",  "DD2.0",
                                 "DD3.1", "DD5.1",  "DDP7", "DON", "DSMP.1", "DSMP", "DDPS.1", "DDPS", "DTS",  "EVO",
                                 "FLAC", "GalaxyRG",  "H264", "H265",  "HDRip",  "HEVC",  "HiDEF", "MULTi",  "MaG",
                                 "NTb", "Prof",  "SCORPIO", "TrueHD", "WEB-DL",  "WEBDL",  "WEBRip",  "ZQ", "x264",
                                 "x265", "-HETeam", "WEB.DL", "AMZN", "NF", "NTG", "Vyndros", "[", "]", ".Joy", "FS89",
                                 "q22", "FS91", "FS97", "HD", ".EVO", "AC3.2.0"]
itemsToRemove2 = [".", "-"]
strWordSeparator = "."
strTypeSource = ".mkv"  # File type the program is looking for
strTypeTarget = ".mp4"  # File type to convert to
strFileListTxtTitle = "Files on Movie Drive"
strFileListSavePath = "/Users/hussein/Movies/Movies"  # Where the hard drive directory text file saves on computer
strRemoveSpecialCharacters = '[?|$|!|\'|(|)]'


def removeFileIfExists(strAllFilesInMkvDir, fileNameArray):  # Used in the main function
    for i in range(0, len(fileNameArray)):
        try:  # Remove the file i if it exists
            strAllFilesInMkvDir.remove(fileNameArray[i])
        except ValueError:
            pass  # If it isn't there, do nothing


def convertToMP4():
    print(colored(strIntro, colorIntroPrints))
    time.sleep(intTimeDelayAfterIntro)
    for eachTargetFolder in arrayTargetFolders:  # For every given target folder
        if os.path.exists(eachTargetFolder):  # If the given folder exists
            strPathOfMKVs = eachTargetFolder
            if not os.path.exists(strPathOfMP4s):  # If the Not Backed Up folder doesn't exist,
                os.makedirs(strPathOfMP4s)  # Make the folder
            os.chdir(strPathOfMKVs)  # Change directory to that folder (whether if it was preexisting or just created)
            strAllFilesInMkvDir = os.listdir(strPathOfMKVs)  # Get all files in the source folder
            print("Looking in " + strPathOfMKVs)
            if boolDevPrintListDirArrays:
                print(str(strAllFilesInMkvDir))
            removeFileIfExists(strAllFilesInMkvDir, arrayRemoveTheseFilesFromListsIfTheyExist)
            if len(strAllFilesInMkvDir) == 0:  # If the folder is empty
                print(colored(strFolderIsEmpty, colorFileNotMkv))
            elif len(strAllFilesInMkvDir) == 1:  # If there is 1 file in the folder
                print(colored(str(len(strAllFilesInMkvDir)), colorCompleted) + " item in folder")
            else:  # If there are files in the folder
                print(colored(str(len(strAllFilesInMkvDir)), colorCompleted) + " items in folder")
            for i in range(0, len(strAllFilesInMkvDir)):  # For every element in the directory
                if strAllFilesInMkvDir[i][-(len(strTypeSource)):] == strTypeSource:  # If the last characters are ".mkv"
                    print(colored(strFoundFileToConvertPrefix, colorMkvExists) + strAllFilesInMkvDir[i])
                    if boolRemoveOtherFileKeywords:
                        fileNameOriginal = strAllFilesInMkvDir[i]
                        fileName = fileNameOriginal
                        for itemToRemove in strStringsToRemoveInFileNames:
                            fileName = fileName.replace(itemToRemove, "")  # Replaces the items if they exist
                        fileName = re.sub(strRemoveSpecialCharacters, '', fileName)
                        while "."*2 in fileName:
                            fileName = fileName.replace("."*2, ".")
                        fileName = fileName[:-len(strTypeSource)]
                        for j in itemsToRemove2:  # This loop deals with the . between the removed items
                            fileName = fileName.replace(j, " ")  # Causes spaces between words and a bunch at the end
                        fileName = fileName.rstrip()  # Removes the bunch of spaces at the end
                        fileName.replace(" ", strWordSeparator)  # Replaces spaces between words with . again
                        # Right now the program MIGHT only work when strWordSeparator is ".". Emphasis on MIGHT
                        fileName = fileName + strTypeSource  # Add the file extension back in
                        os.rename(eachTargetFolder + "/" + fileNameOriginal, eachTargetFolder + "/" + fileName)
                        filePath = eachTargetFolder + "/"
                        os.rename(filePath + fileName, filePath + fileName.replace(" ", strSpaceReplacerInFiles))
                        strAllFilesInMkvDir[i] = fileName.replace(" ", strSpaceReplacerInFiles)
                        print(colored("\t\tRenamed to: ", colorFileRenamed) + strAllFilesInMkvDir[i])
                    print(colored(strConvertingMovie, colorMkvExists))
                    strAllFilesInMkvDir[i] = strAllFilesInMkvDir[i][:-len(strTypeSource)]  # Remove the ".mkv"
                    if boolShowTerminalPrints:  # Show the prints
                        strShowTerminalPrints = ""
                    else:
                        strShowTerminalPrints = " -hide_banner -loglevel panic"
                    # Below: Basically turn off library's prints, source path copy to new path as different file type
                    convertCommand = "ffmpeg" + strShowTerminalPrints + " -i " + strPathOfMKVs + "/" \
                                     + strAllFilesInMkvDir[i] + strTypeSource \
                                     + " -c:v copy -c:a copy -tag:v hvc1 " \
                                     + strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget
                    # -loglevel quiet   --> Turns off print statements from ffmpeg itself
                    # -c copy           --> Leave the original copy alone
                    try:
                        os.system(convertCommand)  # This line will run the program in terminal
                    except Exception as e:
                        print("170: " + str(e))
                    # Check file size of the file that was just created
                    try:
                        file_stats = os.stat(strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget)
                        if file_stats.st_size == 0:
                            # print(colored("\t\tConversion failed. Running alternate...", colorWarning))
                            fileToDelete = strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget
                            if os.path.exists(fileToDelete):
                                os.remove(fileToDelete)
                            # Run the command without the tag
                            convertCommand = "ffmpeg" + strShowTerminalPrints + " -i " + strPathOfMKVs \
                                             + "/" + strAllFilesInMkvDir[i] + strTypeSource \
                                             + " -c:v copy -c:a copy " \
                                             + strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget
                            # -loglevel quiet   --> Turns off print statements from ffmpeg itself
                            # -c copy           --> Leave the original copy alone
                            os.system(convertCommand)  # This line will run the program in terminal
                            file_stats = os.stat(strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget)
                    except Exception as e:
                        print(colored(strConvertingAlternate, colorWarning))
                        fileToDelete = strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget
                        if os.path.exists(fileToDelete):
                            os.remove(fileToDelete)
                        # Run the command without the tag
                        convertCommand = "ffmpeg" + strShowTerminalPrints + " -i " + strPathOfMKVs \
                                         + "/" + strAllFilesInMkvDir[i] + strTypeSource \
                                         + " -c:v copy -c:a copy " \
                                         + strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget
                        # -loglevel quiet   --> Turns off print statements from ffmpeg itself
                        # -c copy           --> Leave the original copy alone
                        os.system(convertCommand)  # This line will run the program in terminal
                        fileToCheck = strPathOfMP4s2 + "/" + strAllFilesInMkvDir[i] + strTypeTarget
                        if os.path.exists(fileToCheck):
                            file_stats = os.stat(fileToCheck)
                    arrayTempConvertedFiles.append(strAllFilesInMkvDir[i])
                    try:
                        print(colored(strFileConverted, colorFileConverted) + " "
                              + ("%.2f" % (file_stats.st_size/1000000000)) + " GB")
                    except:
                        pass
                    if boolDeleteSourceFileAfterConvert:
                        file = strAllFilesInMkvDir[i] + strTypeSource
                        os.replace(strPathOfMKVs + "/" + file, strPathOfTrash + file)
                        strDisplay = strAllFilesInMkvDir[i] + strTypeSource
                        if len(strDisplay) > 56:
                            strDisplay = strDisplay[:50] + "..."
                        print(colored(strFileDeleted, colorFilesDeletedNotification) + strDisplay)
                    else:
                        print(colored("\t\t" + strAllFilesInMkvDir[i] + strTypeSource +
                                      " no longer needed", colorFileNoLongerNeeded))
                elif boolShowNonMkvFileNames:  # If the current file is not an MKV (ex. .srt or .txt)
                    print(colored("\t" + strAllFilesInMkvDir[i], colorFileNotMkv))
                time.sleep(intTimeDelayBetweenFileIterations)
            time.sleep(intTimeDelayBetweenFolderIterations)
        else:  # If the given folder does not exist
            print(colored("Folder DNE: " + eachTargetFolder, colorFolderDNE))

    # FINAL code, after everything has been converted
    os.chdir(strPathOfMP4s)
    os.listdir(strPathOfMP4s)
    print(colored("Converted " + str(len(arrayTempConvertedFiles)) + " files", colorCompleted))
    if boolDeleteSourceFileAfterConvert:
        print(colored(str(len(arrayTempConvertedFiles)) + " original files deleted", colorFilesDeletedNotification))
    if os.path.exists(strSmartConverterPath):
        for file in os.listdir(strSmartConverterPath):
            try:
                shutil.move(strSmartConverterPath + "/" + file, strPathOfMP4s2 + "/" + file)
            except Exception as e:
                pass
        if not any(strTypeTarget in s for s in os.listdir(strSmartConverterPath)):
            # If there are no more items in the folder with ".mp4"
            shutil.rmtree(strSmartConverterPath)
    if boolTryToMoveMoviesToHardDriveIfConnected:
        try:
            os.chdir(strPathOfMP4s)
            arrayItemsNotBackedUp = os.listdir(strPathOfMP4s)
            time.sleep(intTimeDelayIfHardDriveConnected)
            os.chdir(strPathOfMovieDrive)
            print(colored(strMovingFilesToHardDrive, colorMkvExists))
            arrayItemsInHardDrive = os.listdir(strPathOfMovieDrive)
            arrayItemsBackedUp = []
            removeFileIfExists(arrayItemsNotBackedUp, arrayRemoveTheseFilesFromListsIfTheyExist)
            for i in range(len(arrayItemsNotBackedUp) - 1, -1, -1):
                if arrayItemsNotBackedUp[i] in arrayItemsInHardDrive:
                    print(colored("File exists already: " + arrayItemsNotBackedUp[i], colorDenied))
                else:
                    arrayItemsBackedUp.append(arrayItemsNotBackedUp[i])
                    print(colored("Moving file: " + arrayItemsNotBackedUp[i], colorLoading))
                    shutil.copyfile(strPathOfMP4s + "/" + arrayItemsNotBackedUp[i], strPathOfBackedUpMovies + "/"
                                    + arrayItemsNotBackedUp[i])
                    shutil.move(strPathOfMP4s + "/" + arrayItemsNotBackedUp[i], strPathOfMovieDrive
                                + "/" + arrayItemsNotBackedUp[i])
                    print(colored("Done.", colorLoading))
            arrayFilesInHardDrive = os.listdir(strPathOfMovieDrive)
            date = str(datetime.datetime.now())[0:18]
            dateInFileName = date[0:10].replace("-", " ")
            movieFileName = dateInFileName + " " + strFileListTxtTitle
            movieFileFullPath = strFileListSavePath + "/" + movieFileName
            fileCheckFirstRun = True
            fileCheckKeepRunning = True
            fileNameCheck = movieFileName
            add = 1  # Starting number to check
            while fileCheckKeepRunning:  # This loop prevents making duplicates
                if fileCheckFirstRun:  # First check without a number
                    fileCheckKeepRunning = os.path.exists(movieFileFullPath + ".txt")  # Actual line that checks
                    fileCheckFirstRun = False  # Make sure it only does it once
                else:  # If this is not the first time, check with the numbers
                    fileNameCheck = movieFileName + " " + str(add)  # Check this string
                    # Below: Actual line that checks if the file exists
                    fileCheckKeepRunning = os.path.exists(strFileListSavePath + "/" + fileNameCheck + ".txt")
                    if not fileCheckKeepRunning:  # If it is not going to run again
                        movieFileName = fileNameCheck  # Replace the file name with the one with the number
                        movieFileFullPath = strFileListSavePath + "/" + movieFileName
                    else:  # If it will be run again
                        add += 1  # The next search will check the next number
            print(colored("Making ls file to ", colorFileListNotifications) + strFileListSavePath + ".txt")
            arrayFilesInHardDrive = sorted(arrayFilesInHardDrive)
            # Remove this file if it exists so it doesn't list it
            removeFileIfExists(arrayFilesInHardDrive, arrayRemoveTheseFilesFromListsIfTheyExist)
            with open(movieFileFullPath + ".txt", "w") as f:
                f.write(strFileListTxtTitle)
                f.write("\n")
                f.write(dateInFileName)
                f.write("\n")
                for i in arrayFilesInHardDrive:
                    f.write("\n")
                    f.write(i)
            print(colored("File made: ", colorFileListNotifications) + fileNameCheck)
            for i in range(0, len(arrayItemsBackedUp)):
                print(colored("File moved to drive: " + arrayItemsBackedUp[i], colorCompleted))
        except FileNotFoundError:
            print(colored(strHardDriveNotConnectedMovingTo, colorWarning))
        except Exception as e:
            print(colored(strUnexpectedError + str(e), colorUnexpectedError))
            pass


if __name__ == "__main__":
    convertToMP4()
