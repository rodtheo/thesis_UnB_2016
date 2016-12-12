# Repositório
Este repositório armazena todos os códigos e pipelines produzidos para analisar os dados da dissertação intitulada: Genômica comparativa de cepas de _Aspergillus_ _terreus_ visando a produção de lovastatina. A intenção do repositório é permitir a reproducibilidade dos resultados e sanar dúvidas adicionais quanto à metodologia e resultados presentes no documento.

A estrutura do repositório segue a dos tópicos da dissertação. Isto é, cada seção da dissertação na qual houve necessidade de produzir um script será um diretório neste repositório. Cabe ressaltar que tarefas rotineiras para exploração dos dados como, por exemplo, contagem de _reads_ num BAM, visualização de mapeamentos e códigos para gerar diversas figuras não tiveram seus scripts armazenados. O intiuito principal do repositório é armazenar códigos chave como a pipeline reprodutível usada com  [snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home) para identificar SNVs ou os códigos relativos às metodologias propostas.

Estrutura do repo:

```
Repositório/
├── Mapeamento_SNP_Call/
│   ├── README.md
│   ├── Samples/
│   ├── trimming.snakefile.py
│   ├── pipeline.snakefile.py
│   ├── buscar_cov_anomalas.py
│   └── config.json
├── Montagem_de_novo/
│   ├── pipeline.snake
│   ├── Visualização_Circus/
│   |    ├── README.md
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
│   |    |    |     └── Sample_genomes.css
├── POA_primers/
│   ├── README.md
|   └── poa_primer.py
├── BCGs_de_Bruijn_Colorido/
│   ├── README.md
|   └── bcg_de_bruijn.snake
```
