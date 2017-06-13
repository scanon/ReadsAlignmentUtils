### Version 0.0.1
__Initial version of the module to upload, download, validate and export RNASeq Alignment data.__
- Validates, saves and retrieves the alignment data file generated either by BowTie2, TopHat2 or HISAT2 App.
- The data is saved in the sorted BAM format. If the input given is in SAM format, it is converted to sorted BAM before saving.
- This module also generates and saves aligner stats from the file provided for upload.
- During download and export, the user has the option to download in BAM, SAM and BAI formats.
__Changes__
- wrapped samtools-v1.4.1 and picard validation for sam/bam alignment formats (latest from github)