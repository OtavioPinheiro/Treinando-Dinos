import csv
import time

import neat
import pygame
import os
import random
import math
import sys
import datetime

from pygame.pixelarray import PixelArray

import GeradorDeGraficos

pygame.init()

# Constantes Globais
ALTURA_TELA = 600
LARGURA_TELA = 1400
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

CORRENDO = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
            pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

PULANDO = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

CACTO_PEQ = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
             pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
             pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

CACTO_GRD = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
             pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
             pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

PTERO = [pygame.image.load(os.path.join("Assets/SpriteSheets", "pitero_voa_1.png")),
         pygame.image.load((os.path.join("Assets/SpriteSheets", "pitero_voa_2.png")))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONTE = pygame.font.Font('freesansbold.ttf', 20)

CORES: dict = {
    "vermelho": (169, 1, 1),
    "azul": (0, 80, 184),
    "amarelo": (235, 160, 0),
    "verde": (77, 158, 7),
    "cinza": (83, 83, 83),
    "roxo": (89, 0, 184),
    "rosa": (159, 0, 138)
}

DADOS = []


class Dino:
    X_POS = 80
    Y_POS = 310
    ALTURA_PULO = 8.5

    def __init__(self, img=CORRENDO[0]):
        self.imagem = img
        self.dino_corre = True
        self.dino_pula = False
        self.pulo_vel = self.ALTURA_PULO
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.i: int = 0
        self.cor = sorted(CORES.values())[random.randint(0, 6)]
        self.step_index = 0

    def update(self):
        if self.dino_corre:
            self.corre()
        if self.dino_pula:
            self.pula()
        if self.step_index >= 10:
            self.step_index = 0

    def pula(self):
        self.imagem = PULANDO
        if self.dino_pula:
            self.rect.y -= self.pulo_vel * 4
            self.pulo_vel -= 0.8
        if self.pulo_vel <= -self.ALTURA_PULO:
            self.dino_pula = False
            self.dino_corre = True
            self.pulo_vel = self.ALTURA_PULO

    def corre(self):
        self.imagem = CORRENDO[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, TELA):
        TELA.blit(self.imagem, (self.rect.x, self.rect.y))
        pygame.draw.rect(TELA, self.cor, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        arr = PixelArray(self.imagem)
        arr.replace((83, 83, 83), self.cor)
        arr.close()
        for obstaculo in obstaculos:
            pygame.draw.line(TELA, self.cor, (self.rect.x + 54, self.rect.y + 12), obstaculo.rect.center, 2)


class Obstaculos:
    def __init__(self, imagem, numero_de_imgs, cor=(83, 83, 83)):
        self.imagem = imagem
        self.cor = cor
        self.type = numero_de_imgs
        self.rect = self.imagem[self.type].get_rect()
        self.rect.x = ALTURA_TELA + 700

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstaculos.pop()

    def draw(self, TELA):
        TELA.blit(self.imagem[self.type], self.rect)
        for img in self.imagem:
            arr = PixelArray(img)
            arr.replace((83, 83, 83), self.cor)
            arr.close()


class PeqCacto(Obstaculos):
    def __init__(self, imagem, numero_de_cactos, cor):
        super().__init__(imagem, numero_de_imgs=numero_de_cactos, cor=cor)
        self.rect.y = 325


class GrdCacto(Obstaculos):
    def __init__(self, imagem, numero_de_cactos, cor):
        super().__init__(imagem, numero_de_imgs=numero_de_cactos, cor=cor)
        self.rect.y = 300


class Ptero(Dino):
    X_POS = ALTURA_TELA + 700
    Y_POS = 150

    def __init__(self, altura: int, imagem=PTERO[0]):
        super().__init__(imagem)
        self.rect = self.imagem.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS + altura
        self.step_index = 0

    def voa(self):
        self.imagem = PTERO[self.step_index // 5]
        # self.rect.x = self.X_POS
        self.rect.x -= game_speed
        # self.rect.y = self.Y_POS
        self.step_index += 1

    def update(self):
        self.voa()
        if self.rect.x < -self.rect.width:
            obstaculos.pop()
        if self.step_index >= 10:
            self.step_index = 0

    def draw(self, TELA):
        TELA.blit(self.imagem, self.rect)


def remove(indice):
    dinos.pop(indice)
    ge.pop(indice)
    nets.pop(indice)


def distancia(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def angulo(cat_op: float, hip: float) -> float:
    return cat_op / hip


def define_max_score(pontos: int, geracao: int) -> int:
    global pontuacao_max, pontuacao
    if geracao == 0:
        pontuacao = []
        pontuacao_max = 0
    if pontos > pontuacao_max:
        pontuacao.append(pontos)
        pontuacao_max = max(pontuacao)
    return pontuacao_max


def escrever_no_arquivo(dados: list) -> str:
    cabecalho = ['Pontuação máxima', 'Geração']
    data = datetime.date.today()
    hora = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    sec = datetime.datetime.now().second
    sufixo = f"{data}_{hora}_{min}_{sec}"
    caminho_dos_dados = f"data/dados_{sufixo}.csv"
    if os.path.isfile(caminho_dos_dados):
        with open(caminho_dos_dados, 'r', encoding='UTF8', newline='') as fl:
            reader = csv.DictReader(fl)
            with open(caminho_dos_dados, 'a', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=cabecalho)
                print(f'cabeçalho: {reader.fieldnames}')
                if reader.fieldnames != cabecalho:
                    writer.writeheader()
                writer.writerows(dados)
    else:
        with open(caminho_dos_dados, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cabecalho)
            writer.writeheader()
            writer.writerows(dados)

    return caminho_dos_dados


def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstaculos, dinos, ge, nets, pontos
    clock = pygame.time.Clock()
    pontos = 0

    obstaculos = []
    dinos = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    for genome_id, genome in genomes:
        dinos.append(Dino())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global pontos, game_speed
        pontos += 1
        if pontos % 100 == 0:
            if game_speed >= 55:
                if pontos % 250 == 0:
                    game_speed += 1
            else:
                game_speed += 1
        text = FONTE.render(f'Pontos: {str(pontos)}', True, (0, 0, 0))
        TELA.blit(text, (950, 50))

    def estatisticas():
        global dinos, game_speed, ge, pontuacao_max
        cor_do_texto = (0, 0, 0)
        geracao = pop.generation
        pontuacao_max = define_max_score(pontos, geracao)
        texto_1 = FONTE.render(f'Dinossauros vivos: {str(len(dinos))}', True, cor_do_texto)
        texto_2 = FONTE.render(f'Geração: {geracao}', True, cor_do_texto)
        texto_3 = FONTE.render(f'Velocidade do Jogo: {str(game_speed)}', True, cor_do_texto)
        texto_4 = FONTE.render(f'Pontuação Máxima: {str(pontuacao_max)}', True, cor_do_texto)

        TELA.blit(texto_1, (50, 450))
        TELA.blit(texto_2, (50, 480))
        TELA.blit(texto_3, (50, 510))
        TELA.blit(texto_4, (50, 540))

    def background():
        global x_pos_bg, y_pos_bg
        largura_imagem = BG.get_width()
        TELA.blit(BG, (x_pos_bg, y_pos_bg))
        TELA.blit(BG, (largura_imagem + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -largura_imagem:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    linha = {}
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        TELA.fill((255, 255, 255))

        for dino in dinos:
            dino.update()
            dino.draw(TELA)

        if len(dinos) == 0:
            geracao = pop.generation
            linha["Pontuação máxima"] = pontos
            linha["Geração"] = geracao
            DADOS.append(linha)
            break

        if len(obstaculos) == 0:
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                obstaculos.append(PeqCacto(CACTO_PEQ, random.randint(0, 2), (6, 165, 54)))
            elif rand_int == 1:
                obstaculos.append(GrdCacto(CACTO_GRD, random.randint(0, 2), (6, 165, 54)))
            elif rand_int == 2:
                obstaculos.append(Ptero(random.randint(0, 150)))
                # obstaculos.append(Ptero(0))

        for obstaculo in obstaculos:
            obstaculo.draw(TELA)
            obstaculo.update()
            for i, dino in enumerate(dinos):
                if dino.rect.colliderect(obstaculo.rect):
                    # responsável por reduzir as chances de passar os genes para a próxima geração
                    # é a punição caso ele se colida com o obstáculo
                    ge[i].fitness -= 10
                    remove(i)
                else:
                    ge[i].fitness = pontos

        # user_input = pygame.key.get_pressed()
        # angulo((dino.rect.y - obstaculo.rect.y),distancia((dino.rect.x, dino.rect.y), obstaculo.rect.midtop))

        for i, dino in enumerate(dinos):
            output = nets[i].activate((dino.rect.y - obstaculo.rect.y,
                                       dino.rect.x - obstaculo.rect.x,
                                       distancia((dino.rect.x, dino.rect.y), obstaculo.rect.midtop),
                                       obstaculo.rect.y - 110,
                                       distancia((dino.rect.x, dino.rect.y), obstaculo.rect.midtop) - game_speed))
            # print(output[0])
            if output[0] > 0.0 and dino.rect.y == dino.Y_POS:
                dino.dino_pula = True
                dino.dino_corre = False

            # if user_input[pygame.K_SPACE]:
            #   dino.dino_pula = True
            #   dino.dino_corre = False

        estatisticas()
        score()
        background()
        clock.tick(30)
        pygame.display.update()
    # END main loop


# Setup the NEAT
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.run(eval_genomes, 5000)
    print(f'Pontuação máxima: {define_max_score(pontos, pop.generation)}')
    escrever_no_arquivo(DADOS)


if __name__ == "__main__":
    try:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        run(config_path)
    except SystemExit as ext:
        if ext.code:
            pass
        else:
            pass
    finally:
        caminhos_dos_dados = escrever_no_arquivo(DADOS)
        GeradorDeGraficos.gerar_grafico_linha_sns(caminhos_dos_dados)
