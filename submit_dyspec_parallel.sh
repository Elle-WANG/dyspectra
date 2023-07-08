#!/bin/bash

# test for dynamic spectra 

#SBATCH --partition=all-x86-cpu
#SBATCH --time=01:00:00
#SBATCH --job-name=vast
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=30gb
#SBATCH --output=/o9000/ASKAP/VAST/fast_test/dyspec_test/logfiles/run_dyspec_%A.output
#SBATCH --error=/o9000/ASKAP/VAST/fast_test/dyspec_test/logfiles/run_dyspec_%A.error
#SBATCH --export=all


# setting working environment
module use /home/app/modulefiles
#module load casa/6.1.0-118
module load casa/5.0.0-218.el6


# start data processing

SOURCE=$1
SBID=$2
FIELD=$3
BEAM=$4

echo $SOURCE, $SBID, $FIELD, $SBID
echo /o9000/ASKAP/VAST/fast_test/$FIELD/corrected_data/scienceData_"$SBID"_"$FIELD"."$BEAM"_averaged_cal.ms
echo $SLURM_JOBID
echo 

# start with refresh data
rm -r /o9000/ASKAP/VAST/fast_test/$FIELD/corrected_data/scienceData_"$SBID"_"$FIELD"."$BEAM"_averaged_cal."$SOURCE".ms

# recenter the phase
time casa --logfile /o9000/ASKAP/VAST/fast_test/dyspec_test/logfiles/casa_rephase_"$SLURM_JOBID"_"$SOURCE".log --nologger --nogui -c /home/ymwang/dyspectra/recenter_phase.py /o9000/ASKAP/VAST/fast_test/$FIELD/corrected_data/scienceData_"$SBID"_"$FIELD"."$BEAM"_averaged_cal.ms $SOURCE

# average baselines
time casa --logfile /o9000/ASKAP/VAST/fast_test/dyspec_test/logfiles/casa_baseavg_"$SLURM_JOBID"_"$SOURCE".log --nologger --nogui -c /home/ymwang/dyspectra/avg_baseline.py /o9000/ASKAP/VAST/fast_test/$FIELD/corrected_data/scienceData_"$SBID"_"$FIELD"."$BEAM"_averaged_cal."$SOURCE".ms

# remove the middle files
rm -r /o9000/ASKAP/VAST/fast_test/$FIELD/corrected_data/scienceData_"$SBID"_"$FIELD"."$BEAM"_averaged_cal."$SOURCE".ms


# setting python environment
module load python/cpu-3.6.5
module load casacore/cpu-py3.6.5-3.1.0


# generate the dynamic spectrum
time python /home/ymwang/dyspectra/make_stokes.py /o9000/ASKAP/VAST/fast_test/$FIELD/corrected_data/scienceData_"$SBID"_"$FIELD"."$BEAM"_averaged_cal."$SOURCE".baseavg.ms --noshow --outdir "$SBID"_"$SOURCE" 


