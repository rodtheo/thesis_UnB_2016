"""
Rule for analysing primers for comparative genomic studies.
"""
from Bio import SeqIO
import yaml
import csv
configfile: 'config.yaml'


### PROGRAM PATHS
POA = '/work/opt/bioinfo/src/poaV2/poa'
MATRIX = '/work/opt/bioinfo/src/poaV2/blosum80.mat'
#samples = 'ATCC BU27 BU33 BU35 U10 U22 U26 U9'.split()

#CHROM = config["chromossomes"][wildcards.chromossome]
#GENOME = config["references"][wildcards.reference]

samples = config["samples"].keys()
genome = config["reference"]
points = [x for x in config["primer"].values()]
primers = list(config["primer"].keys())
chromossome=config["chromossome"]
lengthExtend=int(config["bp_to_extend"])

def _get_primers(primerx):
    return (config["primer"][primerx]["1_1"], config["primer"][primerx]["1_2"])

def _get_forward(primerx,lengthExtend):
    position,_ = _get_primers(primerx)
    return (int(position) - lengthExtend, int(position))

def _get_reverse(primerx,lengthExtend):
    _,position = _get_primers(primerx)
    return (int(position) , int(position) + lengthExtend)

def _get_sample(path):
    name = path.split("/")[1]
    name2 = name.split("_")[0]
    return name2
def _get_primer_name(path):
    name = path.split("/")[1]
    name2 = name.split(".")[0]
    return name2

def _get_from_yaml_file(yamlfile, direction):
    with open(yamlfile,'r') as inputfile:
        x = yaml.load(inputfile)
    return (x[direction]['begin'],x[direction]['end'])

rule all:
    input: expand('consensus/{sample}_{primer}.{d}.fasta', sample=samples, primer=primers, d=[1,2]), expand('call/{sample}.{primer}.{d}.vcf.gz', sample=samples, primer=primers, d=[1,2]),expand('consensus/total.{primer}.{d}.fasta',primer=primers,d=[1,2]),expand('primers/graph.{primer}.{d}.poa',primer=primers,d=[1,2]), expand('primers/{primer}.eprimer3', primer=primers),'primers/final.eprimer3','primers/epcr.results'

rule call:
    input: '{sample}.sorted.id.bam'
    output: outfor='call/{sample}.{primer}.1.vcf.gz', outrev='call/{sample}.{primer}.2.vcf.gz'
    run:
        fprimeri, fprimere=_get_forward(wildcards.primer,lengthExtend)
        rprimeri, rprimere=_get_reverse(wildcards.primer,lengthExtend)
        shell("samtools mpileup -E -r {0}:{1}-{2} -uf {genome} {input} | bcftools call -M -m -O z > {output}".format(chromossome,fprimeri,fprimere, genome=genome,input=input, output=output.outfor))
        shell("samtools mpileup -E -r {0}:{1}-{2} -uf {genome} {input} | bcftools call -M -m -O z > {output}".format(chromossome,rprimeri,rprimere, genome=genome,input=input, output=output.outrev))

rule idxtabix:
    input: 'call/{sample}.{primer}.{d}.vcf.gz'
    output: 'call/{sample}.{primer}.{d}.vcf.gz.idx'
    shell:
        'bcftools index {input} && touch {output}'

rule consensus1:
    input: gz='call/{sample}.{primer}.1.vcf.gz',idx='call/{sample}.{primer}.1.vcf.gz.idx'
    output: outfor='consensus/{sample}_{primer}.1.fasta'
    run:
        fprimeri, fprimere=_get_forward(wildcards.primer,lengthExtend)
        try:
            shell('samtools faidx {genome} {0}:{1}-{2} | bcftools consensus {input} > {output}'.format(chromossome,fprimeri,fprimere,genome=genome,input=input.gz,output=output))
        except:
            print(input.gz)
            pass

rule consensus2:
    input: gz='call/{sample}.{primer}.2.vcf.gz',idx='call/{sample}.{primer}.2.vcf.gz.idx'
    output: 'consensus/{sample}_{primer}.2.fasta'
    run:
        rprimeri, rprimere=_get_reverse(wildcards.primer,lengthExtend)
        try:
            shell('samtools faidx {genome} {0}:{1}-{2} | bcftools consensus {input} > {output}'.format(chromossome,rprimeri,rprimere,genome=genome,input=input.gz,output=output))
        except:
            print(input.gz)
            pass

rule concatenateSeqs1:
    input: expand('consensus/{sample}_{primer}.1.fasta',sample=samples,primer=primers)
    output: 'consensus/total.{primer}.1.fasta'
    run:
        outs = []
        ids = []
        for filex in input:
            with open(filex,"rU") as inputfile:
                for record in SeqIO.parse(inputfile, "fasta"):
                    if record.id.split("-")[-1] == config["primer"][wildcards.primer]["1_1"]:
                        record.id = _get_sample(filex) + "_" + record.id
                        if record.id not in ids:
                            ids.append(record.id)
                            outs.append(record)
        with open(output[0],"w") as outfile:
            SeqIO.write(outs, outfile, "fasta")

rule concatenateSeqs2:
    input: expand('consensus/{sample}_{primer}.2.fasta',sample=samples,primer=primers)
    output: 'consensus/total.{primer}.2.fasta'
    run:
        outs = []
        ids = []
        for filex in input:
            with open(filex,"rU") as inputfile:
                for record in SeqIO.parse(inputfile, "fasta"):
                    if record.id.split(":")[-1].split("-")[0] == config["primer"][wildcards.primer]["1_2"]:
                        record.id = _get_sample(filex) + "_" + record.id
                        if record.id not in ids:
                            ids.append(record.id)
                            outs.append(record)
        with open(output[0],"w") as outfile:
            SeqIO.write(outs, outfile, "fasta")

rule poa:
    input: 'consensus/total.{primer}.{d}.fasta'
    output: 'primers/graph.{primer}.{d}.poa'
    shell:
        "{POA} -read_fasta {input} -do_global -po {output} {MATRIX}"

rule primers:
    input: 'primers/graph.{primer}.1.poa', 'primers/graph.{primer}.2.poa'
    output: 'primers/{primer}.yaml'
    shell:
        "python2.7 graphPrimer.py {input} {output} {lengthExtend}"

rule eprimer3Forward:
    input: 'primers/{primer}.yaml'
    output: fr='primers/{primer}.eprimer3'
    run:
        bforward, eforward = _get_from_yaml_file(input[0],'forward')
        breverse, ereverse = _get_from_yaml_file(input[0],'reverse')
        excludebegin = eforward
        excludeend = breverse
        primerrange = ereverse - bforward + 100
        print(output.fr)
        shell('eprimer3 -sf "fasta" -sequence /array/rodtheo/A_terreus/ATCC/PERGA/Scaf254.fa -includedregion [{0},{1}] -excludedregion [{2},{3}] -prange 100-{4} -task 1 -outfile {output}'.format(bforward, ereverse, eforward, breverse, primerrange, output = output.fr))
#        shell('eprimer3 -sf "fasta" -sequence /array/rodtheo/A_terreus/ATCC/PERGA/Scaf254.fa -includedregion [{0},{1}] -task 3 -outfile {output}'.format(breverse,ereverse,output=output.rev))

rule parseEPrimer:
    input: expand('primers/{primer}.eprimer3',primer=primers)
    output: info='primers/final.eprimer3',epcr='primers/epcr.eprimer3'
    run:
        from Bio.Emboss import Primer3
        primersearch = {}
        print("ID","START","Tm","PRIMER_LENGTH","GC","SEQ")
        with open(output.info, 'w') as eprimerfile:
            eprimercsv = csv.writer(eprimerfile, delimiter="\t")
            eprimercsv.writerow(["#ID","START","Tm","PRIMER_LENGTH","GC","SEQ"])
            for candidate in input:
                handle = open(candidate, 'r')
                for primer3record in Primer3.parse(handle):
                    pass
                try:
                    primer = primer3record.primers[0]
                    primerlist = [] 
                    for primers in primer3record.primers:
                        if abs(primers.forward_tm - primer.reverse_tm) < float(2):
                            primerlist.append(primers)
                    if len(primerlist) > 0:
                        primer = primerlist[0]
                    name = _get_primer_name(candidate)
                    primersearch[name] = [primer.forward_seq, primer.reverse_seq]
                    eprimercsv.writerow([name, "forward", primer.forward_start, primer.forward_tm, primer.forward_length,primer.forward_gc, primer.forward_seq])
                    eprimercsv.writerow([name, "reverse", primer.reverse_start, primer.reverse_tm, primer.reverse_length, primer.reverse_gc,primer.reverse_seq])
                    print(name, "forward", primer.forward_start, primer.forward_tm, primer.forward_length,primer.forward_gc, primer.forward_seq)
                    print(name, "reverse", primer.reverse_start, primer.reverse_tm, primer.reverse_length, primer.reverse_gc,primer.reverse_seq)
                except:
                    name = _get_primer_name(candidate)
                    print("Couldnt find primer for {primer}".format(primer = name))
        with open(output.epcr, 'w') as epcrfile:
            for key, value in primersearch.items():
                epcrfile.write("{0}\t{1}\t{2}\n".format(key, value[0], value[1]))
#                raise("Very polymorphic region, please increase range region.")

rule ePCR:
    input: 'primers/epcr.eprimer3'
    output: 'primers/epcr.results'
    shell:
        'primersearch -sf "fasta" -seqall {genome} -infile {input} -outfile {output}'
    


