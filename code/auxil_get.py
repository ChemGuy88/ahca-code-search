import os
import sys
from pathlib import Path
from textwrap import indent

if sys.platform.startswith("linux") or sys.platform == "darwin":
    os_offset = 1
elif sys.platform == "win32":
    os_offset = 2

def getlastline(path):
    """
    Reads the last line in a file.
    """
    with open(path, "r+", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell() - os_offset
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)
        line = file.read()
    return line

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

if True:
    def getTargets(path):
        """
        Generator item that reads the last line in a file
        BETA. This is under test to see if the generator loads a file into memory or reads it each time it generates a result. This is being tested because the source file will be modified in the for-loop.
        """
        line = getlastline(path)
        return Path(line)

    targetDir = r"\\hq3fsvip01\MPI Detection\Data Unit Projects\05 Project"
    allTargets = Path(targetDir).rglob("*")
    runsDir = os.path.join(r"\\hq3hfsvip01\autoreh\Assignments\Code Search - Provider EM Code Distribution\code", "searches")

    targetsToDopath = os.path.join(runsDir, "targetsToDo.txt")
    resultspath = os.path.join(runsDir, "results.txt")
    finishedTargetspath = os.path.join(runsDir, "finishedTargets.txt")

    # Simulate files
    li = "BETA. This is under test to see if the generator loads a file into memory or reads it each time it generates a result. This is being tested because the source file will be modified in the for-loop.".split()
    with open(targetsToDopath, "w") as file:
        for el in li:
            file.write(el)
            file.write("\n")
    with open(resultspath, "w") as file:
        file.write("")
    with open(finishedTargetspath, "w") as file:
        file.write("")
    lastline = getlastline(targetsToDopath)
    path = Path(lastline)
    i = 0
    results = []
    while not lastline == "":
        results.append(path)
        print([results[-1]])
        if path.is_file():
            result = True
        elif path.is_file():
            result = False
        else:
            result = None
        # Write result to results.txt
        with open(resultspath, "a") as file:
            file.write(str(result))
            file.write("\n")
        # Append path to finishedTargets.txt
        with open(finishedTargetspath, "a") as file:
            file.write(str(path))
            file.write("\n")
        # Remove path from targetsToDo.txt
        truncate(targetsToDopath)
        i += 1
        if i == 10:
            i = 0
            input("Press any key to continue.")
        lastline = getlastline(targetsToDopath)
        path = Path(lastline)

# So we don't need to create a new function, `getTargets`. Let's try this current method. It should be efficient enough.