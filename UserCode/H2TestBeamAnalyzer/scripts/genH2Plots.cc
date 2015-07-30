




#define NUMPHIS 3
#define NUMETAS 13
#define NUMDEPTHS 2

struct TCalibLedInfo
{
	int numChs;
	int iphi[50];
	int ieta[50];
	int cBoxChannel[50];
	vector<string> *cBoxString;
	int nTS[50];
	double pulse[50][10];
};

struct THFInfo
{
	int numChs;
	int numTS;
	int iphi[2000];
	int ieta[2000];
	int depth[2000];
	double pulse[2000][50];
};

struct H2Triggers
{
	int ped;
	int led;
	int laser;
	int beam;
};

struct H2MapChannel
{
	int i;
	int crate;
	int slot;
	char topBottom;
	int dcc;
	int spigot;
	int fiber;
	int fiberCh;
	string subDet;
	int ieta;
	int iphi;
	int depth;
};

vector<double> *wcX[5];
vector<double> *wcY[5];

void genH2Plots(int verb, string inFileName, string outFileName)
{
	TCalibLedInfo calibInfo;
	THFInfo hfInfo;
	H2Triggers triggers;

	TFile *in = new TFile(inFileName.c_str());

	in->cd("HFData");
	TTree *treeHF = (TTree*)gDirectory->Get("Events");
	treeHF->SetBranchAddress("numChs", &hfInfo.numChs);
	treeHF->SetBranchAddress("numTS", &hfInfo.numTS);
	treeHF->SetBranchAddress("iphi", &hfInfo.iphi);
	treeHF->SetBranchAddress("ieta", &hfInfo.ieta);
	treeHF->SetBranchAddress("depth", &hfInfo.depth);
	treeHF->SetBranchAddress("pulse", hfInfo.pulse);

	in->cd("Triggers");
	TTree *treeTriggers = (TTree*)gDirectory->Get("Events");
	treeTriggers->SetBranchAddress("ped", &triggers.ped);
	treeTriggers->SetBranchAddress("led", &triggers.led);
	treeTriggers->SetBranchAddress("beam", &triggers.beam);

	in->cd("WCData");
	TTree *treeWC = (TTree*)gDirectory->Get("Events");
	treeWC->SetBranchAddress("xA", &(wcX[0]));
	treeWC->SetBranchAddress("yA", &(wcY[0]));
	treeWC->SetBranchAddress("xB", &(wcX[1]));
	treeWC->SetBranchAddress("yB", &(wcY[1]));
	treeWC->SetBranchAddress("xC", &(wcX[2]));
	treeWC->SetBranchAddress("yC", &(wcY[2]));
	treeWC->SetBranchAddress("xD", &(wcX[3]));
	treeWC->SetBranchAddress("yD", &(wcY[3]));
	treeWC->SetBranchAddress("xE", &(wcX[4]));
	treeWC->SetBranchAddress("yE", &(wcY[4]));

	TFile *out = new TFile(outFileName.c_str(), "recreate");
	out->mkdir("Histos");
	out->mkdir("AvgPulses");
	out->mkdir("XY");
	TH1D *hSignal[NUMPHIS][NUMETAS][NUMDEPTHS];
	TProfile *pSignalPulses[NUMPHIS][NUMETAS][NUMDEPTHS];
	TH2D *hXY[5];
	char wcNames[5] = {'A', 'B', 'C', 'D', 'E'};
	out->cd("XY");
	char nameXY[200];
	for (int i=0; i<5; i++)
	{
		sprintf(nameXY, "XY%c", wcNames[i]);
		hXY[i] = new TH2D(nameXY, nameXY, 10000, -100, 100, 10000, -100, 100);
	}

	char histName[200];
	for (int iiphi=0; iiphi<NUMPHIS; iiphi++)
	{
		for (int iieta=0; iieta<NUMETAS; iieta++)
		{
			for (int idepth=0; idepth<NUMDEPTHS; idepth++)
			{
				out->cd("Histos");
				sprintf(histName, "Signal_IPHI%d_IETA%d_D%d",
						2*iiphi+1, iieta+29, idepth+1);
				hSignal[iiphi][iieta][idepth] = new TH1D(
						histName, histName, 5000, 0, 1000);

				out->cd("AvgPulses");
				sprintf(histName, "SignalAvgPulse_IPHI%d_IETA%d_D%d",
						2*iiphi+1, iieta+29, idepth+1);
				pSignalPulses[iiphi][iieta][idepth] = new TProfile(
						histName, histName, 30, 0, 30);
			}
		}
	}

	cout << "### Starting the Analysis..." << endl;
	int numEvents = treeHF->GetEntries();
	cout << "### Total Number of Events=" << numEvents << endl;
	for (int iEvent=0; iEvent<numEvents; iEvent++)
	{
		treeHF->GetEntry(iEvent);
		treeTriggers->GetEntry(iEvent);
		treeWC->GetEntry(iEvent);

		//
		//	Fill Wire Chambers XY Profiles
		//
		for (int i=0; i<5; i++)
		{
			double xx = wcX[0]->at(0);
			double yy = wcY[0]->at(0);
			hXY[i]->Fill(xx, yy);
		}

		if (iEvent%1000==0)
			cout << "### Event=" << iEvent << endl;

		if (triggers.ped==1 && verb>1)
		{
			cout << "### PED Trigger..." << endl
				<< "beamtrigger=" << triggers.beam << endl;
			continue;
		}

		for (int iCh=0; iCh<hfInfo.numChs; iCh++)
		{
			int iphi = hfInfo.iphi[iCh];
			int ieta = hfInfo.ieta[iCh];
			int depth = hfInfo.depth[iCh];
			int iiphi = (iphi-1)/2;
			int iieta = ieta-29;
			int idepth = depth-1;

			Double_t totSigSum = 0;
			if (verb>1 && iEvent<=10)
				cout << "### Digi->Pulse: " << iphi << "  " << ieta << "  "
					<< depth << endl;
			for (int iTS=0; iTS<hfInfo.numTS; iTS++)
			{
				totSigSum += hfInfo.pulse[iCh][iTS];
				pSignalPulses[iiphi][iieta][idepth]->Fill(iTS, 
						hfInfo.pulse[iCh][iTS]);

				if (verb>1 && iEvent<=10)
					cout << hfInfo.pulse[iCh][iTS] << "  ";
			}
			if (verb>1 && iEvent<=10)
				cout << endl;
			hSignal[iiphi][iieta][idepth]->Fill(totSigSum);
		}
	}

	out->Write();
	out->Close();

	return;
}
















