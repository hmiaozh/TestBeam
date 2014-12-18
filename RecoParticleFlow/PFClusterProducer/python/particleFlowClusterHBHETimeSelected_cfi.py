import FWCore.ParameterSet.Config as cms
particleFlowClusterHBHETimeSelected = cms.EDProducer(
    "PFClusterTimeSelector",
    src = cms.InputTag('particleFlowClusterHBHE'),

    cuts = cms.VPSet(
        cms.PSet(
            depth=cms.double(1.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(False),
            minTime = cms.double(-22.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(2.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(False),
            minTime = cms.double(-22.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(3.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(False),
            minTime = cms.double(-20.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(1.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(False),
            minTime = cms.double(-20.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(2.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(False),
            minTime = cms.double(-15.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(3.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(False),
            minTime = cms.double(-15.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(1.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(False),
            minTime = cms.double(-10.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(2.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(False),
            minTime = cms.double(-8.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(3.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(False),
            minTime = cms.double(-8.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(1.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(True),
            minTime = cms.double(-20.),
            maxTime = cms.double(10.)
        ),
        cms.PSet(
            depth=cms.double(2.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(True),
            minTime = cms.double(-15.),
            maxTime = cms.double(10.)
        ),
        cms.PSet(
            depth=cms.double(3.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(10.)
        ),
        cms.PSet(
            depth=cms.double(4.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(5.0),
            minEnergy = cms.double(0.0),
            maxEnergy = cms.double(2.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(5.)
        ),

        cms.PSet(
            depth=cms.double(1.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(True),
            minTime = cms.double(-15.),
            maxTime = cms.double(10.)
        ),
        cms.PSet(
            depth=cms.double(2.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(10.)
        ),
        cms.PSet(
            depth=cms.double(3.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(10.)
        ),
        cms.PSet(
            depth=cms.double(4.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(5.)
        ),
        cms.PSet(
            depth=cms.double(5.0),
            minEnergy = cms.double(2.0),
            maxEnergy = cms.double(5.0),
            endcap = cms.bool(True),
            minTime = cms.double(-12.),
            maxTime = cms.double(5.)
        ),

        cms.PSet(
            depth=cms.double(1.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(True),
            minTime = cms.double(-25.),
            maxTime = cms.double(35.)
        ),
        cms.PSet(
            depth=cms.double(2.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(True),
            minTime = cms.double(-25.),
            maxTime = cms.double(35.)
        ),
        cms.PSet(
            depth=cms.double(3.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(True),
            minTime = cms.double(-25.),
            maxTime = cms.double(35.)
        ),
        cms.PSet(
            depth=cms.double(4.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(True),
            minTime = cms.double(-25.),
            maxTime = cms.double(35.)
        ),
        cms.PSet(
            depth=cms.double(5.0),
            minEnergy = cms.double(5.0),
            maxEnergy = cms.double(1000000.0),
            endcap = cms.bool(True),
            minTime = cms.double(-25.),
            maxTime = cms.double(25.)
        )
)



)

    
