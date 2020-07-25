from datetime import date
import re
import requests
import os, sys
from templates.writeups import *

W_DIR = '../_writeups/{0}'.format(date.today().year)

createdFileNames = []
ctfName = ''

def createDirIfNotExists(path):
    print('Creating directory: {0}'.format(path))
    if not os.path.exists(path): 
        os.makedirs(path)

def getCtfFrontMatter():
    return ctfCompetitionTemplate.format(
        ctfName, 
        ctfName.replace(" ", "-"),
        date.today()
    )

def writeCtfFrontMatter():
    createDirIfNotExists('{0}/{1}/'.format(W_DIR, ctfName.replace(" ", "-")))
    createDirIfNotExists('../assets/CTFs/{0}/'.format(ctfName.replace(" ", "-")))
    file = open('{}/{}/{}.md'.format(W_DIR, ctfName.replace(" ", "-"), "index"), 'w+')
    file.write(getCtfFrontMatter())
    file.close()

def writeWriteupFrontMatter(challName, descUrl, points, solves, tags, comments):
    writeupFileName = '{}/{}/{}.md'.format(
        W_DIR, 
        ctfName.replace(" ", "-"), 
        challName.replace(" ", "-")
    )
    file = open(writeupFileName, 'w+')
    file.write(ctfWriteupTemplate.format(
        ctfName, 
        descUrl, 
        points, 
        solves, 
        tags, 
        date.today(),
        comments
    ))
    file.close()
    createdFileNames.append(writeupFileName)

def openCreatedFiles():
    for fileName in createdFileNames:
        os.system('code "{0}"'.format(fileName))

def main():
    global ctfName
    ctfName = input('Enter CTF Name: ')
    writeCtfFrontMatter()
    while True:
        challName = input('Enter chall name: ')
        descUrl = input('Enter challenge description URL: ')
        points = input('Enter points: ')
        solves = input('Enter no. of solves: ')
        tags = input('Enter chall tags: ')
        comments = 'true' if input('Enable Comments? (y/n): ') == 'y' else 'false'
        writeWriteupFrontMatter(challName, descUrl, points, solves, tags, comments)
        if input('Add another chall? (y/n): ') != 'y':
            break
    openCreatedFiles()

main()