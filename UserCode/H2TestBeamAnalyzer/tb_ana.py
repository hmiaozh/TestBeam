#!/usr/bin/env python

print "Importing modules"
import sys
import optparse
from tb_utils import *
from tb_chanmap import *
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
ntp["hbhe"] = file.Get("HBHEData/Events")
ntp["hf"] = file.Get("HFData/Events")
ntp["wc"] = file.Get("WCData/Events")

vname = {}
vname["hbhe"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse"]
vname["hf"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse"]
#vname["hf"] = ["numChs", "numTS", "iphi", "ieta", "depth"]
vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC", "xD", "yD", "xE", "yE"]
#vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC", "xD", "yD"]


ROOT.gROOT.ProcessLine("struct hbhe_struct {Int_t numChs; Int_t numTS; Int_t iphi[120]; Int_t ieta[120]; Int_t depth[120]; Double_t pulse[6000];};")
shbhe = ROOT.hbhe_struct()
for ivname in vname["hbhe"]:
    ntp["hbhe"].SetBranchAddress(ivname, ROOT.AddressOf(shbhe, ivname))

ROOT.gROOT.ProcessLine("struct hf_struct {Int_t numChs; Int_t numTS; Int_t iphi[120]; Int_t ieta[120]; Int_t depth[120]; Double_t pulse[6000];};")  # Treat pulse like 1D array of length 120*50
shf = ROOT.hf_struct()
for ivname in vname["hf"]:
    ntp["hf"].SetBranchAddress(ivname, ROOT.AddressOf(shf, ivname))

vec = {}
for ivname in vname["wc"]:
    vec[ivname] = ROOT.vector("double")()
    ntp["wc"].SetBranchStatus (ivname, 1)
    ntp["wc"].SetBranchAddress(ivname, vec[ivname])
    

nevts    = ntp["hbhe"].GetEntries()
nevts_wc = ntp["wc"].GetEntries()
if nevts != nevts_wc:
    print "HBHE ntuple = ", nevts
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
#for ip0 in wcList:
#    # 2D histos for x vs y in each chamber
#    hist["x"+ip0+"_v_y"+ip0]          = ROOT.TH2F("h_x"+ip0+"_v_y"+ip0, "h_x"+ip0+"_v_y"+ip0, 
#                                                  400, -100., 100., 400, -100., 100.)
#    hist["x"+ip0+"_v_y"+ip0, "clean"] = ROOT.TH2F("h_x"+ip0+"_v_y"+ip0+"_clean", "h_x"+ip0+"_v_y"+ip0+"_clean", 
#                                                  400, -100., 100., 400, -100., 100.)
#
#    for ixy in ["x", "y"]:
#        # 1D histos for x and y in all 4 chambers
#        hist[ixy+ip0] = ROOT.TH1F("h_"+ixy+"_"+ip0, "h_"+ixy+"_"+ip0, 400, -100., 100.)
#        hist[ixy+ip0, "clean"] = ROOT.TH1F("h_"+ixy+"_"+ip0+"_clean", "h_"+ixy+"_"+ip0+"_clean", 400, -100., 100.)
#        # 2D histos for x and y correlations for all histo combinations
#        
#    for ip1 in wcList:
#        if ((ip0 == "A" and ip1 == "B") or (ip0 == "A" and ip1 == "C") or (ip0 == "A" and ip1 == "D") or (ip0 == "A" and ip1 == "E") or 
#            (ip0 == "B" and ip1 == "C") or (ip0 == "B" and ip1 == "D") or (ip0 == "B" and ip1 == "E") or
#            (ip0 == "C" and ip1 == "D") or (ip0 == "C" and ip1 == "E") or
#            (ip0 == "D" and ip1 == "E")):
#            for ixy in ["x", "y"]:
#                hist[ixy+ip0+"_v_"+ixy+ip1]          = ROOT.TH2F("h_"+ixy+"_"+ip0+"v"+ip1,
#                                                                 "h_"+ixy+"_"+ip0+"v"+ip1, 
#                                                                 400, -100., 100., 400, -100., 100.)
#                hist[ixy+ip0+"_v_"+ixy+ip1, "clean"] = ROOT.TH2F("h_"+ixy+"_"+ip0+"v"+ip1+"_clean",
#                                                                 "h_"+ixy+"_"+ip0+"v"+ip1+"_clean", 
#                                                                 400, -100., 100., 400, -100., 100.)
#
#hist["dx_BC"] = ROOT.TH1F("h_dx_BC", "h_dx_BC", 400, -100., 100.)
#hist["dy_BC"] = ROOT.TH1F("h_dy_BC", "h_dy_BC", 400, -100., 100.)
#hist["dx_AC"] = ROOT.TH1F("h_dx_AC", "h_dx_AC", 400, -100., 100.)
#hist["dy_AC"] = ROOT.TH1F("h_dy_AC", "h_dy_AC", 400, -100., 100.)
#hist["dx_AE"] = ROOT.TH1F("h_dx_AE", "h_dx_AE", 400, -100., 100.)
#hist["dy_AE"] = ROOT.TH1F("h_dy_AE", "h_dy_AE", 400, -100., 100.)
#
#hist["dx_BC", "clean"] = ROOT.TH1F("h_dx_BC_clean", "h_dx_BC_clean", 400, -100., 100.)
#hist["dy_BC", "clean"] = ROOT.TH1F("h_dy_BC_clean", "h_dy_BC_clean", 400, -100., 100.)
#hist["dx_AC", "clean"] = ROOT.TH1F("h_dx_AC_clean", "h_dx_AC_clean", 400, -100., 100.)
#hist["dy_AC", "clean"] = ROOT.TH1F("h_dy_AC_clean", "h_dy_AC_clean", 400, -100., 100.)
#hist["dx_AE", "clean"] = ROOT.TH1F("h_dx_AE_clean", "h_dx_AE_clean", 400, -100., 100.)
#hist["dy_AE", "clean"] = ROOT.TH1F("h_dy_AE_clean", "h_dy_AE_clean", 400, -100., 100.)

for ichan in chanList:
    ieta = chanmap[ichan][0]
    iphi = chanmap[ichan][1]
    depth = chanmap[ichan][2]
    label = "ieta" + str(ieta) + "_iphi" + str(iphi) + "_depth" + str(depth)
    hist["avgpulse", ichan] = ROOT.TProfile("AvgPulse_"+label, "AvgPulse_"+label, 10, -0.5, 9.5, 0., 500.)
    for its in range(10):
        hist["charge", ichan, its] = ROOT.TH1F("Charge_"+label+"_ts"+str(its),
                                               "Charge_"+label+"_ts"+str(its), 1500, 0., 1500.)

    hist["e_4TS_noPS", ichan] = ROOT.TH1F("Energy_noPS_"+label,"Energy_noPS_"+label, 1000, 0., 1000.)                                          
    hist["e_4TS_PS", ichan] = ROOT.TH1F("Energy_"+label,"Energy_"+label, 1000, 0., 1000.)                                          

for depth in [1,2,3]:
    hist["e_4TS_etaphi",depth] = ROOT.TProfile2D("Energy_Avg_depth"+str(depth),"Average Energy per event in each ieta,iphi for depth "+str(depth), 16, 14.5, 30.5, 16, 1.5, 17.5, 0., 500.)
    hist["occupancy_event_etaphi",depth] = ROOT.TH2F("Occ_Event_depth_"+str(depth),"Fraction of Events with a hit in each ieta,iphi for depth "+str(depth), 16, 14.5, 30.5, 16, 1.5, 17.5) 

# Plot average 4TS energy sum (z-axis) in plane of track coords from WC C
#for ichan in chanList:
#    hist["e_wcC"  , ichan] = ROOT.TH2F("h_e_wcC_chan"+str(chanmap[ichan])  , "h_e_wcC_chan"+str(chanmap[ichan])  , 100 , -100., 100., 100, -100., 100.)
#    hist["e_wcC_x", ichan] = ROOT.TH1F("h_e_wcC_x_chan"+str(chanmap[ichan]), "h_e_wcC_x_chan"+str(chanmap[ichan]), 400 , -100., 100.)
#    hist["e_wcC_y", ichan] = ROOT.TH1F("h_e_wcC_y_chan"+str(chanmap[ichan]), "h_e_wcC_y_chan"+str(chanmap[ichan]), 400 , -100., 100.)
#    hist["e_4TS"  , ichan] = ROOT.TH1F("h_e_4TS_chan"+str(chanmap[ichan])  , "h_e_4TS_chan"+str(chanmap[ichan])  , 4002,  -0.5, 2000.5)
#
#    hist["e_4TS_withSCSN", ichan] = ROOT.TH1F("h_e_4TS_withSCSN_chan"+str(chanmap[ichan]),
#                                              "h_e_4TS_withSCSN_chan"+str(chanmap[ichan]),
#                                              4002,  -0.5, 2000.5)

esum = {}
        
####################################################
# Event Loop
####################################################

fillEplots = True

print "Run %5i has %7i total events. " % (runnum, nevts)
#nevts = 1000 #use to limit the number of events for diagnostic purposes
print "Processing ",nevts," events."    
for ievt in xrange(nevts):
    if (ievt+1) % 1000 == 0: print "Processing Run %5i Event %7i" % (runnum, (ievt+1))

#    #######################
#    # WC Analysis
#    #######################
#    ntp["wc"].GetEvent(ievt)
#
#    # Count events with hits in each view of all WC
#    # and determine cleaning
#    ###############################################
#    has = {}
#    for ivname in vname["wc"]:
#        has[ivname] = False
#        isize = int(vec[ivname].size())
#        wc_counts[ivname, isize] += 1.
#        if isize == 1: has[ivname] = True
#
#    for iwc in wcList:
#        has[iwc] = has["x"+iwc] and has["y"+iwc]
#        if has[iwc]: wc_counts[iwc] += 1.
#    has["AB"]   = has["A"]   and has["B"]
#    has["ABC"]  = has["AB"]  and has["C"]
#    has["ABCD"] = has["ABC"] and has["D"]
#    has["ABCE"] = has["ABC"] and has["E"]
#    for iwc in ["AB", "ABC", "ABCD", "ABCE"]:
#        if has[iwc]: wc_counts[iwc] += 1.
#
#    clean = False
#    if has["ABCE"]: 
#        xA = vec["xA"].at(0); yA = vec["yA"].at(0)
#        xB = vec["xB"].at(0); yB = vec["yB"].at(0)
#        xC = vec["xC"].at(0); yC = vec["yC"].at(0)
#        #xD = vec["xD"].at(0); yD = vec["yD"].at(0)
#        xE = -1.*vec["xE"].at(0); yE = vec["yE"].at(0)
#        
#        hist["dx_BC"].Fill(xB-xC)
#        hist["dy_BC"].Fill(yB-yC)
#        hist["dx_AC"].Fill(xA-xC)
#        hist["dy_AC"].Fill(yA-yC)
#        hist["dx_AE"].Fill(xA-xE)
#        hist["dy_AE"].Fill(yA-yE)
#
#        passXBCp = False; passXBCm = False; passYBCp = False; passYBCm = False;
#        passXACp = False; passXACm = False; passYACp = False; passYACm = False;
#        
#        if xB-xC < wc_res["x", "BC", "mean"]+sigma_thold*wc_res["x", "BC", "rms" ]: passXBCp = True
#        if xB-xC > wc_res["x", "BC", "mean"]-sigma_thold*wc_res["x", "BC", "rms" ]: passXBCm = True
#        if yB-yC < wc_res["y", "BC", "mean"]+sigma_thold*wc_res["y", "BC", "rms" ]: passYBCp = True
#        if yB-yC > wc_res["y", "BC", "mean"]-sigma_thold*wc_res["y", "BC", "rms" ]: passYBCm = True
#        if xA-xC < wc_res["x", "AC", "mean"]+sigma_thold*wc_res["x", "AC", "rms" ]: passXACp = True
#        if xA-xC > wc_res["x", "AC", "mean"]-sigma_thold*wc_res["x", "AC", "rms" ]: passXACm = True
#        if yA-yC < wc_res["y", "AC", "mean"]+sigma_thold*wc_res["y", "AC", "rms" ]: passYACp = True
#        if yA-yC > wc_res["y", "AC", "mean"]-sigma_thold*wc_res["y", "AC", "rms" ]: passYACm = True
#
#        if passXBCp: wc_counts["passXBCp"] += 1.
#        if passXBCm: wc_counts["passXBCm"] += 1.
#        if passYBCp: wc_counts["passYBCp"] += 1.
#        if passYBCm: wc_counts["passYBCm"] += 1.
#        if passXACp: wc_counts["passXACp"] += 1.
#        if passXACm: wc_counts["passXACm"] += 1.
#        if passYACp: wc_counts["passYACp"] += 1.
#        if passYACm: wc_counts["passYACm"] += 1.
#
#        if passXBCp and passXBCm and passYBCp and passYBCm and passXACp and passXACm and passYACp and passYACm:
#            clean = True
#
#            hist["dx_BC", "clean"].Fill(xB-xC)
#            hist["dy_BC", "clean"].Fill(yB-yC)
#            hist["dx_AC", "clean"].Fill(xA-xC)
#            hist["dy_AC", "clean"].Fill(yA-yC)
#            hist["dx_AE", "clean"].Fill(xA-xE)
#            hist["dy_AE", "clean"].Fill(yA-yE)
#        


    # Select events with straight tracks by requiring that 
    # events have one and only one x hit and 1-and-only-1 y hit in WC A, B, C, E
    # and events are within N standard deviations of xWC1 - xWC2 residuals

#if not clean: continue
#    wc_counts["clean"] += 1.

#    # Fill histograms
#    ########################
#    for iwc in wcList:
#        if has[iwc]: 
#            x = adjust["x", iwc, runnum]*vec["x"+iwc].at(0)
#            y = adjust["y", iwc, runnum]*vec["y"+iwc].at(0)
#            hist["x"+iwc+"_v_y"+iwc].Fill(x, y)   # x vs y within WC
#            hist["x"+iwc]           .Fill(x) # x within WC
#            hist["y"+iwc]           .Fill(y) # y within WC
#            if clean: 
#                hist["x"+iwc+"_v_y"+iwc, "clean"].Fill(x, y) # x vs y within WC
#                hist["x"+iwc, "clean"]           .Fill(x) # x within WC
#                hist["y"+iwc, "clean"]           .Fill(y) # y within WC
#
#        for ip1 in wcList:
#            if not has[iwc] or not has[ip1]: continue
#            if ((iwc == "A" and ip1 == "B") or (iwc == "A" and ip1 == "C") or (iwc == "A" and ip1 == "D") or (iwc == "A" and ip1 == "E") or 
#                (iwc == "B" and ip1 == "C") or (iwc == "B" and ip1 == "D") or (iwc == "B" and ip1 == "E") or
#                (iwc == "C" and ip1 == "D") or (iwc == "C" and ip1 == "E") or
#                (iwc == "D" and ip1 == "E")):
#                
#                for ixy in ["x", "y"]:
#                    xy_iwc = adjust[ixy, iwc, runnum]*vec[ixy+iwc].at(0)
#                    xy_ip1 = adjust[ixy, ip1, runnum]*vec[ixy+ip1].at(0)
#                    
#                    hist[ixy+iwc+"_v_"+ixy+ip1].Fill(xy_iwc, xy_ip1) # xWC1 vs xWC2 and yWC1 vs yWC2
#                    if clean: hist[ixy+iwc+"_v_"+ixy+ip1, "clean"].Fill(xy_iwc, xy_ip1) # xWC1 vs xWC2 and yWC1 vs yWC2
#                        
#
#    # Check if beam is within edges of sample
#    isIn = {}
#    for ichan in chanList:
#        xL = edges[ichan, runnum][0]
#        xH = edges[ichan, runnum][1]
#        yL = edges[ichan, runnum][2]
#        yH = edges[ichan, runnum][3]
#        ix = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
#        iy = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
#        if ix<xH and ix>xL and iy<yH and iy>yL: 
#            isIn[ichan] = True
#        else:
#            isIn[ichan] = False
#        if isIn[ichan]: wc_counts["nIn", ichan] += 1.



    #######################
    # QIE Analysis
    #######################
    ntp["hbhe"].GetEvent(ievt)

    # Find the channels 
    ########################
    
    # ichan is the channel number (a single integer index) defined in tb_chanmap.py
    # corresponding to a specific ieta,iphi,depth.
    #
    # chanList contains a list of the channel numbers to process.
    
    # create chansToFind, a list of [(ieta1,iphi1,depth1), (ieta2,iphi2,depth2), ...]
    # for processing
    
    chansToFind = []
    for ichan in chanList: chansToFind.append(chanmap[ichan])
    
    # rchan is the channel number associated with (ieta,iphi,depth) in the data
    # rchan probably doesn't equal ichan, which is just an index

    # By matching (ieta,iphi,depth), we create a mapping of fchan[ichan] = rchan
    # fchan contains the found channels    
            
    fchan = {}
    for rchan in range(shbhe.numChs):
        test_chan = (shbhe.ieta[rchan], shbhe.iphi[rchan], shbhe.depth[rchan])
        if test_chan in chansToFind:
            chansToFind.remove(test_chan)
            fchan[chanmap[test_chan]] = rchan
    
    # these are the (ieta,iphi,depth) that we expected to find
    # (from chanList/chanmap) that never appeared in the data
    
    if len(chansToFind) > 0:
        print "Did not find channels"
        print chansToFind, "."
        #print "Exiting."
        #sys.exit()
        
    # Skip events with anomalously large pulses
    clean = True
    for rchan in fchan.itervalues():
        for its in range(2): #for now, only check lowest two ts (0-1)
            if shbhe.pulse[rchan*50+its] > 90:
                clean = False
                break
        #for its in range(8,10): #for now, only check highest two ts (8-9)
        #    if shbhe.pulse[rchan*50+its] > 90: 
        #        clean = False
        #        break
    if not clean: continue

    # Skip events with anomalous energy
    for rchan in fchan.itervalues():
        for its in range(10):  #ts (0-9)
            if shbhe.pulse[rchan*50+its] > 1500:
                clean = False
                break
    if not clean: continue


    charge = {} 
    energy = {}   
    
    for ichan,rchan in fchan.items():
        
        # Pull charges and energies for each time sample
        for its in range(10):
            charge[ichan,its] = shbhe.pulse[rchan*50+its]  #[row][col] -> [row*n_cols + col]
            energy[ichan,its] = charge[ichan,its]*calib[ichan]

        ped_ts_list = [0,1,2]   #time samples in which to sum charge for pedestals (0-2)    
        ped_esum = 0.
        for its in ped_ts_list:   
            ped_esum += energy[ichan,its]
        ped_avg = ped_esum/len(ped_ts_list)    
        esum[ichan, "PED"] = ped_avg

        ts_list = [4,5,6,7]   #time samples in which to sum charge for signal (4-7)
        sig_esum = 0.
        sig_esum_ps = 0.
        for its in ts_list:  
            sig_esum += energy[ichan,its]
            sig_esum_ps += energy[ichan,its]-ped_avg  #pedestal-subtracted energy  
        esum[ichan, "4TS_noPS"] = sig_esum
        esum[ichan, "4TS_PS"] = sig_esum_ps          

        # Fill pulse shape plot
        if fillEplots: 
            for its in range(10):
                hist["avgpulse", ichan].Fill(its,energy[ichan,its])

        if fillEplots: 
            for its in range(10):
                hist["charge", ichan, its].Fill(charge[ichan,its])

        # Fill 4TS energy sum plot
        if fillEplots: hist["e_4TS_noPS", ichan].Fill(esum[ichan, "4TS_noPS"])

        # Fill 4TS pedestal-corrected energy sum plot
        if fillEplots: hist["e_4TS_PS", ichan].Fill(esum[ichan, "4TS_PS"])
                
        # Fill energy profile in ieta, iphi
        if fillEplots:            
            ieta = chanmap[ichan][0]
            iphi = chanmap[ichan][1]
            depth = chanmap[ichan][2]
            hist["e_4TS_etaphi", depth].Fill(ieta, iphi, esum[ichan, "4TS_PS"])
            hist["occupancy_event_etaphi", depth].Fill(ieta,iphi,1./nevts)  #a bit ugly
                                                                                                                                                                
            # Fill plot of wire chamber position for events with sufficient energy
    #        if esum[ichan, "4TS"]>25.:
    #            x = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
    #            y = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
    #            hist["e_wcC"  , ichan].Fill(x,y)
    #            hist["e_wcC_x", ichan].Fill(x)
    #            hist["e_wcC_y", ichan].Fill(y)

#
#print "Fraction of events with N hits in each WC view"
#print "============================================================"
#print "view : N hits : fraction"
#for ivname in vname["wc"]:
#    for isize in range(5):
#        print "%2s : %1i : %5.2f" % (ivname, isize , wc_counts[ivname, isize]/nevts)
#    print " "
#
#print "Efficiency for requiring WC combinations in event"
#print "============================================================"
#for iwc in ["A","B", "C", "D", "E", "AB", "ABC", "ABCD", "ABCE"]:
#    print "WC %4s : %5.2f" % (iwc, wc_counts[iwc]/nevts)
#
#print " "
#print " "
#print "Track event cleaning efficiency for hitting each sample:"
#print "============================================================"
#print "WC quantity : efficiency "
#print "x_BC_p : %5.2f " % (wc_counts["passXBCp"]/nevts)
#print "x_BC_m : %5.2f " % (wc_counts["passXBCm"]/nevts)
#print "y_BC_p : %5.2f " % (wc_counts["passYBCp"]/nevts)
#print "y_BC_m : %5.2f " % (wc_counts["passYBCm"]/nevts)
#print "x_AC_p : %5.2f " % (wc_counts["passXACp"]/nevts)
#print "x_AC_m : %5.2f " % (wc_counts["passXACm"]/nevts)
#print "y_AC_p : %5.2f " % (wc_counts["passYACp"]/nevts)
#print "y_AC_m : %5.2f " % (wc_counts["passYACm"]/nevts)
#print "Total  : %5.2f " % (   wc_counts["clean"]/nevts)
#print " "
#print " "
#print "Geometric event cleaning efficiency for hitting each sample:"
#print "============================================================"
#print "Channel : description : efficiency for clean events : total efficiency"
#for ichan in chanList:
#    print "%3i : %30s : %5.2f : %5.2f" % (ichan, chanType[ichan, runnum], wc_counts["nIn", ichan]/wc_counts["clean"], wc_counts["nIn", ichan]/nevts)

#if os.path.isfile(outfile):
#    method = "update"
#else:
#    method = "recreate"

print "Finished Run %5i." % runnum

method = "recreate"
outtfile = ROOT.TFile(outfile,method)
for hist in sorted(hist.values()):
    outtfile.Delete(hist.GetName()+";*")
    hist.Write()
outtfile.Close()

