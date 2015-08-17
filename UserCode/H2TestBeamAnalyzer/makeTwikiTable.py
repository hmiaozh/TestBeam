from tablePos import *

runTable = {}

#runTable[runnumber] = [eta, phi, nev, beamcounters, beamtype]
runTable[8582] = (9884,40500,5000,"134","150m")
runTable[8583] = (9884,36800,5000,"134","150m")
runTable[8584] = (9884,33100,5000,"134","150m")
runTable[8585] = (9884,29400,5000,"134","150m")
runTable[8586] = (9884,25700,5000,"134","150m")
runTable[8587] = (9884,22000,5000,"134","150m")
runTable[8588] = (9884,18300,5000,"134","150m")
runTable[8589] = (9884,14600,5000,"134","150m")
runTable[8590] = (9884,10900,5000,"134","150m")
runTable[8591] = (9884,7200,5000,"134","150m")
runTable[8592] = (9884,3482,5000,"134","150m")

runTable[8594] = (9503,23400,5000,"134","150m")
runTable[8593] = (9573,23400,5000,"134","150m")
runTable[8595] = (9643,23400,5000,"134","150m")
runTable[8596] = (9713,23400,5000,"134","150m")
runTable[8597] = (9783,23400,5000,"134","150m")
runTable[8598] = (9853,23400,5000,"134","150m")
runTable[8599] = (9923,23400,5000,"134","150m")
runTable[8600] = (9993,23400,5000,"134","150m")
runTable[8601] = (10063,23400,5000,"134","150m")
runTable[8602] = (10133,23400,5000,"134","150m")
runTable[8603] = (10205,23400,5000,"134","150m")

runTable[8604] = (10804,40500,5000,"134","150m")
runTable[8606] = (10804,36800,5000,"134","150m")
runTable[8607] = (10804,33100,5000,"134","150m")
runTable[8608] = (10804,29400,5000,"134","150m")
runTable[8609] = (10804,25700,5000,"134","150m")
runTable[8610] = (10804,22000,5000,"134","150m")
runTable[8611] = (10804,18300,5000,"134","150m")
runTable[8612] = (10804,14600,5000,"134","150m")
runTable[8614] = (10804,10900,5000,"134","150m")
runTable[8615] = (10804,7200,5000,"134","150m")
runTable[8616] = (10804,3482,5000,"134","150m")

runTable[8617] = (10517,23400,5000,"134","150m")
runTable[8618] = (10572,23400,5000,"134","150m")
runTable[8619] = (10627,23400,5000,"134","150m")
runTable[8620] = (10682,23400,5000,"134","150m")
runTable[8621] = (10737,23400,5000,"134","150m")
runTable[8622] = (10792,23400,5000,"134","150m")
runTable[8624] = (10847,23400,5000,"134","150m")
runTable[8625] = (10903,23400,5000,"134","150m")
runTable[8626] = (10957,23400,5000,"134","150m")
runTable[8627] = (11012,23400,5000,"134","150m")
runTable[8628] = (11067,23400,5000,"134","150m")
runTable[8629] = (11074,23400,5000,"134","150m")

runTable[8630] = (8200,40500,489257,"134","150m")

runTable[8632] = (11884,40500,5000,"134","150m")
runTable[8633] = (11884,36799,5000,"134","150m")
runTable[8634] = (11884,33099,5000,"134","150m")
runTable[8636] = (11884,29101,5000,"134","150m")
runTable[8637] = (11884,25700,5000,"134","150m")
runTable[8638] = (11884,22101,5000,"134","150m")
runTable[8639] = (11884,21999,5000,"134","150m")
runTable[8640] = (11884,18299,5000,"134","150m")
runTable[8641] = (11884,14599,5000,"134","150m")
runTable[8642] = (11884,10900,5000,"134","150m")
runTable[8643] = (11884,7200,5000,"134","150m")
runTable[8644] = (11884,3482,5000,"134","150m")

runTable[8645] = (11609,23400,5000,"134","150m")
runTable[8646] = (11664,23400,5000,"134","150m")
runTable[8647] = (11717,23400,5000,"134","150m")
runTable[8648] = (11774,23400,5000,"134","150m")
runTable[8649] = (11826,23400,5000,"134","150m")
runTable[8650] = (11882,23400,5000,"134","150m")
runTable[8651] = (11939,23400,5000,"134","150m")
runTable[8652] = (11992,23400,5000,"134","150m")
runTable[8653] = (12048,23400,5000,"134","150m")
runTable[8654] = (12104,23400,5000,"134","150m")
runTable[8655] = (12158,23400,5000,"134","150m")


def makeTwikiFragment(runtable, snippetname):
    """ Create a long format table with all run information for the given runtable. """

    f = open(snippetname, 'w')
    
    f.write("| Run number | Eta | Phi | # events | beam counters | beam type | \n")

    for k in sorted(runTable.keys()):
        l = "| %(run)s | %(teta)s (%(ieta).2f) | %(tphi)s (%(iphi).2f) | %(nev)s | %(bc)s | %(bt)s | \n" % {"run" : k,
                                                                                                            "teta" : runTable[k][0],
                                                                                                            "tphi" : runTable[k][1],
                                                                                                            "nev" : runTable[k][2],
                                                                                                            "bc" : runTable[k][3],
                                                                                                            "bt" : runTable[k][4],
                                                                                                            "ieta": getieta(runTable[k][0]),
                                                                                                            "iphi": getiphi(runTable[k][1])}
        f.write(l)
        
    f.close()


def makeEtaPhiTable(runTable, snippetname):
    """ Create a 2D (eta,phi) table for all runs in the specified runTable. """

    f = open(snippetname, 'w')

    # find all eta values in table
    etaset = set([info[0] for info in runTable.values()])
    # order them
    etalist = sorted(list(etaset))
    
    # find all phi values in table
    phiset = set([info[1] for info in runTable.values()])
    philist = sorted(list(phiset))

    heading = " | ".join([str(phi) for phi in philist])
    f.write("| | Phi | %s |\n" % (heading))
    heading2 = " | ".join(["%.2f"%getiphi(phi) for phi in philist])
    f.write("| Eta | | %s |\n" % (heading2))

    for eta in etalist:
        # construct the line in eta
        ieta = getieta(eta)
        l1 = "| %(eta)s | %(ieta).2f | " % locals()
        
        # go through runs and find all compatible with this eta
        runlist = [" "]*len(philist)
        for r,info in runTable.iteritems():
            if info[0] == eta:
                # find which phi it is
                phi_index = philist.index(info[1])
                runlist[phi_index] = str(r)
        l2 = " | ".join(runlist)
        f.write("%s%s |\n" % (l1, l2))

    f.close()


if __name__ == '__main__':

    print "uncomment what you want to turn into a twiki snippet"
    # makeTwikiFragment(runTable, "twiki1.txt")
    # makeEtaPhiTable(runTable, "twiki2.txt")
