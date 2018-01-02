# Repo

This repository stores all the codes and pipelines produced to analyze the data of my dissertation entitled: [Comparative genomics of strains of Aspergillus _terreus_ aiming the production of lovastatin] (http://repositorio.unb.br/handle/10482/23117). The intent of the repository is to allow reproducibility of results obtained in the dissertation.

The structure of the repository follows the topics of the dissertation. That is, each section of the dissertation in which there was a need to produce a script will be a directory in this repository. It should be noted that routine tasks for data exploration, such as counting _reads_ in a BAM, visualizing mappings and codes to generate several figures did not have their scripts stored in this repo. The main goal of the repository is to store key codes as the pipelines used with [snakemake] (https://bitbucket.org/snakemake/snakemake/wiki/Home) to identify SNVs (single nucleotide variants) or codes related to the applied methodologies.

## Folder structure

The folder names are in portugues-br and the translated names in english within parenthesis.

```
Repo/
├── Mapeamento_SNP_Call/    (Mapping and SNV call)
│   ├── README.md
│   ├── Samples/
│   ├── trimming.snakefile.py
│   ├── pipeline.snakefile.py
│   ├── buscar_cov_anomalas.py
│   └── config.json
├── Montagem_de_novo/       (De Novo Assembly)
│   ├── pipeline.snakefile.py
│   ├── fgmp.rules
│   ├── Visu_Circos/
│   |    ├── README.md      (Iterative Circus visualization)
│   |    ├── scripts/
│   |    |    ├── index.html
│   |    |    ├── js/
│   |    |    |     ├── circularplot2.js
│   |    |    |     ├── d3-tip.js
│   |    |    |     ├── d3.min.js
│   |    |    |     ├── jquery-1.12.0.min.js
│   |    |    |     ├── labeler.js
│   |    |    |     └── tracks.css
│   |    |    ├── db/
│   |    |    |     ├── Sample.json
│   |    |    |     └── Sample_genomes.json
├── POA_primers/            (Designing Primmers with Partial Order Alignment)
│   ├── README.md
│   ├── src/
│   |    ├── poaV2.tar.gz
│   ├── POA.py
│   ├── GraphPOA.py
│   ├── primers.snakefile.py
|   └── graphPrimer.py
├── BCGs_de_Bruijn_Colorido/  (Detecting BCGs with Colored De Bruijn Graphs)
│   ├── README.md
│   ├── raw_data/
│   |    ├── sample.1.fastq
│   |    ├── sample.2.fastq
|   └── bcg_de_bruijn.snakefile.py
```
