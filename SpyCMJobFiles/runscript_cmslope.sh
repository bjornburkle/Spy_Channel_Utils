#!/bin/bash

RunNumber=$1
EventStart=$2
EventEnd=$3
FilterCluster=0


currentDir=/afs/cern.ch/work/b/bburkle/public/CMSSW_GitHub/CMSSW_12_1_0/src/DQM/SiStripMonitorHardware/test
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
cd $currentDir
eval `scramv1 runtime -sh`

cmsRun ${currentDir}/spyCMslopeMonitor_cfg.py start=$EventStart end=$EventEnd run=$RunNumber clusterFilter=$FilterCluster

