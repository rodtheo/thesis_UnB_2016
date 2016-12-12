import os

BASE=os.getcwd()
N_THREADS=10
GENOME_BWT="/array/rodtheo/A_terreus/GENOME/CADRE/Aterreus.29"
SAMPLES = ["ATCC","BU27","BU33","BU35","U26","U22","U10","U9"]
GENOME_PATH = "/array/rodtheo/A_terreus/RNA-SEQ/scaffold/"
SAMP=["SRR2409422","SRR2409423","SRR2409424","SRR2409425"]
QUARRY_PATH="/array/rodtheo/programas/CodingQuarry_v2.0"


os.environ["QUARRY_PATH"]=os.path.join(QUARRY_PATH,"QuarryFiles")


rule all:
	input:
		'data/merged.fastq.gz',
		exapand("Samples/{samples}.{n}.trimmed.paired.fq", samples=SAMPLES, n=[1,2])
		expand("data/{sample}.fastq.gz", sample=SAMP),
		expand("{samples}/results/alignments/tophat_merged/accepted_hits.bam", samples=SAMPLES),
		expand("{samples}/results/cufflinks/transcripts.gtf", samples=SAMPLES),
		expand("{samples}/out/PredictedPass.gff3",samples=SAMPLES),
		expand("{samples}.SPADES/spades_output/scaffolds.fasta",samples=SAMPLES),
		expand("{samples}/bwt/scaffolds.1.bt2",samples=SAMPLES),
		expand("{samples}/mask/scaffolds.fasta.masked",samples=SAMPLES),
		expand("{samples}/interpro/results.tsv",samples=SAMPLES),
		expand("{samples}/out/predicted.pep",samples=SAMPLES),
		expand("{samples}.SPADES/spades_output/scaffolds.fasta.unfiltered.renamed.hmmsearch.full_report", samples=SAMPLES),
		expand("{samples}.SPADES/spades_output/scaffolds.fasta",samples=SAMPLES),
		expand("{samples}.SPADES/spades_output/fgmp.config",samples=SAMPLES)

rule SPADES:
	input:
		fq1="Samples/{samples}.1.trimmed.paired.fq", fq2="Samples/{samples}.2.trimmed.paired.fq"
	output:
		"{samples}.SPADES/spades_output/scaffolds.fasta"
	shell:
		"spades.py -k 21,33,55,77,99,127 --careful -t 20 --pe1-1 {input.fq1} --pe1-2 {input.fq2} -o {wildcards.samples}.SPADES/spades_output"

include:
    "fgmp.rules"

rule buildbwt:
	input:
		"{samples}.SPADES/spades_output/scaffolds.fasta"
	output:
		"{samples}/bwt/scaffolds.1.bt2"
	params:
		base="{samples}/bwt/scaffolds"
	shell:
		"bowtie2-build {input} {params.base}"


rule merge:
	input:
		expand('data/{sample}.fastq.gz', sample=SAMP)
	output:
		'data/merged.fastq.gz'
	threads: 1
	shell:
		'zcat {input} | gzip -c > {output}'

rule tophat:
	input:
		fq='data/merged.fastq.gz',bt="{samples}/bwt/scaffolds.1.bt2"
	output:
		"{samples}/results/alignments/tophat_merged/accepted_hits.bam"
	params:
		base = "{samples}/results/alignments/tophat_merged",genome="{samples}/bwt/scaffolds"
	threads: N_THREADS
	message:
		'Running TopHat2 (thr = {threads}) on {input}'
	shell:
		'tophat2 '
		'-p {threads} '
		'-o {params.base} '
		'{params.genome} '
		'{input.fq}'

rule sortToSam:
	input:
		"{samples}/results/alignments/tophat_merged/accepted_hits.bam"
	output:
		"{samples}/results/alignments/tophat_merged/accepted_hits.sam"
	shell:
		'samtools view -Sh {input} > {output}'

rule cufflinks:
	input:
		"{samples}/results/alignments/tophat_merged/accepted_hits.sam"
	output:
		"{samples}/results/cufflinks/transcripts.gtf"
	params:
		base = "{samples}/results/cufflinks"
	threads: N_THREADS
	shell:
		'cufflinks '
		'-o {params.base} '
		'-p {threads} '
		'{input}'

rule GTFcuffToGFF:
	input:
		"{samples}/results/cufflinks/transcripts.gtf"
	output:
		"{samples}/results/cufflinks/transcripts.gff3"
	threads: N_THREADS
	shell:
		'python ' + QUARRY_PATH + '/CufflinksGTF_to_CodingQuarryGFF3.py {input} > {output}'

rule CodingQuarry:
	input:
		gff="{samples}/results/cufflinks/transcripts.gff3",genome="{samples}.SPADES/spades_output/scaffolds.fasta"
	output:
		gff="{samples}/out/PredictedPass.gff3",cds="{samples}/out/Predicted_CDS.fa"
	threads: N_THREADS
	params: base="{samples}/"
	run:
		os.chdir("./{}".format(params.base))
		shell(QUARRY_PATH + '/CodingQuarry '
		'-f '+BASE+'/{input.genome} '
		'-t '+BASE+'/{input.gff} '
		'-p {threads} -d')
		os.chdir("{}".format(BASE))

rule repeatMasker:
	input:
		"{samples}.SPADES/spades_output/scaffolds.fasta"
	output:
		"{samples}/mask/scaffolds.fasta.masked"
	params:
		base="{samples}/mask/"
	threads: N_THREADS
	shell:
		'RepeatMasker -pa {threads} -s -gff -a -dir {params.base} {input} -species "Aspergillus terreus"'

rule convertToPep:
	input:
		cds="{samples}/out/Predicted_CDS.fa",rm="{samples}/out/PredictedPass.gff3"
	output:
		"{samples}/out/predicted.pep"
	shell:
		"transeq {input.cds} {output} -clean"


rule interproscan:
	input:
		infile="{samples}/out/predicted.pep", rm="{samples}/out/PredictedPass.gff3"
	output:
		"{samples}/interpro/results.tsv"
	shell:
		"/array/rodtheo/programas/interpro/interproscan-5.18-57.0/interproscan.sh -i {input.infile} -o {output} -f tsv"

























