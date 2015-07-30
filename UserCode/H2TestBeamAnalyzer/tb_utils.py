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
    hist.GetXaxis().SetNdivisions(506)
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetXaxis().SetLabelFont(62)
    hist.GetYaxis().SetLabelFont(62)
    hist.GetXaxis().SetTitleFont(62)
    hist.GetYaxis().SetTitleFont(62)
    hist.GetXaxis().SetNdivisions(412,1)
    return 0

def setHist(hist, xtitle, ytitle, xrange, yrange, yoff, color, style=1):
    setHistBasic(hist)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetLineColor(color)
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
    hist.GetXaxis().SetNdivisions(506)                                                                                 
    hist.GetXaxis().SetTitleOffset(1.15)                                                                               
    hist.GetXaxis().SetLabelFont(62)                                                                                   
    hist.GetYaxis().SetLabelFont(62)                                                                                   
    hist.GetXaxis().SetTitleFont(62)                                                                                   
    hist.GetYaxis().SetTitleFont(62)                                                                                   
    hist.GetXaxis().SetNdivisions(412,1)
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


# Channel List
chanList = [4, 5, 6, 12, 17, 18, 22, 23]
chanList = [4, 5, 6, 12, 17, 18, 22, 23, 24]
    

chanmap = {}
#iphi ieta depth channelId
chanmap[3,  29,  1] =  1
chanmap[3,  30,  1] =  2
chanmap[3,  31,  1] =  3
chanmap[3,  32,  1] =  4
chanmap[3,  33,  1] =  5
chanmap[3,  34,  1] =  6
chanmap[3,  35,  1] =  7
chanmap[3,  36,  1] =  8
chanmap[3,  37,  1] =  9
chanmap[3,  38,  1] =  10
chanmap[3,  39,  1] =  11
chanmap[3,  29,  2] =  12
chanmap[3,  30,  2] =  13
chanmap[3,  31,  2] =  14
chanmap[3,  32,  2] =  15
chanmap[3,  33,  2] =  16
chanmap[3,  34,  2] =  17
chanmap[3,  35,  2] =  18
chanmap[3,  36,  2] =  19
chanmap[3,  37,  2] =  20
chanmap[3,  38,  2] =  21  
chanmap[3,  39,  2] =  22
chanmap[5,  29,  1] =  23
chanmap[5,  30,  1] =  24 

chanmap[1 ] =    (3,  29,  1)
chanmap[2 ] =    (3,  30,  1)
chanmap[3 ] =    (3,  31,  1)
chanmap[4 ] =    (3,  32,  1)
chanmap[5 ] =    (3,  33,  1)
chanmap[6 ] =    (3,  34,  1)
chanmap[7 ] =    (3,  35,  1)
chanmap[8 ] =    (3,  36,  1)
chanmap[9 ] =    (3,  37,  1)
chanmap[10] =    (3,  38,  1)
chanmap[11] =    (3,  39,  1)
chanmap[12] =    (3,  29,  2)
chanmap[13] =    (3,  30,  2)
chanmap[14] =    (3,  31,  2)
chanmap[15] =    (3,  32,  2)
chanmap[16] =    (3,  33,  2)
chanmap[17] =    (3,  34,  2)
chanmap[18] =    (3,  35,  2)
chanmap[19] =    (3,  36,  2)
chanmap[20] =    (3,  37,  2)
chanmap[21] =    (3,  38,  2)
chanmap[22] =    (3,  39,  2)
chanmap[23] =    (5,  29,  1)
chanmap[24] =    (5,  30,  1)

calib = {}
calib[4] = 1.
calib[5] = 1.
calib[6] = 1.
calib[12] = 1.
calib[17] = 1.
calib[18] = 1.
calib[22] = 1.
calib[23] = 1.
calib[24] = 1.

runList = [7522, 7526, 7532, 7545, 7591]

chanType = {}
chanType[4 , 7522] = "20x20cm SCSN-81 (PdB)"
chanType[5 , 7522] = "T3 2x10cm"
chanType[6 , 7522] = "PTP 6 blue WLS"
chanType[12, 7522] = "PET 2mm/3mm tiles"
chanType[17, 7522] = "PEN 2 sigma (2mm)"
chanType[18, 7522] = "HE 10x10cm SCSN-81 (JF)"
chanType[23, 7522] = "T5 CSL 2x10cm"
chanType[22, 7522] = "2x10cm SCSN-81"

chanType[4 , 7526] = "SCSN-81 20x20cm (PdB)"
chanType[5 , 7526] = "Mix RTV 10x2cm (JF)"
chanType[6 , 7526] = "PET 10x10cm 2sigma (IA)"
chanType[12, 7526] = "Eileen-PTP 8x10cm (IA)"
chanType[17, 7526] = "PEN 10x10cm sigma (IA)"
chanType[18, 7526] = "SCSN-81 10x10cm (JF)"
chanType[22, 7526] = "T6 (JF)"
chanType[23, 7526] = "Mix 7 LS (JF)"

#http://cmsonline.cern.ch/cms-elog/826344 Sun/Oct19/14:21
chanType[4 , 7532] = "SCSN-81 20x20cm (PdB)"
chanType[5 , 7532] = "T3 10x2cm (JF)"
chanType[6 , 7532] = "SCSN-81 10x10cm (JF)"
chanType[12, 7532] = "PET 10x10cm 2 blue WLS (IA)"
chanType[17, 7532] = "PEN 10x10cm sigma (IA)"
chanType[18, 7532] = "HEM 10x10cm 2 edge fiber (IA)"
chanType[22, 7532] = "SCSN-81 10x2cm (JF)"
chanType[23, 7532] = "Mix 7 LS (JF)"

# 7545 - 7548
# http://cmsonline.cern.ch/cms-elog/826336 Sun/Oct19/20:08
chanType[4 , 7545] = "SCSN-81 20x20cm (PdB)"
chanType[5 , 7545] = "Mix 4 RTV"
chanType[6 , 7545] = "SCSN-81 10x10cm (JF)"
chanType[12, 7545] = "Anthracene/Quartz edge"
chanType[17, 7545] = "PEN 10x10cm sigma (IA)"
chanType[18, 7545] = "HEM 10x10cm 2 edge fiber (IA)"
chanType[22, 7545] = "SCSN-81 10x2cm (JF)"
chanType[23, 7545] = "T6 (6121 Polysiloxane)"


# confirm 7549-7560, 7561-62
# Based on http://cmsonline.cern.ch/cms-elog/826367
chanType[4 , ] = "SCSN-81 20x20cm (PdB)"
chanType[5 , ] = "Mix 4 RTV"
chanType[6 , ] = "SCSN-81 10x10cm (JF)"
chanType[12, ] = "Anthracene/Quartz + 2mm AN "
chanType[17, ] = "PEN 10x10cm sigma (IA)"
chanType[18, ] = "HEM 10x10cm 4 WLS (IA)"
chanType[22, ] = "SCSN-81 10x2cm (JF)"
chanType[23, ] = "T6 (6121 Polysiloxane)"

# ??? Undocumented change before
# runs 7567-7573 http://cmsonline.cern.ch/cms-elog/826452

# http://cmsonline.cern.ch/cms-elog/826456 
# Tues/Oct21/02:35
# run 7579
chanType[4 , 7579] = "SCSN-81 20x20cm (PdB)"
chanType[5 , 7579] = "Mix 4 RTV"
chanType[6 , 7579] = "SCSN-81 10x10cm (JF)"
chanType[12, 7579] = "Anthracene/Quartz - 6 WLS"
chanType[17, 7579] = "PEN 10x10cm sigma (IA)"
chanType[18, 7579] = "HEM fiber edge RO (IA)"
chanType[19, 7579] = "PEN tile - sigma (IA)"
chanType[22, 7579] = "SCSN-81 10x2cm (JF)"
chanType[23, 7579] = "T6 (6121 Polysiloxane)"

# http://cmsonline.cern.ch/cms-elog/826491 
# Tues/Oct21/07:26
# run 7583 (7591???)
chanType[4 , 7591] = "SCSN-81 20x20cm (PdB)"
chanType[5 , 7591] = "Mix 4 RTV"
chanType[6 , 7591] = "PET bare shape 6 WLS (IA)"
chanType[12, 7591] = "PEN sigma (IA)"
chanType[17, 7591] = "PEN 10x10cm sigma (IA)"
chanType[18, 7591] = "AN 6 WLS (IA)"
chanType[19, 7591] = "SCSN-81 10x10cm (JF)"
chanType[22, 7591] = "SCSN-81 10x2cm (JF)"
chanType[23, 7591] = "T6 - 6121 Polysiloxane (JF)"
chanType[24, 7591] = "EJ-309 (MD)"                  



edges = {}         #     x-,  x+,        y-,      y+
edges[4 , 7526] = [-80.    , 80.,     -80. ,     80.]  #"20x20cm SCSN-81 (PdB)"      
edges[5 , 7526] = [12.-80. , 12.,  12.-15. ,     12.]  #"mix RTV" 10x2cm                   
edges[6 , 7526] = [20.-80. , 20.,  44.-80. ,     44.]  #"PET 10x10cm 2sigma"         
edges[12, 7526] = [20.-80. , 20.,  42.-70. ,     42.]  #"Eileen PTP 8x10cm"
edges[17, 7526] = [15.-80. , 15.,  45.-80. ,     45.]  #"PEN 10x10cm sigma"          
edges[18, 7526] = [15.-80. , 15.,  45.-80. ,     45.]  #"HE 10x10cm SCSN-81 (JF)"    
edges[22, 7526] = [25.-80. , 25., -5.      , -5.+15.]  #"T6"                         
edges[23, 7526] = [15.-80. , 15., -1.      , -1.+15.]  #"mix 7 LS"                   
 
                   #     x-,  x+,        y-,      y+
edges[4 , 7532] = [   -80. , 80.,     -80. ,     80.] # 20x20cm SCSN-81 (PdB)
edges[5 , 7532] = [15.-80. , 15.,      -5. , -5.+15.] # T3  10x2cm                   
edges[6 , 7532] = [15.-80. , 15.,  40.-80. ,     40.] # HE  10x10cm SCSN-81 (JF)
edges[12, 7532] = [15.-80. , 15.,  40.-80. ,     40.] # PET 10x10cm 2 blue WLS
edges[17, 7532] = [15.-80. , 15.,  45.-80. ,     45.] # PEN 10x10cm sigma
edges[18, 7532] = [ 5.-80. ,  5.,  40.-80. ,     40.] # HEM 10x10cm 2 edge fiber
edges[22, 7532] = [17.-80. , 17., -3.      , -3.+15.] # SCSN-81 2x10cm SCSN-81 (JF)
edges[23, 7532] = [17.-80. , 17., -3.      , -3.+15.] # Mix 7 LS (JF)                      

edges[4 , 7545] = [   -80. , 80.,     -80. ,     80.] # 20x20cm SCSN-81 (PdB)
edges[5 , 7545] = [   -45. , 20.,       2. ,     12.] # Mix 4 RTV
edges[6 , 7545] = [17.-80. , 17.,  40.-80. ,     40.] # HE  10x10cm SCSN-81 (JF)
edges[12, 7545] = [27.-80. , 27.,  40.-80. ,     40.] # Anthracene/Quartz edge
edges[17, 7545] = [18.-80. , 18.,  45.-80. ,     45.] # PEN 10x10cm sigma
edges[18, 7545] = [20.-80. , 20.,  45.-80. ,     45.] # HEM 10x10cm 2 edge fiber
edges[22, 7545] = [28.-80. , 28.,  17.-14. ,     17.] # SCSN-81 2x10cm SCSN-81 (JF)
edges[23, 7545] = [   -45. , 25.,       3. ,     15.] # T6 (6121 Polysiloxane)


#edges[4 , 7591] = [   -80. , 80.,     -80. ,     80.] # "SCSN-81 20x20cm (PdB)"     
#edges[5 , 7591] = [   -45. , 20.,       2. ,     12.] # "Mix 4 RTV"                 
#edges[6 , 7591] = [17.-80. , 17.,  40.-80. ,     40.] # "PET bare shape 6 WLS (IA)" 
#edges[12, 7591] = [27.-80. , 27.,  40.-80. ,     40.] # "PEN sigma (IA)"            
#edges[17, 7591] = [18.-80. , 18.,  45.-80. ,     45.] # "PEN 10x10cm sigma (IA)"    
#edges[18, 7591] = [20.-80. , 20.,  45.-80. ,     45.] # "AN 6 WLS (IA)"             
#edges[19, 7591] = [20.-80. , 20.,  45.-80. ,     45.] # "SCSN-81 10x10cm (JF)"      
#edges[22, 7591] = [28.-80. , 28.,  17.-14. ,     17.] # "SCSN-81 10x2cm (JF)"       
#edges[23, 7591] = [   -45. , 25.,       3. ,     15.] # "T6 (6121 Polysiloxane)"    
#edges[24, 7591] = [   -45. , 25.,       3. ,     15.] # "Maryland"                  

# 5% threshold
edges[ 4, 7591] = [-44.8,  35.2, -34.2,  46.8]
edges[ 5, 7591] = [-45.8,  23.8,   2.2,  18.8]
edges[ 6, 7591] = [-45.2,  28.2, -32.2,  46.8]
edges[12, 7591] = [-45.2,  31.2, -35.2,  47.2]
edges[17, 7591] = [-50.0,  50.0, -50.0,  50.0]
edges[18, 7591] = [-42.2,  30.8, -35.8,  45.2]
edges[22, 7591] = [-45.2,  30.8,   3.2,  22.2]
edges[23, 7591] = [-45.2,  30.8,   4.8,  22.2]
edges[24, 7591] = [-44.8,  26.2,  -2.2,  48.2]

# 10% threshold
edges[ 4, 7591] = [-39.2,  30.2, -28.2,  41.8]
edges[ 5, 7591] = [-40.2,  18.2,   3.2,  17.2]
edges[ 6, 7591] = [-40.2,  22.8, -26.2,  41.8]
edges[12, 7591] = [-39.8,  27.2, -29.8,  43.2]
edges[17, 7591] = [-50.0,  50.0, -50.0,  50.0]
edges[18, 7591] = [-35.8,  24.2, -24.2,  40.2]
edges[22, 7591] = [-40.2,  25.2,   4.8,  21.2]
edges[23, 7591] = [-40.8,  24.2,   6.2,  20.8]
edges[24, 7591] = [-39.2,  20.8,   0.8,  44.8]

                                                      
# ped,   1pe,   2pe,    chi2  
pecal = {}
pecal[1 ] =  [13.33, 35.19, 57.06,  164.45]
pecal[2 ] =  [14.04, 25.56, 37.07,  133.54]
pecal[3 ] =  [13.56, 26.54, 39.53,  101.01]
pecal[4 ] =  [14.84, 33.63, 52.41,  345.07]
pecal[5 ] =  [15.96, 32.29, 48.62,  249.49]
pecal[6 ] =  [14.23, 35.93, 57.63,  303.38]
pecal[7 ] =  [14.31, 27.81, 41.30,  260.33]
pecal[8 ] =  [13.94, 22.63, 31.32,  516.74]
pecal[9 ] =  [14.62, 24.01, 33.39,  228.05]
pecal[10] =  [15.06, 23.55, 32.03,  695.07]
pecal[11] =  [14.34, 21.95, 29.55, 1094.26]
pecal[12] =  [15.62, 33.28, 50.93,  156.97]
pecal[13] =  [12.69, 21.58, 30.47,   73.60]
pecal[14] =  [15.72, 22.92, 30.12,  651.71]
pecal[15] =  [14.47, 31.43, 48.40,  223.02]
pecal[16] =  [14.55, 23.56, 32.58,  101.86]
pecal[17] =  [16.93, 36.39, 55.85,  135.57]
pecal[18] =  [15.36, 24.02, 32.67,  242.25]
pecal[19] =  [15.87, 33.47, 51.07,  155.58]
pecal[20] =  [14.61, 32.71, 50.81,  170.51]
pecal[21] =  [14.61, 25.75, 36.90,  372.48]
pecal[22] =  [15.52, 31.51, 47.49,   96.96]
pecal[23] =  [14.33, 28.30, 42.27,  172.36]
pecal[24] =  [15.75, 30.54, 45.33,  170.79]
