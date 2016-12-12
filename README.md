# Repositório
Este repositório armazena todos os códigos e pipelines produzidos para analisar os dados da dissertação intitulada `Genômica comparativa de cepas de __Aspergillus terreus__ visando a produção de lovastatina`. A intenção do repositório é permitir a reproducibilidade dos resultados e sanar dúvidas adicionais quanto à metodologia e resultados presentes no documento.

A estrutura do repositório segue a dos tópicos da dissertação. Isto é, cada seção da dissertação na qual houve necessidade de produzir um script será um diretório neste repositório. Cabe ressaltar que tarefas rotineiras para exploração dos dados como, por exemplo, contagem de _reads_ num BAM, visualização de mapeamentos e códigos para gerar diversas figuras não tiveram seus scripts armazenados. O intiuito principal do repositório é armazenar códigos chave como a pipeline reprodutível usada com  [snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home) para identificar SNVs ou os códigos relativos às metodologias propostas.

Estrutura do repo:

bootstrap/
├── less/
├── js/
├── fonts/
├── dist/
│   ├── css/
│   ├── js/
│   └── fonts/
└── docs/
    └── examples/
