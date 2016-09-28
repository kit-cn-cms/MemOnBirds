from Definitions import *
import ROOT
import os
import stat
import glob

def create_script(cmsswpath,samplesname,rootfile):
    print samplename
    script='#!/bin/bash\n'
    script+='export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n'
    script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
    script+='cd '+cmsswpath+'src\neval `scram runtime -sh`\n'
    script+='python '+cmsswpath+'src/MEMDataBase/MEMDataBase/test/createDataBaseFromTree_new.py '+OutputDirectoryForMEMDatabase+' '+samplename+' '+rootfile
    filename='scripts_database/'+samplename+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)
    
    
rootfiles=glob.glob(OutputDirectoryForMEMTrees+'*.root')
samplenames=[samplename.replace(OutputDirectoryForMEMTrees,"").replace(".root","") for samplename in rootfiles]
#print rootfiles
#print samplenames

for rootfile,samplename in zip(rootfiles,samplenames):
    print samplename,rootfile
    create_script(cmsswpath,samplename,rootfile)