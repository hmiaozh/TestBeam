#if !defined(__CINT__) || defined(__MAKECINT__)
#include <TROOT.h>
#include <TSystem.h>
#include <TFile.h>
#include <TChain.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TGraphErrors.h>
#include <TProfile.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <vector>
#include <iostream>
#include <iomanip>
#include <math.h>

//#include "tree.h"

#endif

double sigmaSiPMQIE10(double ifC) {
  if(ifC < 200) return (0.7416 + 0.0358*ifC)/3.;
  return (15.225  + 0.0268*ifC + 9e-8*ifC*ifC)/3.;
}


void TestBeamdebug(TString outfile="sampletest/tb_ele_sc_bin3.root") {


  TChain *chain = new TChain("QIE11Data/Events");
/*
//pion
	chain->AddFile("ana_h2_tb_run003195_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
	chain->AddFile("ana_h2_tb_run003187_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
  	chain->AddFile("ana_h2_tb_run003201_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
  	chain->AddFile("ana_h2_tb_run003207_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
  	chain->AddFile("ana_h2_tb_run003137_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
  	chain->AddFile("ana_h2_tb_run003239_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
  	chain->AddFile("ana_h2_tb_run003143_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
  	chain->AddFile("ana_h2_tb_run003328_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003329_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003150_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003176_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003353_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003178_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003179_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
        chain->AddFile("ana_h2_tb_run003322_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");

//muon
	chain->AddFile("ana_h2_tb_run003234_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
	chain->AddFile("ana_h2_tb_run003232_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
	chain->AddFile("ana_h2_tb_run003230_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
	chain->AddFile("ana_h2_tb_run003228_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
	chain->AddFile("ana_h2_tb_run003226_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
	chain->AddFile("ana_h2_tb_run003224_EMAP-22JUL2017_Phase1_RM1RM2_Phase2_RM3_processing.root");
*/
//electron
  chain->AddFile("ana_h2_tb_run003298.root"); //300
  chain->AddFile("ana_h2_tb_run003269.root"); //120
  chain->AddFile("ana_h2_tb_run003302.root"); //200
  chain->AddFile("ana_h2_tb_run003371.root"); //200
  chain->AddFile("ana_h2_tb_run003372.root"); //200
  chain->AddFile("ana_h2_tb_run003377.root"); //200
  chain->AddFile("ana_h2_tb_run003290.root"); //250
  chain->AddFile("ana_h2_tb_run003291.root"); //250
  chain->AddFile("ana_h2_tb_run003295.root"); //250
  chain->AddFile("ana_h2_tb_run003297.root"); //250

  Int_t numChs = 0;

  Float_t DigiFC[100][10];
  Float_t DigiPed[100];
  Int_t   DigiIEta[100];
  Int_t   DigiTDC[100][10];
  Int_t   DigiIPhi[100];
  Int_t   DigiDepth[100];


  chain->SetBranchAddress("numChs", &numChs);
  chain->SetBranchAddress("pulse", &DigiFC);
  chain->SetBranchAddress("ped", &DigiPed);
  chain->SetBranchAddress("TDC", &DigiTDC);
  chain->SetBranchAddress("ieta", &DigiIEta);
  chain->SetBranchAddress("iphi", &DigiIPhi);
  chain->SetBranchAddress("depth", &DigiDepth);


  TFile *outf = new TFile(outfile,"recreate");

  TH1D* end2 = new TH1D("end2","end2",100,1,6);
  TH1D* end3 = new TH1D("end3","end3",100,1,6);
  TH1D* end4 = new TH1D("end4","end4",100,1,6);
  TH1D* end5 = new TH1D("end5","end5",100,1,6);
  TH1D* end6 = new TH1D("end6","end6",100,1,6);


  vector<TProfile *> v_p4;
  vector<TProfile *> v_p3;
  vector<TProfile *> v_p5;


  for (int i=0; i<50; i++) {
    char pname[10];
    sprintf(pname,"p4_%i",i);
    v_p4.push_back(new TProfile(pname,pname,10,-0.5,9.5,"e")); v_p4[i]->Sumw2();
    sprintf(pname,"p3_%i",i);
    v_p3.push_back(new TProfile(pname,pname,10,-0.5,9.5,"e")); v_p3[i]->Sumw2();
    sprintf(pname,"p5_%i",i);
    v_p5.push_back(new TProfile(pname,pname,10,-0.5,9.5,"e")); v_p5[i]->Sumw2();
  }


  for (UInt_t k=0; k<chain->GetEntries(); k++) {
//  for (UInt_t k=0; k<10000; k++) {
    chain->GetEntry(k);

    if (k%1000000==0) cout << 100*k/float(chain->GetEntries()) << endl;



//    if (DigiIEta->size()==0) continue;

      
    for (int i=0; i<numChs; i++) {


      double sumFC=0;
      double errSumFC=0;
      for (int j=0; j<10; j++) {
	sumFC+=DigiFC[i][j];
	errSumFC+=sigmaSiPMQIE10(DigiFC[i][j])*sigmaSiPMQIE10(DigiFC[i][j]);
      }
      sumFC = sumFC - 10*DigiPed[i];
      errSumFC += 10*sigmaSiPMQIE10(DigiPed[i])*sigmaSiPMQIE10(DigiPed[i]);  //err^2
//      errSumFC=sqrt(errSumFC);

      if(DigiIEta[i] == 19 && DigiIPhi[i] == 5){

      	if(DigiDepth[i] == 2) end2->Fill(TMath::Log10(sumFC));
      	else if(DigiDepth[i] == 3) end3->Fill(TMath::Log10(sumFC));
      	else if(DigiDepth[i] == 4) end4->Fill(TMath::Log10(sumFC));
      	else if(DigiDepth[i] == 5) end5->Fill(TMath::Log10(sumFC));
      	else if(DigiDepth[i] == 6) end6->Fill(TMath::Log10(sumFC));

      }

//      if (sumFC<316 || sumFC > 3160) continue;
      if (sumFC<200000) continue;

      if(DigiDepth[i] != 2 || DigiIEta[i] != 19 || DigiIPhi[i] != 5) continue;


      if (DigiTDC[i][4]<60) {	
	int tdc_time=DigiTDC[i][4];
	for (int j=0; j<10; j++) {
	  double val = (DigiFC[i][j] - DigiPed[i])/sumFC;
          double erru = sigmaSiPMQIE10(DigiFC[i][j])*sigmaSiPMQIE10(DigiFC[i][j]) + sigmaSiPMQIE10(DigiPed[i])*sigmaSiPMQIE10(DigiPed[i]);
          double err = sqrt( erru/(sumFC*sumFC) + ( errSumFC * (DigiFC[i][j] - DigiPed[i]) * (DigiFC[i][j] - DigiPed[i]) )/(sumFC*sumFC*sumFC*sumFC) );
          v_p4.at(tdc_time)->Fill(j,val, err);
	}
      }
      else if (DigiTDC[i][4]==62 && DigiTDC[i][3]<60) {
	int tdc_time=DigiTDC[i][3];
        for (uint j=0; j<10; j++) {
	  double val = (DigiFC[i][j] - DigiPed[i])/sumFC;
	  double erru = sigmaSiPMQIE10(DigiFC[i][j])*sigmaSiPMQIE10(DigiFC[i][j]) + sigmaSiPMQIE10(DigiPed[i])*sigmaSiPMQIE10(DigiPed[i]);
          double err = sqrt( erru/(sumFC*sumFC) + ( errSumFC * (DigiFC[i][j] - DigiPed[i]) * (DigiFC[i][j] - DigiPed[i]) )/(sumFC*sumFC*sumFC*sumFC) );
          v_p3.at(tdc_time)->Fill(j,val, err);
	}
	
      }
      else if (DigiTDC[i][5]<60) {
        int tdc_time=DigiTDC[i][5];
	for (uint j=0; j<10; j++) {
	  double val = (DigiFC[i][j] - DigiPed[i])/sumFC;
          double erru = sigmaSiPMQIE10(DigiFC[i][j])*sigmaSiPMQIE10(DigiFC[i][j]) + sigmaSiPMQIE10(DigiPed[i])*sigmaSiPMQIE10(DigiPed[i]);
          double err = sqrt( erru/(sumFC*sumFC) + ( errSumFC * (DigiFC[i][j] - DigiPed[i]) * (DigiFC[i][j] - DigiPed[i]) )/(sumFC*sumFC*sumFC*sumFC) );
          v_p5.at(tdc_time)->Fill(j,val, err);
        }
      }

    }


  }


  outf->Write();
  outf->Close();

}
