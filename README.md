# LaTeX utilities

Framework that automates the creation of pdf slides (using Beamer) containing all the plots produced in the Hμμ analysis, reducing hours of daily workload to minutes.
The obtained slides have been used to give weekly presentations at CERN to the ATLAS Collaboration, which led to the final publication of the paper titled _[A search for the dimuon decay of the Standard
Model Higgs boson with the ATLAS detector](https://arxiv.org/pdf/2007.07830.pdf)_

_Written to be run in the CERN LXPLUS cluster, can be easily readapted.
Requires TeX Live 2017, Python3.x and Pytex._


&nbsp;

## :triangular_flag_on_post: SETUP

#### Setup environment, LaTeX and pythonTex
```
source setup.sh
```

&nbsp;

## :triangular_flag_on_post: COMPILE LATEX
Instead of using `pdflatex`, run using the `pytex` command.  
For a generic .tex file:

```
pytex {filename.tex}
```
For a .tex file that takes an input argument `arg` (this means that the variable `\arg` is used in the .tex document):
```
pytex {filename.tex} arg=argvalue
```
&nbsp;


## :triangular_flag_on_post: Folders description

#### Slides
Produced slides, both pdf and source files

#### Templates
LaTeX/Beamer templates

#### Scripts
Python scripts (i.e. to select all pictures in given folder) and .tex short slides

#### Tests
Misc files mainly used for testing


&nbsp;

## :triangular_flag_on_post: Scripts usage

#### makeSStable.tex  
Create single LaTeX table containing selected pdfs for spurious signal tests. Run as
```
pytex makeSStable.tex inputTable={path_to_txt_table}
```
Note: the path is relative to the folder 
`$DIRWORK/ANALYSIS/FITTING_Hmumu/Hmumu_bkgModelStudies/scripts/tableAndConfig_Maker/TableMaker_output/`

(Example `pytex makeSStable.tex inputTable=pdfSelection_BDTv18_3best_nounderscore/allCatResults--passSmin_110-160.txt`)
