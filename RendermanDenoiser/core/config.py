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
# pylint: disable=subprocess-run-check

import sys
import os
import platform
import msvcrt
import subprocess
import importlib

fileM = importlib.import_module("fileManagement", ".")
importlib.reload(fileM)


def checkOS():
    """Check if the operational system is Windows. If is not, close the application.

    Returns:
        None
    """
    if platform.system() != "Windows":
        sys.stderr.write("\nThis application only runs in Windows operational systems.")
        sys.stdout.write("\nYou are currently running %s %s" % (platform.system(), platform.version()))
        sys.stdout.write("\nPress any key to close....")
        msvcrt.getch()
        sys.exit()


def checkRendermanProServer():
    """Check if any version of Renderman Pro Server is installed.

    Returns:
        True: If succeed.
    """
    rmantree = fileM.returnRMANTREE()

    if rmantree is False:
        if "RMANTREE" in os.environ.keys():
            rmantree = os.environ["RMANTREE"]
        else:
            sys.stderr.write("\nCould not find Pixar Renderman Pro Server.\n")
            rmantree = str(input("Path to Pro Server: "))
        fileM.setRMANTREE(rmantree)

    prmanConsistance = checkPRMANConsistance(rmantree)
    while prmanConsistance is False:
        sys.stderr.write("\nPixar Renderman Pro Server path is not consistant.")
        sys.stdout.write("\nCurrent path: \"%s\"." % rmantree)
        sys.stdout.write("\nPlease specify the correct path manually.\n\n")
        rmantree = str(input("Path to Pro Server: "))
        prmanConsistance = checkPRMANConsistance(rmantree)
        if prmanConsistance:
            fileM.setRMANTREE(rmantree)

    sys.stdout.write("\nPixar Renderman Pro Server founded!\n")

    return True


def checkPRMANConsistance(rmantree):
    """Check if Renderman Pro Server path is consistant.

    Args:
        rmantree (string): The Renderman Pro Server path.

    Returns:
        True: If given path is consistant.
    """
    if not os.path.isdir(rmantree):
        return False

    prmanPath = os.path.abspath(os.path.join(rmantree, "bin"))
    if not os.path.isdir(prmanPath):
        return False

    cwd = os.getcwd()
    os.chdir(prmanPath)

    if "denoise.exe" not in os.listdir():
        return False

    denoiser = os.path.abspath(os.path.join(prmanPath, "denoise.exe"))
    result = subprocess.run('"%s" --version' % denoiser, shell=True,
                            stdout=subprocess.PIPE, text=True)
    sys.stdout.write("\n%s" % result.stdout)

    if result.stderr is not None:
        return False

    os.chdir(cwd)

    return True
