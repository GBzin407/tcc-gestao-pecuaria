# tcc-gestao-pecuaria

Pipeline de análise de dados para gestão reprodutiva de rebanho bovino. TCC do curso de Ciência da Computação (Python, SQL, Excel).

## Objetivo

Construir um pipeline de análise de dados que transforma registros brutos de matrizes, touros e partos em indicadores de gestão reprodutiva, exportando uma base tratada em formato compatível com ferramentas de BI.

Objetivos específicos:
- Processar e limpar os dados brutos da planilha de origem.
- Carregar os dados em um banco relacional (SQLite).
- Calcular o Intervalo Entre Partos (IEP) por matriz.
- Mapear a sazonalidade dos partos ao longo do ano.
- Exportar a base tratada em um formato pronto para uso em ferramentas de BI (ex: Power BI).

## Estrutura do projeto

```
tcc-gestao-pecuaria/
├── data/
│   ├── raw/            # Planilha de origem (Gados.xlsx)
│   └── processed/      # Dados intermediários (gerado em tempo de execução)
├── notebooks/
│   └── TCC_Analise_Gado.ipynb   # Pipeline completo de análise
├── reports/
│   ├── dashboard_reproducao.png       # Painel com os indicadores (gerado)
│   └── Relatorio_Fazenda_Final_BR.xlsx # Base tratada, pronta para uso em BI (gerado)
├── sql/
│   └── fazenda.db      # Banco SQLite local (gerado)
├── requirements.txt
└── README.md
```

As pastas `data/processed`, `reports` e `sql` são criadas e preenchidas automaticamente ao rodar o notebook. Os arquivos gerados (banco, imagem e planilha) não são versionados no Git — apenas o código-fonte.

## Tecnologias utilizadas

- Python (pandas, matplotlib)
- SQLite
- Excel (openpyxl)

## Como executar

1. Clone o repositório.
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Coloque a planilha de origem em `data/raw/Gados.xlsx`.
4. Abra `notebooks/TCC_Analise_Gado.ipynb` e execute as células em ordem.

Os resultados (banco SQLite, imagem do painel e planilha final) são gerados automaticamente nas pastas `sql/` e `reports/`.

## Limitações

- A tabela `Touros` é carregada e disponibilizada no banco de dados, mas não existe um campo que relacione cada parto ao touro responsável. Por esse motivo, não foi possível cruzar informações de paternidade com os indicadores reprodutivos nesta versão.
- O cálculo do IEP é limitado pelo volume de dados: poucas matrizes possuem mais de um parto registrado, o que reduz o tamanho da amostra usada nesse indicador.
- O projeto lê os dados de uma planilha estática. Não há uma interface para cadastro ou atualização de registros.
- A planilha final é exportada em um formato pronto para consumo em ferramentas de BI, mas a construção de um dashboard (Power BI ou similar) não faz parte do escopo deste projeto.

## Autor

Gabriel de Oliveira Irineu — TCC de Ciência da Computação.

## Licença

Este projeto está sob a licença MIT (ver `LICENSE`).
