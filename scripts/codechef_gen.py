from datetime import date
import re
import requests
import os, sys
from templates.codechef import *

W_DIR = '../_solutions/Codechef'

createdFileNames = []
contestCode = ''
contestName = ''

def getResponseJson(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(
                'HTTP Response: {0} when trying {1}'
                    .format(response.status_code, url)
            )
            exit()
    except ConnectionError:
        print("Could not reach the Codechef API. Please check your internet connection!")
        exit()
    return response.json()

def createDirIfNotExists(path):
    print('Creating directory: {0}'.format(path))
    if not os.path.exists(path): 
        os.makedirs(path)

def getContestFrontMatter():
    return cpContestTemplate.format(
        'Codechef',
        contestCode, 
        contestName, 
        date.today()
    )

def writeContestFrontMatter():
    createDirIfNotExists('{0}/{1}/'.format(W_DIR, contestCode))
    file = open('{0}/{1}/{2}.md'.format(W_DIR, contestCode, "index"), 'w+')
    file.write(getContestFrontMatter())
    file.close()

def writeProblemFrontMatter(problemCode, problemName, comments, tags):
    problemFileName = '{0}/{1}/{2}.md'.format(W_DIR, contestCode, problemCode)
    file = open(problemFileName, 'w+')
    file.write(cpSolutionTemplate.format(
        'Codechef',
        contestCode,
        contestName,
        problemCode,
        problemName,
        comments,
        tags,
        date.today()
    ))
    file.close()
    createdFileNames.append(problemFileName)

def formatMarkdown(input):
    rSubBlockMath = re.compile(r'(\$\$)(.*?)(\$\$)')
    output = rSubBlockMath.sub(r'\\\\[\2\\\\]', input)
    rSubInlineMath = re.compile(r'(\$)(.*?)(\$)')
    output = rSubInlineMath.sub(r'\\\\(\2\\\\)', output)
    rSubCarriageReturn = re.compile(r'\r\n')
    output = rSubCarriageReturn.sub(r'\n', output)
    return output

def writeProblemStatement(problemCode, problemStatement, problemAuthor):
    createDirIfNotExists('{0}/{1}/_problems/'.format(W_DIR, contestCode))
    file = open(
        '{0}/{1}/_problems/{2}.md'.format(W_DIR, contestCode, problemCode),
        mode = 'w+', 
        encoding = "utf-8"
    )
    file.write(
        '\n**Credit to the author: [{0}](https://codechef.com/users/{0})**\n\n'
            .format(problemAuthor)
    )
    file.write(problemStatement)
    file.close()

def stripLastLine(problemCode):
    file = open(
        '{0}/{1}/_problems/{2}.md'.format(W_DIR, contestCode, problemCode),
        mode = 'r+', 
        encoding = "utf-8"
    )
    lines = file.readlines()
    lines = lines[:-1]
    file = open(
        '{0}/{1}/_problems/{2}.md'.format(W_DIR, contestCode, problemCode),
        mode = 'w+', 
        encoding = "utf-8"
    )
    file.writelines(lines)
    file.close()

def writeSolution(problemJson):  
    if problemJson['status'] == 'success':
        problemName = problemJson['problem_name']
        problemCode = problemJson['problem_code']
        problemStatement = formatMarkdown(problemJson['body'])
        problemAuthor = problemJson['problem_author']
        writeProblemStatement(
            problemCode, 
            problemStatement, 
            problemAuthor
        )
        enableComments = input('Comments enabled? (y/n) : ') == 'y'
        comments = 'true' if enableComments else 'false'
        tags = input('Enter concepts involved (Separated by spaces) : ')
        stripLastLine(problemCode)
        writeProblemFrontMatter(problemCode, problemName, comments, tags)
    else:
        print(json['message'])

def openCreatedFiles():
    for fileName in createdFileNames:
        os.system('code ' + fileName)

def main():
    global contestCode, contestName
    if input('Is it a practice problem? (y/n) : ') == 'y':
        contestCode = 'PRACTICE'
        contestName = 'Practice'
        problemCode = input('Enter problem code : ')
        responseJson = getResponseJson(
            'https://www.codechef.com/api/contests/PRACTICE/problems/{0}' 
                .format(problemCode)
        )
        writeContestFrontMatter()
        writeSolution(responseJson)
    else:
        contestCode = input('Enter Contest Code : ')
        W_DIR = '../_solutions/Codechef/{0}'.format(contestCode)
        contest = getResponseJson(
            'https://www.codechef.com/api/contests/{0}'.format(contestCode)
        )
        if contest['status'] == 'success':
            contestName = contest['name']
            writeContestFrontMatter()
            problemCodes = list(dict(contest['problems']).keys());
            print('Available problem codes: ' + str(problemCodes))
            for i in range(len(problemCodes)):
                if input(
                    '\nDo you want to write solution for {0}? (y/n) :'
                        .format(problemCodes[i])
                    ) == 'y':
                    responseJson = getResponseJson(
                        'https://www.codechef.com/api/contests/{0}/problems/{1}'
                            .format(contestCode, problemCodes[i])
                    )
                    writeSolution(responseJson)
    openCreatedFiles()

main()