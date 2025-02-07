##############################################################################
#FAB-builder-tinker for python 3.X by Yeng-Tseng Wang 
#2021-12-09 
#The atom type of pdb file is suitable for amber force field 
#with minimize and md simulation ...checking the min.key and md.key file
##############################################################################
import shutil
import glob
from module.Homology_modller import Homology_modller
from module.SSBONDCHECKPDBA  import SSBONDCHECKPDBA
from module.TINKERMD         import TINKERMD  
import urllib.request
import os

dictionary_heavy = { }
dictionary_light = { } 
###heavy chain
#source = r'Heavy/Heavy.ali'
#destination = r'Heavy.ali'
#shutil.copyfile(source,destination)
filename = 'Heavy.ali'
dictionary_heavy = Homology_modller(filename)
for file in glob.glob(r'Heavy.*.pdb'):
    shutil.copy(file, 'Heavy.pdb')

###light chain
#source = r'Light/Light.ali'
#destination = r'Light.ali'
#shutil.copyfile(source,destination)
filename = 'Light.ali'
dictionary_light = Homology_modller(filename)
for file in glob.glob(r'Light.*.pdb'):
    shutil.copy(file, 'Light.pdb')

###alignment 
pdbtempaligment = { }
pdbtempaligment_heavy = { }
pdbtempaligment_light = { }
for key1 in dictionary_heavy:
    pdbidkey1    = key1[0:4:]
    pdbchainkey1 = key1[4:5:]
    for key2 in dictionary_light:
        pdbidkey2    = key2[0:4:]
        pdbchainkey2 = key2[4:5:]
        if (pdbidkey1 == pdbidkey2) and (pdbchainkey1 != pdbchainkey2):
            pdbtempaligment[pdbidkey1] = dictionary_heavy[key1] + dictionary_light[key2]
            pdbtempaligment_heavy[pdbidkey1] = pdbchainkey1
            pdbtempaligment_light[pdbidkey1] = pdbchainkey2

max_key = max(pdbtempaligment, key=lambda key: pdbtempaligment[key])
#print(max_key)
#print(pdbtempaligment[max_key])
pdbfile = max_key+'.pdb'
address = 'http://files.rcsb.org/download/'+pdbfile
urllib.request.urlretrieve(address, pdbfile)
############################################################################################
#read SSBOND information with SSBOND module
############################################################################################
chianL = pdbtempaligment_light[max_key]
chainH = pdbtempaligment_heavy[max_key]

SSBONDCHECKPDBA('Heavy.pdb')
SSBONDCHECKPDBA('Light.pdb')


with open(pdbfile) as file:
    with open("Lref.pdb","w") as output:
        for line in file:
            atom    = line[0:4]
            chainid = line[21:22] 
            if (atom == 'ATOM') and (chainid == chianL) :
                output.write(line)

with open(pdbfile) as file:
    with open("Href.pdb","w") as output:
        for line in file:
            atom    = line[0:4]
            chainid = line[21:22] 
            if (atom == 'ATOM') and (chainid == chainH) :
                output.write(line)

#cmd1 = 'rm -rf Prediction.pdb'
os.remove('Prediction.pdb')
cmd2 = 'tools\\TMalign.exe OK.Heavy.pdb Href.pdb -o HH' ##using "\\"" to instead of "\ or /""
cmd3 = 'tools\\TMalign.exe OK.Light.pdb Lref.pdb -o HL'
#os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
TINKERMD()
