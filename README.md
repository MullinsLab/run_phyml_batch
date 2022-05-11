# run_phyml_batch
A toolkit to perform nucleotide and amino acid sequence phylogenetic analysis via PhyML_v3.3 and produce the pairwise distance matrix

### Description
This toolkit can be run phyml program in batch in a directory. It requires Python 3 and [PhyML (v3.3)](https://github.com/stephaneguindon/phyml). it will output the estimated ML tree file as well as the pairwise distance matrix for each input sequence alignment file.

### Usage
#### 1. Clone this repository in your working directory
```
git clone https://github.com/MullinsLab/run_phyml_batch.git
```
 - it will create a directory called "run_phyml_batch" in your working directory
#### 2. Download [PhyML](https://github.com/stephaneguindon/phyml) in your designated directory
```
 git clone -b v3.3.20220408 https://github.com/stephaneguindon/phyml.git phyml_v3.3.20220408
```
 - the current release is v3.3.20220408
 - it will create a directory called "phyml_3.3.20220408"
#### 3. Update files in order to output pairwise distances after running phyml
```
cd phyml_v3.3.20220408/src
python your_working_director/run_phyml_batch/script/updatefiles.py
cd ..
```
#### 4. In the directory of phyml_v3.3.20220408/, install phyml following the instructions on phyml [GitHub](https://github.com/stephaneguindon/phyml)
#### 5. Modify phyml_path.py to set the correct path to run phyml in your computer
 - open phyml_path.py in the directory your_working_director/run_phyml_batch/script/ in a text editor
 - replace "where_your_phyml_path/program_name" with the correct phyml path where you just installed, e.g "your_designated_directory/phyml_v3.3.20220408/src/phyml" (the path should include the program name), and save the file
#### 6. In the directory where the input sequence alignments are, run phyml on each sequence alignment file (must be with .fasta extension) to output tree and distance matrix
```
cd directroy_where_inputs_are/
python your_working_director/run_phyml_batch/script/run_phyml.py -t datatype -p numberOfProcessors
```
 - you have to provide the value of datatype (nt for nuclotide sequences, aa for amino acid sequences)
 - the default value of numberOfProcessors is 1. You can run multiprocessors by providing the value > 1 based on your computer settings
 - it will output estimated ML trees in nuwick and pairwise distance matrix for each input file, and a log subdirectory storing the log message of running the toolkit
