import os
from subprocess import call,check_call,Popen, PIPE, STDOUT
import argparse
import sys
import collections
from latexFunctions import *
from spuriousSignalFunctions import *

# tex("\item $ $ %s \lpipe %s = %s % "ciao"")

with open("../tests/PAPERpiece.tex","wt") as outfile:

  outputsDir = os.environ["DIRWORK"]+"/ANALYSIS/FITTING_Hmumu/Hmumu_bkgModelStudies/output/BDTv19_REW_3best/"
  extension = "/spuriousSig/"
  ranges = ["110-160", "110-200", "110-220", "110-240"]
  
  outputs = []
  for rangei in ranges:
    outputs.append(outputsDir+rangei+extension)
  
  for ioutput in range(len(outputs)):
    spuriousCats, spuriousErrCats = PAPER_grabPdfs(outputs[ioutput])
    # Error SpSig/deltaSpSig plots
    # for spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3, spuriousErrPlot4 in zip(*[iter(spuriousErrCats)]*4):
    # spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3 = zip(*[iter(spuriousErrCats)]*4)
      # print(spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3, spuriousErrPlot4)
    PAPER_fig(spuriousErrCats, outfile, True)
    # bkgPlotsToplot = list(zip(*list(zip(*(bkgPlots.items())))[1]))
    # for bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4 in list(zip(*[iter(bkgPlotsToplot[0])]*4)):
    #   writefourpics('B-only fits', bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4)
    tex('\n', outfile)
