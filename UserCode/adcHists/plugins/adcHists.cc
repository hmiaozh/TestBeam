// -*- C++ -*-
//
// Package:    UserCode/adcHists
// Class:      adcHists
// 
/**\class adcHists adcHists.cc UserCode/adcHists/plugins/adcHists.cc

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  
//         Created:  Fri, 14 Aug 2015 08:41:12 GMT
//
//


// system include files
#include <memory>

#include <map>
#include <string>
#include <sstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "UserCode/adcHists/include/ADC_Conversion.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TBDataFormats/HcalTBObjects/interface/HcalTBTriggerData.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBBeamCounters.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBEventPosition.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBParticleId.h"
#include "TBDataFormats/HcalTBObjects/interface/HcalTBTiming.h"

double edges10[248] = {
  1.58,   4.73,   7.88,   11.0,   14.2,   17.3,   20.5,   23.6,
  26.8,   29.9,   33.1,   36.2,   39.4,   42.5,   45.7,   48.8,
  53.6,   60.1,   66.6,   73.0,   79.5,   86.0,   92.5,   98.9,
  105,    112,    118,    125,    131,    138,    144,    151,
  157,    164,    170,    177,    186,    199,    212,    225,
  238,    251,    264,    277,    289,    302,    315,    328,
  341,    354,    367,    380,    393,    406,    418,    431,
  444,    464,    490,    516,    542,    568,    594,    620,
  645,    670,    695,    720,    745,
  771,    796,    821,    846,    871,    897,    922,    947,
  960,    1010,   1060,   1120,   1170,   1220,   1270,   1320,
  1370,   1430,   1480,   1530,   1580,   1630,   1690,   1740,
  1790,   1840,   1890,   1940,   2020,   2120,   2230,   2330,
  2430,   2540,   2640,   2740,   2850,   2950,   3050,   3150,
  3260,   3360,   3460,   3570,   3670,   3770,   3880,   3980,
  4080,   4240,   4450,   4650,   4860,   5070,   5280,   5490,
  5680,   5880,   6080,   6280,   6480,
  6680,   6890,   7090,   7290,   7490,   7690,   7890,   8090,
  8400,   8810,   9220,   9630,   10000,  10400,  10900,  11300,
  11700,  12100,  12500,  12900,  13300,  13700,  14100,  14500,
  15000,  15400,  15800,  16200,  16800,  17600,  18400,  19300,
  20100,  20900,  21700,  22500,  23400,  24200,  25000,  25800,
  26600,  27500,  28300,  29100,  29900,  30700,  31600,  32400,
  33200,  34400,  36100,  37700,  39400,  41000,  42700,  44300,
  45900,  47600,  49200,  50800,  52500,
  54100,  55700,  57400,  59000,  60600,  62200,  63900,  65500,
  68000,  71300,  74700,  78000,  81400,  84700,  88000,  91400,
  94700,  98100,  101000, 105000, 108000, 111000, 115000, 118000,
  121000, 125000, 128000, 131000, 137000, 145000, 152000, 160000,
  168000, 176000, 183000, 191000, 199000, 206000, 214000, 222000,
  230000, 237000, 245000, 253000, 261000, 268000, 276000, 284000,
  291000, 302000, 316000, 329000, 343000, 356000, 370000, 384000, 398000
};

class adcHists : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
    explicit adcHists(const edm::ParameterSet&);
    ~adcHists();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
    virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endJob() override;

    edm::EDGetTokenT<QIE11DigiCollection> tok_QIE11DigiCollection_;
    edm::EDGetTokenT<HcalTBTriggerData> tok_HcalTBTriggerData_;

    TH1* hq;

    std::map<std::string, TH1*> spectra;
    
    edm::Service<TFileService> fs;
};

adcHists::adcHists(const edm::ParameterSet& iConfig)
{
    usesResource("TFileService");

    hq = fs->make<TH1D>("allMu", "allMu", 247, edges10);

    tok_QIE11DigiCollection_ = consumes<QIE11DigiCollection>(edm::InputTag("hcalDigis"));
    tok_HcalTBTriggerData_ = consumes<HcalTBTriggerData>(edm::InputTag("tbunpack"));
}


adcHists::~adcHists()
{
    
}

void adcHists::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;

    edm::Handle<QIE11DigiCollection> hqie11dc;
    iEvent.getByToken(tok_QIE11DigiCollection_, hqie11dc);

    edm::Handle<HcalTBTriggerData> trigData;
    iEvent.getByToken(tok_HcalTBTriggerData_, trigData);

    //Reject any event which was not a beam trigger and only a beam trigger inside the spill window
    //if(trigData->wasInSpillPedestalTrigger() || trigData->wasOutSpillPedestalTrigger() || trigData->wasSpillIgnorantPedestalTrigger()) return;
    //if(trigData->wasLEDTrigger())   return;
    //if(trigData->wasLaserTrigger()) return;
    if(!trigData->wasBeamTrigger()) return;
    //if(trigData->wasFakeTrigger())  return;
    //if(!trigData->wasInSpill())     return;

    //ADC to nominal charge converter 
    Converter converter;

    const QIE11DigiCollection& qie11dc = *hqie11dc;
    for (int j=0; j < qie11dc.size(); j++)
    {
        // Extract info on detector location
        DetId detid = qie11dc[j].detid();
        HcalDetId hcaldetid = HcalDetId(detid);
        int ieta = hcaldetid.ieta();
        int iphi = hcaldetid.iphi();
        int depth = hcaldetid.depth();
        
        float adc[10];
        for(int i = 0; i < 10; i++)
        {
            adc[i] = converter.linearize(qie11dc[j][i].adc());
        }

	float ped = (adc[0] + adc[1] + adc[2])/3.0;
	float q = adc[4] + adc[5] + adc[6] - 3*ped;

	std::stringstream hname;
	hname << ieta << "_" << iphi << "_" << depth;
	
	auto hist = spectra.find(hname.str());
	if(hist == spectra.end())
	{
	    spectra[hname.str()] = fs->make<TH1D>(hname.str().c_str(), hname.str().c_str(), 247, edges10);
	    spectra[hname.str()]->Fill(q);
	}
	else
	{
	    hist->second->Fill(q);
	}

	hq->Fill(q);

	//std::cout << ped << q;
    }
}


// ------------ method called once each job just before starting event loop  ------------
void adcHists::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void adcHists::endJob() 
{
    for(int i = 1; i <= hq->GetNbinsX(); i++)
    {
	hq->SetBinContent(i, hq->GetBinContent(i)/hq->GetBinWidth(i));
    }

    for(auto& hist : spectra)
    {
	for(int i = 1; i <= hist.second->GetNbinsX(); i++)
	{
	    hist.second->SetBinContent(i, hist.second->GetBinContent(i)/hist.second->GetBinWidth(i));
	}
    }
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void adcHists::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(adcHists);
