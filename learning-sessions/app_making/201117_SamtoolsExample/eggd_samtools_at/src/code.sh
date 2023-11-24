#!/bin/bash
# eggd_samtools_at 0.0.1
# Generated by dx-app-wizard.
#
# Basic execution pattern: Your app will run on a single machine from
# beginning to end.
#
# Your job's input variables (if any) will be loaded as environment
# variables before this script runs.  Any array inputs will be loaded
# as bash arrays.
#
# Any code outside of main() (or any entry point you may add) is
# ALWAYS executed, followed by running the entry point itself.
#
# See https://documentation.dnanexus.com/developer for tutorials on how
# to modify this file.

main() {

    echo "Value of bam_file: '$bam_file'"
    echo "Value of options: '$options'"

    # The following line(s) use the dx command-line tool to download your file
    # inputs to the local file system using variable names for the filenames. To
    # recover the original filenames, you can use the output of "dx describe
    # "$variable" --name".

    echo "Commands to install samtools"

    cd /packages
    tar -jxvf samtools-1.11.tar.bz2
    cd samtools-1.11
    ./configure --prefix=/packages
    make 
    make install

    export PATH=/packages/bin:$PATH
    cd

    echo " Downloading input files"

    dx download "$bam_file" -o bam_file

    samtools sort bam_file -o sorted.bam
    samtools index sorted.bam 



    echo "Uploading output files"
    index_file=$(dx upload sorted.bam.bai --brief)

    # The following line(s) use the utility dx-jobutil-add-output to format and
    # add output variables to your job's output as appropriate for the output
    # class.  Run "dx-jobutil-add-output -h" for more information on what it
    # does.

    dx-jobutil-add-output index_file "$index_file" --class=file
}