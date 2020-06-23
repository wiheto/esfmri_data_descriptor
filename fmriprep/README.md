## fMRIPrep preprocessing

### Input data

Raw data needs to be downloaded from openneuro.org. Preprocessed data is also available on Openneruo so this does not need to be run. 

### Code usage

First, the ./sub-xxx/ses-postop/anat folders are removed to ensure that fMRIPrep uses the preop anatomical T1s.

Second, download the fmriprep Docker file and createa a singularity image. Download a freesurfer licence. For full reprocueibility, download fMRIPrep version: 1.5.1rc1.

Third, change the bids directory, freesurfer licence, and singularity path/filename in slurm

Forth, execute (from terminal):

> sbatch slurm

See [fMRIPres documentation](https://fmriprep.readthedocs.io/en/stable/usage.html) to get fMRIPrep running for you.

### Output data

Will create directory called ./deriviatives/fmriprep/ in the specified location.

