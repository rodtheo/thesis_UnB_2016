import glob
import os
import subprocess
from Bio import SeqIO
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
import yaml
import tempfile
import pybedtools
from Bio.Alphabet import generic_dna

BASE=os.getcwd()
N_THREADS=3
SAMPLES = ["ATCC","BU27","BU33","BU35","U22","U10","U9","U26"]
#SAMPLES = ["ATCC"]
GENOME_PATH = "/array/rodtheo/A_terreus/RNA-SEQ/scaffold/"
NKMER="1G"
MEMORY="40G"
KMERS=[31,63]
REF="/array/rodtheo/A_terreus/GENOME/CADRE/Aspergillus_terreus.CADRE.29.dna.genome.fa"
GFF="/array/rodtheo/A_terreus/GENOME/CADRE/Aspergillus_terreus.CADRE.29.gff3"
rule all:
	input:
		expand("raw_data/{samples}.{id}.fastq", samples=SAMPLES, id=[1,2]),
		expand("k{kmer}/reports/{samples}.delta",kmer=KMERS,samples=SAMPLES),
		expand("raw_data/assemblies/{samples}.spades.fa", samples=SAMPLES),
		expand("k{kmer}/graphs/{samples}_clean.ctx",kmer=KMERS,samples=SAMPLES),
		expand("k{kmer}/stats/{samples}.cov.pdf",kmer=KMERS,samples=SAMPLES),
		expand("k{kmer}/stats/{samples}.len.pdf",kmer=KMERS,samples=SAMPLES),
		expand("raw_data/{samples}.pear.assembled.fastq",samples=SAMPLES),
		expand("k{kmer}/anti/nih_l{samples}/index.html",kmer=KMERS, samples=SAMPLES),
		expand("k{kmer}/stats/NIH_less_{samples}.histo.png", kmer=KMERS, samples=SAMPLES),
		expand("k{kmer}/reports/{samples}.yaml",kmer=KMERS,samples=SAMPLES),
		expand("k{kmer}/ref/ref.ctx", kmer=KMERS),
		expand("k{kmer}/links/{samples}_tosubNIH.ctp.gz",kmer=KMERS,samples=SAMPLES),
		expand("k{kmer}/unitigs/{samples}.clusters.fa",kmer=KMERS,samples=SAMPLES)

rule joining_genomes_dB:
	input:
		pe1="raw_data/{samples}.1.fastq",pe2="raw_data/{samples}.2.fastq"
	output:
		"k{kmer}/graphs/{samples}_raw.ctx"
	log:
		"k{kmer}/logs/build_{samples}.log"
	run:
		#for i in range(0,len(input), 2):
		outfiles = "{}:{}".format(input.pe1,input.pe2)
		samp = input.pe1.split('.')[0]
		samp = samp.split('/')[-1]
		shell("mccortex{} build -Q 10 --remove-pcr -m {} -n {} -k {} --sample {} --seq2 {}:{} {} &> {}".format(wildcards.kmer,MEMORY,NKMER,wildcards.kmer,samp,input.pe1,input.pe2,output,log))

rule cleaning_individual:
	input:
		"k{kmer}/graphs/{samples}_raw.ctx"
	output:
		"k{kmer}/graphs/{samples}_clean.ctx"
	log:
		"k{kmer}/logs/clean_{samples}.log"
	params:
		samp="{samples}"
	shell:
		"mccortex{wildcards.kmer} clean -f -t {N_THREADS} --out {output} -m {MEMORY} -n {NKMER} -c {params.samp}.covB.csv -C {params.samp}.covA.csv -l {params.samp}.lenB.csv -L {params.samp}.lenA.csv {input} &> {log}"

rule plot_before_after_clean:
	input: "k{kmer}/graphs/{samples}_clean.ctx"
	output: cov="k{kmer}/stats/{samples}.cov.pdf",len="k{kmer}/stats/{samples}.len.pdf"
	params:
		samp="{samples}"
	shell: "Rscript --vanilla /array/rodtheo/programas/mccortex/scripts/R/plot-covg-hist.R {params.samp}.covB.csv {params.samp}.covA.csv {output.cov} && Rscript --vanilla /array/rodtheo/programas/mccortex/scripts/R/plot-length-hist.R {params.samp}.lenB.csv {params.samp}.lenA.csv {output.len}"

rule inferedges:
	input: "k{kmer}/graphs/{samples}_clean.ctx"
	output: "k{kmer}/graphs/{samples}_inferedges"
	log: "k{kmer}/logs/{samples}.inferedges.log"
	shell: "mccortex{wildcards.kmer} inferedges -f -n {NKMER} -m {MEMORY} -t {N_THREADS} {input} && touch {output} >& {log}"

rule join_paired_end:
	input: pe1="raw_data/{samples}.1.fastq",pe2="raw_data/{samples}.2.fastq"
	output: "raw_data/{samples}.pear.assembled.fastq"
	log: "raw_data/{samples}.p2join.log"
	params:
		samp="raw_data/{samples}.pear"
	shell: "pear -f {input.pe1} -r {input.pe2} -o {params.samp} -j 13 &> {log}"

rule threads:
	input: cont="k{kmer}/graphs/{samples}_inferedges", reads="raw_data/{samples}.pear.assembled.fastq",graph="k{kmer}/graphs/{samples}_clean.ctx"
	output: graph="k{kmer}/links/{samples}.ctp.gz",hist="k{kmer}/stats/{samples}.ctp.csv"
	log: "k{kmer}/logs/{samples}.threads.log"
	shell: "mccortex{wildcards.kmer} thread -f -g {output.hist} --seq {input.reads} -m {MEMORY} -n {NKMER} -t {N_THREADS} -o {output.graph} {input.graph} &> {log}"

rule graph_ref:
	input: REF
	output: "k{kmer}/ref/ref.ctx"
	shell: "mccortex{wildcards.kmer} build -m {MEMORY} -n {NKMER} -k {wildcards.kmer} --sample REF --seq {input} {output}"

rule subgraph_NIH:
	input: samp="k{kmer}/graphs/{samples}_clean.ctx",ref="k{kmer}/ref/ref.ctx"
	output: "k{kmer}/subgraphs/NIH_less_{samples}.ctx"
	log: "k{kmer}/logs/{samples}.subgraphnih.log"
	shell:
		"mccortex{wildcards.kmer} view -q -k {input.samp} | awk '{{print $1}}' | mccortex{wildcards.kmer} subgraph -f -m {MEMORY} --out {output} --invert --seq - {input.ref} &> {log}"

rule threads_toNIH:
	input: cont="k{kmer}/graphs/{samples}_inferedges", reads="raw_data/{samples}.pear.assembled.fastq",graph="k{kmer}/subgraphs/NIH_less_{samples}.ctx"
	output: graph="k{kmer}/links/{samples}_tosubNIH.ctp.gz",hist="k{kmer}/stats/{samples}_toNIH.ctp.csv"
	log: "k{kmer}/logs/{samples}.threads.log"
	shell: "mccortex{wildcards.kmer} thread -f -g {output.hist} --seq {input.reads} -m {MEMORY} -n {NKMER} -t {N_THREADS} -o {output.graph} {input.graph} &> {log}"

rule contigs_subgraph_NIH:
	input: graph="k{kmer}/subgraphs/NIH_less_{samples}.ctx",path="k{kmer}/links/{samples}_tosubNIH.ctp.gz"
	output: "k{kmer}/contigs/NIH_less_{samples}.fasta"
	log: "k{kmer}/logs/{samples}.contigs.log"
	shell:
		"mccortex{wildcards.kmer} contigs -f -m {MEMORY} -t {N_THREADS} -n {NKMER} -p {input.path} -o {output} {input.graph}"

rule histogram:
	input: "k{kmer}/contigs/NIH_less_{samples}.fasta"
	output: "k{kmer}/stats/NIH_less_{samples}.histo.png"
	run:
		fig,ax = plt.subplots(1,1)
		sample = input[0]
		sizes = [len(rec) for rec in SeqIO.parse(sample, "fasta")]
		hist, bins =  np.histogram(sizes, bins='auto')
		#sizes = xrange(0,100)
		width = 0.7 * (bins[1] - bins[0])
		sizesnp = np.array(sizes)
		center = (bins[:-1] + bins[1:]) / 2
		plt.bar(center, hist, align='center', width=width, log=True)
		#ax.hist(sizesnp,bins='auto')
		plt.title("%i %s sequências (unitigs)\nTamanhos %i até %i" \
			    % (len(sizes),sample,min(sizes),max(sizes)))
		plt.xlabel("Tamanho da sequência (bp)")
		plt.ylabel("log (Contagem)")
		fig.savefig(output[0])


rule subset_fasta:
	input: "k{kmer}/contigs/NIH_less_{samples}.fasta"
	output: "k{kmer}/contigs/NIH_less_{samples}.subset.fasta"
	run:
		sequences = []
		with open(input[0], 'r') as in_handle:
			for rec in SeqIO.parse(in_handle, 'fasta'):
				if len(rec.seq) >= 10000:
					sequences.append(rec)
		with open(output[0], 'w') as out_handle:
			SeqIO.write(sequences, out_handle, 'fasta')

rule antismash:
	input: "k{kmer}/contigs/NIH_less_{samples}.subset.fasta"
	output: "k{kmer}/anti/nih_l{samples}/index.html"
	params:
		dirout="k{kmer}/anti/nih_l{samples}"
	log:
		"k{kmer}/logs/{samples}.antismash.log"
	shell:
		"python /array/rodtheo/programas/antismash-3.0.5.1/run_antismash.py --outputfolder {params.dirout} --clusterblast --smcogs --knownclusterblast --subclusterblast --asf --inclusive --borderpredict -v --logfile {log} {input}"

rule report:
	input: "k{kmer}/anti/nih_l{samples}/index.html","k{kmer}/contigs/NIH_less_{samples}.subset.fasta",GFF
	output: "k{kmer}/reports/{samples}.yaml","k{kmer}/unitigs/{samples}.clusters.fa"
	params: "k{kmer}/anti/nih_l{samples}/*.final.gbk", "{samples}"
	run:
		in_fasta = SeqIO.to_dict(SeqIO.parse(open(input[1],'r'),'fasta'))
		for name in glob.glob(params[0]):
			genbank_file = name
		print(genbank_file)
		in_gb = SeqIO.to_dict(SeqIO.parse(open(genbank_file,'r'),'genbank'))
		sequences=list()
		for key,value in in_gb.items():
			operator = 0
			gb_chr = value
			for rec in value.features:
				if rec.type == 'cluster':
					chromosome = key
					fasta_query_obj = SeqRecord(rec.location.extract(in_fasta[chromosome]).seq, id='cluster_{}'.format(rec.qualifiers['note'][0][-1]))
					sequences.append(fasta_query_obj)
					operator = 1
			if operator == 0:
				fasta_query_no = value
				sequences.append(fasta_query_no)
			
		with open(output[1],'w') as out_handle:
			SeqIO.write(sequences,out_handle,"fasta")
			
		os.system("nucmer --prefix {} --coords {} {}".format(params[1], REF, output[1]))
		in_nucmer = open("{}.coords".format(params[1]),'r')
		out_nucmer = in_nucmer.readlines()[5:]
		out_yaml = {}
		out_yaml[params[1]] = dict()
		for line in out_nucmer:
			genes_over=[]
			df_nucmer = line.rstrip('\n').split('|')
			if float(df_nucmer[3].replace(' ','')) > float(97.00):
				chrom = df_nucmer[-1].split('\t')[1]
				cluster = df_nucmer[-1].split('\t')[0]
				mObj = re.match(r'\W*(\d+)\W*(\d+)', df_nucmer[0])
				start = mObj.group(1)
				end = mObj.group(2)
#				print(cluster,start,end)
				bed = pybedtools.BedTool("{} {} {}".format(cluster,start,end), from_string=True)
				gff = pybedtools.BedTool(input[2])
	#			bed = pybedtools.BedTool(f.name)
				# Recording nucmer hit info contig agains ref
				out_yaml[params[1]][chrom.replace(" ","")] = {"chromossome": cluster, "start": start, "end": end}
				k_intersect = gff.intersect(bed)
				for hit in k_intersect:
	#				print(hit.fields)
					if hit.fields[2] == 'gene':
						genes_over.append(hit.name)
				out_yaml[params[1]][chrom.replace(" ","")] = {"genes_intersect": genes_over}
#			os.remove(f.name)
		with open(output[0],'w') as yaml_file:
			yaml_file.write(yaml.dump(out_yaml, default_flow_style=False))
				
				
rule prova_conceito:
	input: cluster="k{kmer}/unitigs/{samples}.clusters.fa",ref="raw_data/assemblies/{samples}.spades.fa"
	output: "k{kmer}/reports/{samples}.delta"
	params:
		out="k{kmer}/reports/{samples}"
	shell: "nucmer --prefix {params.out} --coords {input.ref} {input.cluster}"
