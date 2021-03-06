// -*- C++ -*-
//
// Package:    H2TestBeamAnalyzer
// Class:      H2TestBeamAnalyzer
// 
/**\class H2TestBeamAnalyzer H2TestBeamAnalyzer.cc UserCode/H2TestBeamAnalyzer/src/H2TestBeamAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Authors:  Jay Dittmann, Nadja Strobbe, Joe Pastika
// Based on work by:  Viktor Khristenko,510 1-004,+41227672815,
//         Created:   Tue Sep 16 15:47:09 CEST 2014
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "EventFilter/HcalRawToDigi/interface/HcalHTRData.h"
#include "EventFilter/HcalRawToDigi/interface/HcalDCCHeader.h"
#include "EventFilter/HcalRawToDigi/interface/HcalUnpacker.h"
#include "DataFormats/HcalDetId/interface/HcalOtherDetId.h"
#include "DataFormats/HcalDigi/interface/HcalQIESample.h"
#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"
#include "DataFormats/HcalDetId/interface/HcalCalibDetId.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/FEDRawData/interface/FEDRawDataCollection.h"
#include "DataFormats/FEDRawData/interface/FEDHeader.h"
#include "DataFormats/FEDRawData/interface/FEDTrailer.h"
#include "DataFormats/FEDRawData/interface/FEDNumbering.h"
#include "DataFormats/FEDRawData/interface/FEDRawData.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalCalibrations.h"
#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"

#include "TBDataFormats/HcalTBObjects/interface/HcalTBTriggerData.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBBeamCounters.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBEventPosition.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBParticleId.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBTiming.h"

#include "RecoTBCalo/HcalTBObjectUnpacker/interface/HcalTBTriggerDataUnpacker.h"
#include "RecoTBCalo/HcalTBObjectUnpacker/interface/HcalTBSlowDataUnpacker.h"

#include "ADC_Conversion.h"
#include "format.h"

#include "TH1D.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TProfile.h"
#include "TFile.h"
#include "TSystem.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include "unpack_name.h"
using namespace std;
using namespace edm;

//
// class declaration
//
	double const adc2fC[256] = {
			1.58, 4.73, 7.88, 11.0, 14.2, 17.3, 20.5, 23.6, 
			26.8, 29.9, 33.1, 36.2, 39.4, 42.5, 45.7, 48.8,
	  		53.6, 60.1, 66.6, 73.0, 79.5, 86.0, 92.5, 98.9,
	    		105, 112, 118, 125, 131, 138, 144, 151,
		 	157, 164, 170, 177, 186, 199, 212, 225,
		   	238, 251, 264, 277, 289, 302, 315, 328,
		     	341, 354, 367, 380, 393, 406, 418, 431,
			444, 464, 490, 516, 542, 568, 594, 620,
	  		569, 594, 619, 645, 670, 695, 720, 745,
	    		771, 796, 821, 846, 871, 897, 922, 947,
		  	960, 1010, 1060, 1120, 1170, 1220, 1270, 1320,
		    	1370, 1430, 1480, 1530, 1580, 1630, 1690, 1740,
	  		1790, 1840, 1890, 1940,  2020, 2120, 2230, 2330,
	    		2430, 2540, 2640, 2740, 2850, 2950, 3050, 3150,
		  	3260, 3360, 3460, 3570, 3670, 3770, 3880, 3980,
		    	4080, 4240, 4450, 4650, 4860, 5070, 5280, 5490,

	  		5080, 5280, 5480, 5680, 5880, 6080, 6280, 6480,
	    		6680, 6890, 7090, 7290, 7490, 7690, 7890, 8090,
		  	8400, 8810, 9220, 9630, 10000, 10400, 10900, 11300,
		    	11700, 12100, 12500, 12900, 13300, 13700, 14100, 14500,
	  		15000, 15400, 15800, 16200, 16800, 17600, 18400, 19300,
	    		20100, 20900, 21700, 22500, 23400, 24200, 25000, 25800,
		  	26600, 27500, 28300, 29100, 29900, 30700, 31600, 32400,
		    	33200, 34400, 36100, 37700, 39400, 41000, 42700, 44300,
	  		41100, 42700, 44300, 45900, 47600, 49200, 50800, 52500,
	    		54100, 55700, 57400, 59000, 60600, 62200, 63900, 65500,
	  		68000, 71300, 74700, 78000, 81400, 84700, 88000, 91400,
	    		94700, 98100, 101000, 105000, 108000, 111000, 115000, 118000,
	  		121000, 125000, 128000, 131000, 137000, 145000, 152000, 160000,
	    		168000, 176000, 183000, 191000, 199000, 206000, 214000, 222000,
	  		230000, 237000, 245000, 253000, 261000, 268000, 276000, 284000,
	    		291000, 302000, 316000, 329000, 343000, 356000, 370000, 384000
		};
class H2TestBeamAnalyzer : public edm::EDAnalyzer 
{
public:
    explicit H2TestBeamAnalyzer(const edm::ParameterSet&);
    ~H2TestBeamAnalyzer();

private:
    virtual void analyze(const edm::Event&, const edm::EventSetup&);

    TFile *_file;
    TTree *_treeHBHE;
    TTree *_treeHF;
    TTree *_treeQIE11;
    TTree *_treeTriggers;
    TTree *_treeWC;
    TTree *_treeBC;
    TTree *_treeTiming;

    string _outFileName;
    int _verbosity;
    double gain_;
    TCalibLedInfo _calibInfo;
    TQIE8Info _hbheInfo;
    TQIE8Info _hfInfo;
    TQIE11Info _qie11Info;

    H2Triggers _triggers;
    H2BeamCounters _BCData;
    H2Timing _timing;

    vector<double> wcX[5];
    vector<double> wcY[5];

    TH1D *x[5];
    TH1D *y[5];
  TH1D *s1, *s2, *s3, *s4;
 
  int EventNumber;
  float _slow_data;
  // TH1F *channelsVSTS[120];

    edm::EDGetTokenT<HBHEDigiCollection> tok_HBHEDigiCollection_;
    edm::EDGetTokenT<HFDigiCollection> tok_HFDigiCollection_;
    edm::EDGetTokenT<HODigiCollection> tok_HODigiCollection_;
    edm::EDGetTokenT<HcalDataFrameContainer<QIE11DataFrame> > tok_QIE11DigiCollection_;
    edm::EDGetTokenT<HcalTBTriggerData> tok_HcalTBTriggerData_;
    edm::EDGetTokenT<HcalTBEventPosition> tok_HcalTBEventPosition_;
    edm::EDGetTokenT<HcalTBBeamCounters> tok_HcalTBBeamCounters_;
    edm::EDGetTokenT<HcalTBParticleId> tok_HcalTBParticleId_;
    edm::EDGetTokenT<HcalTBTiming> tok_HcalTBTiming_;    

  bool _sequencer_flag;
  edm::EDGetTokenT<FEDRawDataCollection> raw_token;
  edm::Handle<FEDRawDataCollection> raw_collection;
  
  hcaltb::HcalTBSlowDataUnpacker sdp;
};

//
// constructors and destructor
//
H2TestBeamAnalyzer::H2TestBeamAnalyzer(const edm::ParameterSet& iConfig) :
    _outFileName(iConfig.getUntrackedParameter<string>("OutFileName")),
    _verbosity(iConfig.getUntrackedParameter<int>("Verbosity")),
    gain_(iConfig.getUntrackedParameter<double>("Gain")),
    _sequencer_flag(iConfig.getUntrackedParameter<int>("Sequencer_Flag"))
{
    tok_HBHEDigiCollection_ = consumes<HBHEDigiCollection>(edm::InputTag("hcalDigis"));
    tok_HFDigiCollection_ = consumes<HFDigiCollection>(edm::InputTag("hcalDigis"));
    tok_HODigiCollection_ = consumes<HODigiCollection>(edm::InputTag("hcalDigis"));
    tok_QIE11DigiCollection_ = consumes<HcalDataFrameContainer<QIE11DataFrame> >(edm::InputTag("hcalDigis"));
    tok_HcalTBTriggerData_ = consumes<HcalTBTriggerData>(edm::InputTag("tbunpack"));
    tok_HcalTBEventPosition_ = consumes<HcalTBEventPosition>(edm::InputTag("tbunpack"));
    tok_HcalTBBeamCounters_ = consumes<HcalTBBeamCounters>(edm::InputTag("tbunpack"));
    tok_HcalTBParticleId_ = consumes<HcalTBParticleId>(edm::InputTag("tbunpack"));
    tok_HcalTBTiming_ = consumes<HcalTBTiming>(edm::InputTag("tbunpack"));

    raw_token = consumes<FEDRawDataCollection>(edm::InputTag("source")); //Slow data
    EventNumber = 0;

    //now do what ever initialization is needed

    _file = new TFile(_outFileName.c_str(), "recreate");
    _file->mkdir("HBHEData");
    _file->mkdir("HFData");
    _file->mkdir("QIE11Data");
    _file->mkdir("Triggers");
    _file->mkdir("WCData");
    _file->mkdir("Timing");
    _file->mkdir("BeamCounters");
    _file->mkdir("Histos");

/*
    _file->cd("DiodeInfo");
    _tree = new TTree("Events", "Events");
    _tree->Branch("numChs", &_calibInfo.numChs, "numChs/I");
    _tree->Branch("iphi", _calibInfo.iphi, "iphi[numChs]/I");
    _tree->Branch("ieta", _calibInfo.ieta, "ieta[numChs]/I");
    _tree->Branch("cBoxChannel", _calibInfo.cBoxChannel, "cBoxChannel[numChs]/I");
    _tree->Branch("cBoxString", &_calibInfo.cBoxString);
    _tree->Branch("nTS", _calibInfo.nTS, "nTS[numChs]/I");
    _tree->Branch("pulse", _calibInfo.pulse, TString::Format("pulse[numChs][%d]/D", NUMTS));
*/

    _file->cd("HBHEData");
    _treeHBHE = new TTree("Events", "Events");
    _treeHBHE->Branch("numChs", &_hbheInfo.numChs, "numChs/I");
    _treeHBHE->Branch("numTS", &_hbheInfo.numTS, "numTS/I");
    _treeHBHE->Branch("iphi", _hbheInfo.iphi, "iphi[numChs]/I");
    _treeHBHE->Branch("ieta", _hbheInfo.ieta, "ieta[numChs]/I");
    _treeHBHE->Branch("depth", _hbheInfo.depth, "depth[numChs]/I");
    _treeHBHE->Branch("pulse", _hbheInfo.pulse, TString::Format("pulse[numChs][%d]/F", NUMTS));
    _treeHBHE->Branch("ped", _hbheInfo.ped, "ped[numChs]/F");
    _treeHBHE->Branch("pulse_adc", _hbheInfo.pulse_adc, TString::Format("pulse_adc[numChs][%d]/b", NUMTS));
    _treeHBHE->Branch("ped_adc", _hbheInfo.ped_adc, "ped_adc[numChs]/F");
    _treeHBHE->Branch("valid", _hbheInfo.valid, "valid[numChs]/O");

    _file->cd("HFData");
    _treeHF = new TTree("Events", "Events");
    _treeHF->Branch("numChs", &_hfInfo.numChs, "numChs/I");
    _treeHF->Branch("numTS", &_hfInfo.numTS, "numTS/I");
    _treeHF->Branch("iphi", _hfInfo.iphi, "iphi[numChs]/I");
    _treeHF->Branch("ieta", _hfInfo.ieta, "ieta[numChs]/I");
    _treeHF->Branch("depth", _hfInfo.depth, "depth[numChs]/I");
    _treeHF->Branch("pulse", _hfInfo.pulse, TString::Format("pulse[numChs][%d]/F", NUMTS));
    _treeHF->Branch("pulse_adc", _hfInfo.pulse_adc, TString::Format("pulse_adc[numChs][%d]/b", NUMTS));
    _treeHF->Branch("ped", _hfInfo.ped, "ped[numChs]/F");
    _treeHF->Branch("ped_adc", _hfInfo.ped_adc, "ped_adc[numChs]/F");
    _treeHF->Branch("valid", _hfInfo.valid, "valid[numChs]/O");

    _file->cd("QIE11Data");
    _treeQIE11 = new TTree("Events", "Events");
    _treeQIE11->Branch("numChs", &_qie11Info.numChs, "numChs/I");
    _treeQIE11->Branch("numTS", &_qie11Info.numTS, "numTS/I");
    _treeQIE11->Branch("iphi", _qie11Info.iphi, "iphi[numChs]/I");
    _treeQIE11->Branch("ieta", _qie11Info.ieta, "ieta[numChs]/I");
    _treeQIE11->Branch("depth", _qie11Info.depth, "depth[numChs]/I");
    _treeQIE11->Branch("pulse", _qie11Info.pulse, TString::Format("pulse[numChs][%d]/F", NUMTS));
    _treeQIE11->Branch("ped", _qie11Info.ped, "ped[numChs]/F");
    _treeQIE11->Branch("pulse_adc", _qie11Info.pulse_adc, TString::Format("pulse_adc[numChs][%d]/b", NUMTS));
    _treeQIE11->Branch("ped_adc", _qie11Info.ped_adc, "ped_adc[numChs]/F");
    _treeQIE11->Branch("capid_error", _qie11Info.capid_error, "capid_error[numChs]/O");
    _treeQIE11->Branch("link_error", _qie11Info.link_error, "link_error[numChs]/O");
    _treeQIE11->Branch("soi", _qie11Info.soi, TString::Format("soi[numChs][%d]/O", NUMTS));
    _treeQIE11->Branch("TSn", _qie11Info.TSn,  TString::Format("TSn[numChs][%d]/I",NUMTS));
    _treeQIE11->Branch("TDC", _qie11Info.tdc,  TString::Format("TSn[numChs][%d]/I",NUMTS));
    _treeQIE11->Branch("Cap_id", _qie11Info.Cap_id,  TString::Format("Cap_id[numChs][%d]/I",NUMTS));
    _treeQIE11->Branch("ped_trigger", &_triggers.ped, "ped/I");
    _treeQIE11->Branch("led_trigger", &_triggers.led, "led/I");
    _treeQIE11->Branch("slow_data", &_slow_data, "val/F");

    _file->cd("Triggers");
    _treeTriggers = new TTree("Events", "Events");
    _treeTriggers->Branch("ped", &_triggers.ped, "ped/I");
    _treeTriggers->Branch("led", &_triggers.led, "led/I");
    _treeTriggers->Branch("laser", &_triggers.laser, "laser/I");
    _treeTriggers->Branch("beam", &_triggers.beam, "beam/I");
//  _treeTriggers->Branch("str", &_triggers.str, "char[200]")
    _treeTriggers->Branch("fakeTrg", &_triggers.fakeTrg, "fakeTrg/I");
    _treeTriggers->Branch("inSpillTrg", &_triggers.inSpillTrg, "inSpillTrg/I");

    _file->cd("WCData");
    _treeWC = new TTree("Events", "Events");
    _treeWC->Branch("xA", &(wcX[0]));
    _treeWC->Branch("yA", &(wcY[0]));
    _treeWC->Branch("xB", &(wcX[1]));
    _treeWC->Branch("yB", &(wcY[1]));
    _treeWC->Branch("xC", &(wcX[2]));
    _treeWC->Branch("yC", &(wcY[2]));
    _treeWC->Branch("xD", &(wcX[3]));
    _treeWC->Branch("yD", &(wcY[3]));
    _treeWC->Branch("xE", &(wcX[4]));
    _treeWC->Branch("yE", &(wcY[4]));

    _file->cd("Timing");
    _treeTiming = new TTree("Events", "Events");
    _treeTiming->Branch("s1Count", &_timing.s1Count, "s1Count/I");
    _treeTiming->Branch("s2Count", &_timing.s2Count, "s2Count/I");
    _treeTiming->Branch("s3Count", &_timing.s3Count, "s3Count/I");
    _treeTiming->Branch("s4Count", &_timing.s4Count, "s4Count/I");
    _treeTiming->Branch("triggerTime", &_timing.triggerTime, "triggerTime/D");
    _treeTiming->Branch("ttcL1Atime", &_timing.ttcL1Atime, "ttcL1Atime/D");

    _file->cd("Histos");
    s1 = new TH1D("s1", "s1", 10000, 0, 1000);
    s2 = new TH1D("s2", "s2", 10000, 0, 1000);
    s3 = new TH1D("s3", "s3", 10000, 0, 1000);
    s4 = new TH1D("s4", "s4", 10000, 0, 1000);
    x[0] = new TH1D("xA", "xA", 10000, -100, 100);
    x[1] = new TH1D("xB", "xB", 10000, -100, 100);
    x[2] = new TH1D("xC", "xC", 10000, -100, 100);
    x[3] = new TH1D("xD", "xD", 10000, -100, 100);
    x[4] = new TH1D("xE", "xE", 10000, -100, 100);
    y[0] = new TH1D("yA", "yA", 10000, -100, 100);
    y[1] = new TH1D("yB", "yB", 10000, -100, 100);
    y[2] = new TH1D("yC", "yC", 10000, -100, 100);
    y[3] = new TH1D("yD", "yD", 10000, -100, 100);
    y[4] = new TH1D("yE", "yE", 10000, -100, 100);

    // char name[100];
    // for(int channelN=0;channelN<120;channelN++){sprintf(name,"channel%d",channelN); channelsVSTS[channelN] = new TH1F(name, name, 10, 0, 9);}

    _file->cd("BeamCounters");
    _treeBC = new TTree("Events", "Events");
    _treeBC->Branch("s1adc", &_BCData.s1adc, "s1adc/D");
    _treeBC->Branch("s2adc", &_BCData.s2adc, "s2adc/D");
    _treeBC->Branch("s3adc", &_BCData.s3adc, "s3adc/D");
    _treeBC->Branch("s4adc", &_BCData.s4adc, "s4adc/D");
}

H2TestBeamAnalyzer::~H2TestBeamAnalyzer()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

    _file->cd("Histos");
    s1->Write();
    s2->Write();
    s3->Write();
    s4->Write();
    x[0]->Write();
    x[1]->Write();
    x[2]->Write();
    x[3]->Write();
    x[4]->Write();
    y[0]->Write();
    y[1]->Write();
    y[2]->Write();
    y[3]->Write();
    y[4]->Write();

    _file->Write();
    _file->Close();
}

// ------------ method called for each event  ------------
void H2TestBeamAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    int mark_bad = 0;
    int mark_adc = 0;
    int mark_tdc = 0;

    //
    //  Extracting All the Collections containing useful Info
    //
    edm::Handle<HBHEDigiCollection> hbheDigiCollection;
    edm::Handle<HFDigiCollection> hfDigiCollection;
    edm::Handle<HODigiCollection> hoDigiCollection;
    edm::Handle<QIE11DigiCollection> qie11DigiCollection;
    edm::Handle<HcalTBTriggerData> trigData;
    edm::Handle<HcalTBEventPosition> eventPos;
    edm::Handle<HcalTBBeamCounters> beamCounters;
    edm::Handle<HcalTBParticleId> pId;
    edm::Handle<HcalTBTiming> timing;

    iEvent.getByToken(tok_HBHEDigiCollection_,hbheDigiCollection);
    iEvent.getByToken(tok_HFDigiCollection_,hfDigiCollection);
    iEvent.getByToken(tok_HODigiCollection_,hoDigiCollection);
    iEvent.getByToken(tok_QIE11DigiCollection_,qie11DigiCollection);
    iEvent.getByToken(tok_HcalTBTriggerData_,trigData);
    iEvent.getByToken(tok_HcalTBEventPosition_,eventPos);
    iEvent.getByToken(tok_HcalTBBeamCounters_,beamCounters);
    iEvent.getByToken(tok_HcalTBParticleId_,pId);
    iEvent.getByToken(tok_HcalTBTiming_,timing);
    
    /* Slow data*/
    iEvent.getByToken(raw_token,raw_collection);
    // if (raw_collection.isValid()) _sequencer_flag=1; else _sequencer_flag=0;
    // cout<<raw_collection.isValid()<<endl;
    if (_sequencer_flag==1){
      name_data slow_data;
      slow_data.parameter = "NULL";
      slow_data.val = -999.0;
      if (_sequencer_flag == 1) {
	slow_data = unpack_name(raw_collection,sdp,EventNumber);
      }
      _slow_data=slow_data.val;
      //  cout<<slow_data.parameter<<" "<<_slow_data<<" "<<EventNumber<<endl;
    }
    EventNumber++;

    //
    //  Extract Trigger Info
    //
    _triggers.ped       = (trigData->wasInSpillPedestalTrigger() || 
                           trigData->wasOutSpillPedestalTrigger() ||
                           trigData->wasSpillIgnorantPedestalTrigger());
    _triggers.led        = trigData->wasLEDTrigger();
    _triggers.laser      = trigData->wasLaserTrigger();
    _triggers.beam       = trigData->wasBeamTrigger();
    _triggers.fakeTrg    = trigData->wasFakeTrigger();
    _triggers.inSpillTrg = trigData->wasInSpill();
    //_triggers.str        = trigData->runNumberSequenceId();
    
    //
    //  Extract Event Position
    //
    const char chambers[5] = {'A', 'B', 'C', 'D', 'E'};
    for (size_t i = 0; i < 5; ++i) {
      vector<double> xxx, yyy;
      eventPos->getChamberHits(chambers[i], xxx, yyy);
      wcX[i] = xxx;
      wcY[i] = yyy;
      
      for (size_t j = 0; j < xxx.size(); ++j) x[i]->Fill(xxx[j]);
      for (size_t j = 0; j < yyy.size(); ++j) y[i]->Fill(yyy[j]);
    }
    
    //
    //  Extract Beam Counters Info
    //
    _BCData.cer1adc = beamCounters->CK1adc();   
    _BCData.cer2adc = beamCounters->CK2adc();
    _BCData.cer3adc = beamCounters->CK3adc();
    _BCData.s1adc = beamCounters->S1adc();
    _BCData.s2adc = beamCounters->S2adc();
    _BCData.s3adc = beamCounters->S3adc();
    _BCData.s4adc = beamCounters->S4adc();

    s1->Fill(_BCData.s1adc);
    s2->Fill(_BCData.s2adc);
    s3->Fill(_BCData.s3adc);
    s4->Fill(_BCData.s4adc);

    //
    //  Extract Timing Info     
    //
    _timing.s1Count = timing->S1Count();
    _timing.s2Count = timing->S2Count();
    _timing.s3Count = timing->S3Count();
    _timing.s4Count = timing->S4Count();
    _timing.triggerTime = timing->triggerTime();
    _timing.ttcL1Atime = timing->ttcL1Atime();
    
    if (_verbosity>0)
    {
        cout << "### Before Loop: " << endl
            << "### HBHE Digis=" << hbheDigiCollection->size() << endl
            << "### HF Digis=" << hfDigiCollection->size() << endl
            << "### HO Digis=" << hoDigiCollection->size() << endl
            << "### QIE11 Digis=" << qie11DigiCollection->size() << endl;

        cout << "### Triggers: " << endl
            << "### PED Trigger: " << _triggers.ped << endl
            << "### Led Trigger: " << _triggers.led << endl
            << "### Laser Trigger: " << _triggers.laser << endl
            << "### Beam Trigger: " << _triggers.beam << endl
            << "### In Spill Trigger: " << _triggers.inSpillTrg << endl;
        /*
        cout << "### Wire Chamber A: NHits=" << _vWCData[0].x.size() << endl
            << "### Wire Chamber B: NHits=" << _vWCData[1].x.size() << endl
            << "### Wire Chamber C: NHits=" << _vWCData[2].x.size() << endl
            << "### Wire Chamber D: NHits=" << _vWCData[3].x.size() << endl
            << "### Wire Chamber E: NHits=" << _vWCData[4].x.size() << endl;
        cout << "HF Table Pos(X, Y, V) = " << tableX << "  " << tableY << "  " <<
            tableV << endl;
            */

        cout << "### Beam Counters:" << endl
            << "### Cerenkov1: " << _BCData.cer1adc << endl
            << "### Cerenkov2: " << _BCData.cer2adc << endl
            << "### Cerenkov3: " << _BCData.cer3adc << endl
            << "### s1adc=" << _BCData.s1adc << endl
            << "### s2adc=" << _BCData.s2adc << endl
            << "### s3adc=" << _BCData.s3adc << endl
            << "### s4adc=" << _BCData.s4adc << endl;

        cout << "### Beam Timing: " << endl
            << "### S1Count: " << _timing.s1Count << endl
            << "### S2Count: " << _timing.s2Count << endl
            << "### S3Count: " << _timing.s3Count << endl
            << "### S4Count: " << _timing.s4Count << endl;
    }
    
    int numChs = 0;
    
    for (HBHEDigiCollection::const_iterator digi=hbheDigiCollection->begin();
         digi!=hbheDigiCollection->end(); ++digi)
    {
        if (numChs >= NUMCHS) {
          throw cms::Exception("BufferOverflow") << "HBHEData buffer overflow (maximum capacity NUMCHS = " << NUMCHS << ")";
        }
        
        int iphi = digi->id().iphi();
        int ieta = digi->id().ieta();
        int depth = digi->id().depth();
        int nTS = digi->size();
        
        if (nTS > NUMTS) {
          throw cms::Exception("BufferOverflow") << "HBHEData time samples buffer overflow (maximum capacity NUMTS = " << NUMTS << ")";
        }
        
        if (_verbosity>1)
        {
            int fiberChanId = digi->elecId().fiberChanId();
            int fiberIndex = digi->elecId().fiberIndex();
            int slbChannelIndex = digi->elecId().slbChannelIndex();
            int slbSiteNumber = digi->elecId().slbSiteNumber();
            string slbChannelCode = digi->elecId().slbChannelCode();
            int htrChanId = digi->elecId().htrChanId();
            int spigot = digi->elecId().spigot();
            int dccid = digi->elecId().dccid();
            int htrSlot = digi->elecId().htrSlot();
            int htrTopBottom = digi->elecId().htrTopBottom();
            int readoutVMECrateId = digi->elecId().readoutVMECrateId();
            int linearIndex = digi->elecId().linearIndex();
            
            cout << "### Digi->elecId:" << endl;
            cout << fiberChanId << "  " << fiberIndex << "  "
            << slbChannelIndex << "  " << slbSiteNumber << "  "
            << slbChannelCode << "  " << htrChanId << "  "
            << spigot << "  " << dccid << "  " << htrSlot << "  "
            << htrTopBottom << "  " << readoutVMECrateId << "  "
            << linearIndex << endl;
            cout << "### Digi->detId:" << endl;
            cout << iphi << "  " << ieta << "  " << depth << endl;
        }
        
        //
        //      Set the Branched arrays
        //
        _hbheInfo.iphi[numChs] = iphi;
        _hbheInfo.ieta[numChs] = ieta;
        _hbheInfo.depth[numChs] = depth;
        _hbheInfo.numTS = nTS;
        
        float ped_fc = 0;
        float ped_adc = 0;
        
        for (int iTS=0; iTS<nTS; iTS++)
        {
            const HcalQIESample& sample = digi->sample(iTS);
            unsigned char adc = sample.adc();
            const float fC = sample.nominal_fC();

            _hbheInfo.pulse[numChs][iTS] = fC;
            _hbheInfo.pulse_adc[numChs][iTS] = adc;
            if (iTS >= 1 && iTS <= 2)
            {
                ped_fc += fC;
                ped_adc += adc;
            }
        }
        
        _hbheInfo.ped[numChs] = ped_fc/2.;
        _hbheInfo.ped_adc[numChs] = ped_adc/2.;
        
        _hbheInfo.valid[numChs] = digi->validate();
        
        if (_verbosity>1)
        {
            cout << "### Digi->Data:" << endl;
            for (int iTS=0; iTS<nTS; iTS++)
                cout << _hbheInfo.pulse[numChs][iTS] << "  ";
            cout << endl;
        }
        
        numChs++;
    }
    _hbheInfo.numChs = numChs;


    numChs = 0;
    for (HFDigiCollection::const_iterator digi=hfDigiCollection->begin();
                        digi!=hfDigiCollection->end(); ++digi)
    {
        if (numChs >= NUMCHS) {
          throw cms::Exception("BufferOverflow") << "HFData buffer overflow (maximum capacity NUMCHS = " << NUMCHS << ")";
        }
        
        int iphi = digi->id().iphi();
        int ieta = digi->id().ieta();
        int depth = digi->id().depth();
        int nTS = digi->size();
        
        if (nTS > NUMTS) {
          throw cms::Exception("BufferOverflow") << "HFData time samples buffer overflow (maximum capacity NUMTS = " << NUMTS << ")";
        }
        
        if (_verbosity>0)
        {
            int fiberChanId = digi->elecId().fiberChanId();
            int fiberIndex = digi->elecId().fiberIndex();
            int slbChannelIndex = digi->elecId().slbChannelIndex();
            int slbSiteNumber = digi->elecId().slbSiteNumber();
            string slbChannelCode = digi->elecId().slbChannelCode();
            int htrChanId = digi->elecId().htrChanId();
            int spigot = digi->elecId().spigot();
            int dccid = digi->elecId().dccid();
            int htrSlot = digi->elecId().htrSlot();
            int htrTopBottom = digi->elecId().htrTopBottom();
            int readoutVMECrateId = digi->elecId().readoutVMECrateId();
            int linearIndex = digi->elecId().linearIndex();

            cout << "### Digi->elecId:" << endl;
            cout << fiberChanId << "  " << fiberIndex << "  "
                << slbChannelIndex << "  " << slbSiteNumber << "  "
                << slbChannelCode << "  " << htrChanId << "  "
                << spigot << "  " << dccid << "  " << htrSlot << "  "
                << htrTopBottom << "  " << readoutVMECrateId << "  "
                << linearIndex << endl;
            cout << "### Digi->detId:" << endl;
            cout << iphi << "  " << ieta << "  " << depth << endl;
        }

        //
        //      Set the Branched arrays
        //
        _hfInfo.iphi[numChs] = iphi;
        _hfInfo.ieta[numChs] = ieta;
        _hfInfo.depth[numChs] = depth;
        _hfInfo.numTS = nTS;
        
        float ped_fc = 0;
        float ped_adc = 0;

        for (int iTS=0; iTS<nTS; iTS++)
        {
            const HcalQIESample& sample = digi->sample(iTS);
            const unsigned char adc = sample.adc();
            const float fC = sample.nominal_fC();
            
            _hfInfo.pulse[numChs][iTS] = fC;
            _hfInfo.pulse_adc[numChs][iTS] = adc;
            if (iTS>=1 && iTS<=2)
            {
                ped_fc += fC;
                ped_adc += adc;
            }
        }
        
        _hfInfo.ped[numChs] = ped_fc/2.;
        _hfInfo.ped_adc[numChs] = ped_adc/2.;
        
        _hfInfo.valid[numChs] = digi->validate();

        if (_verbosity>1)
        {
            cout << "### Digi->Data:" << endl;
            for (int iTS=0; iTS<nTS; iTS++)
                cout << _hfInfo.pulse[numChs][iTS] << "  ";
            cout << endl;
        }

        numChs++;
    }
    _hfInfo.numChs = numChs;


    // --------------------------
    // --   QIE11 Information  --
    // --------------------------
    
    // This does not work:
    // for (QIE11DigiCollection::const_iterator digi=qie11DigiCollection->begin();
    //   digi!=qie11DigiCollection->end(); ++digi)
    //   cout << digi->samples() << endl;
    // But this apparently does..
    
    
    if (_verbosity>0) std::cout << "Trying to access the qie collection" << std::endl;
    
    static const Converter Convertadc2fC(gain_);

    const QIE11DigiCollection& qie11dc=*(qie11DigiCollection);
    
    if (qie11dc.size() > NUMCHS) {
      throw cms::Exception("BufferOverflow") << "QIE11Data buffer overflow (maximum capacity NUMCHS = " << NUMCHS << ")";
    }
    
    if (qie11dc.samples() > NUMTS) {
      throw cms::Exception("BufferOverflow") << "QIE11Data time samples buffer overflow (maximum capacity NUMTS = " << NUMTS << ")";
    }
    
    for (int j=0; j < qie11dc.size(); j++){
        
        if (_verbosity>0){
            std::cout << "Printing raw dataframe" << std::endl;
            std::cout << qie11dc[j] << std::endl;
            
            std::cout << "Printing content of samples() method" << std::endl;
            std::cout << qie11dc[j].samples() << std::endl;
        }
        
        // Extract info on detector location
        DetId detid = qie11dc[j].detid();
        HcalDetId hcaldetid = HcalDetId(detid);
        int ieta = hcaldetid.ieta();
        int iphi = hcaldetid.iphi();
        int depth = hcaldetid.depth();
        
        if (_verbosity>0){
            std::cout << "Where am I?\n detid: " << detid.rawId() << std::endl;
            std::cout << " ieta: " << ieta << "\n"
            << " iphi: " << iphi << "\n"
            << " depth: " << depth << std::endl;
        }
        
        // loop over the samples in the digi
        int nTS = qie11dc[j].samples();

        float ped_adc = 0;
        float ped_fc = 0;

        mark_bad = 0;
        mark_adc = 0;

        for(int i=0; i<nTS; ++i)
        {
            unsigned char adc = qie11dc[j][i].adc();
            if (i==0) adc = 5;
            int tdc = qie11dc[j][i].tdc();
            int capid = qie11dc[j][i].capid();
            int soi = qie11dc[j][i].soi();
	        // channelsVSTS[j]->Fill(i,adc2fC[adc]);

            // store pulse information
            const float charge = adc2fC[adc];
            _qie11Info.pulse[j][i] = charge;
            _qie11Info.pulse_adc[j][i] = adc;
            _qie11Info.soi[j][i] = soi;
	        _qie11Info.TSn[j][i] = i;
	        _qie11Info.tdc[j][i] = tdc;
	        _qie11Info.Cap_id[j][i] = capid;

            if (_verbosity>0)
                std::cout << "Sample " << i << ": ADC=" << adc << " Charge=" << charge << "fC" << " TDC=" << tdc << " Capid=" << capid
                          << " SOI=" << soi << std::endl;

            if ((adc == 188 && tdc == 60) || (adc == 124 && tdc == 47) || (adc == 188 && tdc == 7) || (adc == 188 && tdc == 11) ||
                (adc == 124 && tdc == 31) || (adc == 124 && tdc == 49)) {
               mark_bad = 1;
               mark_adc = adc;
               mark_tdc = tdc;

            if (_verbosity>0)
                std::cout << "Mark TS "<<EventNumber<<":"<<i<<" bad, code="<<mark_bad<<", adc=" << mark_adc << ", tdc=" << mark_tdc << std::endl;

            }

            // compute ped from TS 1&2
            if (i>=1 && i<=2){
                ped_adc += adc;
                ped_fc += charge;
            }
            
        }
        ped_adc = ped_adc/2.;
        ped_fc = ped_fc/2.; 

        if (_verbosity>0)
            std::cout << "The pedestal for this channel is " << ped_adc << "ADC counts and " << ped_fc << " fC" << std::endl;
  
        // -------------------------------------
        // --    Set the Branched arrays      --
        // -------------------------------------
        _qie11Info.iphi[j] = iphi;
        _qie11Info.ieta[j] = ieta;
        _qie11Info.depth[j] = depth;
        _qie11Info.ped[j] = ped_fc;
        _qie11Info.ped_adc[j] = ped_adc;
        _qie11Info.capid_error[j] = qie11dc[j].capidError();
        _qie11Info.link_error[j] = qie11dc[j].linkError();
    }

    _qie11Info.numChs = qie11dc.size();
    _qie11Info.numTS = qie11dc.samples();

    if (mark_bad == 0) {
      _treeHBHE->Fill();
      _treeHF->Fill();
      _treeQIE11->Fill();
      _treeTriggers->Fill();
      _treeWC->Fill();
      _treeBC->Fill();
      _treeTiming->Fill();
    } else {
      std::cout << "Mark event "<<EventNumber<<" bad, code="<<mark_bad<<", adc=" << mark_adc << std::endl;	
    }

    return;
}

//define this as a plug-in
DEFINE_FWK_MODULE(H2TestBeamAnalyzer);
