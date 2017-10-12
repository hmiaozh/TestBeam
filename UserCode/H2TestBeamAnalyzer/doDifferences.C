{

  //-------------------------------------------
  //
  //generate array of numbers
  //
  //-------------------------------------------

  TFile *f = new TFile("sampletest/tb_ele_sc_bin3.root","read");

  
  vector<TProfile*> v_p5;
  vector<TProfile*> v_p4;
  for (int i=0; i<50; i++) {
    char pname[10];
    char ppname[10];
    sprintf(ppname,"p5_%i",i);
    v_p5.push_back((TProfile*)f->Get(ppname));
    sprintf(pname,"p4_%i",i);
    v_p4.push_back((TProfile*)f->Get(pname));

  } 

  TFile *outputfile = new TFile("sampletest/Pulse_ele_sc_bin3.root","recreate");

  TH1D *dall = new TH1D("diff","differenced pulse shape",500,0,250); dall->Sumw2();
  TH1D *gall = new TH1D("raw","TDC-ordered pulse fractions",500,0,250); gall->Sumw2();
/*
  TProfile *norm_tdc5 = new TProfile("norm_tdc5","norm_tdc5",10,-0.5,9.5,"s");

  for(int i=0; i<4; i++){
    norm_tdc5->Fill(i,0);
  }

//  double sft = (v_p4.at(0)->GetBinContent(4+1))/(v_p5.at(0)->GetBinContent(5+1));
  double sft = 1.0 - v_p4.at(0)->GetBinContent(9+1);
  for(int i=4; i<10; i++){
    double hi = (v_p5.at(0)->GetBinContent(i+1))*sft;
    norm_tdc5->Fill(i,hi);
  }
*/

  double newerr[50][10] = {0};

  double leakage = (v_p4.at(0)->GetBinContent(9+1))/50.;
  double errleak = (v_p4.at(0)->GetBinError(9+1))/50;
  for(int i=0; i<50; i++){
    double sf = 1.0 - leakage * (double)i;
    v_p4.at(i)->Scale(sf);
    for(int j=0; j<10; j++){
	double errsf = sf*sf*(v_p4.at(i)->GetBinError(j+1))*(v_p4.at(i)->GetBinError(j+1)) + (v_p4.at(i)->GetBinContent(j+1))*(v_p4.at(i)->GetBinContent(j+1))*(errleak*i)*(errleak*i);
	newerr[i][j] = sqrt(errsf);
    }
  }

/*
double ns[51];

ns[0] = 0.000225834;
ns[1] = 0.000223759;
ns[2] = 0.000221712;
ns[3] = 0.000219692;
ns[4] = 0.0002177;
ns[5] = 0.000215734;
ns[6] = 0.000213793;
ns[7] = 0.000211879;
ns[8] = 0.000209989;
ns[9] = 0.000208125;
ns[10] = 0.000206284;
ns[11] = 0.000204468;
ns[12] = 0.000202674;
ns[13] = 0.000200904;
ns[14] = 0.000199157;
ns[15] = 0.000197432;
ns[16] = 0.000195729;
ns[17] = 0.000194047;
ns[18] = 0.000192387;
ns[19] = 0.000190747;
ns[20] = 0.000189128;
ns[21] = 0.000187529;
ns[22] = 0.00018595;
ns[23] = 0.000184391;
ns[24] = 0.00018285;
ns[25] = 0.000181329;
ns[26] = 0.000179826;
ns[27] = 0.000178342;
ns[28] = 0.000176875;
ns[29] = 0.000175426;
ns[30] = 0.000173995;
ns[31] = 0.000172581;
ns[32] = 0.000171183;
ns[33] = 0.000169803;
ns[34] = 0.000168439;
ns[35] = 0.00016709;
ns[36] = 0.000165758;
ns[37] = 0.000164441;
ns[38] = 0.00016314;
ns[39] = 0.000161854;
ns[40] = 0.000160583;
ns[41] = 0.000159326;
ns[42] = 0.000158084;
ns[43] = 0.000156856;
ns[44] = 0.000155642;
ns[45] = 0.000154442;
ns[46] = 0.000153256;
ns[47] = 0.000152083;
ns[48] = 0.000150923;
ns[49] = 0.000149776;

  double bin9 = v_p4.at(0)->GetBinContent(9+1);
  double sumtail = 0;
  for(int i=1; i<51; i++){
    sumtail += ns[i];
  }
  double leakage = 0;
  for(int i=0; i<50; i++){
    leakage += ns[50-i];
    double sf = 1.0 - leakage/sumtail * bin9;
    v_p4.at(i)->Scale(sf);
  }
*/

  for (int i=0; i<50; i++) {

    gall->SetBinContent(i+1,     v_p4.at(49-i)->GetBinContent(0+1));
    gall->SetBinContent(i+1+50,  v_p4.at(49-i)->GetBinContent(1+1));
    gall->SetBinContent(i+1+100, v_p4.at(49-i)->GetBinContent(2+1));
    gall->SetBinContent(i+1+150, v_p4.at(49-i)->GetBinContent(3+1));
    gall->SetBinContent(i+1+200, v_p4.at(49-i)->GetBinContent(4+1));
    gall->SetBinContent(i+1+250, v_p4.at(49-i)->GetBinContent(5+1));
    gall->SetBinContent(i+1+300, v_p4.at(49-i)->GetBinContent(6+1));
    gall->SetBinContent(i+1+350, v_p4.at(49-i)->GetBinContent(7+1));
    gall->SetBinContent(i+1+400, v_p4.at(49-i)->GetBinContent(8+1));
    gall->SetBinContent(i+1+450, v_p4.at(49-i)->GetBinContent(9+1));

/*
    gall->SetBinError(i+1,     v_p4.at(49-i)->GetBinError(0+1));
    gall->SetBinError(i+1+50,  v_p4.at(49-i)->GetBinError(1+1));
    gall->SetBinError(i+1+100, v_p4.at(49-i)->GetBinError(2+1));
    gall->SetBinError(i+1+150, v_p4.at(49-i)->GetBinError(3+1));
    gall->SetBinError(i+1+200, v_p4.at(49-i)->GetBinError(4+1));
    gall->SetBinError(i+1+250, v_p4.at(49-i)->GetBinError(5+1));
    gall->SetBinError(i+1+300, v_p4.at(49-i)->GetBinError(6+1));
    gall->SetBinError(i+1+350, v_p4.at(49-i)->GetBinError(7+1));
    gall->SetBinError(i+1+400, v_p4.at(49-i)->GetBinError(8+1));
    gall->SetBinError(i+1+450, v_p4.at(49-i)->GetBinError(9+1));
*/

    gall->SetBinError(i+1,     newerr[49-i][0]);
    gall->SetBinError(i+1+50,  newerr[49-i][1]);
    gall->SetBinError(i+1+100, newerr[49-i][2]);
    gall->SetBinError(i+1+150, newerr[49-i][3]);
    gall->SetBinError(i+1+200, newerr[49-i][4]);
    gall->SetBinError(i+1+250, newerr[49-i][5]);
    gall->SetBinError(i+1+300, newerr[49-i][6]);
    gall->SetBinError(i+1+350, newerr[49-i][7]);
    gall->SetBinError(i+1+400, newerr[49-i][8]);
    gall->SetBinError(i+1+450, newerr[49-i][9]);


  }


  for (int i=1; i<500; i++) {
    double temp=gall->GetBinContent(i+1)-gall->GetBinContent(i);
    double terror = gall->GetBinError(i+1)*gall->GetBinError(i+1) + gall->GetBinError(i)*gall->GetBinError(i);
    if (i+1-50>0) {temp+=dall->GetBinContent(i+1-50);
    	terror += dall->GetBinError(i+1-50)*dall->GetBinError(i+1-50);
    }
    dall->SetBinContent(i+1,temp);
    dall->SetBinError(i+1, sqrt(terror));
  }

  gall->Rebin(2);
  gall->Scale(0.5);

  dall->Rebin(2);
  dall->Scale(0.5);

  outputfile->Write();
  outputfile->Close();

}
