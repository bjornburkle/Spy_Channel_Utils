import os, sys
import ROOT as r
r.gROOT.SetBatch(r.kTRUE) # suppress plotting
import glob

inDir = '/eos/user/b/bburkle/SpyChannel/346439_cluster_filtered'
outDir = './CMPlots/346439_cluster_filtered'

rootDir = 'SiStripSpyCMslope/CMslope'

pltEvery = 1 # make plots for every N events

# can choose what distributions you want to make, and other paramters here
toPlot = {
    'CommonModeSlope': {
        'xname': 'event',
        'yname': 'Average CM slope per APV',
        'allPart': True,
        'ymax': 0.1,
        'ymin': -0.1,
    },
    'CommonModeAverage': {
        'xname': 'event',
        'yname': 'Average ADC Count Per Strip',
        'allPart': True,
        'ymax': 150,
        'ymin': 100
    },
}

def getEvtDirs(tfile):
    d = tfile.Get(rootDir)
    keys = [key.GetName() for key in d.GetListOfKeys()]
    evtDirs = [key for key in keys if 'event' in key] # only get TDirectories with event in the name
    evtDirs.sort(key = lambda x: int(x.split('event')[-1])) # sort them based one event number
    return evtDirs

def getDetIds(tfile):
    d = tfile.Get(rootDir+'/Det_IDs')
    keys = [key.GetName() for key in d.GetListOfKeys()]
    keys = [int(key.split('_')[-1]) for key in keys if len(key.split('_')) == 2] # only keeps keys with 2 arguments -> detId_<number> then split to just get det Ids being monitored
    for Id in keys:
        os.system('mkdir -p %s/DetId_%d' % (outDir, Id))
    return keys

def parseRootFile(tfile, evtDirs, pltType):

    nEvts = len(evtDirs)
    c1 = r.TCanvas()

    h_all = r.TH1D("h_%s_all" % pltType, pltType, nEvts+1, 0, nEvts)
    h_TIB = r.TH1D("h_%s_TIB" % pltType, "", nEvts+1, 0, nEvts)
    h_TOB = r.TH1D("h_%s_TOB" % pltType, "", nEvts+1, 0, nEvts)
    h_TID = r.TH1D("h_%s_TID" % pltType, "", nEvts+1, 0, nEvts)
    h_TEC = r.TH1D("h_%s_TEC" % pltType, "", nEvts+1, 0, nEvts)


    for eDir in evtDirs:

        evt = int(eDir.split('event')[-1])
        tempDir = rootDir+'/'+eDir

        h_ev_all = r.TH1D()
        h_ev_TIB = r.TH1D()
        h_ev_TOB = r.TH1D()
        h_ev_TID = r.TH1D()
        h_ev_TEC = r.TH1D()

        tfile.GetObject(tempDir+'/%s' % pltType, h_ev_all)
        if toPlot[pltType]['allPart']:
            tfile.GetObject(tempDir+'/%s_Event_TIB' % pltType, h_ev_TIB)
            tfile.GetObject(tempDir+'/%s_Event_TOB' % pltType, h_ev_TOB)
            tfile.GetObject(tempDir+'/%s_Event_TID' % pltType, h_ev_TID)
            tfile.GetObject(tempDir+'/%s_Event_TEC' % pltType, h_ev_TEC)

        if evt % pltEvery == 0:
            if toPlot[pltType]['allPart']:
                #hs = r.THStack('hs', pltType, h_ev_all.GetNbinsX(), h_ev_all.GetBinLowEdge(1), h_ev_all.GetBinLowEdge(h_ev_all.GetNbinsX()+1))
                hs = r.THStack('hs', "")

                h_ev_all.SetLineColor(r.kBlack)

                h_ev_TIB.SetFillColor(2)
                h_ev_TIB.SetLineColor(2)
                h_ev_TOB.SetFillColor(3)
                h_ev_TOB.SetLineColor(3)
                h_ev_TID.SetFillColor(4)
                h_ev_TID.SetLineColor(4)
                h_ev_TEC.SetFillColor(802)
                h_ev_TEC.SetLineColor(802)

                hs.Add(h_ev_TIB)
                hs.Add(h_ev_TOB)
                hs.Add(h_ev_TID)
                hs.Add(h_ev_TEC)

                h_ev_all.Draw('hist')

                hs.Draw('same')
                hs.SetTitle(pltType+'Event '+str(evt))
                hs.GetXaxis().SetTitle(toPlot[pltType]['yname'])
                hs.GetYaxis().SetTitle('N APV Pairs')


                leg = r.TLegend(0.62,0.75, 0.92, 0.95)
                leg.AddEntry(h_ev_all, 'Sum of All Partitions')
                leg.AddEntry(h_ev_TIB, 'TIB')
                leg.AddEntry(h_ev_TOB, 'TOB')
                leg.AddEntry(h_ev_TID, 'TID')
                leg.AddEntry(h_ev_TEC, 'TEC')
                leg.Draw()

                c1.SaveAs('%s/%s/event%d.png' % (outDir, pltType, evt))
            else:
                h_ev_all.Draw('hist')
                c1.SaveAs('%s/%s/event%d.png' % (outDir, pltType, evt))

        else:
            pass

        h_all.Fill(evt, h_ev_all.GetMean())
        if toPlot[pltType]['allPart']:
            h_TIB.Fill(evt, h_ev_TIB.GetMean())
            h_TOB.Fill(evt, h_ev_TOB.GetMean())
            h_TID.Fill(evt, h_ev_TID.GetMean())
            h_TEC.Fill(evt, h_ev_TEC.GetMean())

    if 'xname' in toPlot[pltType]:
        h_all.GetXaxis().SetTitle(toPlot[pltType]['xname'])
    if 'yname' in toPlot[pltType]:
        h_all.GetYaxis().SetTitle(toPlot[pltType]['yname'])
    if 'ymin' in toPlot[pltType] and 'ymax' in toPlot[pltType]:
        h_all.GetYaxis().SetRangeUser(toPlot[pltType]['ymin'], toPlot[pltType]['ymax'])

    r.gStyle.SetOptStat(0)

    h_all.SetLineColor(1)
    h_TIB.SetLineColor(2)
    h_TOB.SetLineColor(3)
    h_TID.SetLineColor(4)
    h_TEC.SetLineColor(802)

    h_all.Draw('hist')
    if toPlot[pltType]['allPart']:
        h_TIB.Draw('hist same')
        h_TOB.Draw('hist same')
        h_TID.Draw('hist same')
        h_TEC.Draw('hist same')

        leg = r.TLegend(0.62,0.75, 0.92, 0.95)
        leg.AddEntry(h_all, 'Sum of all partitions')
        leg.AddEntry(h_TIB, 'TIB')
        leg.AddEntry(h_TOB, 'TOB')
        leg.AddEntry(h_TID, 'TID')
        leg.AddEntry(h_TEC, 'TEC')
        leg.Draw()

    c1.SaveAs('%s/%s.png' % (outDir, pltType) )

    return

def plotDetIds(tfile, evtDirs, detIds):

    c1 = r.TCanvas()

    for eDir in evtDirs:
        evt = int(eDir.split('event')[-1])
        if evt % pltEvery == 0:
            tempDir = rootDir+'/'+eDir
            for Id in detIds:
                pp = r.TH1S()
                zs = r.TH1S()

                tfile.GetObject('%s/DetId%d_PostPedestal_event%d' % (tempDir, Id, evt), pp)
                tfile.GetObject('%s/DetId%d_ZeroSuppressed_event%d' % (tempDir, Id, evt), zs)

                pp.SetTitle('DetId%d_PostPedestal_event%d' % (Id, evt))
                pp.Draw()
                c1.SaveAs('%s/DetId_%d/PostPedestal_event%d.png' % (outDir, Id, evt))
                zs.SetTitle('DetId%d_ZeroSuppressed_event%d' % (Id, evt))
                zs.Draw()
                c1.SaveAs('%s/DetId_%d/ZeroSuppressed_event%d.png' % (outDir, Id, evt))
        else:
            pass

    return

def main():
    os.system('mkdir -p %s' % outDir)
    tfile = r.TFile(glob.glob(inDir+'/*')[0], 'READ')
    evtDirs = getEvtDirs(tfile)
    detIds = getDetIds(tfile)
    for pltType in toPlot.keys():
        os.system('mkdir -p %s/%s' % (outDir, pltType))
        parseRootFile(tfile, evtDirs, pltType)
    plotDetIds(tfile, evtDirs, detIds)
    return 

if __name__ == '__main__':
    main()
