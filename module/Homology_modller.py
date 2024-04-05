#############################################################################
#sequence ali file (modller) for homology modelling
#Yeng-Tseng wang 2021-12-05
##############################################################################
import operator
import urllib.request
from modeller import *
from modeller.automodel import *
def Homology_modller(alifile):
###definition and check the protein name 
    alijudgement = ">P1;"
    with open(alifile) as file:
        for line in file:
            judgement = line[0:4]
            if judgement == alijudgement :
                prename = line[4:9] 
                #print(prename)

###build profile
    prfname = prename+'_build_profile.prf'
    aliname = prename+'_build_profile.ali'
    env = Environ()
#-- Prepare the input files
#-- Read in the sequence database
    sdb = SequenceDB(env)
    sdb.read(seq_database_file='pdb_95.pir', seq_database_format='PIR',
         chains_list='ALL', minmax_db_seq_len=(30, 4000), clean_sequences=True)

#-- Write the sequence database in binary form
    sdb.write(seq_database_file='pdb_95.bin', seq_database_format='BINARY',
          chains_list='ALL')

#-- Now, read in the binary database
    sdb.read(seq_database_file='pdb_95.bin', seq_database_format='BINARY',
         chains_list='ALL')

#-- Read in the target sequence/alignment
    aln = Alignment(env)
    aln.append(file=alifile, alignment_format='PIR', align_codes='ALL')

#-- Convert the input sequence/alignment into
#   profile format
    prf = aln.to_profile()

#-- Scan sequence database to pick up homologous sequences
    prf.build(sdb, matrix_offset=-450, rr_file='${LIB}/blosum62.sim.mat',
          gap_penalties_1d=(-500, -50), n_prof_iterations=1,
          check_profile=False, max_aln_evalue=0.01)

#-- Write out the profile in text format
    prf.write(file= prfname, profile_format='TEXT')

#-- Convert the profile back to alignment format
    aln = prf.to_alignment()

#-- Write out the alignment file
    aln.write(file= aliname, alignment_format='PIR')  

###find out the best template form prf file 
    tempresiduenumber = { }
    with open(prfname) as file:
        for aline in file:
            XS = aline[47:48:]
            #print(XS)
            if XS == "S" :
                refresiduenumber = aline[69:72:] 
            elif XS == "X" :
                pdbidandchain = aline[6:11:]
                onlypdbid     = aline[6:10:]
                chainpdbid    = aline[10:11:]
                matchpercent  = aline[93:95:]
                tempresiduenumber[pdbidandchain] = int (aline[87:90]) * int(matchpercent) / int (refresiduenumber)
      
        max_key = max(tempresiduenumber, key=lambda key: tempresiduenumber[key])
        pdbid = max_key[0:4:]
        pdbchain = max_key[4:5:]

###Aligning predicting sequence with the template
    pdbfile = pdbid+'.pdb'
    address = 'http://files.rcsb.org/download/'+pdbfile
    urllib.request.urlretrieve(address, pdbfile)
    FIRST = 'FIRST:'+pdbchain 
    LAST  = 'LAST:'+pdbchain
    aln = Alignment(env)
    mdl = Model(env, file=pdbid, model_segment=(FIRST,LAST))
    aln.append_model(mdl, align_codes=max_key, atom_files=pdbfile)
    aln.append(file=alifile, align_codes=prename)
    aln.align2d()
    alifilesecond =prename+"-"+max_key+'.ali'
    pdbfilesecond =prename+"-"+max_key+'.pap'
    aln.write(file=alifilesecond, alignment_format='PIR')
    aln.write(file=pdbfilesecond, alignment_format='PAP')  

####build 3D
    a = AutoModel(env, alnfile=alifilesecond,
              knowns=max_key, sequence=prename,
              assess_methods=(assess.DOPE,
                              #soap_protein_od.Scorer(),
                              assess.GA341))
    a.starting_model = 1
    a.ending_model   = 1
    a.make()  

##return 
    return(tempresiduenumber)                 