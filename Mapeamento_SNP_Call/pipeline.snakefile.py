# vim: syntax=python tabstop=4 expandtab
# coding: utf-8


"""
GATK variant calling following the best practices guide.
Needs at least GATK 3.0, available in your PATH as "gatk".

Expects a json config file with the following structure, assuming that the
desired reference sequence is some genome
to be found under the given path, and two units A and B have been sequenced with Illumina.

{
    "references": {
        "genome": "path/to/genome.fasta"
    },
    "samples": {
        "A": ["A"],
        "B": ["B"]
    },
    "units": {
        "A":
            ["path/to/A_R1.fastq.gz", "path/to/A_R2.fastq.gz"],
        "B":
            ["path/to/B.fastq.gz"]
    },
    "known_variants": {
        "dbsnp": "path/to/dbsnp.vcf",
        "hapmap": "path/to/hapmap_3.3.vcf",
        "g1k": "path/to/1000G_phase1.snps.high_confidence.vcf",
        "omni": "path/to/1000G_omni2.5.vcf",
        "mills": "path/to/Mills_and_1000G_gold_standard.indels.vcf"
    },
    "platform": "Illumina",
    "heterozygosity": 0.001,
    "indel_heterozygosity": 1.25E-4
}

Note the separation between samples and units that allows to have more than
one sequencing run for each sample, or multiple lanes per sample.
"""


__author__ = "Johannes Köster (http://johanneskoester.bitbucket.org)"
__license__ = "MIT"


configfile: "config.json"

include_prefix="/array/rodtheo/A_terreus/snakemake_workflows/snakemake-workflows"

include:
    include_prefix + "/bio/ngs/rules/mapping/bwa_mem.rules"
include: 
    include_prefix + "/bio/ngs/rules/mapping/samfiles.rules"
include: 
    include_prefix + "/bio/ngs/rules/mapping/gatk.rules"
include:
    include_prefix + "/bio/ngs/rules/variant_calling/gatk_haplotype_caller.rules"
if config["known_variants"]["dbsnp"] != "NA":
	include:
	    include_prefix + "/bio/ngs/rules/variant_calling/gatk_variant_recalibrator.rules"

rule all:
    input:
       	"variant_calling/genome/all.vcf"
