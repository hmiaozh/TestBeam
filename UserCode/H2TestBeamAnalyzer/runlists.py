# ------------------------------------
# -- This file contains some basic 
# -- information about the 2015 test 
# -- beam runs.
# --
# -- Originally created by: 
# -- Nadja Strobbe & Jay Dittmann
# ------------------------------------

# EMAPS
EMAP_default = "EMAP-QIE11-L00-21AUG2015-04.txt"
EMAP_specialODU = "EMAP-QIE11-SPECIAL-ODU-22AUG2015-02.txt"

#######################
# table for Aug 13
# Phase 2 eta-phi scan
#######################

runTable_Aug13 = {}

runTable_Aug13[8530] = (8100, 40500, 300000, "", "", "1", EMAP_default)
runTable_Aug13[8531] = (8200, 40500, 300000, "", "", "1", EMAP_default)
runTable_Aug13[8532] = (8310, 40500, 300000, "", "", "1", EMAP_default)
runTable_Aug13[8533] = (8310, 40500, 107500, "", "", "1", EMAP_default)
runTable_Aug13[8535] = (8390, 40500, 400000, "", "", "1", EMAP_default)


#######################
# table for Aug 14 scan
# full eta-phi scan
#######################

runTable_Aug14 = {}

runTable_Aug14[8536] = (9583, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8537] = (9964, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8538] = (10285, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8539] = (10597, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8540] = (10884, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8541] = (11154, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8542] = (11419, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8543] = (11688, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8544] = (11963, 23400, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8545] = (12241, 23400, 50000, "14", "150m", "1", EMAP_default) 

runTable_Aug14[8546] = (9583, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8547] = (9964, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8548] = (10285, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8549] = (10597, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8550] = (10884, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8551] = (11154, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8552] = (11419, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8553] = (11688, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8556] = (11963, 3482, 50000, "14", "150m", "1", EMAP_default) 
runTable_Aug14[8557] = (12241, 3482, 50000, "14", "150m", "1", EMAP_default) 


#########################################
# Muon data - Large stat for Ph2
#########################################

runTable_Ph2_Aug14 = {}

runTable_Ph2_Aug14[8558] = (10884, 23400, 300000, "", "", "1", EMAP_default)
runTable_Ph2_Aug14[8559] = (12241, 23400, 300000, "", "", "1", EMAP_default)
runTable_Ph2_Aug14[8560] = (9583, 23400, 300000, "", "", "1", EMAP_default)
runTable_Ph2_Aug14[8561] = (9583, 3482, 300000, "", "", "1", EMAP_default)
runTable_Ph2_Aug14[8566] = (8390, 40500, 305000, "", "", "1", EMAP_default)
runTable_Ph2_Aug14[8570] = (8450, 40500, 176231, "", "ped", "1", EMAP_default)

runTable_Ph2_Aug15 = {}

runTable_Ph2_Aug15[8578] = (8479, 40500, 300000, "", "150m", "1", EMAP_default)
runTable_Ph2_Aug15[8579] = (8370, 40500, 500000, "", "150m", "1", EMAP_default)
runTable_Ph2_Aug15[8580] = (8370, 40500, 500000, "", "150m", "1", EMAP_default)
runTable_Ph2_Aug15[8581] = (8500, 40500, 1000000, "", "150m", "1", EMAP_default)

#########################################
# Muon data - finely binned eta-phi scan
#########################################

runTable_Aug15 = {}

#runTable_Aug15[runnumber] = [eta, phi, nev, beamcounters, beamtype]
runTable_Aug15[8582] = (9884,40500,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8583] = (9884,36800,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8584] = (9884,33100,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8585] = (9884,29400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8586] = (9884,25700,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8587] = (9884,22000,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8588] = (9884,18300,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8589] = (9884,14600,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8590] = (9884,10900,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8591] = (9884,7200,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8592] = (9884,3482,5000,"134","150m", "1", EMAP_default)

runTable_Aug15[8594] = (9503,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8593] = (9573,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8595] = (9643,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8596] = (9713,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8597] = (9783,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8598] = (9853,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8599] = (9923,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8600] = (9993,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8601] = (10063,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8602] = (10133,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8603] = (10205,23400,5000,"134","150m", "1", EMAP_default)

runTable_Aug15[8604] = (10804,40500,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8606] = (10804,36800,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8607] = (10804,33100,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8608] = (10804,29400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8609] = (10804,25700,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8610] = (10804,22000,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8611] = (10804,18300,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8612] = (10804,14600,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8614] = (10804,10900,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8615] = (10804,7200,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8616] = (10804,3482,5000,"134","150m", "1", EMAP_default)

runTable_Aug15[8617] = (10517,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8618] = (10572,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8619] = (10627,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8620] = (10682,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8621] = (10737,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8622] = (10792,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8624] = (10847,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8625] = (10903,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8626] = (10957,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8627] = (11012,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8628] = (11067,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8629] = (11074,23400,5000,"134","150m", "1", EMAP_default)

runTable_Aug15[8630] = (8200,40500,489257,"134","150m", "1", EMAP_default)

runTable_Aug15[8632] = (11884,40500,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8633] = (11884,36799,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8634] = (11884,33099,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8636] = (11884,29101,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8637] = (11884,25700,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8638] = (11884,22101,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8639] = (11884,21999,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8640] = (11884,18299,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8641] = (11884,14599,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8642] = (11884,10900,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8643] = (11884,7200,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8644] = (11884,3482,5000,"134","150m", "1", EMAP_default)

runTable_Aug15[8645] = (11609,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8646] = (11664,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8647] = (11717,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8648] = (11774,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8649] = (11826,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8650] = (11882,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8651] = (11939,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8652] = (11992,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8653] = (12048,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8654] = (12104,23400,5000,"134","150m", "1", EMAP_default)
runTable_Aug15[8655] = (12158,23400,5000,"134","150m", "1", EMAP_default)

######################################
# Pion data from before beam was lost
###################################### 

runTable_pions_Aug15 = {}

runTable_pions_Aug15[8656] = (10804, 23400, 241547, "134", "50p", "1", EMAP_default)

######################################
# Pion data - Round A
###################################### 

runTable_pions_ODU12 = {}

#runTable[runnumber] = [eta, phi, nev, beamcounters, beamtype, shunt]
runTable_pions_ODU12[8749] = (10350,23400,100000,"14","150p","1/5", EMAP_default)
runTable_pions_ODU12[8750] = (10350,23400,100000,"14","150p","1/11.5", EMAP_default)
runTable_pions_ODU12[8751] = (10650,23400,100000,"14","150p","1/5", EMAP_default)
runTable_pions_ODU12[8752] = (10650,24300,100000,"14","150p","1/11.5", EMAP_default)
runTable_pions_ODU12[8755] = (10925,24300,100000,"14","150p","1/5", EMAP_default)
runTable_pions_ODU12[8756] = (10925,24300,100000,"14","150p","1/11.5", EMAP_default) # might contain events with bad links

runTable_pions_ODU12[8757] = (10350,23400,100000,"14","100p","1", EMAP_default)
runTable_pions_ODU12[8758] = (10350,23400,250000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8759] = (10350,23400,250000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8760] = (10350,23400,250000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8761] = (10350,23400,250000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8762] = (10350,23400,100000,"14","100p","1/11.5", EMAP_default)
runTable_pions_ODU12[8763] = (10650,23400,100000,"14","100p","1", EMAP_default)
runTable_pions_ODU12[8764] = (10650,23400,30321,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8765] = (10650,23400,32000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8766] = (10650,23400,70000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8767] = (10650,23400,100000,"14","100p","1/11.5", EMAP_default)
runTable_pions_ODU12[8768] = (10925,23400,100000,"14","100p","1", EMAP_default)
runTable_pions_ODU12[8769] = (10925,23400,100000,"14","100p","1/5", EMAP_default)
runTable_pions_ODU12[8770] = (10925,23400,100000,"14","100p","1/11.5", EMAP_default)

runTable_pions_ODU12[8794] = (10350, 23400, 100000, "14", "300p", "1/5", EMAP_default)
runTable_pions_ODU12[8793] = (10350, 23400, 100000, "14", "300p", "1/11.5", EMAP_default) # links reinitialized during run (before 25k events)
runTable_pions_ODU12[8781] = (10650, 23400, 20000, "14", "300p", "1/5", EMAP_default)
runTable_pions_ODU12[8782] = (10650, 23400, 41519, "14", "300p", "1/5", EMAP_default)
runTable_pions_ODU12[8784] = (10650, 23400, 40000, "14", "300p", "1/5", EMAP_default)
runTable_pions_ODU12[8777] = (10650, 23400, 84962, "14", "300p", "1/11.5", EMAP_default)
runTable_pions_ODU12[8780] = (10650, 23400, 20000, "14", "300p", "1/11.5", EMAP_default)
runTable_pions_ODU12[8774] = (10925, 23400, 100000, "14", "300p", "1/5", EMAP_default) # beam was displaced for ~4-5mins
runTable_pions_ODU12[8773] = (10925, 23400, 100000, "14", "300p", "1/11.5", EMAP_default) # beam was displaced for ~3mins

runTable_pions_ODU12[8795] = (10350, 23400, 100000, "14", "200p", "1/5", EMAP_default)
runTable_pions_ODU12[8796] = (10350, 23400, 100000, "14", "200p", "1/11.5", EMAP_default)
runTable_pions_ODU12[8797] = (10650, 23400, 100000, "14", "200p", "1/5", EMAP_default)
runTable_pions_ODU12[8798] = (10650, 23400, 100000, "14", "200p", "1/11.5", EMAP_default)
runTable_pions_ODU12[8799] = (10925, 23400, 100000, "14", "200p", "1/5", EMAP_default)
runTable_pions_ODU12[8800] = (10925, 23400, 100000, "14", "200p", "1/11.5", EMAP_default)

runTable_pions_ODU12[8810] = (10350, 23400, 100000, "14", "30p", "1", EMAP_default)
runTable_pions_ODU12[8809] = (10350, 23400, 100000, "14", "30p", "1/5", EMAP_default)
runTable_pions_ODU12[8807] = (10650, 23400, 100000, "14", "30p", "1", EMAP_default)
runTable_pions_ODU12[8806] = (10650, 23400, 100000, "14", "30p", "1/5", EMAP_default)
runTable_pions_ODU12[8803] = (10925, 23400, 100000, "14", "30p", "1", EMAP_default)
runTable_pions_ODU12[8801] = (10925, 23400, 100000, "14", "30p", "1/5", EMAP_default)

runTable_pions_ODU12[8811] = (10350, 23400, 100000, "14", "50p", "1", EMAP_default)
runTable_pions_ODU12[8812] = (10350, 23400, 100000, "14", "50p", "1/5", EMAP_default)
runTable_pions_ODU12[8813] = (10650, 23400, 100000, "14", "50p", "1", EMAP_default)
runTable_pions_ODU12[8814] = (10650, 23400, 100000, "14", "50p", "1/5", EMAP_default)
runTable_pions_ODU12[8815] = (10925, 23400, 100000, "14", "50p", "1", EMAP_default)
runTable_pions_ODU12[8816] = (10925, 23400, 100000, "14", "50p", "1/5", EMAP_default)

runTable_pions_ODU12[8820] = (10350, 23400, 100000, "14", "150p", "1", EMAP_default)
runTable_pions_ODU12[8819] = (10350, 23400, 100000, "14", "150p", "1/3", EMAP_default)
runTable_pions_ODU12[8818] = (10350, 23400, 100000, "14", "150p", "1/9", EMAP_default)
runTable_pions_ODU12[8817] = (10925, 23400, 100000, "14", "150p", "1/11.5", EMAP_default)




######################################
# Put all runs together
###################################### 

runTable_all = {}

for dictionary in [runTable_pions_ODU12, runTable_pions_Aug15,
                   runTable_Aug15, runTable_Aug14, runTable_Aug13,
                   runTable_Ph2_Aug14, runTable_Ph2_Aug15]:
        runTable_all.update(dictionary)

def getEmapFromRun(run):
        if run in runTable_all: 
            emapFile = runTable_all[run][6]
        else:
            if run <= 8823:
               emapFile = EMAP_default
            else:
               emapFile = EMAP_specialODU
        return emapFile

