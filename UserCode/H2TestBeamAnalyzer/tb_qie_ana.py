#!/usr/bin/env python

print "Importing modules"
import os, sys
import numpy
import array
import itertools
import optparse
import ROOT
import cProfile

from tb_qie_utils import *

def main():

    # -------------------
    # --  Get options  --
    # -------------------

    print "Getting options"

    parser = optparse.OptionParser("usage: %prog [options] <input directory> \n")

    parser.add_option ('-o', dest='outfile', type='string',
                       default = None,
                       help="output file")
    parser.add_option ('-i', dest='infile', type='string',
                       default = None,
                       help="input file")
    parser.add_option ('-r', dest='runnum', type='int',
                       default = None,
                       help="run number; not used for the moment")
    parser.add_option ('-n', '--nevents', dest='nevents', type='int',
                       default = -1,
                       help="Number of events to process (default: all)")
    parser.add_option ('--sigTS', dest='sigTS', type='int',
                       default = 2,
                       help="Number of time samples to use as signal (default: 2)")
    parser.add_option ('--verbose', dest='verbose', 
                       action='store_true', default=False,
                       help="Turn on verbose mode")
    
    options, args = parser.parse_args()

    infile = options.infile
    outfile = options.outfile
    runnum = options.runnum
    verbose = options.verbose
    nevents = options.nevents
    sigTS = options.sigTS

    # Do some sanity checks
    if infile is None: 
        print "You did not provide an input file! Exiting."
        sys.exit()
    if outfile is None:
        print "You did not provide an output file! Exiting."
        sys.exit()
    # if runnum is None:
    #    print "You did not provide a run number! Exiting."
    #    sys.exit()


    # -------------------------------------
    # --  Import utilities               --
    # --  Do it here, otherwise optparse --
    # --  help output is not shown       --
    # -------------------------------------
        
    #from tb_qie_utils import *


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
    
    NCont = 255
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


    # -------------------------
    # --  Define histograms  --
    # -------------------------

    print "Preparing histograms"
    ofile = ROOT.TFile(outfile,"RECREATE")

    # Pedestal plots 
    # eta vs phi, for various depths
    h_ped_ieta_v_iphi = {}
    for depth in valid_depth:
        h_ped_ieta_v_iphi[depth] = ROOT.TH2D("h_ped_ieta_vs_iphi_depth%s"%(depth),"Pedestal in ieta vs iphi, for depth %s"%(depth),
                                             len(valid_ieta),valid_ieta[0],valid_ieta[-1]+1,
                                             len(valid_iphi),valid_iphi[0],valid_iphi[-1]+1)
    # eta vs depth, for various phi
    h_ped_ieta_v_depth = {}
    for iphi in valid_iphi:
        h_ped_ieta_v_depth[iphi] = ROOT.TH2D("h_ped_ieta_vs_depth_iphi%s"%(iphi),"Pedestal in ieta vs depth, for iphi %s"%(iphi),
                                             len(valid_ieta),valid_ieta[0],valid_ieta[-1]+1,
                                             len(valid_depth),valid_depth[0],valid_depth[-1]+1)
    # depth vs phi, for various ieta
    h_ped_depth_v_iphi = {}
    for ieta in valid_ieta:
        h_ped_depth_v_iphi[ieta] = ROOT.TH2D("h_ped_depth_vs_iphi_ieta%s"%(ieta),"Pedestal in depth vs iphi, for ieta %s"%(ieta),
                                             len(valid_depth),valid_depth[0],valid_depth[-1]+1,
                                             len(valid_iphi),valid_iphi[0],valid_iphi[-1]+1)



    # CapID rotation error
    h_capid_error = ROOT.TH1D("h_capid_error","Was there a capid error?",2,0,2)

    # some info on signal ADC count
    # eta vs phi, for various depths
    h_sig_ieta_v_iphi = {}
    for depth in valid_depth:
        h_sig_ieta_v_iphi[depth] = ROOT.TH2D("h_sig_ieta_vs_iphi_depth%s"%(depth),"Signal (2TS ave) in ieta vs iphi, for depth %s"%(depth),
                                             len(valid_ieta),valid_ieta[0],valid_ieta[-1]+1,
                                             len(valid_iphi),valid_iphi[0],valid_iphi[-1]+1)
    # eta vs depth, for various phi
    h_sig_ieta_v_depth = {}
    for iphi in valid_iphi:
        h_sig_ieta_v_depth[iphi] = ROOT.TH2D("h_sig_ieta_vs_depth_iphi%s"%(iphi),"Signal (2TS ave) in ieta vs depth, for iphi %s"%(iphi),
                                             len(valid_ieta),valid_ieta[0],valid_ieta[-1]+1,
                                             len(valid_depth),valid_depth[0],valid_depth[-1]+1)
    # depth vs phi, for various ieta
    h_sig_depth_v_iphi = {}
    for ieta in valid_ieta:
        h_sig_depth_v_iphi[ieta] = ROOT.TH2D("h_sig_depth_vs_iphi_ieta%s"%(ieta),"Signal (2TS ave) in depth vs iphi, for ieta %s"%(ieta),
                                             len(valid_depth),valid_depth[0],valid_depth[-1]+1,
                                             len(valid_iphi),valid_iphi[0],valid_iphi[-1]+1)

    # SPY like plots
    h_pulse_per_channel = {}
    for ichan in chanmap_inv:
        h_pulse_per_channel[ichan] = ROOT.TH2D("h_pulse_channel_%s" % (ichan),
                                               "Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                           chanmap_inv[ichan][1],
                                                                                                           chanmap_inv[ichan][0],
                                                                                                           chanmap_inv[ichan][2]),
                                               10,0,10,
                                               256,0,256)


    # -----------------------
    # --  Read input data  --
    # -----------------------

    # Acces input file
    print "Reading input file"
    ifile = ROOT.TFile(infile)
    ntp = {}
    ntp["qie11"] = ifile.Get("QIE11Data/Events")

    ## QIE information stored in the tree:
    ## ["numChs", "numTS", "iphi", "ieta", "depth", "pulse", "soi","ped", "capid_error"]


    # ------------------
    # --  Event Loop  --
    # ------------------

    nevts = ntp["qie11"].GetEntriesFast()
    if nevents != -1 and nevents <= nevts:
        nevts_to_run = nevents
    else:
        nevts_to_run = nevts

    print "Will process", nevts_to_run, "events"

    shape_info = []
    chan_ordering = []

    for ievt in xrange(nevts_to_run):
        if ievt % 100 == 0: print "Processing event ", ievt
    
        #######################
        ## QIE11 Analysis
        #######################
        ientry = ntp["qie11"].GetEntry(ievt)
        if ientry < 0:
            break

        if verbose:
            print " ".join(["Checking all",str(ntp["qie11"].numChs),"channels"])

        nChs = ntp["qie11"].numChs
        ishape = 0 # max is len(chanmap)-1
        # nChs = len(chanmap)
        if nChs == 0:
            print "There are no readout channels in this file! Why do think this will make histograms?? Bye!"
            sys.exit()
    
        if len(shape_info) == 0:
            # we have not initialized the list yet
            shape_info = [[]]*len(chanmap)
            chan_ordering = [[]]*nChs
            

        for ichan in xrange(nChs):
            # get id information
            iphi = ntp["qie11"].iphi[ichan]
            ieta = ntp["qie11"].ieta[ichan]
            depth = ntp["qie11"].depth[ichan]
            if len(chan_ordering[ichan]) == 0: 
                chan_ordering[ichan] = (iphi, ieta, depth)
            if verbose:
                print "iPhi:", iphi
                print "iEta:", ieta
                print "Depth:", depth
                print "Channel id:", ichan
            if not iphi in valid_iphi:
                continue
            if not ieta in valid_ieta:
                continue
            if not depth in valid_depth:
                continue


            # get number of time samples
            nTS = ntp["qie11"].numTS[ichan]
            if nTS == 0:
                print "There are no time samples in this file! Why do think this will make histograms?? Bye!"
                sys.exit()
            if verbose:
                print "Number of time samples:", nTS
        
            # was there a capid_error?
            capid_error = ntp["qie11"].capid_error[ichan]
            if verbose:
                print "CapID error?", capid_error
            if capid_error != 0:
                print "CAPID ROTATION ERROR for channel %s, ieta %s, iphi %s, depth %s" % (ichan, ieta, iphi, depth)
            h_capid_error.Fill(capid_error)

            # get pedestal value
            ped = ntp["qie11"].ped[ichan]
            pednorm = ped/nevts_to_run
            if verbose:
                print "Pedestal:", ped
            # Fill pedestal histograms
            h_ped_ieta_v_iphi[depth].Fill(ieta,iphi,pednorm)
            h_ped_ieta_v_depth[iphi].Fill(ieta,depth,pednorm)
            h_ped_depth_v_iphi[ieta].Fill(depth,iphi,pednorm)


            # pulse shape
            start = ichan*nTS
            if len(shape_info[ishape]) == 0:
                shape_info[ishape] = [[-1]*nevts_to_run for x in xrange(nTS)]
            if verbose:
                print "This is the pulse shape:"
                print "ichan, numTS:", ichan, ntp["qie11"].numTS[ichan]
                print ",".join([str(ntp["qie11"].pulse[s]) for s in xrange(start, start+nTS) ])
                print ",".join([str(ntp["qie11"].soi[s]) for s in xrange(start, start+nTS) ])
        

            # We want the average pulse shape per event, along with its uncertainties
            # We thus fill some lists
            # We also compute the signal pulse from the 5th and 6th TS (can be adjusted with nsigTS
            sig = 0
            soi = -1
            soi_offset = 1 # Can only be positive!
            for s in xrange(start,start+nTS):
                pulse = ntp["qie11"].pulse[s]
                shape_info[ishape][s-start][ievt] = pulse
                h_pulse_per_channel[chanmap[(iphi,ieta,depth)]].Fill(s-start,pulse)
                # find soi
                this_soi = ntp["qie11"].soi[s]
                if this_soi > 0:
                    soi = s-start
                    if verbose:
                        print "SOI index, soi value:",soi, this_soi
                if soi != -1 and (s-start) >= (soi+soi_offset) and (s-start) < (soi+soi_offset) + sigTS:
                    sig = sig + pulse
        

            sig = float(sig)/sigTS - ped
            signorm = sig/nevts_to_run
            h_sig_ieta_v_iphi[depth].Fill(ieta,iphi,signorm)
            h_sig_ieta_v_depth[iphi].Fill(ieta,depth,signorm)
            h_sig_depth_v_iphi[ieta].Fill(depth,iphi,signorm)

            ishape = ishape + 1


    # -----------------------------
    # -- Process the global info --
    # -----------------------------

    print "processing pulse shape"


    # Process the pulse shape information
    nchan = len(shape_info)
    nsamples = len(shape_info[0])

    # Histograms for Time sample for each channel 
    # Include info on average shape (median with 68% envelope, plus outer envelope), computed from all processed events
    h_min_pulse_per_channel = {}
    h_max_pulse_per_channel = {}
    h_mean_pulse_per_channel = {}
    h_median_pulse_per_channel = {}
    h_low_pulse_per_channel = {}
    h_high_pulse_per_channel = {}
    for ichan in chanmap_inv:
        h_min_pulse_per_channel[ichan] = ROOT.TH1D("h_min_pulse_channel_%s" % (ichan),
                                                   "Min Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                                   chanmap_inv[ichan][1],
                                                                                                                   chanmap_inv[ichan][0],
                                                                                                                   chanmap_inv[ichan][2]),
                                                   nsamples,0,nsamples)
        h_max_pulse_per_channel[ichan] = ROOT.TH1D("h_max_pulse_channel_%s" % (ichan),
                                                   "Max Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                                   chanmap_inv[ichan][1],
                                                                                                                   chanmap_inv[ichan][0],
                                                                                                                   chanmap_inv[ichan][2]),
                                                   nsamples,0,nsamples)
        h_mean_pulse_per_channel[ichan] = ROOT.TH1D("h_mean_pulse_channel_%s" % (ichan),
                                                    "Mean Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                                     chanmap_inv[ichan][1],
                                                                                                                     chanmap_inv[ichan][0],
                                                                                                                     chanmap_inv[ichan][2]),
                                                    nsamples,0,nsamples)
        h_median_pulse_per_channel[ichan] = ROOT.TH1D("h_median_pulse_channel_%s" % (ichan),
                                                      "Median Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                                         chanmap_inv[ichan][1],
                                                                                                                         chanmap_inv[ichan][0],
                                                                                                                         chanmap_inv[ichan][2]),
                                                      nsamples,0,nsamples)
        h_low_pulse_per_channel[ichan] = ROOT.TH1D("h_low_pulse_channel_%s" % (ichan),
                                                   "Low Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                                   chanmap_inv[ichan][1],
                                                                                                                   chanmap_inv[ichan][0],
                                                                                                                   chanmap_inv[ichan][2]),
                                                   nsamples,0,nsamples)
        h_high_pulse_per_channel[ichan] = ROOT.TH1D("h_high_pulse_channel_%s" % (ichan),
                                                    "High Pulse shape for channel %s, ieta %s, iphi %s, depth %s" % (ichan, 
                                                                                                                     chanmap_inv[ichan][1],
                                                                                                                     chanmap_inv[ichan][0],
                                                                                                                     chanmap_inv[ichan][2]),
                                                    nsamples,0,nsamples)


    if verbose:
        print "-"*20,"\nPulse data summary: \n","-"*20
    for jchan, chan_info in enumerate(shape_info):
        ichan = chanmap[chan_ordering[jchan]]
        print "jchan, ichan, (iphi, ieta, depth)", jchan, ichan, chan_ordering[jchan], chanmap_inv[ichan]

        if verbose:
            print "Channel", ichan
        for itime, time_info in enumerate(chan_info):
            # compute useful information
            min_pulse = min(time_info)
            max_pulse = max(time_info)
            ave = numpy.mean(time_info)
            median = numpy.median(time_info)
            low = numpy.percentile(time_info,16)
            high = numpy.percentile(time_info,84)
            if verbose:
                padding = 13
                print '    Time sample', itime
                print '{mess: <{fill}}'.format(mess='        Min:',fill=padding), min_pulse
                print '{mess: <{fill}}'.format(mess="        Low:",fill=padding), low
                print '{mess: <{fill}}'.format(mess="        Median:",fill=padding), median
                print '{mess: <{fill}}'.format(mess="        Average:",fill=padding), ave
                print '{mess: <{fill}}'.format(mess="        High:",fill=padding), high
                print '{mess: <{fill}}'.format(mess="        Max:",fill=padding), max_pulse
            # Put the info in a histogram
            h_min_pulse_per_channel[ichan].Fill(itime,min_pulse)
            h_max_pulse_per_channel[ichan].Fill(itime,max_pulse)
            h_mean_pulse_per_channel[ichan].Fill(itime,ave)
            h_median_pulse_per_channel[ichan].Fill(itime,median)
            h_low_pulse_per_channel[ichan].Fill(itime,low)
            h_high_pulse_per_channel[ichan].Fill(itime,high)


    # --------------------------
    # -- Write all histograms --
    # --------------------------

    print "Writing histograms"


    ofile.cd()

    h_capid_error.Write()

    for h in itertools.chain(h_ped_ieta_v_iphi.values(),
                             h_ped_ieta_v_depth.values(),
                             h_ped_depth_v_iphi.values(),
                             h_sig_ieta_v_iphi.values(),
                             h_sig_ieta_v_depth.values(),
                             h_sig_depth_v_iphi.values(),
                             h_min_pulse_per_channel.values(),
                             h_max_pulse_per_channel.values(),
                             h_mean_pulse_per_channel.values(),
                             h_median_pulse_per_channel.values(),
                             h_low_pulse_per_channel.values(),
                             h_high_pulse_per_channel.values(),
                             h_pulse_per_channel.values()
                             ):
        h.Write()



    ofile.Close()
    ifile.Close()



if __name__ == '__main__':

    #cProfile.run('main()')
    main()
