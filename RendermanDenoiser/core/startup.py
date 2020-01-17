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
# from PySide2 import QtCore
# from PySide2 import QtWidgets
# from PySide2 import QtGui
# from PySide2 import QtUiTools


# 1- Check OS
# 2- Check Renderman Pro Server
# 3- Start the application

import sys
import importlib

conf = importlib.import_module("config", ".")
runProc = importlib.import_module("runProcesses", ".")
importlib.reload(conf)
importlib.reload(runProc)

# Checking system
conf.checkOS()
conf.checkRendermanProServer()

# Redeem platform info
processor = runProc.returnProcessor()
numThreads = runProc.returnNumberOfThreads()
gpuList = runProc.returnGPUList()
sys.stdout.write("\n%s | %s Threads\n" % (processor, numThreads))
for i, v in enumerate(gpuList):
    if i == len(gpuList) - 1:
        sys.stdout.write("%s\n" % v)
    else:
        sys.stdout.write("%s" % v)

# Application started
sys.stdout.write("\nApplication successfully started.\n")
