from Definitions import *
import ROOT
import os
import stat
import glob
from subprocess import call

for sample in Samples:
  #print Samples
  array=glob.glob(OutputDirectoryForMEMTrees+sample[0]+'_*.root')
  if not (len(array)>0):
    print "not found", sample
    Samples.remove(sample)
    
for sample in Samples:
  if not os.path.exists(OutputDirectoryForMEMTrees+"/merged"):
      os.makedirs(OutputDirectoryForMEMTrees+"/merged")
  string_add = "hadd "+OutputDirectoryForMEMTrees+"/merged/"+sample[0].replace("_","")+".root "+OutputDirectoryForMEMTrees+sample[0]+'_*.root'
  #string_del = "rm "+OutputDirectoryForMEMTrees+sample[0]+'_*.root'
  #print string_del
  call(string_add,shell=True)
  #call(string_del,shell=True)