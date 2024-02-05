"""
A script to find keywords associated with the provider evaluation and management code distribution Tableau dashboard ("Provider EM Code Distribution")
"""

# TODO
# For production release:
# A valid save must have the auxiliary files present, otherwise, note it on the print screen
# 

import json
import os
import re
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from posixpath import split
from sys import prefix
from datetime import datetime as dt


if sys.platform.startswith("linux") or sys.platform == "darwin":
    os_offset = 1
elif sys.platform == "win32":
    os_offset = 2


class CustomException(Exception):
    """
    Custom exception class.
    """
    def __init__(self, message, path, *args):
        self.message = message
        super(CustomException, self).__init__(message, path, *args)


def getlastline(path):
    """
    Reads the last line in a file
    """
    with open(path, "r+", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell() - os_offset
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)
        line = file.read()
    return line[:-1]


def truncate(path):
    """
    Deletes the last line in a file. Technically, everything from the end of the document to the last newline character.
    h/t https://stackoverflow.com/a/10289740/5478086
    """
    with open(path, "r+", encoding = "utf-8") as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell() - os_offset
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
        elif pos == 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
        else:
            pass
            # TODO raise exception
        file.seek(0, os.SEEK_SET)


def noresults(path):
    """
    """
    target = path.name
    noresults = [{"target": target,
                  "path": path,
                  "detection": False,
                  "line": np.nan,
                  "context": None}]
    return noresults


def kwFind_file_txt(keyword, path):
    """
    """
    target = Path(path).name
    with open(path, "r") as file:
        lines = file.readlines()
        results = []
        for lineNum, line in enumerate(lines, start=1):
            matchli = [match for match in re.finditer(keyword.lower(), line.lower())]
            for match in re.finditer(keyword, line):
                results.append({"target": target,
                                "path": path,
                                "detection": True,
                                "line": lineNum,
                                "context": line})
    if len(results) == 0:
        results = [{"target": target,
                    "path": path,
                    "detection": False,
                    "line": np.nan,
                    "context": None}]
    return results


def kwFind_file_excel(keyword, path):
    """
    """
    df = pd.read_excel(path)
    results = []
    return results


def kwFind_file(keyword, path):
    """
    Searches for keyword in the file or directory located at `path`.

    Handles the following file extensions:
      anb    jl   rep
      crt  json   sql
      csv  jpeg   twb
      dat   jpg   txt
       db   pdf   pem
     docx   png   xls
     html  pptx  xlsx
    hyper    py   zip
      ini     r

    and it treats hidden files as text files. For example, ".Rhistory".
    """
    fileType = path.suffix[1:]  # We will treat multi-suffixed files as singly-suffixed
    # Text-like files
    if fileType.lower() in ["", "crt", "html", "ini", "jl", "json", "pem", "py", "r", "sql", "txt", "twb"]:
        results = kwFind_file_txt(keyword, path)
    # Files that can read with python packages
    # pandas
    elif fileType.lower() in ["csv", "xls", "xlsx"]:
        # Not implemented, temp result
        # results = kwFind_file_excel(keyword, path)
        results = noresults(path)
    # https://stackoverflow.com/questions/25228106/
    elif fileType.lower() in ["docx"]:
        # Not implemented, temp result
        results = noresults(path)
    # https://python-pptx.readthedocs.io/en/latest/
    elif fileType.lower() in ["pptx"]:
        # Not implemented, temp result
        results = noresults(path)
    # https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    elif fileType.lower() in ["pdf"]:
        # Not implemented, temp result
        results = noresults(path)
    # http://vinetto.sourceforge.net/
    elif fileType.lower() in ["db"]:
        # Not implemented, temp result
        results = noresults(path)
    # Files that can only be read with proprietary software
    # anb: IBM Analyst's Notebook
    # REP: Desktop Intelligence Report
    elif fileType.lower() in ["anb", "rep"]:
        # Not implemented, temp result
        results = noresults(path)
    # Hexadecimal files
    elif fileType.lower() in ["dat"]:
        # Not implemented, temp result
        results = noresults(path)
    # Partially readable files
    elif fileType.lower() in ["hyper"]:
        # Not implemented, temp result
        results = noresults(path)
    # Files that should not be read
    elif fileType.lower() in ["zip", "png", "jpg", "jpeg"]:
        # Not implemented, temp result
        results = noresults(path)
    else:
        raise CustomException(f"Unsupported file type: {fileType}", pathstr)
    return results


def kwFind_folder(keyword, path):
    """
    """
    target = path.name
    results = []
    for match in re.finditer(keyword.lower(), target.lower()):
        results.append({"target": target,
                        "path": path,
                        "detection": True,
                        "line": np.nan,
                        "context": None})
    if len(results) == 0:
        results = [{"target": target,
                    "path": path,
                    "detection": False,
                    "line": np.nan,
                    "context": None}]
    return results


def kwFind(keyword, path):
    """
    INPUTS:
        keyword     string
        path        pathlib Path object
    """

    if path.is_file():
        results = kwFind_file(keyword, path)
    elif path.is_dir():
        results = kwFind_folder(keyword, path)
    else:
        message = f"kwFind received invalid input that was interpreted as neither file nor path. The input path is {path}"
        raise CustomException(message, path)
    return results

def unpackResults(result):
    """
    Unpacks values from dictionary while converting data types where necessary.
    """
    target, path, detection, line, context = result["target"], result["path"], result["detection"], result["line"], result["context"]

    pathstr = str(path)
    if isinstance(context, str):
        contextout = context.encode('unicode-escape').decode()
    else:
        contextout = context

    return target, pathstr, detection, line, contextout


# Check for runs. Show runs. New run / Continue old run.
runsDir = os.path.join(r"\\hq3hfsvip01\autoreh\Assignments\Code Search - Provider EM Code Distribution\code", "searches")
if not os.path.isdir(runsDir):
    os.mkdir(runsDir)
elif os.path.isdir(runsDir):
    pass
else:
    message = f"An error occurred while trying to read from or create the following directory: {runsDir}"
    raise CustomException(message, runsDir)
runs = []
for el in os.listdir(runsDir):
    if Path(os.path.join(runsDir, el)).is_dir():
        runs.append(el)
if len(runs) == 0:
    print("No runs available.")
    invalidChoice = True
    while invalidChoice:
        choose = input("Start a new run? Y/N\n")
        if choose.lower() == "y":
            run = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
            invalidChoice = False
        elif choose.lower() == "n":
            invalidChoice = False
            sys.exit()
        else:
            invalidChoice = True
    new = True
elif len(runs) > 0:
    print("Avaiable runs:\n")
    prefix = " "*3
    for run in runs:
        print(prefix + run)
    print("\n")
    invalidChoice = True
    while invalidChoice:
        choose = input("Start a new run or continue an old one? Options:\n\n1 - New run\n2 - Continue an old run\n3 - Exit\n--> ")
        if choose.lower() == "1":
            run = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
            runpath = os.path.join(runsDir, run)
            os.makedirs(runpath)
            new = True
            invalidChoice = False
        elif choose.lower() == "2":
            run = input("Choose which run to continue\n--> ")
            invalidRun = True
            while invalidRun:
                if run in runs:
                    invalidRun = False
                elif not run in runs:
                    run = input(f"Invalid input. You entered '{run}'. Please enter a run from the list shown.\n--> ")
                else:
                    message = f"An error occurred while checking if your input run is in the list of available runs. Input run: {run}. Available runs: {runs}."
                    raise CustomException(message, run)
            new = False
            invalidChoice = False
        elif choose.lower() == "3":
            sys.exit()
        else:
            invalidChoice = True
else:
    message = f"An error occurred while counting the number of runs in the following directory: {runsDir}\n The number of runs counted was {len(runs)}, but expected a non-negative value."
    raise CustomException(message, runsDir)
    

# Define path to run directory
runpath = os.path.join(runsDir, run)
exists = os.path.exists(runpath)
if exists:
    pass
elif not exists:
    os.makedirs(runpath)
else:
    message = f"An error occurred while looking for the run directory: {runpath}\n Expected a boolean but got '{exists}' instead."
    raise CustomException(message, runsDir)


# Define keywords
keywordspath = os.path.join(runpath, "keywords.txt")
if new:
    keywords = "Provider EM Code Distribution".lower().split()
    with open(keywordspath, "w") as file:
        for keyword in keywords:
            file.write(keyword + "\n")
elif not new:
    with open(keywordspath, "r") as file:
        keywords = file.read().split()
else:
    message = f"An error occurred while deciding to start a new run or continue an old one. The program expected a boolean value of 'True' or 'False', but received '{new}'."
    raise CustomException(message, runsDir)

# Define target directory
targetdirpath = os.path.join(runpath, "targetdir.txt")
if new:
    targetDir = r"\\hq3fsvip01\MPI Detection\Data Unit Projects\05 Project"
    # targetDir = r"\\hq3hfsvip01\autoreh\Assignments\Code Search - Provider EM Code Distribution"
    with open(targetdirpath, "w") as file:
        file.write(targetDir)
elif not new:
    with open(targetdirpath, "r") as file:
        targetDir = file.read()
else:
    message = f"An error occurred while deciding to start a new run or continue an old one. The program expected a boolean value of 'True' or 'False', but received '{new}'."
    raise CustomException(message, runsDir)

# Results table
kwdipath = os.path.join(runpath, "keywordMap.txt")
columns = ["rowNum", "target", "path", "detection", "line", "context"]
if new:
    # Define and write keyword map
    kwdi = {id: keyword for id, keyword in enumerate(keywords, 1)}
    with open(kwdipath, "w") as file:
        jsonstring = json.dumps(kwdi)
        file.write(jsonstring)
    # Define results table paths and initialize results table
    resultspathdi = {}
    for id, keyword in kwdi.items():
        resultspath = os.path.join(runpath, f"results-{id}.txt")
        resultspathdi[keyword] = resultspath
        with open(resultspath, "w") as file:
            file.write(','.join(columns))
            file.write('\n')
elif not new:
    # Read keyword map
    with open(kwdipath, "r") as file:
        jsonstring = file.read()
        kwdi = json.loads(jsonstring)
    assert kwdi == {f"{id}": keyword for id, keyword in enumerate(keywords, 1)}, f"The saved keyword dictionary does not match the saved keywords.\n{keywords}\n{kwdi}"
    # Define results table paths
    resultspathdi = {}
    for id, keyword in kwdi.items():
        resultspath = os.path.join(runpath, f"results-{id}.txt")
        resultspathdi[keyword] = resultspath

else:
    message = f"An error occurred while deciding to start a new run or continue an old one. The program expected a boolean value of 'True' or 'False', but received '{new}'."
    raise CustomException(message, runsDir)

# More files
alltargetspath = os.path.join(runpath, "allTargets.txt")
finishedTargetspath = os.path.join(runpath, "finishedTargets.txt")
targetsToDopath = os.path.join(runpath, "targetsToDo.txt")  # Use truncate(path) to remove targets, use pop(path) to read the last target
errorLogpath = os.path.join(runpath, "ErrorLog.txt")
rowTrackerpath = os.path.join(runpath, "rowTracker.json")
timespath = os.path.join(runpath, "times.txt")
if new:
    allTargets = Path(targetDir).rglob("*")
    for target in allTargets:
        with open(alltargetspath, "a") as file:
            file.write(str(target))
            file.write("\n")
        with open(targetsToDopath, "a") as file:
            file.write(str(target))
            file.write("\n")
    with open(finishedTargetspath, "w") as file:
        file.write("")
    # Keep track of number of results per keyword
    rowTracker = {keyword: 0 for keyword in keywords}
    with open(timespath, "w") as file:
        file.write("")
elif not new:
    pass
    # Continue using allTargets.txt
    # Continue using finishedTargets.txt
    # Continue using targetsToDo.txt, the set difference of allTargets - finishedTargets
    # Continue using errorLog.txt
    # Continue using rowTracker.txt
    # Continue using times.txt
    with open(rowTrackerpath, "r") as file:
        text = file.read()
        rowTracker = json.loads(text)
else:
    message = f"An error occurred while deciding to start a new run or continue an old one. The program expected a boolean value of 'True' or 'False', but received '{new}'."
    raise CustomException(message, runsDir)

# Write start time
starttime = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
with open(timespath, "a") as file:
    text = f"Starting run at {starttime}\n"
    file.write(text)
# Analyze paths
it = 0
jt = 1
pathstr = getlastline(targetsToDopath)
path = Path(pathstr)
while not pathstr == "":
    dfdict = {keyword: {} for keyword in keywords}
    for keyword in keywords:
        rowNum = rowTracker[keyword]
        try:
            results = kwFind(keyword, path)
        except (CustomException, UnicodeDecodeError) as e:
            results = noresults(path)
            err = e
            if isinstance(err, UnicodeDecodeError):
                message = f"A UnicodeDecodeError occurred when running `kwFind` on the following path: {pathstr}."
            elif isinstance(err, CustomException):
                message = f"An exception occurred when running `kwFind` on the following path: {pathstr}."
            else:
                message = f"An unexpected error occurred when handling a kwFind Exception. The error is of type {type(err)}."
                raise CustomException(message, path=None)
            with open(errorLogpath, "a") as file:
                file.write(message)
                file.write("\n")
        for result in results:
            target, pathstr, detection, line, context = unpackResults(result)
            dfdict[keyword].update({rowNum: [target, pathstr, detection, line, context]})
            rowNum += 1
        rowTracker[keyword] = rowNum
    for keyword2, results2 in dfdict.items():
        for rowNum, li in results2.items():
            # Append results to each keyword table
            resultspath = resultspathdi[keyword2]
            line = f"{rowNum}," + ",".join([str(el) for el in li])
            with open(resultspath, "a") as file:
                file.write(line)
                file.write("\n")
    # Append path to finishedTargets.txt
    with open(finishedTargetspath, "a") as file:
        file.write(pathstr)
        file.write("\n")
    # Remove path from targetsToDo.txt
    truncate(targetsToDopath)
    # Update rowTracker.json
    with open(rowTrackerpath, "w") as file:
        file.write(json.dumps(rowTracker))
    # Update log
    if it == 1000:
        currentTime = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
        with open(timespath, "a") as file:
            text = f"Batch {jt} completed at {currentTime}\n"
            file.write(text)
        it = 0
        jt += 1
    else:
        it += 1
    # Get next path
    pathstr = getlastline(targetsToDopath)
    path = Path(pathstr)

# Write time to times.txt
starttime = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
with open(timespath, "a") as file:
    text = f"Run complete at {starttime}\n"
    file.write(text)

