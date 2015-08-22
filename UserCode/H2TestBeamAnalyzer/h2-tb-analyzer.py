import FWCore.ParameterSet.Config as cms
import sys
import optparse
import re

parser = optparse.OptionParser("usage: %prog <input filename> [options]")

parser.add_option('-v', dest="verbose", action="store_true", default=False, help="Runs the analysis in verbose mode.")
parser.add_option('-n', dest="nevents", default="-1", help="Number of events to process.")
parser.add_option('-e', '-m', dest="emap", default=None, help="EMAP file")

options, args = parser.parse_args()

numargs = len(args)
if len(args) != 2:
    print "### ERROR: Wrong number of arguments"
    print "### Usage: cmsRun h2-tb-analyzer.py <input filename> [options]"
    sys.exit(1)

inputFile = sys.argv[2]
inputPattern = re.compile("([0-9]+).root")
m = inputPattern.search(inputFile)
if m:
   runNumber = m.group(1)
else:
   print "### ERROR: Could not extract run number from filename."
   print "### The filename must end in:  xxxxxx.root where xxxxxx is the run number."
   sys.exit(1)

doVerbose = options.verbose

numEvents = -1
if options.nevents.isdigit():
   numEvents = int(options.nevents)
   print "Limit on number of events to process: ",numEvents   

rn = int(runNumber)
if options.emap:
    emapFile = "UserCode/H2TestBeamAnalyzer/" + options.emap
    print "Using EMAP: ",emapFile 	
else:
    if rn <= 8823:
        emapFile = "UserCode/H2TestBeamAnalyzer/EMAP-DEFAULT-ODU.txt"
    else:
        emapFile = "UserCode/H2TestBeamAnalyzer/EMAP-SPECIAL-ODU.txt"
    print "No EMAP Specified.  Using EMAP: ",emapFile

print inputFile,emapFile,doVerbose,numEvents,runNumber

sys.exit(1)

process = cms.Process("H2TestBeam")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(numEvents) )

process.source = cms.Source("HcalTBSource",
    fileNames = cms.untracked.vstring(
        'file:'+inputFile
    )
)

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(False)
        )

process.tbunpack = cms.EDProducer("HcalTBObjectUnpacker",
        IncludeUnmatchedHits = cms.untracked.bool(False),
        ConfigurationFile=cms.untracked.string('UserCode/H2TestBeamAnalyzer/configQADCTDC.txt'),
        HcalSlowDataFED = cms.untracked.int32(3),
        HcalTriggerFED = cms.untracked.int32(1),
        HcalTDCFED = cms.untracked.int32(8),
        HcalQADCFED = cms.untracked.int32(8),
            fedRawDataCollectionTag = cms.InputTag('source')
)

process.hcalDigis = cms.EDProducer("HcalRawToDigi",
#       UnpackHF = cms.untracked.bool(True),
        ### Falg to enable unpacking of TTP channels(default = false)
        ### UnpackTTP = cms.untracked.bool(True),
        FilterDataQuality = cms.bool(False),
        InputLabel = cms.InputTag('source'),
        HcalFirstFED = cms.untracked.int32(700),
        ComplainEmptyData = cms.untracked.bool(False),
#       UnpackCalib = cms.untracked.bool(True),
        firstSample = cms.int32(0),
        lastSample = cms.int32(9)
)

process.hcalDigis.FEDs = cms.untracked.vint32(700,928)

process.hcalAnalyzer = cms.EDAnalyzer('H2TestBeamAnalyzer',
        OutFileName = cms.untracked.string('ana_h2_tb_run'+runNumber+'.root'),
        Verbosity = cms.untracked.int32(0)
)

process.hcalADCHists = cms.EDAnalyzer('adcHists')

#
#   For Debugging: Create a Pool Output Module
#
process.output = cms.OutputModule(
        'PoolOutputModule',
        fileName = cms.untracked.string('cmsrun_out_h2_tb_run'+runNumber+'.root')
)

process.TFileService = cms.Service("TFileService",
       fileName = cms.string("analysis.root"),
)

process.load('Configuration.Geometry.GeometryIdeal_cff')
#process.load('RecoLocalCalo.Configuration.hcalLocalReco_cff')
#process.load('RecoLocalCalo.HcalRecProducers.HcalSimpleReconstructor_hf_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['com10']
from CondCore.DBCommon.CondDBSetup_cfi import *

process.GlobalTag.globaltag = autoCond['startup'] 
#process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

#   EMAP Needed for H2 DATA
process.es_ascii = cms.ESSource('HcalTextCalibrations',
        input = cms.VPSet(
               cms.PSet(
                object = cms.string('ElectronicsMap'),
                file = cms.FileInPath(emapFile)  # EMAP here!
               )
        )
)
process.es_prefer = cms.ESPrefer('HcalTextCalibrations', 'es_ascii')

process.dump = cms.EDAnalyzer("HcalDigiDump")

process.p = cms.Path(process.tbunpack*process.hcalDigis*process.hcalAnalyzer*process.hcalADCHists)
# process.p = cms.Path(process.tbunpack*process.hcalDigis*process.dump*process.hcalAnalyzer)
# process.outpath = cms.EndPath(process.output)

