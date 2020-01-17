import sys
import os
import shutil

# Get Paths and key finder
inputPath = input("Type the images path: ")
outputPath = input("Type the output path: ")
key = input("Type the key identifier (e.g. Final.jpg): ")
os.chdir(inputPath)

# Find all files matching config
fileList = [file for file in os.listdir() if key in file]
len(fileList)

# Print all the files founded.
for file in fileList:
    print(file)
print("%s files founded." % len(fileList))

# Confirm operation
print("\n")
print("You are about to copy %s files from [%s] to [%s]." % (len(fileList), inputPath, outputPath))
confirm = input("Are you sure about that? (y or N): ")
print("\n")
if confirm.lower() == "y":
    print("Starting procedure...")
    step = 10
    for i, file in enumerate(fileList):
        filePath = os.path.join(inputPath, file)
        destPath = os.path.join(outputPath, file)
        shutil.copy(filePath, destPath)
        if round(i / len(fileList) * 100, 2) > step:
            print("Progress: %s %%" % step)
            step += 10
    print("Progress: 100 %")
    print("%s files copied successfully!" % len(fileList))
elif confirm.lower() == "n":
    print("Operation canceled.")
else:
    sys.stderr.write("Can't find command [%s]. Aborting..." % str(confirm))