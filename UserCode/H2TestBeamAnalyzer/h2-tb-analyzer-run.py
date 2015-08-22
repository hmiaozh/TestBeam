import FWCore.ParameterSet.Config as cms

import sys
if len(sys.argv) != 7:
    print len(sys.argv)
    print "### ERROR: No Run File has been provided"
    print "### Usage: cmsRun h2-tb-analyzer-run.py <input file> <emap file> <verbose flag> <num events> <run number>"
    sys.exit(1)

inputFile = sys.argv[2]
emapFile = sys.argv[3]
doVerbose = int(sys.argv[4])
numEvents = int(sys.argv[5])
if numEvents == 0: numEvents = -1
runNumber = sys.argv[6]

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
        Verbosity = cms.untracked.int32(doVerbose)
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

if doVerbose:
    process.p = cms.Path(process.tbunpack*process.hcalDigis*process.dump*process.hcalAnalyzer*process.hcalADCHists)
else:
    process.p = cms.Path(process.tbunpack*process.hcalDigis*process.hcalAnalyzer*process.hcalADCHists)

# process.outpath = cms.EndPath(process.output)
