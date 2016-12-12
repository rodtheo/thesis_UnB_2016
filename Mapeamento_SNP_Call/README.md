# Mapeamento de leituras-curtas contra genoma de ref

Este diretório possui a pipeline executada para mapear as leituras das oito amostras contra o genoma de referência _A. terreus_ NIH 2624. Para reproduzir é necessário a instalação dos seguintes pacotes e softwares:

- [Snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home)
- Trimmomatic (http://www.usadellab.org/cms/?page=trimmomatic)
- GATK
- Picard Tools
- Samtools

Além disso, os caminhos relativos da instalação devem ser incluidos nos códigos. Colocar os softwares no PATH é o recomendável.

## Execução

Os fastq brutos devem estar contidos no diretório Samples/, dentro do diretório raiz que deve conter os snakefiles.

1) Execute o snakefile `trimming.snakefile.py` para realizar o pre-processamento das leituras;

2) Execute o snakefile `pipeline.snakefile.py` especificando a configuração `config.json` para chamar os polimorfismos de sequência de acordo com os padrões estabelecidos pelo GATK. O arquivo `config.json` contêm informações adicionais como caminhos relativos de execução de programas, localização do FASTA do genoma e das amostras pré-processadas. Antes de executar a pipeline clone o repositório contendo os [workflows do snakemake](https://bitbucket.org/johanneskoester/snakemake-workflows) e indique o caminho deste na variável `include_prefix` do arquivo `pipeline.snakefile.py`.

3) O resultado final é um gVCF no dir `variant_calling/genome/all.vcf com os sítios variantes e genótipos para cada uma das amostras.

## Buscar regiões anômalas

O script desenvolvido em python para varrer os arquivos de mapemamento e buscar regiões com cobertura anômala (< 2X) é o arquivo em python `buscar_cov_anomalas.py`.

Primeiro instale os seguintes pacotes para python 2.7 antes de executar:

- docopt
- numpy
- pysam
- matplotlib

