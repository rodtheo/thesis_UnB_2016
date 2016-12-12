# Metodologia de detecção de BCGs

A metodologia requer a instalação do programa [mcCortex](https://github.com/mcveanlab/mccortex). Para especificações sobre a instalação checar a página citada.

## Input files

Para executar o workflow adicione os fastq brutos no dir `raw_data/`. A localização do genoma de referência que deve ser especificado na variável `REF` bem como GFF deste na var `GFF`. Note que a seq do genoma de referência e o respectivo GFF é usado para comparar os resultados da busca das BCGs com as anotações conhecidas para o genoma de ref.

## Requisitos workflow

O workflow gera resultados da busca via ferramenta antiSMASH para comparar com as obtidas pela metodologia de bruijn colorida proposta. Para isso precisamos de instalar a [antiSMASH](https://antismash.secondarymetabolites.org/download.html) e especificar sua localização no arquivo `bcg_de_bruijn.snakefile.py`. Instalar também a ferramenta de ligação de paired-end reads [PEAR](http://sco.h-its.org/exelixis/web/software/pear/) afim de garantir o melhor caminho na montagem do grafo.

Para maiores informações sobre a metodologia consultar a dissertação seção 4.7.2 (Metodologia para detecção de BCGs usando estruturas de grafo de Bruijn
multicolorido). Além do script para a execução da metodologia este dir contem o workflow para uso no snakemake para reproduzir os resultados obtidos.




