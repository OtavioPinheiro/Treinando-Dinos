import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime

data = datetime.date.today()
hora = datetime.datetime.now().hour
min = datetime.datetime.now().minute
sec = datetime.datetime.now().second
sufixo = f"{data}_{hora}_{min}_{sec}"


def obter_dados(caminho_dos_dados: str) -> tuple:
    with open(file=caminho_dos_dados, mode='r', encoding='UTF8', newline='') as f:
        pontuacoes = []
        geracoes = []
        leitor = csv.DictReader(f)
        dados = sorted(leitor, key=lambda d: d["Pontuação máxima"])
        for linha in dados:
            pontuacoes.append(linha["Pontuação máxima"])
            geracoes.append(linha["Geração"])

    return pontuacoes, geracoes


def tratar_os_dados(caminho_dos_dados: str) -> tuple:
    dados = obter_dados(caminho_dos_dados)
    dados_pontuacoes: list = dados[0]
    pontuacoes: list = []
    for ponto in dados_pontuacoes:
        ponto = int(ponto)
        pontuacoes.append(ponto)

    dados_geracoes: list = dados[1]
    geracoes: list = []
    for geracao in dados_geracoes:
        geracao = int(geracao)
        geracoes.append(geracao)

    return pontuacoes, geracoes


def gerar_histograma(caminho_dos_dados: str) -> None:
    dados = obter_dados(caminho_dos_dados)
    pontuacoes: list = dados[0]
    plt.hist(x=pontuacoes, bins=10, range=(0, 100), color='green', histtype='bar', rwidth=0.8)
    plt.xlabel('Pontuações')
    plt.ylabel('Gerações')
    plt.title('Histograma de Pontuações')
    plt.savefig(f'graphics/histo_{sufixo}.png', bbox_inches='tight')
    plt.show()


def gerar_grafico_de_barras(caminho_dos_dados: str) -> None:
    dados = tratar_os_dados(caminho_dos_dados)
    pontuacoes = dados[0]
    geracoes = dados[1]

    plt.figure(figsize=(40, 15))
    plt.bar(x=geracoes, height=pontuacoes, align='edge', width=0.7, bottom=0, color="green", edgecolor='black')
    # for i in range(len(geracoes)):
    #     plt.annotate(pontuacoes[i], (i - 0.5, int(pontuacoes[i]) + 500))
    plt.xlabel('Gerações')
    plt.ylabel('Pontuações')
    plt.title('Pontuações x Gerações')
    plt.tight_layout()
    plt.savefig(f'graphics/barras_{sufixo}.png', bbox_inches='tight')
    plt.show()


def gerar_grafico_de_linha(caminho_dos_dados: str) -> None:
    dados = tratar_os_dados(caminho_dos_dados)
    pontuacoes = dados[0]
    geracoes = dados[1]

    plt.figure(figsize=(40, 15))
    plt.plot(geracoes, pontuacoes)
    plt.xlabel('Gerações')
    plt.ylabel('Pontuações')
    plt.title('Pontuações x Gerações')
    plt.tight_layout()
    plt.savefig(f'graphics/linhas_{sufixo}.png', bbox_inches='tight')
    plt.show()


def gerar_grafico_linha_sns(caminho_dos_dados: str) -> None:
    dados = tratar_os_dados(caminho_dos_dados)
    pontuacoes = dados[0]
    geracoes = dados[1]
    ax = sns.relplot(x=geracoes, y=pontuacoes, kind="line")
    ax.set(xlabel='Gerações', ylabel='Pontuações', title='Gerações x Pontuações')
    plt.gcf().set_size_inches(8, 8)
    plt.savefig(f'graphics/linhas_sns_{sufixo}.png', dpi=400)
    plt.show()


if __name__ == "__main__":
    gerar_grafico_linha_sns('data/dados_2022-06-09_10_22_9.csv')
