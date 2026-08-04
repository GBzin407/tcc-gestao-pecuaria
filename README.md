# tcc-gestao-pecuaria

Sistema de análise de dados para gestão reprodutiva de rebanho bovino. TCC do curso de Ciência da Computação (Python, SQL, Excel, Power BI).

## Objetivo

Construir um pipeline de análise de dados que transforma registros brutos de matrizes, touros e partos em indicadores de gestão reprodutiva, servindo de base para um dashboard em Power BI.

Objetivos específicos:
- Processar e limpar os dados brutos da planilha de origem.
- Carregar os dados em um banco relacional (SQLite).
- Calcular o Intervalo Entre Partos (IEP) por matriz.
- Mapear a sazonalidade dos partos ao longo do ano.
- Exportar uma base tratada para consumo externo (Power BI).

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
│   └── Relatorio_Fazenda_Final_BR.xlsx # Base tratada para o Power BI (gerado)
├── sql/
│   └── fazenda.db      # Banco SQLite local (gerado)
├── requirements.txt
└── README.md
```

As pastas `data/processed`, `reports` e `sql` são criadas e preenchidas automaticamente ao rodar o notebook.

## Tecnologias utilizadas

- Python (pandas, matplotlib)
- SQLite
- Excel (openpyxl)
- Power BI (consumo do arquivo exportado)

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

A tabela de touros não possui vínculo direto com os registros de parto na fonte de dados atual, o que impede o cruzamento de informações de paternidade com os indicadores reprodutivos.

## Autor

Gabriel de Oliveira Irineu — TCC de Ciência da Computação.

## Licença

Este projeto está sob a licença MIT (ver `LICENSE`).
