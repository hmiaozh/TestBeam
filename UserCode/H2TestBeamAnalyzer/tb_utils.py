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
chanList = range(1,73)

chanmap = {}
#ieta iphi depth channelId
chanmap[16,3,3] = 1
chanmap[17,3,1] = 2
chanmap[18,3,1] = 3
chanmap[18,3,2] = 4
chanmap[19,3,1] = 5
chanmap[19,3,2] = 6
chanmap[20,3,1] = 7
chanmap[20,3,2] = 8
chanmap[21,3,1] = 9
chanmap[21,3,2] = 10
chanmap[23,3,1] = 11
chanmap[23,3,2] = 12
chanmap[25,3,1] = 13
chanmap[25,3,2] = 14
chanmap[27,3,1] = 15
chanmap[27,3,2] = 16
chanmap[27,3,3] = 17
chanmap[29,3,2] = 18
chanmap[16,4,3] = 19
chanmap[17,4,1] = 20
chanmap[18,4,1] = 21
chanmap[18,4,2] = 22
chanmap[19,4,1] = 23
chanmap[19,4,2] = 24
chanmap[20,4,1] = 25
chanmap[20,4,2] = 26
chanmap[22,4,1] = 27
chanmap[22,4,2] = 28
chanmap[24,4,1] = 29
chanmap[24,4,2] = 30
chanmap[26,4,1] = 31
chanmap[26,4,2] = 32
chanmap[28,4,1] = 33
chanmap[28,4,2] = 34
chanmap[28,4,3] = 35
chanmap[29,4,1] = 36
chanmap[16,5,3] = 37
chanmap[17,5,1] = 38
chanmap[18,5,1] = 39
chanmap[18,5,2] = 40
chanmap[19,5,1] = 41
chanmap[19,5,2] = 42
chanmap[20,5,1] = 43
chanmap[20,5,2] = 44
chanmap[22,5,1] = 45
chanmap[22,5,2] = 46
chanmap[24,5,1] = 47
chanmap[24,5,2] = 48
chanmap[26,5,1] = 49
chanmap[26,5,2] = 50
chanmap[28,5,1] = 51
chanmap[28,5,2] = 52
chanmap[28,5,3] = 53
chanmap[29,5,1] = 54
chanmap[16,6,3] = 55
chanmap[17,6,1] = 56
chanmap[18,6,1] = 57
chanmap[18,6,2] = 58
chanmap[19,6,1] = 59
chanmap[19,6,2] = 60
chanmap[20,6,1] = 61
chanmap[20,6,2] = 62
chanmap[21,6,1] = 63
chanmap[21,6,2] = 64
chanmap[23,6,1] = 65
chanmap[23,6,2] = 66
chanmap[25,6,1] = 67
chanmap[25,6,2] = 68
chanmap[27,6,1] = 69
chanmap[27,6,2] = 70
chanmap[27,6,3] = 71
chanmap[29,6,2] = 72

chanmap[1]  = (16,3,3)
chanmap[2]  = (17,3,1)
chanmap[3]  = (18,3,1)
chanmap[4]  = (18,3,2)
chanmap[5]  = (19,3,1)
chanmap[6]  = (19,3,2)
chanmap[7]  = (20,3,1)
chanmap[8]  = (20,3,2)
chanmap[9]  = (21,3,1)
chanmap[10] = (21,3,2)
chanmap[11] = (23,3,1)
chanmap[12] = (23,3,2)
chanmap[13] = (25,3,1)
chanmap[14] = (25,3,2)
chanmap[15] = (27,3,1)
chanmap[16] = (27,3,2)
chanmap[17] = (27,3,3)
chanmap[18] = (29,3,2)
chanmap[19] = (16,4,3)
chanmap[20] = (17,4,1)
chanmap[21] = (18,4,1)
chanmap[22] = (18,4,2)
chanmap[23] = (19,4,1)
chanmap[24] = (19,4,2)
chanmap[25] = (20,4,1)
chanmap[26] = (20,4,2)
chanmap[27] = (22,4,1)
chanmap[28] = (22,4,2)
chanmap[29] = (24,4,1)
chanmap[30] = (24,4,2)
chanmap[31] = (26,4,1)
chanmap[32] = (26,4,2)
chanmap[33] = (28,4,1)
chanmap[34] = (28,4,2)
chanmap[35] = (28,4,3)
chanmap[36] = (29,4,1)
chanmap[37] = (16,5,3)
chanmap[38] = (17,5,1)
chanmap[39] = (18,5,1)
chanmap[40] = (18,5,2)
chanmap[41] = (19,5,1)
chanmap[42] = (19,5,2)
chanmap[43] = (20,5,1)
chanmap[44] = (20,5,2)
chanmap[45] = (22,5,1)
chanmap[46] = (22,5,2)
chanmap[47] = (24,5,1)
chanmap[48] = (24,5,2)
chanmap[49] = (26,5,1)
chanmap[50] = (26,5,2)
chanmap[51] = (28,5,1)
chanmap[52] = (28,5,2)
chanmap[53] = (28,5,3)
chanmap[54] = (29,5,1)
chanmap[55] = (16,6,3)
chanmap[56] = (17,6,1)
chanmap[57] = (18,6,1)
chanmap[58] = (18,6,2)
chanmap[59] = (19,6,1)
chanmap[60] = (19,6,2)
chanmap[61] = (20,6,1)
chanmap[62] = (20,6,2)
chanmap[63] = (21,6,1)
chanmap[64] = (21,6,2)
chanmap[65] = (23,6,1)
chanmap[66] = (23,6,2)
chanmap[67] = (25,6,1)
chanmap[68] = (25,6,2)
chanmap[69] = (27,6,1)
chanmap[70] = (27,6,2)
chanmap[71] = (27,6,3)
chanmap[72] = (29,6,2)

calib = {}
for channum in chanList:
    calib[channum] = 1.

runList = [7902]

chanType = {}
for channum in chanList:
    chanType[channum,runList[0]] = "Channel "+str(channum)

#chanType[4 , 7522] = "20x20cm SCSN-81 (PdB)"
#chanType[5 , 7522] = "T3 2x10cm"
#chanType[6 , 7522] = "PTP 6 blue WLS"
#chanType[12, 7522] = "PET 2mm/3mm tiles"
#chanType[17, 7522] = "PEN 2 sigma (2mm)"
#chanType[18, 7522] = "HE 10x10cm SCSN-81 (JF)"
#chanType[23, 7522] = "T5 CSL 2x10cm"
#chanType[22, 7522] = "2x10cm SCSN-81"

edges = {}
for channum in chanList:
    edges[channum,runList[0]] = [-80.    , 80.,     -80. ,     80.]

#edges = {}         #     x-,  x+,        y-,      y+
#edges[4 , 7526] = [-80.    , 80.,     -80. ,     80.]  #"20x20cm SCSN-81 (PdB)"
#edges[5 , 7526] = [12.-80. , 12.,  12.-15. ,     12.]  #"mix RTV" 10x2cm
#edges[6 , 7526] = [20.-80. , 20.,  44.-80. ,     44.]  #"PET 10x10cm 2sigma"
#edges[12, 7526] = [20.-80. , 20.,  42.-70. ,     42.]  #"Eileen PTP 8x10cm"
#edges[17, 7526] = [15.-80. , 15.,  45.-80. ,     45.]  #"PEN 10x10cm sigma"
#edges[18, 7526] = [15.-80. , 15.,  45.-80. ,     45.]  #"HE 10x10cm SCSN-81 (JF)"
#edges[22, 7526] = [25.-80. , 25., -5.      , -5.+15.]  #"T6"
#edges[23, 7526] = [15.-80. , 15., -1.      , -1.+15.]  #"mix 7 LS"

# ped,   1pe,   2pe,    chi2  
pecal = {}
for channum in chanList:
    pecal[channum] = [13.33, 35.19, 57.06, 164.45]
