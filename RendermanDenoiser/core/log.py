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
import datetime
import logging
import importlib

fileM = importlib.import_module("fileManagement", ".")
importlib.reload(fileM)


class QueueLog:
    """Logging class of the queue system

    Available methods:
        * writeMessage(message)   : Write a simple message.
        * writeInfo(message)      : Write a info message.
        * writeStart(message)     : Write a process started message.
        * writeFinish(message)    : Write a process finished message.
        * writeWarning(message)   : Write a warning message.
        * writePause(message)     : Write a queue paused message.
        * writeContinue(message)  : Write a queue continued message.
        * writeDone(message)      : Write a queue done message.
        * writeError(message)     : Writa a error message.
    """

    kLogFormat = "[%(levelname)s - %(asctime)s]: %(message)s"
    kLogFormatNotset = "[%(asctime)s]: %(message)s"
    kDateFileFormat = "%b-%d-%Y %H:%M:%S"
    kDateStreamFormat = "%H:%M:%S"

    def __init__(self):
        cwd = os.getcwd()
        os.chdir(fileM.returnLogPath())

        self.createCustomLevels()

        now = datetime.datetime.now()
        self.name = "%s" % now.strftime("%b-%d-%Y_%H-%M-%S")
        self.filename = "%sQueue.log" % self.name
        self.level = logging.NOTSET
        self.filemode = "a"

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.fileFormatter = logging.Formatter(QueueLog.kLogFormat, QueueLog.kDateFileFormat)
        self.fileHandler = logging.FileHandler(self.filename)
        self.fileHandler.setFormatter(self.fileFormatter)
        self.streamFormatter = logging.Formatter(QueueLog.kLogFormat, QueueLog.kDateStreamFormat)
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setFormatter(self.streamFormatter)
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)

        self.fileFormatterNotset = logging.Formatter(QueueLog.kLogFormatNotset, QueueLog.kDateFileFormat)
        self.fileHandlerNotset = logging.FileHandler(self.filename)
        self.fileHandlerNotset.setFormatter(self.fileFormatterNotset)
        self.streamFormatterNotset = logging.Formatter(QueueLog.kLogFormatNotset, QueueLog.kDateStreamFormat)
        self.streamHandlerNotset = logging.StreamHandler()
        self.streamHandlerNotset.setFormatter(self.streamFormatterNotset)

        os.chdir(cwd)

    def createCustomLevels(self):
        """Create custom logging levels

        Returns:
            True: If it succeed.
        """
        logging.root.setLevel(logging.NOTSET)
        logging.MESSAGE = logging.NOTSET + 1
        logging.STARTED = logging.INFO + 1
        logging.FINISHED = logging.INFO + 2
        logging.PAUSED = logging.WARNING + 1
        logging.CONTINUED = logging.WARNING + 2
        logging.DONE = logging.WARNING + 3
        logging.addLevelName(logging.MESSAGE, "")
        logging.addLevelName(logging.STARTED, "PROCESS STARTED")
        logging.addLevelName(logging.FINISHED, "PROCESS FINISHED")
        logging.addLevelName(logging.PAUSED, "QUEUE PAUSED")
        logging.addLevelName(logging.CONTINUED, "QUEUE CONTINUED")
        logging.addLevelName(logging.DONE, "QUEUE DONE")

        return True

    def writeMessage(self, message):
        """Write an info message.

        Args:
            message (string): The message that will be writed as info.

        Returns:
            True: If succeed.
        """
        self.logger.removeHandler(self.fileHandler)
        self.logger.removeHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandlerNotset)
        self.logger.addHandler(self.streamHandlerNotset)
        self.logger.log(logging.MESSAGE, message)
        self.logger.removeHandler(self.fileHandlerNotset)
        self.logger.removeHandler(self.streamHandlerNotset)
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)
        return True

    def writeInfo(self, message):
        """Write an info message.

        Args:
            message (string): The message that will be writed as info.

        Returns:
            True: If succeed.
        """
        self.logger.info(message)
        return True

    def writeStart(self, message):
        """Write an process started message.

        Args:
            message (string): The message that will be writed as process started.

        Returns:
            True: If succeed.
        """
        self.logger.log(logging.STARTED, message)
        return True

    def writeFinish(self, message):
        """Write an process finished message.

        Args:
            message (string): The message that will be writed as process finished.

        Returns:
            True: If succeed.
        """
        self.logger.log(logging.FINISHED, message)
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

    def writePause(self, message):
        """Write an process queue paused message.

        Args:
            message (string): The message that will be writed as queue paused.

        Returns:
            True: If succeed.
        """
        self.logger.log(logging.PAUSED, message)
        return True

    def writeContinue(self, message):
        """Write an process queue continued message.

        Args:
            message (string): The message that will be writed as queue continued.

        Returns:
            True: If succeed.
        """
        self.logger.log(logging.CONTINUED, message)
        return True

    def writeDone(self, message):
        """Write an process queue done message.

        Args:
            message (string): The message that will be writed as queue done.

        Returns:
            True: If succeed.
        """
        self.logger.log(logging.DONE, message)
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
queue.writeMessage("=================================================")
queue.writeWarning("Start filtering all jobs in queue...")
queue.writeStart("Starting filtering Xunda file.")
queue.writeMessage("10%")
queue.writePause("Queue paused...")
# time.sleep(2)
queue.writeContinue("Queue continued...")
queue.writeFinish("Xunda file is finished filtered.")
queue.writeDone("Queue is totally finished!")
queue.writeWarning("The computer is about to shutdown...")
queue.writeMessage("=================================================")
