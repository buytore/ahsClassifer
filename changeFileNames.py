# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:12:46 2016

@author: markbannan
"""
import os

path = os.getcwd()                                  #Get the current directory
#print path
directoryNames = next(os.walk(path))[1]                  #Get all the files in current directory
#print "The directory names please: ", directoryNames

count = 0

for d in directoryNames:
    newPath = os.path.join(path, d)
    print "Processing Directory: ", d
    fullPath = next(os.walk(newPath))[0]
    filenames = next(os.walk(fullPath))[2]

    for f in filenames:
        count += 1
        filename, file_extension = os.path.splitext(f)
        if file_extension == ".txt":
            newFileName = os.path.join(fullPath, filename + "_" + str(count) + file_extension)
            orgFileName = os.path.join(fullPath, f)
            os.rename(orgFileName, newFileName)
#            print "this is the original file name: ", orgFileName
#            print "this is the NEW file : ", newFileName
    count = 0
    
print "all done..."
