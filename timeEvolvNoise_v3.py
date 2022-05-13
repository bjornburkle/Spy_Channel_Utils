# Better written bjorn code

from ROOT import TFile, TH1F, TProfile, TGraph, TCanvas, TStyle, TAxis, TPad,gROOT
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import datetime
import csv
from getEventNumber import getFileEvents

gROOT.SetBatch(1)
c1 = TCanvas("c1","c1",50,50,800,600)

spyprofiles = {}
meanList = []
count=1
counter=1
dictOfStuff = {}
if len(sys.argv)==2:
    partition = sys.argv[1]
else:
    partition = 'TP'
newtimes = []
runNumber = '346439'
#runNumber = '321779'
#argFileName = partition+"_"+runNumber+"_argText.txt"
argFileName = '/afs/cern.ch/work/b/bburkle/public/CMSSW_GitHub/CMSSW_12_1_0/src/DQM/'+partition+"_argText.txt"
argFile = open(argFileName, "r")
lines = argFile.readlines()
Nevent = int(lines[-1].split(', ')[1])
#Nevent = 128

#interval = 100
#Nbins = Nevent/interval
#profile = TProfile(partition,'Noise in 100 Event Intervals', Nbins, 0.0, Nbins*100)
interval = 5
Nbins = Nevent//interval
profile = TProfile(partition,'Noise in %d Event Intervals'%interval, Nbins, 0.0, Nbins*interval)
#count=0
#inputFilePath = '/eos/cms/store/user/jblee/SpyNoise/'+runNumber+'/'+partition+'/'
inputFilePath = '/eos/user/b/bburkle/SpyNoise/'+runNumber+'/'

dataFileNames = getFileEvents(inputFilePath, runNumber, partition)
if not len(dataFileNames) == len(lines):
    print('Expected %d root files but was able to match with %d' % (len(lines), len(dataFileNames)))
    quit()
      
for indx in range(1, Nbins+1):
    #dataFileName = inputFilePath+"SiStripCommissioningSource_TP_09-JUN-2009_1_00321779_137.138.063.155_32457.root"
    #dataFileName = 'SiStripCommissioningSource_TP_09-JUN-2009_1_00346345_188.184.028.066_30944.root'
    #dataFileName = 'SiStripCommissioningSource_TP_09-JUN-2009_1_00321779_188.184.028.066_28323.root'
    dataFileName = dataFileNames[indx-1][1]

    print(dataFileName)
    dataFile = TFile(dataFileName, 'READ')
    meanList = []

    def loopTFile(tDir):
        for i in tDir.GetListOfKeys():
            if not i.IsFolder():
                if 'Noise' in str(i.GetName()):
                    binContents = []
                    spyprofiles[i.GetName()+str(count)] = dataFile.Get('{0}/{1}'.format(tDir.GetPath().split(':')[1],i.GetName()))
                    spyprofiles[i.GetName()+str(count)].SetLineColor(4)
                    NBins = spyprofiles[i.GetName()+str(count)].GetNbinsX()
                    rangeOfBins = list(range(NBins))
                    rangeOfBins.append(NBins)
                    rangeOfBins.remove(0)
                    for bin in rangeOfBins:
                        binValue = spyprofiles[i.GetName()+str(count)].GetBinContent(bin)
                        profile.Fill(indx*interval-0.001, binValue)
                else:
                    continue
            else:   
                iFolder = i.ReadObj()
                loopTFile(iFolder)

    loopTFile(dataFile)        

    '''
    for i in dataFile.GetListOfKeys():
        iFolder = i.ReadObj()
        print(iFolder.GetName())
        if not i.IsFolder(): continue
        for j in iFolder.GetListOfKeys():
            jFolder = j.ReadObj()
            print(jFolder.GetName())
            if not j.IsFolder(): continue
            for k in jFolder.GetListOfKeys():	
                kFolder = k.ReadObj()
                print(kFolder.GetName())
                if not k.IsFolder(): continue
                if not kFolder.IsA().InheritsFrom('TDirectoryFile'): continue                                            
                for l in kFolder.GetListOfKeys():
                    lFolder = l.ReadObj()
                    print(lFolder.GetName())                                                
                    if not l.IsFolder(): continue
                    for m in lFolder.GetListOfKeys():
                        mFolder = m.ReadObj()
                        #print(mFolder.GetName())                                                
                        if not m.IsFolder(): continue
                        for n in mFolder.GetListOfKeys():
                            nFolder = n.ReadObj()
                            #print(nFolder.GetName())                                                
                            if not n.IsFolder(): continue
                            for o in nFolder.GetListOfKeys():
                                oFolder = o.ReadObj()
                                #print(oFolder.GetName())                                                
                                if not o.IsFolder(): continue
                                for q in oFolder.GetListOfKeys():
                                    qOject = q.ReadObj()
                                    #print(qObject.GetName())                                                
                                    if 'Noise' in str(q.GetName()):
                                       #print(q.GetName())
                                       binContents = []
                                       spyprofiles[q.GetName()+str(count)] = dataFile.Get('{0}/{1}'.format(oFolder.GetPath().split(':')[1],q.GetName()))
                                       spyprofiles[q.GetName()+str(count)].SetLineColor(4)
                                       NBins = spyprofiles[q.GetName()+str(count)].GetNbinsX()
                                       rangeOfBins = list(range(NBins))
                                       rangeOfBins.append(NBins)
                                       rangeOfBins.remove(0)
                                       for bin in rangeOfBins:	
                                          binValue = spyprofiles[q.GetName()+str(count)].GetBinContent(bin)
                                          #profile.Fill(indx*100, binValue)
                                          profile.Fill(indx*interval-0.001, binValue)
    '''
    dataFile.Close()

file = TFile('noiseEvolution_'+partition+'_'+runNumber+'TEST.root','recreate')
#profile.GetYaxis().SetRangeUser(5.0, 7.0)
profile.Write()
file.Close()
