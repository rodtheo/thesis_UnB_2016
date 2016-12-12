# Metodologia Desenho de Primers via POA

O script relacionado ao desenho dos primers no BCG de lovastatina usando a metodologia desenvolvida na dissertação estão neste diretório.

Certifique-se que os seguintes requisitos encontram-se instalados:

- POA (link do src no tar `poaV2.tar.gz`)
- Samtools
- BCFtools
- eprimmer3
- primersearch

# Inputs

As etapas necessárias para o desenho dos primers utilizam os arquivos BAM com os mapeamentos de cada cepa contra o genoma de _A. terreus_ e o arquivo `config.json` com especificações a respeito da localização no genoma das regiões que deseja-se desenhar primers.

Um segmento da estrutura do `config.json` é mostrado a seguir onde reference é o genoma para ancorar os mapeamentos e cada objeto do array primer é um limite para a região a ser amplificada. Por exemplo, `"{"LovB1": {"1_1":"23300"}` indica que o algoritmo usará os limites 5' (1_1) e 3' (1_2) para extender em até 200 pb (parâmetro definido na variável bp_to_extend) a região e buscar o melhor segmento entre esses 200 pb para desenhar os primers. A busca é feita com os arquivos de mapeamento das 8 amostras.

```javascript
{
    "reference": "/array/rodtheo/A_terreus/ATCC/PERGA/ATCC_scaffolds.fa",
    "primer": {
        "LovB1": {
        "1_1": "23300",
        "1_2": "25500"
        }
    },
    "samples": {
        "ATCC": ["ATCC"],
        "BU27": ["BU27"],
        "BU33": ["BU33"],
        "BU35": ["BU35"],
        "U10": ["U10"],
        "U22": ["U22"],
        "U26": ["U26"],
        "U9": ["U9"]
    },
    "chromossome":"254",
    "bp_to_extend":"200"
}
```

Os arquivos de input BAM devem estar no mesmo dir de execução do workflow `primers.snakefile.py` respeitando a estrutura do nome {sample}.sorted.id.bam onde {sample} é um dos nomes explicitados no arquivo `config.json`.

O script em python `graphPrimer.py` define o algoritmo para busca da melhor sequência de primers e é chamado na execução do workflow. Os arquivos `POA.py` e `GraphPOA.py` são classes chamadas pelo script principal.