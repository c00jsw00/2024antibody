######################################
#MD simulation with amber99sb force field
######################################
import os
import shutil
def TINKERMD():
    cmd01 = 'tools\\pdbxyz.exe <pdbxyz.HH.in' 
    cmd02 = 'tools\\pdbxyz.exe <pdbxyz.HL.in'
    os.system(cmd01)
    os.system(cmd02)
######################################
#HH.seq and HL.seq
    with open('HH.seq') as HHseq, open('HL.seq') as HLseq :
        with open('abs.seq',"w") as output:
            #HH
            for line in HHseq:
                line1        = line[0:3]
                line2        = line[4:71]
                linetotalHH  = line1+'H'+line2
                output.write(linetotalHH+'\n')
            
            #HL
            for line in HLseq:
                line3        = line[0:3]
                line4        = line[4:71]
                linetotalHL  = line3+'L'+line4
                output.write(linetotalHL+'\n')

#########################################     
    cmd03 = 'tools\\xyzedit.exe <HHHL_xyz.in'
    os.system(cmd03)
    source = r'HL.xyz_2'
    destination = r'abs.xyz'
    shutil.copyfile(source,destination)
    os.remove('HH.seq')
    os.remove('HL.seq')
    os.remove('HH.xyz')
    os.remove('HL.xyz')
    os.remove('HL.xyz_2')
    cmd04 = 'tools\\minimize.exe abs.xyz -k min.key 0.01'
    cmd05 = 'tools\\dynamic.exe  abs.xyz_2 -k md.key 100 1.0 0.1 2 310'
    #dynamic xxx.xyz 100000 2.0 1.0 2 298  (100000 steps, 2.0 fs time step, dump structure every 1.0 ps, option 2 is NVT, 298 is the target T)
    cmd06 = 'tools\\xyzpdb.exe <xyzpdb.in'
    os.system(cmd04)
    os.system(cmd05)
    os.system(cmd06)
    os.remove('abs.xyz')
    #os.remove('abs_2.xyz')
    os.remove('abs.dyn')
    os.remove('abs.seq')
    source = r'abs.pdb'
    destination = r'Prediction.pdb'
    shutil.copyfile(source,destination)
    os.remove('abs.pdb')
