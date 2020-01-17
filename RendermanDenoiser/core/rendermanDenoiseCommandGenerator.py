"""
Test
"""

firstFrame = int(input("First Frame Number: "))
lastFrame = int(input("Last Frame Number: "))
finalPadding = int(input("Padding: "))

outdir = str(input("Output directory: "))

useConfigFiles = str(input("Use config files? (y or n) "))
if useConfigFiles:
    configFiles = str(input("Config file name: "))
    config = "-f %s" % configFiles
else:
    config = ""

crossframe = str(input("Crossframe (y or n): ")).lower()
assert crossframe == "y" or crossframe == "n", "Argument crossframe must be 'y' or 'n'"
cross = "--crossframe -v variance" if crossframe == "y" else ""

override = str(input("Override filter layers independently? (y or n): ")).lower()
assert override == "y" or override == "n", "Argument override must be 'y' or 'n'"
over = "--override filterLayersIndependently true --" if override == "y" else ""

inputFilePath = str(input("Input file path: "))

cmd = 'denoise --outdir "%s" %s %s %s "%s.{"' % (outdir, config, cross, over, inputFilePath)

numRange = list(map(str, range(firstFrame, lastFrame + 1)))

newRange = []
for x in range(len(numRange)):
    indexPadding = len(numRange[x])
    if indexPadding < finalPadding:
        differencePadding = finalPadding - indexPadding
        addedPadding = ""
        for i in range(0, differencePadding):
            addedPadding += "0"
        addedPadding += numRange[x]
        newRange.append(addedPadding)
    else: newRange.append(numRange[x])

string = (cmd+','.join(newRange)+'}.exr"')
print(3*"\n"+"FINAL COMMAND:\n"+string)
