#######################################################
#For ssbonds of amber type
#######################################################
def SSBONDCHECKPDBA(pdbfile): 
    count = 1
    with open(pdbfile) as file:
        for line in file:
            SSBOND    = line[0:6]
            SSBONDID  = line[9:10]
            if (SSBOND == 'SSBOND') :
                if (count == 1):
                    residue1 = line[18:21]
                    residue2 = line[32:35] 
                    count = count + 1
                elif (count == 2):
                    residue3 = line[18:21]
                    residue4 = line[32:35]
                    count = count +1     
            elif (count == 2):
                residue3 = 0
                residue4 = 0 
    
    #print(residue1)
    #print(residue2)
    #print(residue3)
    #print(residue4)
    

    newpdbfile = 'OK.'+pdbfile
    CYX = 'CYX'
    with open(pdbfile) as file:
        with open(newpdbfile,"w") as output:
            for line in file:
                atom      = line[0:4]
                number    = line[23:26]
                numbera   = line[0:17]
                numberb   = line[17:20]
                numberc   = line[20:78]
                if (atom == 'ATOM') and (number == residue1):
                    linetotal = numbera+CYX+numberc
                    output.write(linetotal+'\n')
                elif (atom == 'ATOM') and (number == residue2):
                    linetotal = numbera+CYX+numberc
                    output.write(linetotal+'\n')
                elif (atom == 'ATOM') and (number == residue3) and (count ==3):
                    linetotal = numbera+CYX+numberc
                    output.write(linetotal+'\n')
                elif (atom == 'ATOM') and (number == residue4) and (count ==3):
                    linetotal = numbera+CYX+numberc
                    output.write(linetotal+'\n')
                else:
                    linetotal = numbera+numberb+numberc
                    output.write(linetotal+'\n')

    
