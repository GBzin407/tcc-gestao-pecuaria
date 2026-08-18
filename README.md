# tcc-gestao-pecuaria

Pipeline de análise de dados para gestão reprodutiva de rebanho bovino. TCC do curso de Ciência da Computação (Python, SQL, Excel, Power BI).

## Objetivo

Construir um pipeline que transforma registros brutos de matrizes, touros e partos em indicadores de gestão reprodutiva, disponibilizando o resultado tanto em um banco de dados quanto em um dashboard interativo.

Objetivos específicos:
- Organizar e limpar os dados brutos da planilha de origem.
- Carregar os dados tratados em um banco relacional (SQLite).
- Calcular indicadores reprodutivos, como o ranking de partos por vaca e a proporção de sexo das crias.
- Gerar gráficos que mostrem esses indicadores de forma visual.
- Exportar os dados tratados e os indicadores num formato pronto para uso em ferramentas de BI.
- Montar um dashboard interativo no Power BI que reúna esses indicadores num painel fácil de entender.

## Estrutura do projeto

```
tcc-gestao-pecuaria/
├── data/
│   ├── raw/            # Planilha de origem (Gados.xlsx)
│   └── processed/      # Dados intermediários (gerado em tempo de execução)
├── notebooks/
│   └── TCC_Analise_Gado.ipynb   # Versão original (protótipo, Google Colab) — não é mais atualizada
├── reports/
│   ├── ranking_partos.png             # Gráfico de ranking (gerado)
│   ├── proporcao_sexo.png             # Gráfico de proporção por sexo (gerado)
│   ├── Relatorio_Fazenda_Final_BR.xlsx # Base tratada, pronta para uso em BI (gerado)
│   └── Dashboard_Gestao_Reprodutiva.pbix # Dashboard Power BI (montado manualmente)
├── sql/
│   └── fazenda.db      # Banco SQLite local (gerado)
├── src/
│   └── main.py         # Pipeline completo de análise (script principal)
├── requirements.txt
└── README.md
```

As pastas `data/processed`, `reports` e `sql` são criadas e preenchidas automaticamente ao rodar `src/main.py`. Os arquivos gerados (banco, imagens e planilha) não são versionados no Git — apenas o código-fonte.

## Tecnologias utilizadas

- Python (pandas, matplotlib, xlsxwriter)
- SQLite
- Excel (openpyxl)
- Power BI Desktop (montagem manual do dashboard)

## Como executar

1. Clone o repositório.
2. Crie e ative um ambiente virtual (opcional, recomendado).
3. Instale as dependências:
```
   pip install -r requirements.txt
```
4. Coloque a planilha de origem em `data/raw/Gados.xlsx`.
5. Execute o pipeline:
```
   python src/main.py
```

Os resultados (banco SQLite, gráficos e planilha final) são gerados automaticamente nas pastas `sql/` e `reports/`.

6. O pipeline **não** gera o dashboard sozinho. Abra `reports/Relatorio_Fazenda_Final_BR.xlsx` no Power BI Desktop e monte os visuais manualmente a partir dela. O arquivo `reports/Dashboard_Gestao_Reprodutiva.pbix` neste repositório é o resultado dessa montagem manual, feita uma vez pelo autor — rodar o pipeline de novo não atualiza esse `.pbix` automaticamente.

O notebook em `notebooks/TCC_Analise_Gado.ipynb` corresponde à versão original do protótipo (desenvolvida no Google Colab); ele não é mais atualizado e pode ficar defasado em relação ao código-fonte de referência, `src/main.py`.

## Limitações

- O Intervalo Entre Partos (IEP) e a sazonalidade dos partos não são calculados nesta versão do pipeline. O motivo é o baixo volume de dados: das matrizes cadastradas, apenas uma tem mais de um parto registrado, o que torna esses dois indicadores pouco representativos para o conjunto de dados atual.
- A tabela `Touros` é carregada e disponibilizada no banco de dados, mas não existe um campo que relacione cada parto ao touro responsável. Por esse motivo, não foi possível cruzar informações de paternidade com os indicadores reprodutivos nesta versão.
- O projeto lê os dados de uma planilha estática. Não há uma interface para cadastro ou atualização de registros.
- O dashboard no Power BI é atualizado manualmente; o pipeline não republica o `.pbix` a cada execução.

## Autor

Gabriel de Oliveira Irineu — TCC de Ciência da Computação.

## Licença

Este projeto está sob a licença MIT (ver `LICENSE`).
