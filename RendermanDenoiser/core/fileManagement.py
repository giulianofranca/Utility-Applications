# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

Disclaimer:
    THIS PLUGIN IS JUST A PROTOTYPE. YOU MUST USE THE C++ RELEASE PLUGIN FOR PRODUCTION.
    YOU CAN FIND THE C++ RELEASE PLUGIN FOR YOUR SPECIFIC PLATFORM IN RELEASES FOLDER:
    "gfTools > plug-ins > release"

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * Layers: [--layers]

Sources:
    * NDA

Commands:
    * Output name: [-o]
    * Output directory: [--outdir]
    * Crossframe (checkbox): [--crossframe]
    * Skip first frame (checkbox): [-F]
    * Skip last frame (checkbox): [-L]
    * Motion vectors with crossframe mode. [-v]
    * Number of threads (number widget): [-t]
    * Config files (comboBox): [-f]
    * Override filters (flag system widget): [--override --]


with open("output.txt", "w") as f:
    p1 = subprocess.run("echo 'test'", stdout=f, text=True)

# Ignore errors:
    p1 = subprocess.run("echo 'test'", stderr=subdprocess.DEVNULL)


This code supports Pylint. Rc file in project.
"""

import os
import json


def returnLogPath():
    """Returns the log folder path.

    Returns:
        string: The log folder path.
    """
    corePath = os.path.abspath(os.path.dirname(__file__))
    appPath = os.path.abspath(os.path.join(corePath, os.pardir))
    logPath = os.path.abspath(os.path.join(appPath, "log"))

    return logPath


def returnAppPath():
    """Returns the application folder path.

    Returns:
        string: The application folder path.
    """
    corePath = os.path.abspath(os.path.dirname(__file__))
    appPath = os.path.abspath(os.path.join(corePath, os.pardir))

    return appPath


def returnCorePath():
    """Returns the core folder path.

    Returns:
        string: The core folder path.
    """
    corePath = os.path.abspath(os.path.dirname(__file__))

    return corePath


def returnConfigDict():
    """Return the dictionary containing all the application config settings.

    Returns:
        dict: The dictionary containing all the application config settings.
    """
    cwd = os.getcwd()
    os.chdir(returnCorePath())

    if "config.json" not in os.listdir():
        emptyFile = dict()
        with open("config.json", "w") as f:
            json.dump(emptyFile, f, indent=4)
        configDict = emptyFile
    else:
        with open("config.json", "r") as f:
            configDict = json.load(f)

    os.chdir(cwd)

    return configDict


def returnRMANTREE():
    """Return RMANTREE in config.json if exists.

    In case if its not, return False

    Returns:
        string: The RMANTREE path if exists, False if its not.
    """
    configDict = returnConfigDict()

    if "RMANTREE" not in configDict.keys():
        return False

    rmantree = configDict["RMANTREE"]
    if not os.path.isdir(rmantree):
        return False

    rmantreePath = os.path.abspath(configDict["RMANTREE"])

    return rmantreePath


def setRMANTREE(path):
    """Set RMANTREE in config.json.

    Returns:
        True: If succeed.
    """
    configDict = returnConfigDict()
    configDict["RMANTREE"] = path

    cwd = os.getcwd()
    os.chdir(returnCorePath())

    with open("config.json", "w") as f:
        json.dump(configDict, f, indent=4)

    os.chdir(cwd)

    return True


def generateProcessFile():
    """Generate a .py file with all commands in queue to execute.

    Returns:
        True: If succeed.
    """
    return True
