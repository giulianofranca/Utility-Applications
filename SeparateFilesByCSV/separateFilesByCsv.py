import os
import argparse
import shutil
import csv


description = """
Separate files by CSV pattern.
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description
)

parser.add_argument("sourceDirectory", type=str,
                    help="The directory where all images live.")
parser.add_argument("destDirectory", type=str,
                    help="The images output directory.")
parser.add_argument("csvFile", type=str,
                    help="The path to the csv file.")

args = parser.parse_args()


print("")
if not os.path.isdir(args.sourceDirectory):
    raise RuntimeError("Source directory '%s' does not exists." % args.sourceDirectory)
print("Source directory:\t%s" % args.sourceDirectory)
if not os.path.isdir(args.destDirectory):
    raise RuntimeError("Destination directory '%s' does not exists." % args.destDirectory)
print("Destination directory:\t%s" % args.destDirectory)
if not os.path.isfile(args.csvFile):
    raise RuntimeError("CSV file '%s' does not exists." % args.csvFile)
print("CSV file location:\t%s" % args.csvFile)
print("")

source = args.sourceDirectory
dest = args.destDirectory
csvFile = args.csvFile
ids = []

with open(csvFile) as f:
    csvReader = csv.reader(f)
    next(csvReader)
    for i, row in enumerate(csvReader):
        if i == 0:
            continue
        ids.append(row[0])

print("Found %s IDs." % len(ids))
status = input("Copy the files to destination folder? (y, n) ")
if status.lower() == "y":
    copiedFiles = 0
    for curId in ids:
        for sourceFileName in os.listdir(source):
            if curId in sourceFileName:
                sourceFile = os.path.abspath(os.path.join(source, sourceFileName))
                print("Copying %s to %s." % (sourceFile, dest))
                shutil.copy(sourceFile, dest)
                copiedFiles += 1

print("")
print("Finished. Copied %s files to %s." % (copiedFiles, dest))
