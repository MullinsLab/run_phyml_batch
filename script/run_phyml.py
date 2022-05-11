#!/usr/bin/python

##########################################################################################
# Program: V705_alignment_process.py
# Purpose: In a GP/POL/REN directory with sequence fasta files,
# collapses sequences into unique sequences,
# adds reference HXB2 GP/POL/REN sequence,
# left-align unique sequences and HXB2 via Muscle
# uncollapse and verify sequences
# extract alignment into region of gag/pol/env
# translate NA sequence alignment into AA sequence alignment
# retrieve functional protein sequence alignment
# collapse functional protein sequence alignment
# Author: Wenjie Deng
# Date: 2021-10-29
# Modified: multiprocessing
# Date: 2021-11-03
# Modified: change the structure of output files based on sample id
# Date: 2021-11-05
##########################################################################################

import sys, re, os
import argparse
import glob
import fasta2phylip
import phyml
import parse_dist
from multiprocessing import Pool


def worker(file, logdir, dt):
    fields = file.split("/")
    filename = fields[-1]
    logfilename = filename.replace(".fasta", ".log")
    logfile = logdir + "/" + logfilename

    with open(logfile, "w") as lfp:
        # convert to phylip file
        phylipfile = file.replace(".fasta", ".phy")
        print("\n" + "=== Processing file " + file + " ===")
        covertlog = fasta2phylip.main(file, phylipfile)
        lfp.write("=== Processing file " + file + " ===" + "\n")
        lfp.write("** Convert " + file + " to " + phylipfile + "**\n")
        lfp.write("input: " + file + "\n")
        lfp.write("output: " + phylipfile + "\n")
        lfp.write(covertlog + "\n")

        # run phyml
        phymllog = phyml.main(phylipfile, dt)
        lfp.write("** Run PhyML on " + phylipfile + " **" + "\n")
        lfp.write("input: " + phylipfile + "\n")
        lfp.write("datatype: " + dt + "\n")
        lfp.write(phymllog + "\n")

        # output distance matrix file
        if re.search("PhyML succeed: ", phymllog):
            phymlout = phylipfile+"_phyml.txt"
            distfile = phylipfile+"_pwcoldist.txt"
            distlog = parse_dist.main(phymlout, distfile)
            lfp.write("** Parse pairwise distances in " + phymlout + " **" + "\n")
            lfp.write("input: " + phymlout + "\n")
            lfp.write("output: " + distfile + "\n")
            lfp.write(distlog + "\n")

            # output success info
            lfp.write("*** Succeed ***\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")
    parser.add_argument("-t", "--datatype", help="sequence datatype, must be 'nt' for nucleotide or 'aa' for amino acid", nargs="?", const=1, type=str, required=True)
    parser.add_argument("-p", "--processes", help="number of processes for multiprocessing", nargs="?", const=1, type=int,
                        default="1")
    args = parser.parse_args()
    dir = args.dir
    dt = args.datatype
    proc = args.processes

    logdir = dir+"/run_phyml_logs"
    if os.path.isdir(logdir) is False:
        os.mkdir(logdir)

    files = []
    for file in glob.glob(os.path.join(dir, '*.fasta')):
        files.append(file)

    pool = Pool(proc)
    pool.starmap(worker, [(file, logdir, dt) for file in files])

    pool.close()
    pool.join()

    alllogfile = logdir + "/run_phyml.log"
    with open(alllogfile, "w") as afp:
        for file in files:
            fields = file.split("/")
            filename = fields[-1]
            logfilename = filename.replace(".fasta", ".log")
            logfile = logdir + "/" + logfilename
            with open(logfile, "r") as lfp:
                for line in lfp:
                    afp.write(line)
                afp.write("\n")
