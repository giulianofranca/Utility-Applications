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

import os
import collections
import subprocess
import multiprocessing
import importlib

fileM = importlib.import_module("fileManagement", ".")
importlib.reload(fileM)


def returnDenoiseCmdString():
    """Return the denoise command in a string

    Returns:
        string: The denoise command.
    """
    rmantree = fileM.returnRMANTREE()
    prmanPath = os.path.abspath(os.path.join(rmantree, "bin"))
    denoiser = os.path.abspath(os.path.join(prmanPath, "denoise.exe"))

    return denoiser


def returnNumberOfThreads():
    """Return the number of CPU Threads.

    Returns:
        int: The number of CPU Threads.
    """
    return multiprocessing.cpu_count()


def returnProcessor():
    """Return the CPU info.

    Returns:
        string: The processor info.
    """
    result = subprocess.run("wmic cpu get name", shell=True, stdout=subprocess.PIPE, text=True)
    resultSplit = result.stdout.split("  ")[-2]
    processor = resultSplit.split("\n")[-1]

    return processor


def returnGPUList():
    """Return the available CUDA GPU list.

    Returns:
        list: The list of all GPUs.
    """
    denoiserCmd = returnDenoiseCmdString()
    result = subprocess.run('"%s" --list-gpus' % denoiserCmd, shell=True,
                            stdout=subprocess.PIPE, text=True)
    gpuList = result.stdout.rstrip().split("\n")

    return gpuList


def generateProcessList(queue):
    """Generate a process dictionary containing all the commands in queue.

    Args:
        Queue (None): The queue list widget containing all information.

    Returns:
        True: If succeed.
    """
    # 1- Read all jobs in queue
    # 2- Create a dict with all commands in queue
    # 3- Return this dict
    procList = collections.OrderedDict()
    shutdownCmd = "shutdown /s"
    return True


def generateFrameRange(first, last, padding):
    """Generate a string with all numbers in the frame range.

    Args:
        Something (str): Shit.
        First (int): The number that will be starting the string.
        Last (int): The last number of the string.
        Padding (int): The padding of the numbers.

    Returns:
        string: The string with all numbers in frame range.
    """
    assert isinstance(first, int)
    assert isinstance(last, int)

    numbersList = list(map(str, range(first, last + 1)))
    resultRange = []

    for _, number in enumerate(numbersList):
        curPadding = len(number)
        if curPadding < padding:
            newNumber = ""
            for _ in range(0, padding - curPadding):
                newNumber += "0"
            newNumber += number
        else:
            newNumber = number
        resultRange.append(newNumber)

    resultString = ",".join(resultRange)

    return resultString
