# Pipeline de Análise de Dados Reprodutivos - Rebanho Bovino
# TCC - Ciência da Computação
# Gabriel de Oliveira Irineu - 1230113289
# 

from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

# configuração de diretórios
# __file__ está em src/, então o projeto raiz é uma pasta acima
root_dir = Path(__file__).resolve().parent.parent
data_dir = root_dir / "data"
raw_dir = data_dir / "raw"
processed_dir = data_dir / "processed"
sql_dir = root_dir / "sql"
reports_dir = root_dir / "reports"

# configuração visual dos gráficos
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "ggplot")
plt.rcParams["figure.figsize"] = (12, 7)
plt.rcParams["font.size"] = 10


def configurar_diretorios():
    # cria as pastas do projeto caso ainda não existam
    for folder in [raw_dir, processed_dir, sql_dir, reports_dir]:
        folder.mkdir(parents=True, exist_ok=True)
    print(f"Diretório raiz: {root_dir}")
    print("Pastas configuradas com sucesso.")

def carregar_dados():
    # lê a planilha de origem e devolve os três dataframes tratados
    caminho_planilha = raw_dir / "Gados.xlsx"

    with pd.ExcelFile(caminho_planilha) as xls:
        df_matrizes = pd.read_excel(xls, sheet_name="Matrizes")
        df_touros = pd.read_excel(xls, sheet_name="Touros")
        df_partos = pd.read_excel(xls, sheet_name="Eventos_Partos")

    # padronização de chaves
    if "ID_Vaca" in df_matrizes.columns:
        df_matrizes.rename(columns={"ID_Vaca": "ID_Matriz"}, inplace=True)

    # tipagem numérica
    df_partos["ID_Matriz"] = pd.to_numeric(df_partos["ID_Matriz"], errors="coerce").astype("Int64")
    df_partos["ID_Parto"] = pd.to_numeric(df_partos["ID_Parto"], errors="coerce").astype("Int64")

    # conversão de datas
    df_partos["Data_Parto"] = pd.to_datetime(df_partos["Data_Parto"], format="%d/%m/%Y", errors="coerce")
    df_matrizes["Data_Nascimento"] = pd.to_datetime(df_matrizes["Data_Nascimento"], errors="coerce")

    # limpeza de texto
    df_partos["Sexo_Cria"] = df_partos["Sexo_Cria"].str.upper().str.strip()

    print(f"Matrizes: {len(df_matrizes)}")
    print(f"Touros: {len(df_touros)}")
    print(f"Partos: {len(df_partos)}")
    print(f"Partos sem ID_Matriz: {df_partos['ID_Matriz'].isna().sum()}")
    print(f"Matrizes sem Data_Nascimento: {df_matrizes['Data_Nascimento'].isna().sum()} de {len(df_matrizes)} "
          f"(dado não coletado na planilha de origem)")

    return df_matrizes, df_touros, df_partos

def modelar_banco(df_matrizes, df_touros, df_partos):
    # carrega as tabelas tratadas num banco SQLite local
    caminho_banco = sql_dir / "fazenda.db"
    conn = sqlite3.connect(caminho_banco)

    try:
        df_matrizes_sql = df_matrizes.copy()
        df_partos_sql = df_partos.copy()

        df_matrizes_sql["Data_Nascimento"] = df_matrizes_sql["Data_Nascimento"].dt.strftime("%Y-%m-%d")
        df_partos_sql["Data_Parto"] = df_partos_sql["Data_Parto"].dt.strftime("%Y-%m-%d")

        df_matrizes_sql.to_sql("matrizes", conn, if_exists="replace", index=False)
        df_touros.to_sql("touros", conn, if_exists="replace", index=False)
        df_partos_sql.to_sql("eventos_partos", conn, if_exists="replace", index=False)

        print("Banco de dados SQLite atualizado.")

        query_val = """
        SELECT
            COUNT(CASE WHEN ID_Matriz IS NOT NULL THEN 1 END) AS partos_validos,
            COUNT(CASE WHEN ID_Matriz IS NULL THEN 1 END) AS partos_orfaos
        FROM eventos_partos;
        """
        print(pd.read_sql(query_val, conn))

    finally:
        conn.close()

    return caminho_banco

def ranking_e_sexo(caminho_banco):
    # calcula o ranking de partos por matriz e a distribuição por sexo da cria
    conn = sqlite3.connect(caminho_banco)

    try:
        query_ranking = """
        SELECT
            m.ID_Matriz,
            m.Nome AS Nome_Vaca,
            COUNT(p.ID_Parto) AS Total_Partos
        FROM matrizes m
        INNER JOIN eventos_partos p ON m.ID_Matriz = p.ID_Matriz
        GROUP BY m.ID_Matriz, m.Nome
        ORDER BY Total_Partos DESC;
        """
        df_ranking = pd.read_sql(query_ranking, conn)

        query_sexo = """
        SELECT
            COALESCE(Sexo_Cria, 'Não Informado') AS Sexo_Cria,
            COUNT(*) AS Total,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM eventos_partos WHERE ID_Matriz IS NOT NULL), 2) AS Porcentagem
        FROM eventos_partos
        WHERE ID_Matriz IS NOT NULL
        GROUP BY Sexo_Cria;
        """
        df_sexo = pd.read_sql(query_sexo, conn)

        print("Ranking por matriz:")
        print(df_ranking.head())

        print("\nProporção por sexo:")
        print(df_sexo)

    finally:
        conn.close()

    return df_ranking, df_sexo

def gerar_graficos(df_ranking, df_sexo):
    # gera e salva os gráficos de ranking e proporção por sexo
    fig, ax = plt.subplots()
    ax.bar(df_ranking["Nome_Vaca"], df_ranking["Total_Partos"], color="#6b8e23")
    ax.set_title("Ranking de Partos por Matriz")
    ax.set_xlabel("Matriz")
    ax.set_ylabel("Total de Partos")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    caminho_ranking = reports_dir / "ranking_partos.png"
    fig.savefig(caminho_ranking, dpi=150)
    plt.close(fig)

    rotulos_sexo = {"M": "Macho", "F": "Fêmea"}
    labels_pizza = df_sexo["Sexo_Cria"].map(rotulos_sexo).fillna(df_sexo["Sexo_Cria"])

    fig, ax = plt.subplots()
    ax.pie(df_sexo["Total"], labels=labels_pizza, autopct="%1.1f%%", startangle=90)
    ax.set_title("Proporção de Sexo das Crias")
    plt.tight_layout()
    caminho_sexo = reports_dir / "proporcao_sexo.png"
    fig.savefig(caminho_sexo, dpi=150)
    plt.close(fig)

    print(f"Gráficos salvos em: {caminho_ranking} e {caminho_sexo}")
    return caminho_ranking, caminho_sexo

def exportar_relatorio_excel(df_ranking, df_sexo, caminho_ranking, caminho_sexo):
    # exporta os resultados pra um arquivo excel com abas e gráficos embutidos
    caminho_relatorio = reports_dir / "Relatorio_Fazenda_Final_BR.xlsx"

    with pd.ExcelWriter(caminho_relatorio, engine="xlsxwriter") as writer:
        df_ranking.to_excel(writer, sheet_name="Ranking_Partos", index=False)
        df_sexo.to_excel(writer, sheet_name="Proporcao_Sexo", index=False)

        workbook = writer.book

        ws_ranking = writer.sheets["Ranking_Partos"]
        ws_ranking.insert_image("E2", str(caminho_ranking))

        ws_sexo = writer.sheets["Proporcao_Sexo"]
        ws_sexo.insert_image("E2", str(caminho_sexo))

    print(f"Relatório Excel salvo em: {caminho_relatorio}")
    return caminho_relatorio

if __name__ == "__main__":
    configurar_diretorios()
    df_matrizes, df_touros, df_partos = carregar_dados()
    caminho_banco = modelar_banco(df_matrizes, df_touros, df_partos)
    df_ranking, df_sexo = ranking_e_sexo(caminho_banco)
    caminho_ranking, caminho_sexo = gerar_graficos(df_ranking, df_sexo)
    exportar_relatorio_excel(df_ranking, df_sexo, caminho_ranking, caminho_sexo)