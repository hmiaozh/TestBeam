#!/usr/bin/env python

print "Importing modules"
import sys
import optparse
import os
import ROOT
import array
import time
from tb_utils import *
from math import exp, sqrt, log

#######################
# Get options
#######################

print "Getting options"

parser = optparse.OptionParser("usage: %prog [options]\
<input directory> \n")

parser.add_option ('--o', dest='outdir', type='string',
                   default = 'none',
                   help="output directory")
parser.add_option ('--i', dest='infile', type='string',
                   default = 'none',
                   help="output directory")
parser.add_option ('--r', dest='runnum', type='int',
                   default = 1,
                   help="output directory")
parser.add_option ('--pe_only', action="store_true",
                   dest="doPE", default=False)

#parser.add_option ('--tout', action="store_true",
#                   dest="tout", default=False)

options, args = parser.parse_args()

doPE   = options.doPE
infile = options.infile
outdir = options.outdir
runnum = options.runnum
if outdir != "none":
    outdir += "/"
    if not os.path.isdir(outdir):
        os.system("mkdir -p "+outdir)


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

def setPadPasMargin(pad, rightMargin=0.05):                                                                                   
  pad.SetFrameFillStyle(1001)                                                                                                 
  pad.SetTicks()                                                                                                              
  pad.SetTopMargin(0)                                                                                                         
  pad.SetFillColor(0)                                                                                                         
  leftMargin   = 0.16                                                                                                         
  topMargin    = 0.1                                                                                                          
  bottomMargin = 0.15                                                                                                         
  pad.SetLeftMargin(leftMargin)                                                                                               
  pad.SetRightMargin(rightMargin)                                                                                             
  pad.SetTopMargin(topMargin)                                                                                                 
  pad.SetBottomMargin(bottomMargin)                                                                                           


def setHistBasic(hist):
    hist.GetYaxis().SetLabelSize(0.045)
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetXaxis().SetLabelSize(0.045)
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetXaxis().SetLabelFont(62)
    hist.GetYaxis().SetLabelFont(62)
    hist.GetXaxis().SetTitleFont(62)
    hist.GetYaxis().SetTitleFont(62)
    hist.GetXaxis().SetNdivisions(406,1)
    return 0

def setHist(hist, xtitle, ytitle, xrange, yrange, yoff, color=-1, style=-1):
    setHistBasic(hist)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitle(xtitle)
    if color > 0:
        hist.SetLineColor(color)
    if style > 0:
        hist.SetLineStyle(style)
    hist.SetLineWidth(2)
    hist.GetYaxis().SetTitleOffset(yoff)                                                                               
    if yrange != 0:                                                                             
        hist.GetYaxis().SetRangeUser(yrange[0], yrange[1])
    if xrange != 0:
        hist.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    return 0

def setHist2D(hist, xtitle, ytitle, ztitle, xrange, yrange, zrange, xoff, yoff, zoff):
    setHistBasic(hist)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetZaxis().SetTitle(ztitle)
    hist.GetYaxis().SetTitleOffset(yoff)                                                                               
    hist.GetXaxis().SetTitleOffset(xoff)                                                                               
    hist.GetZaxis().SetTitleOffset(zoff)                                                                               
    if yrange != 0:                                                                             
        hist.GetYaxis().SetRangeUser(yrange[0], yrange[1])
    if xrange != 0:
        hist.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    if zrange != 0:
        hist.GetZaxis().SetRangeUser(zrange[0], zrange[1])
    return 0

def setGraph(hist, xtitle, ytitle, xrange, yrange, yoff, color, mstyle, msize):
    hist.SetMarkerStyle(mstyle)
    hist.SetMarkerColor(color)
    hist.SetLineColor  (color)
    hist.SetFillColor  (0)
    hist.SetMarkerSize (msize)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetLabelSize(0.045)                                                                                
    hist.GetYaxis().SetTitleSize(0.055)                                                                                
    hist.GetYaxis().SetTitleOffset(yoff)                                                                               
    hist.GetXaxis().SetLabelSize(0.045)                                                                                
    hist.GetXaxis().SetTitleSize(0.055)                                                                                
    hist.GetXaxis().SetTitleOffset(1.15)                                                                               
    hist.GetXaxis().SetLabelFont(62)                                                                                   
    hist.GetYaxis().SetLabelFont(62)                                                                                   
    hist.GetXaxis().SetTitleFont(62)                                                                                   
    hist.GetYaxis().SetTitleFont(62)                                                                                   
    hist.GetXaxis().SetNdivisions(406,1)
    if yrange != 0:                                                                             
        hist.GetYaxis().SetRangeUser(yrange[0], yrange[1])
    if xrange != 0:
        hist.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    return 0
    
def addHists(hist1, hist2, name):
    hfist3 = hist1.Clone(name)
    hist3.Add(hist2)
    return hist3

def getText(ip, ip2, E_base_phase=0):
    outText = []
    if ip == "05" : ipA = "0.5"
    else : ipA = ip
    if ip2 == "05": ipB = "0.5"
    else : ipB = ip2
    name = "Peak current = "
    if ipB == 0:
        outText.append(name+ipA+" #muA")
    else:
        outText.append(name+ipA+" #muA + "+ipB+" #muA")
    outText.append("E_{tot} = "+uA2gev[ip, "t"]+" GeV")
    if E_base_phase == "0":
        outText.append("not timed in")
    else:
        outText.append("timed in for "+uA2gev[E_base_phase, "t"]+" GeV")
        #outText.append("phase = "+str(out_phase[E_base_phase])+" ns")
    return outText

# choose channel to plot along side all other channels in E_4TS  plots
refChan = 22

# edge threshold
edge_thold = 0.1

pstyle = {}
pstyle[22, "col"] = 1
pstyle[ 5, "col"] = 9
pstyle[23, "col"] = 419
pstyle[17, "col"] = 2
pstyle[18, "col"] = 4
pstyle[ 4, "col"] = 6
pstyle[ 6, "col"] = 46
pstyle[12, "col"] = 28
pstyle[24, "col"] = 3


tfile = ROOT.TFile(infile)

vname = {}
vname["hf"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse"]
vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC", "xD", "yD"]

hist = {}
# Define wire chamber histograms
for ip0 in ["A", "B", "C", "D"]:
    hist["x"+ip0+"_v_y"+ip0]          = tfile.Get("h_x"+ip0+"_v_y"+ip0+"_clean")
    for ixy in ["x", "y"]:
        # 1D histos for x and y in all 4 chambers
        hist[ixy+ip0]          = tfile.Get("h_"+ixy+"_"+ip0+"_clean")
        # 2D histos for x and y correlations for all histo combinations
        
    for ip1 in ["A", "B", "C", "D"]:
        if ((ip0 == "A" and ip1 == "B") or (ip0 == "A" and ip1 == "C") or (ip0 == "A" and ip1 == "D") or 
            (ip0 == "B" and ip1 == "C") or (ip0 == "B" and ip1 == "D") or (ip0 == "C" and ip1 == "D")):            
            for ixy in ["x", "y"]:
                hist[ixy+ip0+"_v_"+ixy+ip1] = tfile.Get("h_"+ixy+"_"+ip0+"v"+ip1+"_clean")

                
# Make energy plots
for ichan in chanList:
    hist["avgpulse", ichan] = tfile.Get("h_avgpulse_chan"+str(ichan))
    hist["e_wcC"   , ichan] = tfile.Get("h_e_wcC_chan"   +str(ichan))
    hist["e_wcC_x" , ichan] = tfile.Get("h_e_wcC_x_chan" +str(ichan))
    hist["e_wcC_y" , ichan] = tfile.Get("h_e_wcC_y_chan" +str(ichan))
    hist["e_4TS"   , ichan] = tfile.Get("h_e_4TS_chan"   +str(ichan))

################################################################
# Get Npe for all samples from counting zeros and average
################################################################

#print "Chan :                    description :: Npe 0's : ped/tot :: Npe Mean : Npe Mean_2 : mean : chi2"
print "Chan :                    description :: Npe zero-counting : Npe (mean-ped)/gain"
print "================================================================================================="
for ichan in chanList:
    # Counting zeros    
    ped = hist["e_4TS", ichan].Integral(1,51)
    tot = hist["e_4TS", ichan].Integral(1,5000)
    pePerMip0 =  -1.*log(ped/tot)
    # Mean
    mean = hist["e_4TS", ichan].GetMean()
    pePerMipMean = (mean-pecal[ichan][0])/(pecal[ichan][1]-pecal[ichan][0])
    pePerMipMean2 = (mean-pecal[ichan][0])/(pecal[ichan][2]-pecal[ichan][1])

    #    print "%4i : %30s ::   %5.2f :   %5.2f ::    %5.2f :      %5.2f :%5.0f :%5.0f" % (ichan, chanType[ichan, runnum], pePerMip0, ped/tot, pePerMipMean, pePerMipMean2, mean, pecal[ichan][3])
    print "%4i : %30s :: %5.2f : %5.2f" % (ichan, chanType[ichan, runnum], pePerMip0, pePerMipMean)


################################################################
# Find edges of samples
################################################################
find_edge = {}
for ichan in chanList:
    for ixy in ["x", "y"]:
        h1 = hist["e_wcC_"+ixy , ichan]
        nbins = h1.GetNbinsX()
        tot   = h1.Integral(1,nbins)
        if tot == 0: 
            find_edge[ichan, ixy, "L"] = -50.
            find_edge[ichan, ixy, "H"] =  50.
            continue
        for ibin in range(1,nbins):
            iint = h1.Integral(1,ibin)
            if iint/tot > edge_thold:
                
                find_edge[ichan, ixy, "L"] = h1.GetBinCenter(ibin)
                break
        for ibin in range(1,nbins):
            iint = h1.Integral(nbins-ibin,nbins)
            if iint/tot > edge_thold:
                find_edge[ichan, ixy, "H"] = h1.GetBinCenter(nbins-ibin)
                break
print " " 
print "Computed edges for threshold of %2.0f percent" % (100.*edge_thold)
print "================================================"
for ichan in chanList:
    print "edges[%2i, %4i] = [%5.1f, %5.1f, %5.1f, %5.1f]" % (ichan, runnum, 
                                                              find_edge[ichan, "x", "L"], 
                                                              find_edge[ichan, "x", "H"],
                                                              find_edge[ichan, "y", "L"],
                                                              find_edge[ichan, "y", "H"])

if doPE : sys.exit()    



##################################
# Plot pulse shape comparison
##################################
cname = "comp_avgPulseShape"
canv = ROOT.TCanvas(cname, cname, 400, 424)
pad = canv.GetPad(0)
setPadPasMargin(pad)
for ichan in chanList:
    setHist(hist["avgpulse", ichan], "time sample", "Average Linearized ADC", 0, (0.,50.), 1.3, pstyle[ichan, "col"])
    if ichan == chanList[0]: hist["avgpulse", ichan].Draw()
    else: hist["avgpulse", ichan].Draw("same")

textsize = 0.03; legx0 = 0.17; legx1 = 0.7; legy0 = 0.7; legy1 = 1.0
leg = ROOT.TLegend(legx0, legy0, legx1, legy1)
leg.SetFillColor(0)
leg.SetTextSize(textsize)
leg.SetColumnSeparation(0.0)
leg.SetEntrySeparation(0.1)
leg.SetMargin(0.2)
for ichan in chanList:
    leg.AddEntry(hist["avgpulse", ichan], "ch"+str(ichan)+" : "+chanType[ichan, runnum])
leg.Draw()
        
for end in [".pdf", ".gif"]:
    canv.SaveAs(outdir+cname+end)

#######################################
# Plot energy in bins of WC C position
#######################################

ledge = {}
elist = ["xL", "xH", "yL", "yH"]
for ichan in chanList:
    ledge["xL", ichan] = ROOT.TLine(edges[ichan , runnum][0], -100., edges[ichan , runnum][0], 100.)
    ledge["xH", ichan] = ROOT.TLine(edges[ichan , runnum][1], -100., edges[ichan , runnum][1], 100.)
    ledge["yL", ichan] = ROOT.TLine(-100., edges[ichan , runnum][2], 100., edges[ichan , runnum][2])
    ledge["yH", ichan] = ROOT.TLine(-100., edges[ichan , runnum][3], 100., edges[ichan , runnum][3])
    for iedge in elist:
        ledge[iedge, ichan].SetLineStyle(2)

for ichan in chanList:
    cname = "energy_wcC_chan"+str(ichan)
    canv = ROOT.TCanvas(cname, cname, 400, 424)
    pad = canv.GetPad(0)
    #    pad.SetLogz()
    setPadPasMargin(pad, 0.25)

    setHist(hist["e_wcC", ichan], "Wire Chamber C x (mm)", "Wire Chamber C y (mm)", 0, 0, 1.3)
    hist["e_wcC"   , ichan].GetZaxis().SetTitle("Evts with E_{4TS} > 25 linADC")
    hist["e_wcC"   , ichan].GetZaxis().SetLabelSize(0.03)    
    hist["e_wcC"   , ichan].GetZaxis().SetTitleOffset(1.3)
    hist["e_wcC"   , ichan].Draw("colz")
    for iedge in elist:
        ledge[iedge, ichan].Draw()
    textsize = 0.04; xstart = 0.2; ystart = 0.85
    latex = ROOT.TLatex(); latex.SetNDC(); latex.SetTextAlign(12); latex.SetTextSize(textsize)    
    latex.DrawLatex(xstart, ystart, "Channel "+str(ichan)+": "+chanType[ichan, runnum])
    for end in [".pdf", ".gif"]:
        canv.SaveAs(outdir+cname+end)


#######################################
# Plot 1D energy in bins of WC C position
#######################################
for ichan in chanList:
    for ixy in ["x", "y"]:
        cname = "energy_wcC_"+ixy+"_chan"+str(ichan)
        canv = ROOT.TCanvas(cname, cname, 400, 424)
        pad = canv.GetPad(0)
        setPadPasMargin(pad, 0.25)
        setHist(hist["e_wcC_"+ixy, ichan], "Wire Chamber C "+ixy+" (mm)", "Evts with E_{4TS} > 25 linADC", 0, 0, 1.3)
        hist["e_wcC_"+ixy, ichan].Draw()
        #        for iedge in ["L","H"]:
        #    ledge[ixy+iedge, ichan].Draw()
        textsize = 0.04; xstart = 0.2; ystart = 0.85
        latex = ROOT.TLatex(); latex.SetNDC(); latex.SetTextAlign(12); latex.SetTextSize(textsize)    
        latex.DrawLatex(xstart, ystart, "Channel "+str(ichan)+": "+chanType[ichan, runnum])
        for end in [".pdf", ".gif"]:
            canv.SaveAs(outdir+cname+end)

#######################################
# Plot 4TS energy
#######################################

for ichan in chanList:
    #    hist["e_4TS"   , ichan].Rebin()
    #    hist["e_4TS"   , ichan].SetLineWidth(1)
    hist["e_4TS"   , ichan].SetLineColor(pstyle[ichan, "col"])

setHist(hist["e_4TS", refChan], "Energy in 4TS (LinADC)", "Events", (0.,200.), (0.5, 3.e4), 1.3, pstyle[refChan, "col"])
for ichan in chanList:
    cname = "energy_4TS_chan"+str(ichan)
    canv = ROOT.TCanvas(cname, cname, 400, 424)
    pad = canv.GetPad(0)
    pad.SetLogy()
    setPadPasMargin(pad)
    setHist(hist["e_4TS", ichan], "Energy in 4TS (LinADC)", "Events", (0.,200.), (0.5, 3.e4), 1.3, pstyle[ichan, "col"])
    hist["e_4TS"   , refChan].Draw()
    hist["e_4TS"   , ichan  ].Draw("same")
    textsize = 0.03; legx0 = 0.4; legx1 = 0.9; legy0 = 0.8; legy1 = 0.93
    leg = ROOT.TLegend(legx0, legy0, legx1, legy1)
    leg.SetFillColor(0)
    leg.SetTextSize(textsize)
    leg.SetColumnSeparation(0.0)
    leg.SetEntrySeparation(0.1)
    leg.SetMargin(0.2)
    leg.AddEntry(hist["e_4TS", ichan], "ch"+str(ichan)+" : "+chanType[ichan, runnum])
    leg.AddEntry(hist["e_4TS", refChan], "ch"+str(refChan)+" : "+chanType[refChan, runnum])
    leg.Draw()

    for end in [".pdf", ".gif"]:
        canv.SaveAs(outdir+cname+end)
    


