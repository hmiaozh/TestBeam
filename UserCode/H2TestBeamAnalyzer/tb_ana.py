#!/usr/bin/env python

print "Importing modules"
import sys
import optparse
from tb_utils import *
import os
import ROOT
import array
import time
from math import exp, sqrt

#######################
# Get options
#######################

print "Getting options"

parser = optparse.OptionParser("usage: %prog [options]\
<input directory> \n")

parser.add_option ('--o', dest='outfile', type='string',
                   default = 'none',
                   help="output file")
parser.add_option ('--i', dest='infile', type='string',
                   default = 'none',
                   help="output directory")
parser.add_option ('--r', dest='runnum', type='int',
                   default = -1,
                   help="output directory")

parser.add_option ('--doRefTile', action="store_true",
                   dest="doRefTile", default=False)

options, args = parser.parse_args()

infile = options.infile
outfile = options.outfile
runnum = options.runnum
doRefTile = options.doRefTile

print "Setting ROOT options"
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
#ROOT.gStyle.SetOptStat(111111111)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetNdivisions(405,"x");
#ROOT.gStyle.SetEndErrorSize(0.)
#ROOT.gStyle.SetErrorX(0.001)

NCont = 255
#stops = [ 0.00, 0.02, 0.34, 0.51, 0.64, 1.00 ]
#red   = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51 ]
#green = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00 ]
#blue  = [ 1.00, 0.51, 1.00, 0.12, 0.00, 0.00 ]

#stops = [ 0.00, 0.34, 0.61, 0.84, 0.92, 1.00]
#red   = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51]
#green = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00]
#blue  = [ 0.00, 0.51, 1.00, 0.12, 0.00, 0.00]

stops  = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
red    = [ 0.00, 0.00, 0.87, 1.00, 0.51 ]
green  = [ 0.00, 0.81, 1.00, 0.20, 0.00 ]
blue   = [ 0.51, 1.00, 0.12, 0.00, 0.00 ]

NRGBs = len(stops)

stopsArray = array.array('d', stops)
redArray   = array.array('d', red)
greenArray = array.array('d', green)
blueArray  = array.array('d', blue)
ROOT.TColor.CreateGradientColorTable(NRGBs, stopsArray, redArray, greenArray, blueArray, NCont)
ROOT.gStyle.SetNumberContours(NCont)

###############
# Choose
################
# TS to sum
ts_list = [4,5,6,7]
# Number of standard deviations for WC residuals cut
sigma_thold = 1.
# Channel to use as reference tile counter, currently 2x10 SCSN-81
refchan = 22  
#refchan = 23
# Energy to require to TS4 sum in reference tile counter (depends on channel):
refE = {}
refE[22] = 150.
refE[23] = 30.
# Chamber to use for location
refchamb = "E"
#refchamb = "C"

# Wire chamber means and standard deviations (xA-xC, xA-xC, yA-yC, etc.)
wc_res = {}
wc_res["x", "BC", "mean"] = -5.83e-01
wc_res["y", "BC", "mean"] = -1.75e+01
wc_res["x", "AC", "mean"] = -1.24e+00
wc_res["y", "AC", "mean"] = -8.78e+00
wc_res["x", "BC", "rms" ] =  3.96e+00
wc_res["y", "BC", "rms" ] =  3.88e+00
wc_res["x", "AC", "rms" ] =  4.30e+00
wc_res["y", "AC", "rms" ] =  5.08e+00

wcList = ["A", "B", "C", "D", "E"]

adjust = {}
for iwc in wcList:
    for ixy in ["x", "y"]:
        for irun in runList:
            if ixy == "x" and iwc == "E":
                adjust[ixy, iwc, runnum] = -1.
            else:
                adjust[ixy, iwc, runnum] = 1.
    

file = ROOT.TFile(infile)
#ntp = file.Get("HFData/Events;3")
ntp = {}
ntp["hf"] = file.Get("HFData/Events")
ntp["wc"] = file.Get("WCData/Events")

vname = {}
vname["hf"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse"]
#vname["hf"] = ["numChs", "numTS", "iphi", "ieta", "depth"]
vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC", "xD", "yD", "xE", "yE"]
#vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC", "xD", "yD"]


ROOT.gROOT.ProcessLine("struct hf_struct {Int_t numChs; Int_t numTS; Int_t iphi[50]; Int_t ieta[50]; Int_t depth[50]; Double_t pulse[2400];};")
#ROOT.gROOT.ProcessLine("struct wc_struct {Int_t numChs; Int_t numTS; Int_t iphi[50]; Int_t ieta[50]; Int_t depth[50]; Double_t pulse[48][50];};") # Treat pulse like 1D array of length 48*50
shf = ROOT.hf_struct()
for ivname in vname["hf"]:
    ntp["hf"].SetBranchAddress(ivname, ROOT.AddressOf(shf, ivname))

vec = {}
for ivname in vname["wc"]:
    vec[ivname] = ROOT.vector("double")()
    ntp["wc"].SetBranchStatus (ivname, 1)
    ntp["wc"].SetBranchAddress(ivname, vec[ivname])
    

nevts    = ntp["hf"].GetEntries()
nevts_wc = ntp["wc"].GetEntries()
if nevts != nevts_wc:
    print "HF ntuple = ", nevts
    print "WC ntuple = ", nevts_wc
    print "Mismatch in event counts.  Exiting."
    #sys.exit()


wc_counts = {}
for ivname in vname["wc"]:
    for isize in range(20):
        wc_counts[ivname, isize] = 0.
for iwc in wcList:
    wc_counts[iwc] = 0.
wc_counts["AB"] = 0.
wc_counts["ABC"] = 0.
wc_counts["ABCD"] = 0.
wc_counts["ABCE"] = 0.
wc_counts["clean"] = 0.
wc_counts["passXBCp"] = 0.
wc_counts["passXBCm"] = 0.
wc_counts["passYBCp"] = 0.
wc_counts["passYBCm"] = 0.
wc_counts["passXACp"] = 0.
wc_counts["passXACm"] = 0.
wc_counts["passYACp"] = 0.
wc_counts["passYACm"] = 0.
wc_counts["badEnergy"] = 1.

    
for ichan in chanList:
    wc_counts["nIn", ichan] = 0.

####################################################
# Define histograms
####################################################
hist = {}
# Define wire chamber histograms
for ip0 in wcList:
    # 2D histos for x vs y in each chamber
    hist["x"+ip0+"_v_y"+ip0]          = ROOT.TH2F("h_x"+ip0+"_v_y"+ip0, "h_x"+ip0+"_v_y"+ip0, 
                                                  400, -100., 100., 400, -100., 100.)
    hist["x"+ip0+"_v_y"+ip0, "clean"] = ROOT.TH2F("h_x"+ip0+"_v_y"+ip0+"_clean", "h_x"+ip0+"_v_y"+ip0+"_clean", 
                                                  400, -100., 100., 400, -100., 100.)

    for ixy in ["x", "y"]:
        # 1D histos for x and y in all 4 chambers
        hist[ixy+ip0] = ROOT.TH1F("h_"+ixy+"_"+ip0, "h_"+ixy+"_"+ip0, 400, -100., 100.)
        hist[ixy+ip0, "clean"] = ROOT.TH1F("h_"+ixy+"_"+ip0+"_clean", "h_"+ixy+"_"+ip0+"_clean", 400, -100., 100.)
        # 2D histos for x and y correlations for all histo combinations
        
    for ip1 in wcList:
        if ((ip0 == "A" and ip1 == "B") or (ip0 == "A" and ip1 == "C") or (ip0 == "A" and ip1 == "D") or (ip0 == "A" and ip1 == "E") or 
            (ip0 == "B" and ip1 == "C") or (ip0 == "B" and ip1 == "D") or (ip0 == "B" and ip1 == "E") or
            (ip0 == "C" and ip1 == "D") or (ip0 == "C" and ip1 == "E") or
            (ip0 == "D" and ip1 == "E")):
            for ixy in ["x", "y"]:
                hist[ixy+ip0+"_v_"+ixy+ip1]          = ROOT.TH2F("h_"+ixy+"_"+ip0+"v"+ip1,
                                                                 "h_"+ixy+"_"+ip0+"v"+ip1, 
                                                                 400, -100., 100., 400, -100., 100.)
                hist[ixy+ip0+"_v_"+ixy+ip1, "clean"] = ROOT.TH2F("h_"+ixy+"_"+ip0+"v"+ip1+"_clean",
                                                                 "h_"+ixy+"_"+ip0+"v"+ip1+"_clean", 
                                                                 400, -100., 100., 400, -100., 100.)

hist["dx_BC"] = ROOT.TH1F("h_dx_BC", "h_dx_BC", 400, -100., 100.)
hist["dy_BC"] = ROOT.TH1F("h_dy_BC", "h_dy_BC", 400, -100., 100.)
hist["dx_AC"] = ROOT.TH1F("h_dx_AC", "h_dx_AC", 400, -100., 100.)
hist["dy_AC"] = ROOT.TH1F("h_dy_AC", "h_dy_AC", 400, -100., 100.)
hist["dx_AE"] = ROOT.TH1F("h_dx_AE", "h_dx_AE", 400, -100., 100.)
hist["dy_AE"] = ROOT.TH1F("h_dy_AE", "h_dy_AE", 400, -100., 100.)

hist["dx_BC", "clean"] = ROOT.TH1F("h_dx_BC_clean", "h_dx_BC_clean", 400, -100., 100.)
hist["dy_BC", "clean"] = ROOT.TH1F("h_dy_BC_clean", "h_dy_BC_clean", 400, -100., 100.)
hist["dx_AC", "clean"] = ROOT.TH1F("h_dx_AC_clean", "h_dx_AC_clean", 400, -100., 100.)
hist["dy_AC", "clean"] = ROOT.TH1F("h_dy_AC_clean", "h_dy_AC_clean", 400, -100., 100.)
hist["dx_AE", "clean"] = ROOT.TH1F("h_dx_AE_clean", "h_dx_AE_clean", 400, -100., 100.)
hist["dy_AE", "clean"] = ROOT.TH1F("h_dy_AE_clean", "h_dy_AE_clean", 400, -100., 100.)
                
for ichan in chanList:
    hist["avgpulse", ichan] = ROOT.TH1F("h_avgpulse_chan"+str(ichan), "h_avgpulse_chan"+str(ichan), 11, -0.5, 10.5)
    for its in range(11):
        hist["energy", ichan, its] = ROOT.TH1F("h_energy_chan"+str(ichan)+"_ts"+str(its), 
                                               "h_energy_chan"+str(ichan)+"_ts"+str(its), 300, 0., 3000.)

# Plot average 4TS energy sum (z-axis) in plane of track coords from WC C
for ichan in chanList:
    hist["e_wcC"  , ichan] = ROOT.TH2F("h_e_wcC_chan"+str(ichan)  , "h_e_wcC_chan"+str(ichan)  , 100 , -100., 100., 100, -100., 100.)
    hist["e_wcC_x", ichan] = ROOT.TH1F("h_e_wcC_x_chan"+str(ichan), "h_e_wcC_x_chan"+str(ichan), 400 , -100., 100.)
    hist["e_wcC_y", ichan] = ROOT.TH1F("h_e_wcC_y_chan"+str(ichan), "h_e_wcC_y_chan"+str(ichan), 400 , -100., 100.)
    hist["e_4TS"  , ichan] = ROOT.TH1F("h_e_4TS_chan"+str(ichan)  , "h_e_4TS_chan"+str(ichan)  , 4002,  -0.5, 2000.5)

    hist["e_4TS_withSCSN", ichan] = ROOT.TH1F("h_e_4TS_withSCSN_chan"+str(ichan), 
                                              "h_e_4TS_withSCSN_chan"+str(ichan), 
                                              4002,  -0.5, 2000.5)

esum = {}
for ichan in chanList:
    for its in range(50):
        esum[ichan, its] = 0.
        esum[ichan, its, "nevts"] = 0.
        
####################################################
# Event Loop
####################################################

#nevts = 10000    
print "Processing ", nevts, "total events."
for ievt in range(nevts):
    if ievt % 20000 == 0: print "Processing event ", ievt

    #######################
    # WC Analysis
    #######################
    ntp["wc"].GetEvent(ievt)

    # Count events with hits in each view of all WC
    # and determine cleaning
    ###############################################
    has = {}
    for ivname in vname["wc"]:
        has[ivname] = False
        isize = int(vec[ivname].size())
        wc_counts[ivname, isize] += 1.
        if isize == 1: has[ivname] = True

    for iwc in wcList:
        has[iwc] = has["x"+iwc] and has["y"+iwc]
        if has[iwc]: wc_counts[iwc] += 1.
    has["AB"]   = has["A"]   and has["B"]
    has["ABC"]  = has["AB"]  and has["C"]
    has["ABCD"] = has["ABC"] and has["D"]
    has["ABCE"] = has["ABC"] and has["E"]
    for iwc in ["AB", "ABC", "ABCD", "ABCE"]:
        if has[iwc]: wc_counts[iwc] += 1.

    clean = False
    if has["ABCE"]: 
        xA = vec["xA"].at(0); yA = vec["yA"].at(0)
        xB = vec["xB"].at(0); yB = vec["yB"].at(0)
        xC = vec["xC"].at(0); yC = vec["yC"].at(0)
        #xD = vec["xD"].at(0); yD = vec["yD"].at(0)
        xE = -1.*vec["xE"].at(0); yE = vec["yE"].at(0)
        
        hist["dx_BC"].Fill(xB-xC)
        hist["dy_BC"].Fill(yB-yC)
        hist["dx_AC"].Fill(xA-xC)
        hist["dy_AC"].Fill(yA-yC)
        hist["dx_AE"].Fill(xA-xE)
        hist["dy_AE"].Fill(yA-yE)

        passXBCp = False; passXBCm = False; passYBCp = False; passYBCm = False;
        passXACp = False; passXACm = False; passYACp = False; passYACm = False;
        
        if xB-xC < wc_res["x", "BC", "mean"]+sigma_thold*wc_res["x", "BC", "rms" ]: passXBCp = True
        if xB-xC > wc_res["x", "BC", "mean"]-sigma_thold*wc_res["x", "BC", "rms" ]: passXBCm = True
        if yB-yC < wc_res["y", "BC", "mean"]+sigma_thold*wc_res["y", "BC", "rms" ]: passYBCp = True
        if yB-yC > wc_res["y", "BC", "mean"]-sigma_thold*wc_res["y", "BC", "rms" ]: passYBCm = True
        if xA-xC < wc_res["x", "AC", "mean"]+sigma_thold*wc_res["x", "AC", "rms" ]: passXACp = True
        if xA-xC > wc_res["x", "AC", "mean"]-sigma_thold*wc_res["x", "AC", "rms" ]: passXACm = True
        if yA-yC < wc_res["y", "AC", "mean"]+sigma_thold*wc_res["y", "AC", "rms" ]: passYACp = True
        if yA-yC > wc_res["y", "AC", "mean"]-sigma_thold*wc_res["y", "AC", "rms" ]: passYACm = True

        if passXBCp: wc_counts["passXBCp"] += 1.
        if passXBCm: wc_counts["passXBCm"] += 1.
        if passYBCp: wc_counts["passYBCp"] += 1.
        if passYBCm: wc_counts["passYBCm"] += 1.
        if passXACp: wc_counts["passXACp"] += 1.
        if passXACm: wc_counts["passXACm"] += 1.
        if passYACp: wc_counts["passYACp"] += 1.
        if passYACm: wc_counts["passYACm"] += 1.

        if passXBCp and passXBCm and passYBCp and passYBCm and passXACp and passXACm and passYACp and passYACm:
            clean = True

            hist["dx_BC", "clean"].Fill(xB-xC)
            hist["dy_BC", "clean"].Fill(yB-yC)
            hist["dx_AC", "clean"].Fill(xA-xC)
            hist["dy_AC", "clean"].Fill(yA-yC)
            hist["dx_AE", "clean"].Fill(xA-xE)
            hist["dy_AE", "clean"].Fill(yA-yE)
        
        

    # Select events with straight tracks by requiring that 
    # events have one and only one x hit and 1-and-only-1 y hit in WC A, B, C, E
    # and events are within N standard deviations of xWC1 - xWC2 residuals
    if not clean: continue
    wc_counts["clean"] += 1.

    # Fill histograms
    ########################
    for iwc in wcList:
        if has[iwc]: 
            x = adjust["x", iwc, runnum]*vec["x"+iwc].at(0)
            y = adjust["y", iwc, runnum]*vec["y"+iwc].at(0)
            hist["x"+iwc+"_v_y"+iwc].Fill(x, y)   # x vs y within WC
            hist["x"+iwc]           .Fill(x) # x within WC
            hist["y"+iwc]           .Fill(y) # y within WC
            if clean: 
                hist["x"+iwc+"_v_y"+iwc, "clean"].Fill(x, y) # x vs y within WC
                hist["x"+iwc, "clean"]           .Fill(x) # x within WC
                hist["y"+iwc, "clean"]           .Fill(y) # y within WC

        for ip1 in wcList:
            if not has[iwc] or not has[ip1]: continue
            if ((iwc == "A" and ip1 == "B") or (iwc == "A" and ip1 == "C") or (iwc == "A" and ip1 == "D") or (iwc == "A" and ip1 == "E") or 
                (iwc == "B" and ip1 == "C") or (iwc == "B" and ip1 == "D") or (iwc == "B" and ip1 == "E") or
                (iwc == "C" and ip1 == "D") or (iwc == "C" and ip1 == "E") or
                (iwc == "D" and ip1 == "E")):
                
                for ixy in ["x", "y"]:
                    xy_iwc = adjust[ixy, iwc, runnum]*vec[ixy+iwc].at(0)
                    xy_ip1 = adjust[ixy, ip1, runnum]*vec[ixy+ip1].at(0)
                    
                    hist[ixy+iwc+"_v_"+ixy+ip1].Fill(xy_iwc, xy_ip1) # xWC1 vs xWC2 and yWC1 vs yWC2
                    if clean: hist[ixy+iwc+"_v_"+ixy+ip1, "clean"].Fill(xy_iwc, xy_ip1) # xWC1 vs xWC2 and yWC1 vs yWC2
                        

    # Check if beam is within edges of sample
    isIn = {}
    for ichan in chanList:
        xL = edges[ichan, runnum][0]
        xH = edges[ichan, runnum][1]
        yL = edges[ichan, runnum][2]
        yH = edges[ichan, runnum][3]
        ix = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
        iy = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
        if ix<xH and ix>xL and iy<yH and iy>yL: 
            isIn[ichan] = True
        else:
            isIn[ichan] = False
        if isIn[ichan]: wc_counts["nIn", ichan] += 1.
    
            
    #######################
    # QIE Analysis
    #######################
    ntp["hf"].GetEvent(ievt)

    # Find the channels 
    ########################
    chansToFind = []
    for ichan in chanList: chansToFind.append(chanmap[ichan])
    fchan = {}
    # ichan in root file coords
    for ichan in range(shf.numChs):
        test_chan = (shf.iphi[ichan], shf.ieta[ichan], shf.depth[ichan])
        if test_chan in chansToFind: 
            chansToFind.remove(test_chan)
            fchan[chanmap[test_chan]] = ichan
    if len(chansToFind) > 0: 
        print "Did not find channels"
        print chansToFind, "."
        print "Exiting."
        sys.exit()
        
    # Skip events with anomalously large pulses
    ################################################
    
    for ichan in chanList:
        jchan = fchan[ichan]
        for its in range(3):
            if shf.pulse[jchan*50+its] > 90: 
                clean = False
                break 
        for its in range(7,11):
            if shf.pulse[jchan*50+its] > 90: 
                clean = False
                break
            
    # Reject events with anomalous energy
    if not clean: continue
    for ichan in chanList:
        for its in range(11):
            if shf.pulse[jchan*50+its] > 1500: 
                clean = False
                break
    # Reject events with anomalous energy
    if not clean: continue
 
    # Plot energy
    ################################################
    # Get 4TS energy sum for later use
    for ichan in chanList:
        jchan = fchan[ichan]
        esum[ichan, "4TS"] = 0.
        for its in ts_list:
            esum[ichan, "4TS"] += shf.pulse[jchan*50+its]*calib[ichan] #[row][col] -> [row*n_cols + col]

    # Loop through again and fill other plots
    for ichan in chanList:
        jchan = fchan[ichan]

        # Decide whether to fill plot based on position of track ("isIn") and energ in SCSN reference ("esum")
        fillEplots = False
        if isIn[ichan] and not doRefTile: fillEplots = True
        elif doRefTile and isIn[ichan] and (esum[refchan, "4TS"]>refE[refchan] or ichan==refchan) : fillEplots = True

        # Fill pulse shape plot
        for its in range(11):
            esum[ichan, its] += shf.pulse[jchan*50+its]*calib[ichan]  #[row][col] -> [row*n_cols + col]
            esum[ichan, its, "nevts"] += 1.
            if fillEplots: hist["energy", ichan, its].Fill(shf.pulse[jchan*50+its]*calib[ichan])

        # Fill 4TS energy sum plot
        if fillEplots: hist["e_4TS", ichan].Fill(esum[ichan, "4TS"])
            
        # Fill plot of wire chamber position for events with sufficient energy
        if esum[ichan, "4TS"]>25.:
            x = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
            y = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
            hist["e_wcC"  , ichan].Fill(x,y)
            hist["e_wcC_x", ichan].Fill(x)
            hist["e_wcC_y", ichan].Fill(y)

for ichan in chanList:
    for its in range(11):
        #        print "ichan : its : E_sum = ", ichan, ":", its, ":", esum[ichan, its]/nevts
        hist["avgpulse", ichan].SetBinContent(its+1, esum[ichan, its]/esum[ichan, its, "nevts"])


print "Fraction of events with N hits in each WC view"
print "============================================================"
print "view : N hits : fraction"
for ivname in vname["wc"]:
    for isize in range(5):
        print "%2s : %1i : %5.2f" % (ivname, isize , wc_counts[ivname, isize]/nevts)
    print " "

print "Efficiency for requiring WC combinations in event"
print "============================================================"
for iwc in ["A","B", "C", "D", "E", "AB", "ABC", "ABCD", "ABCE"]:
    print "WC %4s : %5.2f" % (iwc, wc_counts[iwc]/nevts)

print " "
print " "
print "Track event cleaning efficiency for hitting each sample:"
print "============================================================"
print "WC quantity : efficiency "
print "x_BC_p : %5.2f " % (wc_counts["passXBCp"]/nevts)
print "x_BC_m : %5.2f " % (wc_counts["passXBCm"]/nevts)
print "y_BC_p : %5.2f " % (wc_counts["passYBCp"]/nevts)
print "y_BC_m : %5.2f " % (wc_counts["passYBCm"]/nevts)
print "x_AC_p : %5.2f " % (wc_counts["passXACp"]/nevts)
print "x_AC_m : %5.2f " % (wc_counts["passXACm"]/nevts)
print "y_AC_p : %5.2f " % (wc_counts["passYACp"]/nevts)
print "y_AC_m : %5.2f " % (wc_counts["passYACm"]/nevts)
print "Total  : %5.2f " % (   wc_counts["clean"]/nevts)
print " "
print " "
print "Geometric event cleaning efficiency for hitting each sample:"
print "============================================================"
print "Channel : description : efficiency for clean events : total efficiency"
for ichan in chanList:
    print "%3i : %30s : %5.2f : %5.2f" % (ichan, chanType[ichan, runnum], wc_counts["nIn", ichan]/wc_counts["clean"], wc_counts["nIn", ichan]/nevts)
    
if os.path.isfile(outfile):
    method = "update"
else:
    method = "recreate"        
outtfile = ROOT.TFile(outfile,method)
for hist in hist.values():
    outtfile.Delete(hist.GetName()+";*")
    hist.Write()
outtfile.Close()

