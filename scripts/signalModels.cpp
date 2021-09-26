/*
FITS SIGNAL MODEL TO MC SIGNAL TEMPLATE
EXTRACTS DOUBLE CRYSTAL BALL PARAMETERS FOR 20 CATEGORIES
PUTS PARAMETERS AND TOTAL SIGNAL VALUES IN TABLE
ALSO ABLE TO PRODUCE SIGNAL FIT PLOTS AND SIGNAL MODELS CONFIG FILES
*/

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooGaussian.h"
#include "RooCBShape.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TTree.h"
#include "TH1D.h"
#include "TRandom.h"
#include "RooTwoSidedCBShape.h"
#include "RooTwoSidedCBShape.cxx"

#include "CommonFunc.h"
#include "CommonFunc.cxx"

using namespace RooFit ;

const int nSig=6;
const double xmin=110, xmax=160;
const TString sigName[nSig]={"ggF", "VBF", "WH", "ZH", "ggZH", "ttH"};

TH1D* readSignal(TString fileNamePrefix, double yield[nSig], TString histName){
  TH1D *hSig=NULL;
  for(int i=0; i<nSig; i++){
    TFile f(fileNamePrefix+sigName[i]+".root");
    TH1D *h=(TH1D*)f.Get(histName);
    h=CommonFunc::RerangeTH1D(h, xmin, xmax, sigName[i]);
    h->SetDirectory(0);
    f.Close();
    cout<<h<<" "<<hSig<<endl;
    if(!hSig) hSig=(TH1D*)h->Clone(histName+"_merge");
    else hSig->Add(h);
    h->Print();
    hSig->Print();
    cout<<hSig->GetNbinsX()<<" "<<h->GetNbinsX()<<endl;
    yield[i]=h->Integral();
    cout<<sigName[i]<<" "<<yield[i]<<endl;
  }
  return hSig;
}

// void FitSignal_SimplifiedCBG( TString FileName = "../../input/histogram/20200318_sherpa_smearedHist.root", TString xmlDir="xml/config/v8/testalice/", const int nCat = 12 )
void signalModels( TString FileName = "../../ANALYSIS/FITTING_Hmumu/Hmumu_bkgModelStudies5/analysis/hist/sherpa/20200310/sherpa_smearedHist.root", TString xmlDir="xml/config/v8/testalice/", const int nCat = 20 )
{
  RooMsgService::instance().getStream(1).removeTopic(RooFit::NumIntegration) ;
  RooMsgService::instance().getStream(1).removeTopic(RooFit::Fitting) ;
  RooMsgService::instance().getStream(1).removeTopic(RooFit::Minimization) ;
  RooMsgService::instance().getStream(1).removeTopic(RooFit::InputArguments) ;
  RooMsgService::instance().getStream(1).removeTopic(RooFit::Eval) ;
  RooMsgService::instance().setGlobalKillBelow(RooFit::ERROR);
  TH1::SetDefaultSumw2(kTRUE);
  gStyle->SetOptStat(11111);
  gStyle->SetOptFit(11111);
  // system("mkdir -vp "+xmlDir+"/model");
  
  double totalSignal[nCat];
  double mval[nCat];
  double ahval[nCat];
  double alval[nCat];
  double sival[nCat];
  double nhval[nCat];
  double nlval[nCat];
  for(int icat = 0; icat<nCat; icat++) {
    totalSignal[icat] = 0;
    mval[nCat] = 0;
    ahval[nCat] = 0;
    alval[nCat] = 0;
    sival[nCat] = 0;
    nhval[nCat] = 0;
    nlval[nCat] = 0;
  }

  for(int icat = 1; icat<=nCat; icat++){
  // for(int icat = 1; icat<=1; icat++){
    TString categoryName="BDT"+to_string(icat);
    TString histName="sigHist_"+to_string(icat);
    double sigYield[nSig];
    // TH1D* MassInc=readSignal(FileName, sigYield, histName);
    TFile f(FileName);
    TH1D* MassInc=(TH1D*)f.Get(histName);
    MassInc = CommonFunc::RerangeTH1D(MassInc, xmin, xmax);
    MassInc->SetDirectory(nullptr);
    //  MassInc->Draw();

    // Declare observable x
    RooRealVar x("x","x",110.,160.) ;

    // Create a binned dataset that imports contents of TH1 and associates its contents to observable 'x'
    RooDataHist dh("dh","dh",x,Import(*MassInc)) ;
    // Crystal Ball Component
    RooRealVar CB_mean("CB_mean","mean of CB",124.5, 123., 126.) ;
    RooRealVar CB_sigma("CB_sigma","sigma of CB",2.5,0.5, 8.0) ;
    RooRealVar CB_alphaLo("CB_alphaLo","alpha of CB",1.8, 0., 5.) ;
    RooRealVar CB_alphaHi("CB_alphaHi","alpha of CB",1.8, 0., 5.) ;
    RooRealVar CB_nLo("CB_nLo","n of CB",3, 0, 100);
    RooRealVar CB_nHi("CB_nHi","n of CB",10, 0, 100);
    RooTwoSidedCBShape sig("cb1","Signal Component 2",x,CB_mean,CB_sigma,CB_alphaLo,CB_nLo,CB_alphaHi,CB_nHi);

    // P l o t   a n d   f i t   a   R o o D a t a H i s t
    // ---------------------------------------------------

    // fit signal PDF to Data
    // RooFitResult *fitr = sig.fitTo(dh,Save());
    // RooFitResult *fitr = sig.fitTo(dh, Minos(kTRUE),Save(),Range(110.,135.),PrintLevel(-1));
    unique_ptr<RooFitResult> fitr(sig.fitTo(dh, Minos(kTRUE),Save(),PrintLevel(-1)));
    fitr.reset(sig.fitTo(dh, Minos(kTRUE),Save(),PrintLevel(-1)));
    sig.Print();
    fitr->Print();

    double hintegral = MassInc->GetSumOfWeights();
    cout << "Signal Integral = " << hintegral << endl;
    // Plot Fit results
    RooPlot* xframe = x.frame(Title("Fit Higgs to mumu Signal"));
    dh.plotOn(xframe, MarkerColor(kBlack),DataError(RooAbsData::SumW2));
    sig.plotOn(xframe,LineColor(kBlue));
    cout << "chi^2 = " << xframe->chiSquare() << endl;
    // Construct a histogram with the residuals of the data w.r.t. the curve
    RooHist* hresid = xframe->residHist() ; 
    double resintegral = hresid->Integral();
    cout << "Residuals Integral = " << resintegral << endl;
    cout << "Relative Signal Bias = " << resintegral/hintegral << endl;

    // // Construct a histogram with the pulls of the data w.r.t the curve
    // RooHist* hpull = xframe->pullHist();
    // // Create a new frame to draw the residual distribution and add the distribution to the frame
    // RooPlot* frame2 = x.frame(Title("Residual Distribution")) ;
    // frame2->addPlotable(hresid,"P") ;
    // // Create a new frame to draw the pull distribution and add the distribution to the frame
    // RooPlot* frame3 = x.frame(Title("Pull Distribution")) ;
    // frame3->addPlotable(hpull,"P") ;
    //
    // TCanvas* c = new TCanvas("chi2residpull","chi2residpull",1800,900) ;
    // c->Divide(3) ;
    // c->cd(1) ; gPad->SetLeftMargin(0.15) ; xframe->GetYaxis()->SetTitleOffset(1.6) ; xframe->Draw() ;
    // c->cd(2) ; gPad->SetLeftMargin(0.15) ; frame2->GetYaxis()->SetTitleOffset(1.6) ; frame2->Draw() ;
    // c->cd(3) ; gPad->SetLeftMargin(0.15) ; frame3->GetYaxis()->SetTitleOffset(1.6) ; frame3->Draw() ;
    // c->Update();
    // c->Print(xmlDir+"/model/signal_"+categoryName+".pdf");
    // c->Print(xmlDir+"/model/signal_"+categoryName+".png");

    // // Print out signal model XML file
    // TString outputModelFileName=xmlDir+"/model/signal_"+categoryName+".xml";
    // RooRealVar varInName[6]={CB_alphaLo, CB_mean, CB_nLo, CB_sigma, CB_alphaHi, CB_nHi};
    // TString varOutName[6]={"alphaCBLo", "meanNom", "nCBLo", "sigmaCBNom", "alphaCBHi", "nCBHi"};
    // ofstream fout(outputModelFileName);
    // fout<<"<!DOCTYPE Model SYSTEM 'AnaWSBuilder.dtd'>"<<endl;
    // fout<<"<Model Type=\"UserDef\">"<<endl;
    // for(int ivar=0; ivar<6; ivar++){
    //   fout<<"  <Item Name=\""+varOutName[ivar]+Form("[%f]\"/>", varInName[ivar].getVal())<<endl;
    // }
    // fout<<Form("  <Item Name=\"expr::mean('@0+@1-125', meanNom, mH[125])\"/>")<<endl;
    // fout<<Form("  <ModelItem Name=\"RooTwoSidedCBShape::signalPdf(:observable:, mean, sigmaCBNom, alphaCBLo, nCBLo, alphaCBHi, nCBHi)\"/>")<<endl;
    // fout<<"</Model>"<<endl;
    // fout.close();

    TString bkgHistName=histName;
    bkgHistName.ReplaceAll("sig","bkg");
    TH1* bkgHist=(TH1*)f.Get(bkgHistName);
    double bkgIntegral=bkgHist->Integral();
    
    // Add category signal integral to total signal integral
    totalSignal[icat-1] += hintegral;
    mval[icat-1]  = CB_mean.getVal();
    nhval[icat-1] = CB_nLo.getVal();
    nlval[icat-1] = CB_nHi.getVal();
    sival[icat-1] = CB_sigma.getVal();
    ahval[icat-1] = CB_alphaHi.getVal();
    alval[icat-1] = CB_alphaLo.getVal();
  }

  


  ofstream fout_table("outputs/outTable.tex");
  if (!fout_table) { cout << "Output file not found\n"; return; }


  fout_table << "%\\usepackage{graphicx}" << endl;
  fout_table << "%\\usepackage{multirow}" << endl;
  fout_table << "%\\usepackage{array}" << endl;
  fout_table << "%\\usepackage{booktabs}" << endl;
  fout_table << "%\\usepackage{rotating}" << endl;

  fout_table << "\\begin{sidewaystable}" << endl;
  fout_table << "\\scalebox{0.7}{" << endl;
  fout_table << "\\addtolength{\\tabcolsep}{-2pt}" << endl;
  fout_table << "\\renewcommand{\\arraystretch}{1.2}" << endl;
  fout_table << "\\begin{tabular}{ l | rrrr | rrrr | rrrr | rrrr | rrr | r }" << endl;
  fout_table << "\\toprule" << endl;
  fout_table << "\\multirow{2}{*}{Category} & \\multicolumn{4}{c}{VBF}      & \\multicolumn{4}{c}{Higgs-2Jet}      & \\multicolumn{4}{c}{Higgs-1Jet}      & \\multicolumn{4}{c}{Higgs-0Jet}      & \\multicolumn{3}{c}{VH}      & \\multicolumn{1}{c}{\\multirow{2}{*}{ttH}} \\\\" << endl;
  
  fout_table << "  & High & Med & Low & VeryLow &      High & Med & Low & VeryLow &      High & Med & Low & VeryLow &      High & Med & Low & VeryLow &      4L-Tight & 3L-Tight & 3L-Low &    \\\\" << endl;
  fout_table << "\\midrule" << endl;
  
  fout_table << "Signal  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", totalSignal[icat]);
  }
  fout_table << "\\\\" << endl;
  
  fout_table << "\\midrule" << endl;
  fout_table << "Parameters     &        &        &        &        &        &        &        &        &        &         &         &         &         &         &         &         &         &         &         &         \\\\" << endl;
  fout_table << "\\midrule" << endl;
  
  fout_table << "$M_{CB}$  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", mval[icat]);
  }
  fout_table << "\\\\" << endl;
  
  fout_table << "$\\sigma_{CB}$  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", sival[icat]);
  }
  fout_table << "\\\\" << endl;
  
  fout_table << "$\\alpha_{low}$  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", alval[icat]);
  }
  fout_table << "\\\\" << endl;
  
  fout_table << "$\\alpha_{high}$  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", ahval[icat]);
  }
  fout_table << "\\\\" << endl;
  
  fout_table << "$n_{low}$  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", nlval[icat]);
  }
  fout_table <<Form("\\\\") << endl;
  
  fout_table << "$n_{high}$  " << endl;
  for (int icat=0; icat<nCat; icat++) {
    fout_table << Form("&  %2.2f  ", nhval[icat]);
  }
  fout_table << "\\\\" << endl;
  
  fout_table << "\\bottomrule" << endl;
  fout_table << "\\end{tabular}" << endl;
  fout_table << "}" << endl;
  fout_table << "\\caption{A summary of signal yields and fitter parameters in analysis regions. Signal yields are calculated for the full
    mass range from \\SI{110}{\\GeV} onward ($m(\\mu\\mu)>\SI{110}{\\GeV}$).}" << endl; 
  fout_table << "\\label{tab:signalmodelling:signals}" << endl;
  fout_table << "\\end{sidewaystable}" << endl;



  cout<<endl<<"TOTAL SIGNAL: "<<totalSignal[0]<<endl;
}
