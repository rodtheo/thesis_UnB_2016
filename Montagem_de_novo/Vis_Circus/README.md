# Visualização com Circos iterativo

A visualização com circos foi usada na dissertação para explorar o alinhamento dos contigs obtidos _de novo_ contra o loco do agrupamento gênico de biossíntese de lovastatina da ATCC 20542. Portanto, antes de visualizar é necessário o alinhamento com o programa `nucmer` com parâmetro *-maxmatch -c 100* dos `contigs` resultantes do assembly contra as sequências [AH007774](https://www.ncbi.nlm.nih.gov/nuccore/AH007774) e [AF151722](https://www.ncbi.nlm.nih.gov/nuccore/AF151722).

A visualização dos alinhamentos foi implementada através da linguagem JavaScript com auxilio da biblioteca D3-v3.0. No arquivo `scripts/index.html` pode-se visualizar uma amostra. Além dos arquivos referentes ao código em JavaScript contidos no dir `js/`, o visualizador precisa dos arquivos em JSON do dir `db/`. Nestes arquivos estão presentes as informações a respeito do alinhamento entre as sequências. Os arquivos JSON devem ser estruturados como o exemplo contido em `db/`.

Para visualizar o exemplo neste diretório entre no dir `scripts/` e execute o comando *python -m SimpleHTTPServer 8888*. Depois vá até o brwoser de sua escolha e digite a URL `localhost:8888`.

Seguem os links dos gráficos iterativos para as cepas usadas na dissertação:

- [ATCC 20542](https://rodtheo.github.io/blog/2016/09/16/circos-ATCC)
- [BU35](https://rodtheo.github.io/blog/2016/09/16/circos-BU35)
- [BU27](https://rodtheo.github.io/blog/2016/09/16/circos-BU27)
- [BU33](https://rodtheo.github.io/blog/2016/09/16/circos-BU33)
- [U9](https://rodtheo.github.io/blog/2016/09/16/circos-U9)
- [U10](https://rodtheo.github.io/blog/2016/09/16/circos-U10)
- [U22](https://rodtheo.github.io/blog/2016/09/16/circos-U22)
- [U26](https://rodtheo.github.io/blog/2016/09/16/circos-U26)