#usr/bin/sh
#################
#tranfer fasta to modller ali file
for i in *.fasta
do
	if   [ "$i"  != "$1" ]
	then
		rm -rf `basename $i .fasta`
		mkdir `basename $i .fasta`
		mv $i `basename $i .fasta`
		echo ">P1;"`basename $i .fasta` >> `basename $i .fasta`/`basename $i .fasta`.ali
		echo "sequence:"`basename $i .fasta`":::::::0.00: 0.00" >> `basename $i .fasta`/`basename $i .fasta`.ali
		cat `basename $i .fasta`/$i|awk 'NR > 1' >> `basename $i .fasta`/`basename $i .fasta`.ali
		truncate -s -1 `basename $i .fasta`/`basename $i .fasta`.ali
		echo  "*" >> `basename $i .fasta`/`basename $i .fasta`.ali
		echo "`basename $i .fasta`"
	fi
done