import os,sys
from ROOT import *


scriptsList = ['jobsTI.sh','jobsTM.sh','jobsTP.sh','jobsTO.sh']
runNumber = '346439'
#scriptsList = ['jobsTP_'+runNumber+'.sh']

note=''

interval = 5

for script in scriptsList:
    #try:
    #    os.mkdir('condor_jobs')
    #except:
    #    pass
    #try:
    #    os.mkdir('condor_jobs/'+script.split("jobs")[1].split(".sh")[0])
    #except:
    #    print("aleady exists")
    part = script.split("jobs")[1].split(".sh")[0]
    os.system('mkdir -p condor_jobs/'+runNumber+'/'+part)

    for bashline in open(script).readlines():
        if "sourcefromedm" in bashline[:-1]:
            cfgFile = bashline[:-1].split("cmsRun ")[1].split(" first")[0] 
            print("cfgFile : ",cfgFile)
            for cfgline in open(cfgFile).readlines():
                if "inputPath" in cfgline and "/eos/" in cfgline:
                    filePath = cfgline[:-1].split("inputPath = ")[1][1:-1]
                if "infilename" in cfgline and "run" in cfgline: 
                    temp = cfgline[:-1].split("/run")[1]
                    file = "run"+temp[:-1]
                    runNumber = temp[:-6]
    print("filePath : ",filePath)
    #rootFile = TFile(filePath+"/"+runNumber+"/"+file)
    rootFile = TFile(filePath+"/"+file)
    tree = rootFile.Get("Events")
    totalNentries = tree.GetEntries()
    Nsplit = totalNentries//interval
    argFileName = part+"_argText.txt"
    path = os.getcwd()+"/condor_jobs/"+runNumber+"/"+part+"/"
    print("argFileName : ", argFileName)
    dict={'PARTITION':part,'SCRIPT':script, 'ARGFileName':argFileName,'PATH':path}        
    ArgFile = open(part+"_argText.txt","w")
    for start in range(0, Nsplit):
        string = str(1+start*interval)+', '+str((start+1)*interval)+'\n'
        ArgFile.write(string)
        last = (start+1)*interval 
    string = str(last)+', '+str(last+totalNentries%interval)
    ArgFile.write(string)
    
    jdfName='condor_script_%(PARTITION)s.job'%dict
    print(jdfName)
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(SCRIPT)s
Output = %(PATH)s%(SCRIPT)s$(start).out
Error = %(PATH)s%(SCRIPT)s$(start).err
Log = %(PATH)s%(SCRIPT)s$(start).log
Notification = Never
Arguments = $(start) $(end)

queue start,end from %(ARGFileName)s"""%dict)
    jdf.close()
#     os.system('condor_script_%(PARTITION)s.job'%dict)

