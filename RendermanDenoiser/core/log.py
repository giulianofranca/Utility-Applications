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
import logging
import importlib

fileM = importlib.import_module("fileManagement", ".")
importlib.reload(fileM)


class QueueLog:
    """Test
    """

    kLogFileFormat = "[%(levelname)s - %(asctime)s]: %(message)s"
    kLogStreamFormat = "[%(levelname)s - %(asctime)s]: %(message)s"
    kDateFileFormat = "%b-%d-%Y %H:%M:%S"
    kDateStreamFormat = "%H:%M:%S"

    def __init__(self):
        cwd = os.getcwd()
        os.chdir(fileM.returnLogPath())

        self.name = "TestQueue1"
        self.filename = "%s.log" % self.name
        self.level = logging.INFO
        self.filemode = "a"

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.fileFormatter = logging.Formatter(QueueLog.kLogFileFormat, QueueLog.kDateFileFormat)
        self.fileHandler = logging.FileHandler(self.filename)
        self.streamFormatter = logging.Formatter(QueueLog.kLogStreamFormat, QueueLog.kDateStreamFormat)
        self.streamHandler = logging.StreamHandler()
        self.fileHandler.setFormatter(self.fileFormatter)
        self.streamHandler.setFormatter(self.streamFormatter)
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)
        # logging.basicConfig(
        #     filename=self.filename,
        #     level=self.level,
        #     format=QueueLog.kLogFormat,
        #     filemode=self.filemode
        # )

        os.chdir(cwd)

    def writeInfo(self, message):
        """Write an info message.

        Args:
            message (string): The message that will be writed as info.

        Returns:
            True: If succeed.
        """
        self.logger.info(message)
        return True

    def writeWarning(self, message):
        """Write an warning message.

        Args:
            message (string): The message that will be writed as warning.

        Returns:
            True: If succeed.
        """
        self.logger.warning(message)
        return True

    def writeError(self, message):
        """Write an warning message.

        Args:
            message (string): The message that will be writed as warning.

        Returns:
            True: If succeed.
        """
        self.logger.exception(message)
        return True

queue = QueueLog()
queue.writeInfo("Test")
