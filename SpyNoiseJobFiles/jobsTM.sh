#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
#cd /afs/cern.ch/work/b/bburkle/public/copy_of_jblee/CMSSW_10_6_0_pre4/src
cd /afs/cern.ch/work/b/bburkle/public/CMSSW_GitHub/CMSSW_12_1_0/src/DQM
eval `scramv1 runtime -sh`
#export CONFDB=cms_trk_r/1A3C5E7G:FIN@cms_omds_lb
export CONFDB=cms_trk_r/Liwcer_2_JUI@cms_omds_lb
#export CONFDB=cms_trk_r/Liwcer_2_JUI@cmsonr1
cmsRun sourcefromedm_TM_09-JUN-2009_1_346439_cfg.py first=$1 last=$2

echo "Done"
