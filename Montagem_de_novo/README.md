# Montagem _de novo_

A montagem dos genomas foram realizadas através do montador [SPADES](http://bioinf.spbau.ru/spades) usando valores de _k-mer_: -k 21, 33, 55, 77, 99, 127. A anotação dos genes requer o download das leituras do experimento de RNA-Seq envolvendo _A. terreus_ [link do estudo](http://trace.ddbj.nig.ac.jp/DRASearch/study?acc=SRP063843). Estas leituras ajudarão a delimitar os limites gênicos e exônicos pela ferramenta [CodingQuarry](10.1186/s12864-015-1344-4). Além disso, a qualidade da montagem é testada pela busca de marcadores pela ferramenta [FGMP](https://github.com/stajichlab/FGMP) com o uso das regras para `fgmp.rules`.

## Requisitos

Algumas ferramentas e pacotes são necessárias para a execução desta pipeline:

- snakemake
- FGMP
- CodingQuarry
- tophat
- SPADES
- Bowtie-2
- RepeatMask
- transeq (pacote EMBL)

Lembre-se de ajustar os caminhos nos scripts nas variáveis no cabeçalho.