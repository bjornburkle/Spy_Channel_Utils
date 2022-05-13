import os, sys
import subprocess
import glob

def getFileEvents(inPath, run, part):
    '''
    SiStripCommissioningSource.cc names output file based on the IP address that ran the script
    When running on condor, this is the IP address of the condor node
    which is given in the log files.

    Condor log files are named based off of the first event
    so can use that to associate output root filename with
    corresponding event range the job was run over
    '''

    #condor_dir = 'condor_jobs/%s/%s' % (run, part)
    condor_dir = '/afs/cern.ch/work/b/bburkle/public/CMSSW_GitHub/CMSSW_12_1_0/src/DQM/condor_jobs/%s/%s' % (run, part)
    #condor_files = glob.glob(condor_dir+'/*.log')
    rootFiles = glob.glob('%s/*%s*.root' % (inPath, part))

    #condor_files.sort(key = lambda x: int(x.split('.')[1].split('sh')[0]))
    ip_list = subprocess.check_output('grep "executing on host" %s/*' % condor_dir, shell=True).splitlines()
    eInfo = [(str(line).split('.log')[0].split('.sh')[-1], str(line).split('<')[1].split(':')[0]) for line in ip_list]

    files = []
    for event, ip in eInfo:
        # assuming there is only one occurance of each IP and partition
        ip = '.'.join([i.zfill(3) for i in ip.split('.')])
        #print('%s/*%s*%s*%s.root' % (inPath, part, run, ip))
        rootFile = glob.glob('%s/*%s*%s*%s*.root' % (inPath, part, run, ip))
        if not len(rootFile) == 1:
            print('Error, found %d matches for following run number, partition, and host IP address:' % len(rootFile))
            print(run, part, ip)
            print(rootFile)
            continue
        files.append([int(event), rootFile[0]])

    files.sort(key = lambda x: x[0])
    print('Found following event and root file combinations:\n', files)

    return files
        
