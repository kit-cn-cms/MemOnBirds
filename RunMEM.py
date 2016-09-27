from Definitions import *
import ROOT
import os
import stat
def get_event_ranges(number_of_events_per_job,sample):
    n_entries=sample.GetEntries()
    #print n_entries
    #print number_of_events_per_job
    ranges=[]
    i=0
    while (((i+1)*number_of_events_per_job)<n_entries):
      range_=[]
      range_.append(i*number_of_events_per_job)
      range_.append((i+1)*number_of_events_per_job-1)
      ranges.append(range_)
      i=i+1
    ranges.append([i*number_of_events_per_job,int(n_entries-1)])
    return ranges
  
def create_script(cmsswpath,looperpath,rootfile,firstevent,lastevent,jobnumber,samplename,do_mem):
    script='#!/bin/bash\n'
    script+='export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n'
    script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
    script+='cd '+cmsswpath+'src\neval `scram runtime -sh`\n'
    if do_mem:
      script+='python '+looperpath+'cc_looper_new.py --infile '+InputDirectoryOfMEMTrees+rootfile+' --firstEvent '+str(firstevent)+' --lastEvent '+str(lastevent)+' --outfile '+OutputDirectoryForMEMTrees+samplename+'_'+str(jobnumber)+'.root'+' --conf CSV --doMem'
    else:
      script+='python '+looperpath+'cc_looper_new.py --infile '+InputDirectoryOfMEMTrees+rootfile+' --firstEvent '+str(firstevent)+' --lastEvent '+str(lastevent)+' --outfile '+OutputDirectoryForMEMTrees+samplename+'_'+str(jobnumber)+'.root'+' --conf CSV'
    filename=samplename+'_'+str(jobnumber)+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)
    
    
    
do_mem=True
  
trees=[]  
plot_ranges=[]
  
for sample in Samples:
  tree = ROOT.TChain("tree",sample[0])
  tree.Add(InputDirectoryOfMEMTrees+sample[1])
  trees.append(tree)
  
for tree,sample in zip(trees,Samples):
  plot_ranges.append(get_event_ranges(sample[2],tree))
#sample = ROOT.TChain("tree","test")
#print MaxEventsPerTree
#print InputDirectoryOfMEMTrees+Samples[0][1]
#sample.Add(InputDirectoryOfMEMTrees+Samples[0][1])

#print get_event_ranges(MaxEventsPerTree,sample)


      
for sample,plot_range in zip(Samples,plot_ranges):
  i=0
  for plot_range_ in plot_range:
    create_script(cmsswpath,looperpath,sample[1],plot_range_[0],plot_range_[1],i,sample[0],do_mem)
    i=i+1
  
  