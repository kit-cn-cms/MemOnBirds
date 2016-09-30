from Definitions import *
import ROOT
import os
import stat
import glob

def create_script(cmsswpath,samplename,rootfile,systematic,syst):
    #print samplename
    script='#!/bin/bash\n'
    script+='export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n'
    script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
    script+='cd '+cmsswpath+'src\neval `scram runtime -sh`\n'
    script+='mkdir '+OutputDirectoryForMEMDatabase_ETH+samplename+systematic+'\n'
    script+='python '+cmsswpath+'src/MEMDataBase/MEMDataBase/test/createDataBaseFromTree_ETH.py '+OutputDirectoryForMEMDatabase_ETH+samplename+systematic+' '+samplename+' '+str(syst)+' '+rootfile
    filename='scripts_database_ETH/'+samplename+systematic+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

path_ETH_trees="/nfs/dust/cms/user/kelmorab/ETHmems/"
#cmsswpath='/nfs/dust/cms/user/mwassmer/CMSSW_8_0_19/'
systematics=["nominal","JESUP","JESDOWN","JERUP","JERDOWN"] 
systs=[0,1,2,3,4]
rootfiles=glob.glob(path_ETH_trees+'*.root')
samples=[rootfile.replace(path_ETH_trees,"").replace(".root","").replace("_","") for rootfile in rootfiles]
#samplenames=[samplename.replace(OutputDirectoryForMEMTrees,"").replace(".root","") for samplename in rootfiles]
print rootfiles
print samples


for rootfile,sample in zip(rootfiles,samples):
    print sample,rootfile
    #create_script(cmsswpath,samplename,rootfile)
    for systematic,syst in zip(systematics,systs):
      print systematic,syst
      create_script(cmsswpath,sample,rootfile,systematic,syst)
