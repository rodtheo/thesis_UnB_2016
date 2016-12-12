"""
Rules for analysing fasta files with FastQC.

For usage, include this in your workflow.
"""

"""
This script was designed to run into rodtheo@dna.unb
Remember that all the paths are relative to the user rodtheo
"""
from snakemake.utils import R
import re
import csv
import os

# Path to Trimmomatic software.. Make sure you modify them to call exactly were your software is installed
samples = 'ATCC BU27 BU33 BU35 U10 U22 U26 U9'.split()
TRIMO = '/array/fonsecaea/rodrigo/programs/Trimmomatic-0.30'

# The main output directory
workdir: '/array/rodtheo/A_terreus/final'

def createDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ds_all(path):
    return [path.format(sample=sample) for sample in samples ]

rule all:
    input: expand("Opt/{sample}.trimmed.tmp", sample=samples),expand("Opt/{sample}.tmp", sample=samples), expand("Samples/{sample}.1.fastq", sample=samples), expand("Samples/{sample}.2.fastq", sample=samples), expand("Samples/{sample}.2.trimmed.paired.fq", sample=samples), expand("Samples/{sample}.1.trimmed.paired.fq", sample=samples)

rule fastqc:
   input:
       fq1="Samples/{sample}.1.fastq", fq2="Samples/{sample}.2.fastq"
   output:
   	"Opt/{sample}.tmp"
   shell:
       "fastqc -o fastqc/ {input.fq1} && fastqc -o fastqc/ {input.fq2} && touch {output}"

rule trimmer:
   input:
       fq1="Samples/{sample}.1.fastq",fq2="Samples/{sample}.2.fastq"
   output:
       "Samples/{sample}.1.trimmed.paired.fq","Samples/{sample}.2.trimmed.paired.fq"
   run:
       samples_less_bp=['ATCC','U22']
       sample_file_name1=str({input.fq1}).split("/")[1]
       sample_file_name=sample_file_name1.split(".")[0]
       print("Performing trimmer of %s"%(sample_file_name))
       if sample_file_name in samples_less_bp:
           shell("java -jar {TRIMO}/trimmomatic-0.30.jar PE -threads 5 -phred33 Samples/%s.1.fastq Samples/%s.2.fastq Samples/%s.1.trimmed.paired.fq Samples/%s.1.trimmed.unpaired.fq Samples/%s.2.trimmed.paired.fq Samples/%s.2.trimmed.unpaired.fq LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:134 HEADCROP:15"%(sample_file_name,sample_file_name,sample_file_name,sample_file_name,sample_file_name,sample_file_name))
       elif sample_file_name not in samples_less_bp:
           shell("java -jar {TRIMO}/trimmomatic-0.30.jar PE -threads 5 -phred33 Samples/%s.1.fastq Samples/%s.2.fastq Samples/%s.1.trimmed.paired.fq Samples/%s.1.trimmed.unpaired.fq Samples/%s.2.trimmed.paired.fq Samples/%s.2.trimmed.unpaired.fq LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:244 HEADCROP:15"%(sample_file_name,sample_file_name,sample_file_name,sample_file_name,sample_file_name,sample_file_name))


rule fastqc_after_trimming:
   input:
       fq1="Samples/{sample}.1.trimmed.paired.fq",fq2="Samples/{sample}.2.trimmed.paired.fq"
   output:
       "Opt/{sample}.trimmed.tmp"
   shell:
       "fastqc -o fastqc/fastqc_trim/ {input.fq1} && fastqc -o fastqc/fastqc_trim/ {input.fq2} && touch {output}"
