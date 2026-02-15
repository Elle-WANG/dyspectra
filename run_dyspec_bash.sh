#!/bin/bash

# start data processing

# example 
# bash ~/dyspectra/submit_dyspec_parallel.sh J083720.17-460248.44 SB45577 beam26

SOURCE=$1
SBID=$2
#FIELD=$3
BEAM=$3

#path='/import/eve/fast_imaging'
path=`pwd`
mspath=$path/$SBID/data
logpath=$path/dyspec/logfiles
outpath=$path/dyspec

loc=$(dirname "$0")

affix=".ms.corrected"
#affix=".ms"

datacolumn="DATA"
#datacolumn="CORRECTED_DATA"

msfile=$mspath/scienceData*"$SBID"*"$BEAM"*"$affix"

echo Input parameters: $SOURCE, $SBID, $FIELD, $BEAM
echo Reading folder $path 
echo Reading measurement sets in $mspath
echo Saving logfiles to $logpath 
echo Reading scripts located in $loc
echo 

# start with refresh data
rm -r $mspath/scienceData*"$SBID"*"$BEAM"*"$SOURCE"*"$affix"

# recenter the phase
time casa --logfile $logpath/casa_rephase_"$SLURM_JOBID"_"$SOURCE".log --nologger --nogui -c $loc/recenter_phase_casa6.py $msfile $SOURCE

# average baselines
msnew=$mspath/scienceData*"$SBID"*"$BEAM"*"$SOURCE""$affix"
time casa --logfile $logpath/casa_baseavg_"$SLURM_JOBID"_"$SOURCE".log --nologger --nogui -c $loc/avg_baseline.py $msnew

# remove the middle files
rm -r $msnew

# generate the dynamic spectrum
msavg=$mspath/scienceData*"$SBID"*"$BEAM"*"$SOURCE".baseavg"$affix"
time python $loc/make_stokes.py $msavg --noshow --outdir $outpath/"$SBID"_"$SOURCE"_"$BEAM" --columnname $datacolumn

rm *.last
