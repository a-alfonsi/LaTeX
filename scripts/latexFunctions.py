import os
from subprocess import call,check_call,Popen, PIPE, STDOUT
import argparse
import sys
import collections
from shutil import copy2


def tex(text, outfile=None):
  if outfile==None:
    print(text)
    print('%s' % text)
    print('\n')
  else:
    outfile.write('%s' % text)
    outfile.write('\n')


# make figure for paper
def PAPER_fig(pics, outfile=None, copyFiles=True):
  tex("\\begin{figure}[]", outfile)
  tex('\\centering', outfile)
  unzipList = list(pics)
  picList = []
  # Copy pictures in wanted folder
  for pic in unzipList:
    # print(pic[0])
    picNameList = pic[0].rsplit('/',4)
    picName = picNameList[1]+"_"+picNameList[3]+"_"+picNameList[4]
    picCp = "../tests/PAPERpics/" + picName
    picList.append(picCp)
    # print(pic[0])
    # print(picCp)
    if copyFiles: copy2(pic[0], picCp)
  # print(picList)
  # Create latex picture
  if len(unzipList)==12:
    for i in range(len(picList)):
      print(picList[i])
      # tex('\\subfloat[]{{\\includegraphics[width=0.33\\columnwidth]{{modelling/{}}}}}'.format(pic), outfile)
      # if 
    for pic1, pic2, pic3 in zip(*[iter(unzipList)]*3):
      # print(pic1)
      # print(pic2)
      # print(pic3)
      tex('\\subfloat[]{{\\includegraphics[width=0.33\\columnwidth]{{modelling/{}}}}}'.format(pic1[0]), outfile)
      tex('\\subfloat[]{{\\includegraphics[width=0.33\\columnwidth]{{modelling/{}}}}}'.format(pic2[0]), outfile)
      tex('\\subfloat[]{{\\includegraphics[width=0.33\\columnwidth]{{modelling/{}}}}}\\\\'.format(pic3[0]), outfile)
    tex('\\caption{CAPTION}', outfile)
    tex('\\label{LABEL}', outfile)
    tex('\\end{figure}', outfile)


# List of pdfs
def writeItemList(title, var, items):
  print(r'\begin{frame}{%s}' % title)
  for item in items:
    print(r'\begin{itemize}')
    print(r'\item $ $ %s \lpipe %s = %s' % (item[0],var,item[1]) )
    print(r'\end{itemize}')
  print(r'\end{frame}')

# Write single picture
def writeincludepic(picture, caption):
  print(r'\begin{figure}')
  print(r'\includegraphics[scale=0.5]{%s}' % picture)
  print(r'\caption{$s}' % caption)
  print(r'\end{figure}')

# Write group of three pictures in one slide with title 'title'
def writethreepics(title, pic1, pic2, pic3):
  print(r'\begin{frame}{%s}' % title)
  print(r'\makebox[\textwidth]{')
  print(r'\begin{tabular}{ c c }')
  if os.path.isfile(pic1[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} &' % pic1[0])
  else:
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} &')
  if os.path.isfile(pic2[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} \\ ' % pic2[0])  
  else:
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} \\ ')
  print(r'[-7pt]')
  print(r'\scriptsize %s & ' % pic1[1])
  print(r'\scriptsize %s \\ ' % pic2[1])
  if os.path.isfile(pic3[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} &' % pic3[0])
  else:
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} &')
  print(r' \\ ')
  print(r'[-7pt]')
  print(r'\scriptsize %s & ' % pic3[1])
  print(r'\scriptsize \\ ')
  print(r'\end{tabular}')
  print(r'}')
  print(r'\end{frame}')

# Write group of four pictures in one slide with title 'title'
def writefourpics(title, pic1, pic2, pic3, pic4):
  print(r'\begin{frame}{%s}' % title)
  print(r'\makebox[\textwidth]{')
  print(r'\begin{tabular}{ c c }')
  if os.path.isfile(pic1[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} &' % pic1[0])
  else:
    #print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} &')
    print(r'{%s} &' % pic1[0])
  if os.path.isfile(pic2[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} \\ ' % pic2[0])  
  else:
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} \\ ')
  print(r'[-7pt]')
  print(r'\scriptsize %s & ' % pic1[1])
  print(r'\scriptsize %s \\ ' % pic2[1])
  if os.path.isfile(pic3[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} &' % pic3[0])
  else:
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} &')
  if os.path.isfile(pic4[0]):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} \\ ' % pic4[0])
  else:
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{placeholder.png} \\ ')
  print(r'[-7pt]')
  print(r'\scriptsize %s & ' % pic3[1])
  print(r'\scriptsize %s \\ ' % pic4[1])
  print(r'\end{tabular}')
  print(r'}')
  print(r'\end{frame}')

# Write group of four pictures in one slide with title 'title'
def writesixpics(title, pic1, pic2, pic3, pic4, pic5, pic6):
  print(r'\setlength{\tabcolsep}{-6pt}')
  print(r'\begin{frame}{%s}' % title)
  print(r'\makebox[\textwidth]{')
  print(r'\begin{tabular}{ c c c }')
  if os.path.isfile(pic1[0]):
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{%s} &' % pic1[0])
  else:
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{placeholder.png} &')
  if os.path.isfile(pic2[0]):
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{%s} &' % pic2[0])  
  else:
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{placeholder.png} &')
  if os.path.isfile(pic3[0]):
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{%s} \\ ' % pic3[0])
  else:
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{placeholder.png} \\ ')
  print(r'[-7pt]')
  print(r'\scriptsize %s & ' % pic1[1])
  print(r'\scriptsize %s & ' % pic2[1])
  print(r'\scriptsize %s \\ ' % pic3[1])
  if os.path.isfile(pic4[0]):
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{%s} &' % pic4[0])
  else:
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{placeholder.png} &')
  if os.path.isfile(pic5[0]):
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{%s} &' % pic5[0])
  else:
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{placeholder.png} &')
  if os.path.isfile(pic6[0]):
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{%s} \\ ' % pic6[0])
  else:
    print(r'\includegraphics[height=3.3cm,keepaspectratio]{placeholder.png} \\ ')
  print(r'[-7pt]')
  print(r'\scriptsize %s & ' % pic4[1])
  print(r'\scriptsize %s & ' % pic5[1])
  print(r'\scriptsize %s \\ ' % pic6[1])
  print(r'\end{tabular}')
  print(r'}')
  print(r'\end{frame}')

def writepic(title, pic1):
  print(r'\begin{frame}{%s}' % title)
  print(r'\makebox[\textwidth]{')
  print(r'\begin{tabular}{ c c }')
  if os.path.isfile(pic1):
    print(r'\includegraphics[height=3.5cm,keepaspectratio]{%s} &' % pic1)
  print(r'\end{tabular}')
  print(r'}')
  print(r'\end{frame}')