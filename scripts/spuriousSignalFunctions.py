import os
from subprocess import call,check_call,Popen, PIPE, STDOUT
import argparse
import sys
import collections
from latexFunctions import *



def grabPdfs(inputDir):

  # GRAB PLOTS TO BE PRINTED

  categories = []
  pdfs = set()
  # selPdfs = []
  selPdfs = collections.OrderedDict()

  # S+B plots
  spuriousPlots = [] # nCat
  spuriousErrPlots = [] # nCat
  corrSpuriousPlots = [] # nCat*nPdf
  # B-only plots
  bkgPlots = collections.OrderedDict()
  respullPlots = collections.OrderedDict()
  corrBkgPlots = collections.OrderedDict()
  
  # Loop over categories, only selected pdfs
  for category in os.listdir(inputDir):
    categoryPath = os.path.join(inputDir, category)
    if os.path.isdir(categoryPath):
      categories.append(category)
      spuriousPlots.append(categoryPath+'/all_nSignal_noErr.pdf')
      spuriousErrPlots.append(categoryPath+'/all_Z_legend.pdf')
      # Get best pdf
      selPdfs[category] = []
      bkgPlots[category] = []
      with open(categoryPath+'/results.txt', 'r') as resultsFile:
        for line in resultsFile:
          if not line.rstrip() or line.startswith('Name') or line.startswith('==>'): pass
          else: 
            selPdf = line.split(' ',1)[0]
            selPdfs[category].append(selPdf)
            pdfPath = os.path.join(categoryPath,selPdf)
            bkgPath = os.path.join(pdfPath,'BkgOnly')
            bkgPlots[category].append( (bkgPath+'/'+selPdf+'_extended_fit_forChi2_ratio.pdf', category) )
            # respullPlots.append(bkgPath+'/'+selPdf+'_extended_ResidualPull.pdf')
            # corrBkgPlots.append(bkgPath+'/'+selPdf+'_extended_correlation.pdf')
            point0Path = os.path.join(pdfPath,'Points/Point0')
            if os.path.isdir(point0Path):
              corrSpuriousPlots.append(point0Path+'/'+selPdf+'_extended_correlation.pdf')


  # CREATE PDF FILE

  spuriousCats = zip(spuriousPlots, categories)
  spuriousErrCats = zip(spuriousErrPlots, categories)

  # Error SpSig/deltaSpSig plots

  for spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3, spuriousErrPlot4 in zip(*[iter(spuriousErrCats)]*4):
    writefourpics('Spurious Signal relative uncertainties', spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3, spuriousErrPlot4)

  # for spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3 in zip(*[iter(spuriousErrCats)]*3):
  #   writethreepics('Spurious Signal relative uncertainties', spuriousErrPlot1, spuriousErrPlot2, spuriousErrPlot3)
  
  # bkgPlotsToplot = list(zip(*list(zip(*(bkgPlots.items())))[1]))
  # for bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4 in list(zip(*[iter(bkgPlotsToplot[0])]*4)):
  #   writefourpics('B-only fits', bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4)




def PAPER_grabPdfs(inputDir, pdfList):

  # GRAB PLOTS TO BE PRINTED
  categories = []
  pdfs = set()
  selPdfs = collections.OrderedDict()
  
  # plots with selected pdf
  bkgPlots = collections.OrderedDict()
  selSpuriousErrPlots = collections.OrderedDict()

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
    pdfPath = os.path.join(categoryPath,selPdf)
    bkgPath = os.path.join(pdfPath,'BkgOnly')
    bkgPlots[category] = bkgPath+'/'+selPdfs[category]+'_fit_forChi2_ratio.pdf'
    
  inv_selSpuriousErrPlots = {v: k for k, v in selSpuriousErrPlots.items()}
  for selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3, selSpuriousErrPlot4 in zip(*[iter(inv_selSpuriousErrPlots.items())]*4):
    writefourpics('Spurious Signal', selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3, selSpuriousErrPlot4)
  
  inv_bkgPlots = {v: k for k, v in bkgPlots.items()}
  for bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4 in zip(*[iter(inv_bkgPlots.items())]*4):
    writefourpics('B-only plots', bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4)




def PAPER_selSpuriousPlots(inputDir, pdfList):

  # GRAB PLOTS TO BE PRINTED
  categories = []
  selPdfs = collections.OrderedDict()
  
  # plots with selected pdf
  selSpuriousErrPlots = collections.OrderedDict()

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
    
  inv_selSpuriousErrPlots = {v: k for k, v in selSpuriousErrPlots.items()}
  for selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3, selSpuriousErrPlot4 in zip(*[iter(inv_selSpuriousErrPlots.items())]*4):
    writefourpics('Spurious Signal', selSpuriousErrPlot1, selSpuriousErrPlot2, selSpuriousErrPlot3, selSpuriousErrPlot4)



def PAPER_selBkgPlots(inputDir, pdfList):

  # GRAB PLOTS TO BE PRINTED
  categories = []
  selPdfs = collections.OrderedDict()
  
  # plots with selected pdf
  bkgPlots = collections.OrderedDict()

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
    titlePlot = 'B-only plots, '+inputDir.rsplit('/',2)[1]
    bkgPlots[category] = categoryPath+'/'+selPdfs[category]+'_fit_forChi2_ratio.pdf'
    
  inv_bkgPlots = {v: k for k, v in bkgPlots.items()}
  for bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4 in zip(*[iter(inv_bkgPlots.items())]*4):
    writefourpics(titlePlot, bkgPlot1, bkgPlot2, bkgPlot3, bkgPlot4)

