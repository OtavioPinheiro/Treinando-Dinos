import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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


def gerar_histograma(caminho_dos_dados: str) -> None:
    dados = obter_dados(caminho_dos_dados)
    pontuacoes: list = dados[0]
    plt.hist(x=pontuacoes, bins=10, range=(0, 100), color='green', histtype='bar', rwidth=0.8)
    plt.xlabel('Pontuações')
    plt.ylabel('Gerações')
    plt.title('Histograma de Pontuações')
    plt.savefig('graphics/histo.png', bbox_inches='tight')
    plt.show()


def gerar_grafico_de_barras(caminho_dos_dados: str) -> None:
    dados = obter_dados(caminho_dos_dados)
    pontuacoes: list = dados[0]
    geracoes: list = dados[1]
    plt.figure(figsize=(40, 15))
    plt.bar(x=geracoes, height=pontuacoes, align='edge', width=1.0, bottom=-1, color="green", edgecolor='black')
    # for i in range(len(geracoes)):
    #     plt.annotate(pontuacoes[i], (i - 0.5, int(pontuacoes[i]) + 500))
    plt.xlabel('Gerações')
    plt.ylabel('Pontuações')
    plt.title('Pontuações x Gerações')
    plt.tight_layout()
    plt.savefig('graphics/barras.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    gerar_grafico_de_barras('data/dados.csv')
