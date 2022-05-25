## Configuration for testing the FED processing monitor module
##=============================================================

import FWCore.ParameterSet.Config as cms
import sys, os
from Configuration.AlCa.GlobalTag import GlobalTag
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.register('start',
    default=-1,
    mult=VarParsing.VarParsing.multiplicity.singleton,
    mytype=VarParsing.VarParsing.varType.int,
    info='First event to process')
options.register('end',
    default=-1,
    mult=VarParsing.VarParsing.multiplicity.singleton,
    mytype=VarParsing.VarParsing.varType.int,
    info='Last event to process')
options.register('run',
    default=0,
    mult=VarParsing.VarParsing.multiplicity.singleton,
    mytype=VarParsing.VarParsing.varType.int,
    info='run number of event being processed')
options.register('clusterFilter',
    default=1,
    mult=VarParsing.VarParsing.multiplicity.singleton,
    mytype=VarParsing.VarParsing.varType.int,
    info='Use ZS signal to subtract strips with clusters from common mode')
options.register('TEST',
    default=0,
    mult=VarParsing.VarParsing.multiplicity.singleton,
    mytype=VarParsing.VarParsing.varType.int,
    info='Run in test mode. Makes nEvts=5 and output=test.root')
options.parseArguments()

process = cms.Process('SiStripSpyCMslope')

run_number = options.run
start = options.start
end = options.end
#run_number = 321054

filter_str = ''
if options.clusterFilter:
    filter_str='_cluster_filtered'

str_dict = {'run':run_number,'start':start,'end':end, 'filter':filter_str}
range_string = '%(run)d:%(start)d-%(run)d:%(end)d' % str_dict
input_file = 'file:/eos/cms/store/group/dpg_tracker_strip/tracker/Online/store/data/SpyRuns/run%(run)d/run%(run)d.root' % str_dict

maxEvts = -1
if options.TEST:
    maxEvts = 5
    process.load("DQM.SiStripCommon.MessageLogger_cfi")


process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        input_file,
	    ),
	#eventsToProcess = cms.untracked.VEventRange(range_string),
    skipEvents = cms.untracked.uint32(0)
    )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(maxEvts) )

## ---- Conditions ----

## Global tag see SWGuideFrontierConditions
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
#process.load("Configuration.Geometry.GeometryRecoDB_cff")

# --- The unpacking configuration ---
process.load('DQM.SiStripMonitorHardware.SiStripSpyUnpacker_cfi')
process.load('DQM.SiStripMonitorHardware.SiStripSpyDigiConverter_cfi')

# * Scope digi settings
process.SiStripSpyUnpacker.FEDIDs = cms.vuint32()                   #use a subset of FEDs or leave empty for all.
process.SiStripSpyUnpacker.InputProductLabel = cms.InputTag('rawDataCollector')
process.SiStripSpyUnpacker.AllowIncompleteEvents = True
process.SiStripSpyUnpacker.StoreCounters = True
process.SiStripSpyUnpacker.StoreScopeRawDigis = cms.bool(True)      # Note - needs to be True for use in other modules.
## * Module digi settings
process.SiStripSpyDigiConverter.InputProductLabel = cms.InputTag('SiStripSpyUnpacker','ScopeRawDigis')
process.SiStripSpyDigiConverter.StorePayloadDigis = True
process.SiStripSpyDigiConverter.StoreReorderedDigis = True
process.SiStripSpyDigiConverter.StoreModuleDigis = True
process.SiStripSpyDigiConverter.StoreAPVAddress = True
process.SiStripSpyDigiConverter.MinDigiRange = 100
process.SiStripSpyDigiConverter.MaxDigiRange = 1024
process.SiStripSpyDigiConverter.MinZeroLight = 0
process.SiStripSpyDigiConverter.MaxZeroLight = 1024
process.SiStripSpyDigiConverter.MinTickHeight = 0
process.SiStripSpyDigiConverter.MaxTickHeight = 1024
process.SiStripSpyDigiConverter.ExpectedPositionOfFirstHeaderBit = 6
process.SiStripSpyDigiConverter.DiscardDigisWithWrongAPVAddress = False

# --- Fed Emulation Configuration ---
process.load('DQM.SiStripMonitorHardware.SiStripFEDEmulator_cfi')
process.SiStripFEDEmulator.SpyReorderedDigisTag = cms.InputTag('SiStripSpyDigiConverter','SpyReordered')
process.SiStripFEDEmulator.SpyVirginRawDigisTag = cms.InputTag('SiStripSpyDigiConverter','SpyVirginRaw')
process.SiStripFEDEmulator.ByModule = cms.bool(True) #use the digis stored by module (i.e. detId)


# --- Configuration for Common Mode Analysis ---

## ---- if running on matched events     ----
process.load('EventFilter.SiStripRawToDigi.SiStripDigis_cfi')
#process.siStripDigis.ProductLabel = cms.InputTag('source')
process.siStripDigis.UnpackCommonModeValues = cms.bool(True)


## ---- SpyChannel Monitoring ----
## For spy channel monitoring plugin
process.load('DQM.SiStripMonitorHardware.SiStripSpyCMslope_cfi')

if options.clusterFilter:
    process.SiStripSpyCMslope.filterClusters = cms.bool(True)
else:
    process.SiStripSpyCMslope.filterClusters = cms.bool(False)

# ---- ESProducers for Tracker Geometry ----
#process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.TrackerNumberingBuilder.trackerTopology_cfi")
process.load("Geometry.TrackerGeometryBuilder.trackerParameters_cfi")
process.load("Geometry.TrackerGeometryBuilder.trackerGeometry_cfi")
#process.load("Geometry.TrackerNumberingBuilder.trackerNumberingGeometry_cfi") # in extended
process.load("Geometry.CMSCommonData.cmsExtendedGeometry2017XML_cfi")
#process.load("Geometry.CMSCommonData.cmsExtendedGeometry2021XML_cfi")
process.load("RecoTracker.GeometryESProducer.TrackerRecoGeometryESProducer_cfi")
process.load('CalibTracker.SiStripESProducers.SiStripQualityESProducer_cfi') ## as in stream express, no info on bad-channels, DetOff ..                                           etc..                                                    
process.siStripQualityESProducer.ListOfRecordToMerge = cms.VPSet(
#    cms.PSet( record = cms.string("SiStripDetVOffRcd"),    tag    = cms.string("") ),
    cms.PSet( record = cms.string("SiStripDetCablingRcd"), tag    = cms.string("") ),
    cms.PSet( record = cms.string("SiStripBadStripRcd"),   tag    = cms.string("") ),
    cms.PSet( record = cms.string("SiStripBadChannelRcd"), tag    = cms.string("") ),
    cms.PSet( record = cms.string("SiStripBadFiberRcd"),   tag    = cms.string("") ),
    cms.PSet( record = cms.string("SiStripBadModuleRcd"),  tag    = cms.string("") )
    )
#process.siStripQualityESProducer.UseEmptyRunInfo = cms.bool(False)
#process.load('Configuration.Geometry.GeometryExtended_cff')
#process.load('Configuration.Geometry.GeometryExtended2017_cff')
#process.load('Configuration.Geometry.GeometryExtended2017_cff')
process.trackerTopology = cms.ESProducer("TrackerTopologyEP")
process.geometricDet = cms.ESProducer("TrackerGeometricDetESModule")
#process.PTrackerAdditionalParametersPerDetRcd = cms.ESProducer("TrackerAdditionalParametersPerDetESModule")
process.TrackerAdditionalParametersPerDet = cms.ESProducer("TrackerAdditionalParametersPerDetESModule")
#process.DQMStore = cms.Service("DQMStore",
#    verbose = cms.untracked.int32(1)
#)

## Select the detIDs of choice here
process.SiStripSpyCMslope.detIDs = cms.vuint32(
    )
process.SiStripSpyCMslope.InputPostPedestalRawDigiLabel     = cms.InputTag("SiStripFEDEmulator","PedSubtrModuleDigis")
process.SiStripSpyCMslope.InputZeroSuppressedDigiLabel      = cms.InputTag("SiStripFEDEmulator","ZSModuleDigis")

##mainline data - if running on matched events
process.SiStripSpyCMslope.OutputFolderName = cms.string("CMslope")

## ---- Sequence ----
process.p = cms.Path(
    process.SiStripSpyUnpacker
    *process.SiStripSpyDigiConverter
    *process.SiStripFEDEmulator
    *process.SiStripSpyCMslope
    )

if not os.path.isdir('/eos/user/b/bburkle/SpyChannel/%d%s' % (run_number, filter_str)):
    os.makedirs('/eos/user/b/bburkle/SpyChannel/%d%s' % (run_number, filter_str))

outString = 'file:/eos/user/b/bburkle/SpyChannel/%(run)d%(filter)s/CMSlope_%(run)d_%(start)d-%(end)d.root' % str_dict 

if options.TEST:
    outString = 'file:test.root'
    process.SiStripSpyCMslope.DEBUG = cms.bool(True)

## ------ TFileService
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string( outString ),
    )

