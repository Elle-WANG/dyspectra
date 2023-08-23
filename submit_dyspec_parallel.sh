#!/bin/bash

# test for dynamic spectra 

#SBATCH --partition=purley-cpu
#SBATCH --time=01:00:00
#SBATCH --job-name=DynamicSpectra
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=30gb
#SBATCH --output=/o9000/ASKAP/VAST/fast_survey/dyspec/logfiles/run_dyspec_%A.output
#SBATCH --error=/o9000/ASKAP/VAST/fast_survey/dyspec/logfiles/run_dyspec_%A.error
#SBATCH --export=all


# setting working environment
module use /home/app/modulefiles
#module load casa/6.1.0-118
module load casa/5.0.0-218.el6


# start data processing

# sbatch ~/dyspectra/submit_dyspec_parallel.sh J083720.17-460248.44 SB45577 beam26

SOURCE=$1
SBID=$2
#FIELD=$3
BEAM=$3

path='/o9000/ASKAP/VAST/fast_survey'
mspath=$path/$SBID/data
logpath=$path/dyspec/logfiles

msfile=$mspath/scienceData*"$SBID"*"$BEAM"*.ms.corrected

echo $SOURCE, $SBID, $FIELD, $BEAM
echo $msfile
echo $SLURM_JOBID
echo 

# start with refresh data
rm -r $mspath/scienceData*"$SBID"*"$BEAM"*"$SOURCE"*.ms.corrected

# recenter the phase
time casa --logfile $logpath/casa_rephase_"$SLURM_JOBID"_"$SOURCE".log --nologger --nogui -c /home/ymwang/dyspectra/recenter_phase.py $msfile $SOURCE

# average baselines
msnew=$mspath/scienceData*"$SBID"*"$BEAM"*"$SOURCE".ms.corrected
time casa --logfile $logpath/casa_baseavg_"$SLURM_JOBID"_"$SOURCE".log --nologger --nogui -c /home/ymwang/dyspectra/avg_baseline.py $msnew

# remove the middle files
rm -r $msnew


# setting python environment
module load python/cpu-3.6.5
module load casacore/cpu-py3.6.5-3.1.0


# generate the dynamic spectrum
msavg=$mspath/scienceData*"$SBID"*"$BEAM"*"$SOURCE".baseavg.ms.corrected
time python /home/ymwang/dyspectra/make_stokes.py $msavg --noshow --outdir "$SBID"_"$SOURCE" 


