#!/usr/bin/env python

print "Importing modules"
import os, sys
import optparse
import ROOT
import array


# -------------------
# --  Get options  --
# -------------------

print "Getting options"

parser = optparse.OptionParser("usage: %prog [options]\
-i <input directory> -o <output directory> -r <run number> \n")

parser.add_option ('-o', dest='outdir', type='string',
                   default = None,
                   help="output directory")
parser.add_option ('-i', dest='infile', type='string',
                   default = None,
                   help="input file")
parser.add_option ('-r', dest='runnum', type='int',
                   default = None,
                   help="run number")

options, args = parser.parse_args()

infile = options.infile
outdir = options.outdir
runnum = options.runnum

# Do some sanity checks
if infile is None: 
    print "You did not provide an input file! Exiting."
    sys.exit()
if outdir is None:
    print "You did not provide an output directory! Exiting."
    sys.exit()
else:
    outdir += "/"
    if not os.path.isdir(outdir):
        os.system("mkdir -p "+outdir)
if runnum is None:
    print "You did not provide a run number! Exiting."
    sys.exit()


# -------------------------------------
# --  Import utilities               --
# --  Do it here, otherwise optparse --
# --  help output is not shown       --
# -------------------------------------
from tb_qie_utils import *

# ------------------------
# --  Set ROOT options  --
# ------------------------

print "Setting ROOT options"
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetNdivisions(405,"x");
#ROOT.gStyle.SetErrorX(0.001)
ROOT.gStyle.SetPaintTextFormat("4.1f")

NCont = 255
stops = array.array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
red   = array.array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
green = array.array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
blue  = array.array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
NRGBs = len(stops)
ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
ROOT.gStyle.SetNumberContours(NCont)



# ----------------------
# --  Get histograms  --
# ----------------------

# open input file
inputfile = ROOT.TFile.Open(infile)
# create output file
outputfile = ROOT.TFile.Open(outdir+"/plots_run_%s.root"%(runnum),"RECREATE")

# ----------------------
# --  Pedestal plots  --
# ----------------------
for depth in valid_depth:
    h = inputfile.Get("h_ped_ieta_vs_iphi_depth%s"%(depth))
    setHist2D(h, "ieta", "iphi", "pedestal (ADC)",
              xoff=0.8, yoff=0.8, zoff=0.9)
    c = ROOT.TCanvas(h.GetName())
    c.SetRightMargin(0.15)
    c.cd()
    h.Draw("colztext")
    t = ROOT.TText()
    t.DrawTextNDC(0.7,0.93,'Depth = %s'%(depth) )
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".pdf")
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".gif")

     
# eta vs depth, for various phi
for iphi in valid_iphi:
    h = inputfile.Get("h_ped_ieta_vs_depth_iphi%s"%(iphi))
    setHist2D(h, "ieta", "depth", "pedestal (ADC)",
              xoff=0.8, yoff=0.8, zoff=0.9)
    c = ROOT.TCanvas(h.GetName())
    c.SetRightMargin(0.15)
    c.cd()
    h.Draw("colztext")
    t = ROOT.TText()
    t.DrawTextNDC(0.7,0.93,'iphi = %s'%(iphi) )
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".pdf")
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".gif")

# depth vs phi, for various ieta
for ieta in valid_ieta:
    h = inputfile.Get("h_ped_depth_vs_iphi_ieta%s"%(ieta))
    setHist2D(h, "depth", "iphi", "pedestal (ADC)",
              xoff=0.8, yoff=0.8, zoff=0.9)
    c = ROOT.TCanvas(h.GetName())
    c.SetRightMargin(0.15)
    c.cd()
    h.Draw("colztext")
    t = ROOT.TText()
    t.DrawTextNDC(0.7,0.93,'ieta = %s'%(ieta) )
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".pdf")
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".gif")


# --------------------
# --  Signal plots  --
# --------------------
h_sig_ieta_v_iphi = {}
for depth in valid_depth:
    h = inputfile.Get("h_sig_ieta_vs_iphi_depth%s"%(depth))
    setHist2D(h, "ieta", "iphi", "signal (ADC)",
              xoff=0.8, yoff=0.8, zoff=0.9)
    c = ROOT.TCanvas(h.GetName())
    c.SetRightMargin(0.15)
    c.cd()
    h.Draw("colztext")
    t = ROOT.TText()
    t.DrawTextNDC(0.7,0.93,'Depth = %s'%(depth) )
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".pdf")
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".gif")
     
# eta vs depth, for various phi
h_sig_ieta_v_depth = {}
for iphi in valid_iphi:
    h = inputfile.Get("h_sig_ieta_vs_depth_iphi%s"%(iphi))
    setHist2D(h, "ieta", "depth", "signal (ADC)",
              xoff=0.8, yoff=0.8, zoff=0.9)
    c = ROOT.TCanvas(h.GetName())
    c.SetRightMargin(0.15)
    c.cd()
    h.Draw("colztext")
    t = ROOT.TText()
    t.DrawTextNDC(0.7,0.93,'iphi = %s'%(iphi) )
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".pdf")
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".gif")

# depth vs phi, for various ieta
h_sig_depth_v_iphi = {}
for ieta in valid_ieta:
    h = inputfile.Get("h_sig_depth_vs_iphi_ieta%s"%(ieta))
    setHist2D(h, "depth", "iphi", "signal (ADC)",
              xoff=0.8, yoff=0.8, zoff=0.9)
    c = ROOT.TCanvas(h.GetName())
    c.SetRightMargin(0.15)
    c.cd()
    h.Draw("colztext")
    t = ROOT.TText()
    t.DrawTextNDC(0.7,0.93,'ieta = %s'%(ieta) )
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".pdf")
    c.SaveAs(outdir+"/"+h.GetName().replace("h_","",1)+".gif")



# ------------------------
# --  Capid error plot  --
# ------------------------
h_capid_error = inputfile.Get("h_capid_error")
setHist(h_capid_error, "capid error", "Entries",
        yoff=1.3, color=ROOT.kBlue)
c_capid = ROOT.TCanvas(h_capid_error.GetName())
c_capid.SetRightMargin(0.05)
c_capid.SetLeftMargin(0.15)
c_capid.SetBottomMargin(0.15)
c_capid.cd()
h_capid_error.Draw("hist")
outputfile.cd()
c_capid.Write()
c_capid.SaveAs(outdir+"/"+h_capid_error.GetName().replace("h_","",1)+".pdf")
c_capid.SaveAs(outdir+"/"+h_capid_error.GetName().replace("h_","",1)+".gif")



# -------------------------
# --  Pulse shape plots  --
# -------------------------

h_min_pulse_per_channel = {}
h_max_pulse_per_channel = {}
h_mean_pulse_per_channel = {}
h_median_pulse_per_channel = {}
h_low_pulse_per_channel = {}
h_high_pulse_per_channel = {}
for ichan in chanmap_inv:
    h_min = inputfile.Get("h_min_pulse_channel_%s" % (ichan))
    h_max = inputfile.Get("h_max_pulse_channel_%s" % (ichan))
    h_mean = inputfile.Get("h_mean_pulse_channel_%s" % (ichan))
    h_median = inputfile.Get("h_median_pulse_channel_%s" % (ichan))
    h_low = inputfile.Get("h_low_pulse_channel_%s" % (ichan))
    h_high = inputfile.Get("h_high_pulse_channel_%s" % (ichan))

    iphi, ieta, depth = chanmap_inv[ichan]

    hmax = 20
    if h_max.GetMaximum() > 20:
        hmax = h_max.GetMaximum()*1.1
    setHist(h_max, "TS", "ADC", 
            yrange_=[0, hmax],
            color=ROOT.kGray, width=3)
    setHist(h_min, "TS", "ADC", 
            yrange_=[0, hmax],
            color=ROOT.kGray, width=3)
    setHist(h_high, "TS", "ADC", 
            yrange_=[0, hmax],
            color=ROOT.kCyan-6, width=3)
    setHist(h_low, "TS", "ADC", 
            yrange_=[0, hmax],
            color=ROOT.kCyan-6, width=3)
    setHist(h_median, "TS", "ADC", 
            yrange_=[0, hmax],
            width=3)
    setHist(h_mean, "TS", "ADC", 
            yrange_=[0, hmax],
            style=7, width=3)

    # Draw the 68% band as TGraphAsymmErrors
    #nbinsx = h_median.GetXaxis().GetNbins()
    #x = array.array('d', [h_median.GetXaxis().GetBinLowEdge(i) for i in xrange(1, nbinsx+1)])
    #y = array.array('d', [h_median.GetBinContent(i) for i in xrange(1, nbinsx+1)])
    #exl = array.array('d', [0.01 for i in xrange(i, nbinsx+1) ])
    #exh = array.array('d', [h_median.GetBinWidth(i) for i in xrange(i, nbinsx+1) ])
    #eyl = array.array('d', [h_median.GetBinContent(i) - h_low.GetBinContent(i) if (h_median.GetBinContent(i) - h_low.GetBinContent(i) > 0) else 0.01 for i in xrange(1, nbinsx+1) ])
    #eyh = array.array('d', [h_high.GetBinContent(i) - h_median.GetBinContent(i) if (h_high.GetBinContent(i) - h_median.GetBinContent(i) > 0) else 0.01 for i in xrange(1, nbinsx+1) ])
    #n = len(x)
    #gr = ROOT.TGraphAsymmErrors(n,x,y,exl,exh,eyl,eyh)
    #gr.SetFillStyle(1001)
    #gr.SetFillColor(ROOT.kCyan-6)
    # graph drawing not turning up properly

    c = ROOT.TCanvas("/ieta-%s_iphi-%s_depth-%s.pdf"%(ieta,iphi,depth))
    c.SetRightMargin(0.05)
    c.SetLeftMargin(0.13)
    c.SetBottomMargin(0.15)
    c.cd()
    h_max.Draw("hist")
    h_min.Draw("histsame")
    #gr.Draw("psame")
    h_high.Draw("histsame")
    h_low.Draw("histsame")
    h_median.Draw("histsame")
    h_mean.Draw("histsame")
    t = ROOT.TText()
    t.DrawTextNDC(0.5,0.93,'ieta = %s, iphi = %s, depth = %s'%(ieta, iphi, depth) )
    leg = ROOT.TLegend(0.17,0.65,0.4,0.88)
    leg.SetBorderSize(0)
    leg.AddEntry(h_mean, "Mean", "l")
    leg.AddEntry(h_median, "Median", "l")
    leg.AddEntry(h_max, "Min/Max", "l")
    leg.AddEntry(h_high, "68% band", "l")
    leg.Draw()
    outputfile.cd()
    c.Write()
    c.SaveAs(outdir+"/ieta-%s_iphi-%s_depth-%s.pdf"%(ieta,iphi,depth))
    c.SaveAs(outdir+"/ieta-%s_iphi-%s_depth-%s.gif"%(ieta,iphi,depth))
    

inputfile.Close()
outputfile.Close()

