# 
# Creates LaTeX code for all the b-only and spurious signal plots in each category
# 
# USAGE EXAMPLE:
# python PAPERTEX.py 20200404_Sherpa_updateSigModel
# 



import os
from subprocess import call,check_call,Popen, PIPE, STDOUT
import argparse
import sys
import collections
from shutil import copy2



# Write group of three pictures as three subfloats
def PAPERTEX_3pics(title, pic1, pic2, pic3):
  print(r'\subfloat[]{\includegraphics[width=0.3\textwidth]{%s}}' % pic1[0])
  print(r'\subfloat[]{\includegraphics[width=0.3\textwidth]{%s}}' % pic2[0])
  print(r'\subfloat[]{\includegraphics[width=0.3\textwidth]{%s}}\\' % pic3[0])



# Write group of four pictures as three subfloatss
# Used for SS plots in 20 categories scenario
def PAPERTEX_4pics(title, pic1, pic2, pic3, pic4):
  print(r'\subfloat[]{\includegraphics[width=0.35\textwidth]{%s}}' % pic1[0])
  print(r'\subfloat[]{\includegraphics[width=0.35\textwidth]{%s}}\\' % pic2[0])
  print(r'\subfloat[]{\includegraphics[width=0.35\textwidth]{%s}}' % pic3[0])
  print(r'\subfloat[]{\includegraphics[width=0.35\textwidth]{%s}}\\' % pic4[0])



# Write group of three pictures as three subfloats in figure, with title
# Used for b-only plots: a call of this function produces the set of three b-only plots
# (smeared mc, fullsim, data) for a given category
def PAPERTEX_bonly_3pics(title, pic1, pic2, pic3):
  categoryNames = {
       'BDT1'     : 'VBF-High'          ,
       'BDT2'     : 'VBF-Medium'        ,
       'BDT3'     : 'VBF-Low'           ,
       'BDT4'     : 'VBF-VeryLow'       ,
       'BDT5'     : 'Higgs-2Jet-High'   ,
       'BDT6'     : 'Higgs-2Jet-Medium' ,
       'BDT7'     : 'Higgs-2Jet-Low'    ,
       'BDT8'     : 'Higgs-2Jet-VeryLow',
       'BDT9'     : 'Higgs-1Jet-High'   ,
       'BDT10'    : 'Higgs-1Jet-Medium' ,
       'BDT11'    : 'Higgs-1Jet-Low'    ,
       'BDT12'    : 'Higgs-1Jet-VeryLow',
       'BDT13'    : 'Higgs-0Jet-High'   ,
       'BDT14'    : 'Higgs-0Jet-Medium' ,
       'BDT15'    : 'Higgs-0Jet-Low'    ,
       'BDT16'    : 'Higgs-0Jet-VeryLow',
       'BDT17'    : 'VH-4L-Tight'       ,
       'BDT18'    : 'VH-3L-Tight'       ,
       'BDT19'    : 'VH-3L-Low'         ,
       'BDT20'    : 'ttH'              
  }
  categoryName = categoryNames[title]
  print(r'\begin{figure}[!ht]')
  print(r'\centering') 
  print(r'\subfloat[]{\includegraphics[width=0.5\columnwidth]{%s}}' % pic1)
  print(r'\subfloat[]{\includegraphics[width=0.5\columnwidth]{%s}}\\' % pic2)
  print(r'\subfloat[]{\includegraphics[width=0.5\columnwidth]{%s}}' % pic3)
  print(r'\caption{Dimuon invariant mass spectra in category %s overlaid with background-only fit in the range of 110~--~160~\GeV\ for (a) fully simulated MC background, (b) data, (c) smeared Drell-Yan MC template reweighted to data sideband.' % categoryName)
  print(r'The red line in the bottom panel is the signal PDF normalized to the predicted cross-section divided with the background PDF.')
  print(r'}')
  print(r'\label{fig:LABEL_%s}' % title)
  print(r'\end{figure}')



# Write group of two pictures as two subfloats in figure, with title
# Used for b-only plots for categories VH/ttH: a call of this function produces the set of two b-only plots
# (fullsim, data) for a given category (VH/ttH use fullSim for SS as well, so smearHist corresponds to full sim here...)
def PAPERTEX_bonly_2pics(title, pic1, pic2):
  categoryNames = {
       'BDT1'     : 'VBF-High'          ,
       'BDT2'     : 'VBF-Medium'        ,
       'BDT3'     : 'VBF-Low'           ,
       'BDT4'     : 'VBF-VeryLow'       ,
       'BDT5'     : 'Higgs-2Jet-High'   ,
       'BDT6'     : 'Higgs-2Jet-Medium' ,
       'BDT7'     : 'Higgs-2Jet-Low'    ,
       'BDT8'     : 'Higgs-2Jet-VeryLow',
       'BDT9'     : 'Higgs-1Jet-High'   ,
       'BDT10'    : 'Higgs-1Jet-Medium' ,
       'BDT11'    : 'Higgs-1Jet-Low'    ,
       'BDT12'    : 'Higgs-1Jet-VeryLow',
       'BDT13'    : 'Higgs-0Jet-High'   ,
       'BDT14'    : 'Higgs-0Jet-Medium' ,
       'BDT15'    : 'Higgs-0Jet-Low'    ,
       'BDT16'    : 'Higgs-0Jet-VeryLow',
       'BDT17'    : 'VH-4L-Tight'       ,
       'BDT18'    : 'VH-3L-Tight'       ,
       'BDT19'    : 'VH-3L-Low'         ,
       'BDT20'    : 'ttH'              
  }
  categoryName = categoryNames[title]
  print(r'\begin{figure}[!ht]')
  print(r'\centering') 
  print(r'\subfloat[]{\includegraphics[width=0.5\columnwidth]{%s}}' % pic1)
  print(r'\subfloat[]{\includegraphics[width=0.5\columnwidth]{%s}}\\' % pic2)
  print(r'\caption{Dimuon invariant mass spectra in category %s overlaid with background-only fit in the range of 110~--~160~\GeV\ for (a) fully simulated MC background, (b) data.' % categoryName)
  print(r'The red line in the bottom panel is the signal PDF normalized to the predicted cross-section divided with the background PDF.')
  print(r'}')
  print(r'\label{fig:LABEL_%s}' % title)
  print(r'\end{figure}')





# Grabs spurious signal plots for selected function in each category
def PAPERTEX_selSpuriousPlots(inputDir, pdfList, outputDir):

  # GRAB PLOTS TO BE PRINTED
  categories = []
  selPdfs = collections.OrderedDict()
  
  # plots with selected pdf
  selSpuriousErrPlots = collections.OrderedDict()
  selSpuriousErrPlots_relative = collections.OrderedDict()

  for category in os.listdir(inputDir):
    categoryPath = os.path.join(inputDir, category)
    if os.path.isdir(categoryPath):
      categories.append(category)
  
  with open(pdfList, 'r') as resultsFile:
    lines = resultsFile.readlines()
    for i in range(len(lines)):  
      line = lines[i]
      if not line.rstrip() or line.startswith('Name') or line.startswith('==>'): pass
      else:
        selPdf = line.split(' ',1)[0]
        selPdfs[categories[i]] = selPdf
  
  # Loop over categories, only selected pdfs
  for category in categories:
    categoryPath = os.path.join(inputDir, category)
    selSpuriousErrPlots[category] = categoryPath+'/'+selPdfs[category]+'_Z.pdf'
    if os.path.isfile(selSpuriousErrPlots[category]):
      plotName = selSpuriousErrPlots[category].rsplit('/',1)[1]
      plotOutput = outputDir + category + "_" + plotName
      os.system("cp %s %s" % (selSpuriousErrPlots[category], plotOutput))
      selSpuriousErrPlots_relative[category] = "figures" + plotOutput.split('figures',1)[1]
    else:
      print("ERROR")
      return

  inv_selSpuriousErrPlots_relative = collections.OrderedDict()

  for k,v in selSpuriousErrPlots_relative.items():
    inv_selSpuriousErrPlots_relative[v] = k

  return inv_selSpuriousErrPlots_relative





# Grabs b-only plots from their ss/bonly study location (inputDir) for the selected pdfs (from pdfList) in each category
# Copies them in the output latex directory (outputDir)
# Returns the ntuple with their addresses (relative to the outputDir)
def PAPERTEX_selBkgPlots(inputDir, pdfList, outputDir):

  # GRAB PLOTS TO BE PRINTED
  categories = []
  selPdfs = collections.OrderedDict()
  selSpuriousErrPlots_relative = collections.OrderedDict()

  # plots with selected pdf
  bkgPlots = collections.OrderedDict()
  bkgPlots_relative = collections.OrderedDict()

  for category in os.listdir(inputDir):
    categoryPath = os.path.join(inputDir, category)
    if os.path.isdir(categoryPath):
      categories.append(category)
  
  with open(pdfList, 'r') as resultsFile:
    lines = resultsFile.readlines()
    for i in range(len(lines)):  
      line = lines[i]
      if not line.rstrip() or line.startswith('Name') or line.startswith('==>'): pass
      else:
        selPdf = line.split(' ',1)[0]
        selPdfs[categories[i]] = selPdf
  
  # Loop over categories, only selected pdfs
  for category in categories:
    categoryPath = os.path.join(inputDir, category)
    # titlePlot = 'B-only plots, '+inputDir.rsplit('/',2)[1]
    titlePlot = inputDir.rsplit('/',2)[1]
    # print titlePlot
    bkgPlots[category] = categoryPath+'/'+selPdfs[category]+'_fit_forChi2_ratio.pdf'
    if os.path.isfile(bkgPlots[category]):
      plotName = bkgPlots[category].rsplit('/',1)[1]
      plotOutput = outputDir + titlePlot + "/" + category + "_" + plotName
      # print "plot output = ", plotOutput
      bkgFolder = plotOutput.replace(plotOutput.rsplit('/',1)[1], "")
      # print(bkgFolder)
      os.system("mkdir -p %s" %bkgFolder)
      os.system("cp %s %s" % (bkgPlots[category], plotOutput))
      bkgPlots_relative[category] = "figures" + plotOutput.split('figures',1)[1]
      # print "plot relative", bkgPlots_relative[category]
    else:
      print("ERROR")
      return

  return bkgPlots_relative





# --------------------------------------------------
#   MAIN FUNCTION
# --------------------------------------------------
# MAIN: PRODUCES THE OUTPUT TO COPY AND PASTE INTO LATTEX FILE

def main(args):

  frameworkDir = args["frameworkDir"]
  selPdfs = frameworkDir + "config/" + args["plotsFolder"] + "/smearHist_reweight_110-160_pdfList_passSmin.txt"
  plotsDir = frameworkDir + "output/" + args["plotsFolder"]
  paperDir = args["paperDir"]
    


  # SPURIOUS SIGNAL PLOTS

  print("\n\n\n%SS PLOTS\n")

  # Create list of folders containing SS plots 
  SSFolderPaths = []
  extensionSS = "/110-160/spuriousSig/smearHist_reweight/"
  SSFolderPaths.append(plotsDir+extensionSS)
  SSPlotsPath = paperDir+"spurious/"+args["plotsFolder"]+"/"
  # print SSPlotsPath
  os.system("mkdir -p %s" % SSPlotsPath)
  
  for SSFolderPath in range(len(SSFolderPaths)):
    selSSPlots = PAPERTEX_selSpuriousPlots(SSFolderPaths[SSFolderPath], selPdfs, SSPlotsPath)

  # Produce LaTeX output
  print(r'\begin{figure}[htbp]')
  print(r'\centering')
  # for selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3 in zip(*[iter(inv_selSpuriousErrPlots_relative.items())]*3):
    # PAPERTEX_3pics('Spurious Signal', selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3)
  for selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3, selSpuriousErrPlot4 in zip(*[iter(selSSPlots.items())]*4):
    PAPERTEX_4pics('Spurious Signal', selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3, selSpuriousErrPlot4)
  print(r'\caption{CAPTION}')
  print(r'\label{fig:LABEL}')
  print(r'\end{figure}')



  # B-ONLY PLOTS

  print("\n\n\n%B-ONLY PLOTS\n")

  # Create list of folders containing b-only plots (one for each b-only template needed)
  bkgFolderPaths = []
  extensionBkg = "/110-160/bkgOnly/"
  bkgFolderNames = ['bkgHist/', 'dataHist_fillWin/', 'smearHist_reweight_fullab-1/']
  for bkgFolderName in bkgFolderNames:
    bkgFolderPaths.append(plotsDir+extensionBkg+bkgFolderName)

  # Create list of selected b-only plots in each category
  allPlotsBkg = collections.OrderedDict()
  bkgPlotsPath = paperDir+"bonly/"+args["plotsFolder"]+"/"
  for bkgFolderPath in range(len(bkgFolderPaths)):
    selBkgPlots = PAPERTEX_selBkgPlots(bkgFolderPaths[bkgFolderPath], selPdfs, bkgPlotsPath)
    for category in selBkgPlots.keys():
      allPlotsBkg.setdefault(category, list()).append(selBkgPlots[category])



  # Produce LaTeX output
  VHttH = ["BDT17","BDT18","BDT19","BDT20"]
  for category in selBkgPlots.keys():
    bkgPlot1, bkgPlot2, bkgPlot3 = allPlotsBkg[category]
    print('% '+r'%s' % category)
    if category in VHttH:
      PAPERTEX_bonly_2pics(category, bkgPlot3, bkgPlot2)
    else:
      PAPERTEX_bonly_3pics(category, bkgPlot1, bkgPlot2, bkgPlot3)
    print("\n", end='')
  print(r'\FloatBarrier')
  print("\n", end='')




# --------------------------------------------------
#   PARSER
# --------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Create LaTeX figures of spurious signal and b-only plots for the paper')
  parser.add_argument('plotsFolder', type=str, default='20200404_Sherpa_updateSigModel', help='folder containing the plots (it is the studyFolder from the bkg modelling study)')
  parser.add_argument('frameworkDir', type=str, nargs='?', default="/afs/cern.ch/work/a/aalfonsi/ANALYSIS/FITTING_Hmumu/Hmumu_bkgModelStudies5/", help='path of the framework used to run the ss/bonly study')
  parser.add_argument('paperDir', type=str, nargs='?', default="/afs/cern.ch/work/a/aalfonsi/PAPERS/HmumuPAPER2020/figures/modelling/", help='folder where the LaTeX paper modelling figures are located')
  parser.add_argument("-d" ,"--debug", help="Activate debug information", action="store_true")
  args = parser.parse_args()
  main(vars(args));
