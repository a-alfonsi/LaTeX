#!/bin/bash

# Make sure the latest available LaTeX version (TeX Live 2017) is being used
export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/2017/bin/x86_64-linux/:$PATH

# Setup pytex
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_94python3 x86_64-slc6-gcc62-opt

# Define main tex folder
export DIRTEX=${PWD}

# Define main 
export DIRWORK=/afs/cern.ch/work/a/${USER}/

# Define pytex command
alias pytex='source $DIRTEX/.runPythonTex'
alias pdflatex='texfot pdflatex'
