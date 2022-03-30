import neat
import pygame
import os
import random
import math
import sys

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

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONTE = pygame.font.Font('freesansbold.ttf', 20)


class Dino:
    X_POS = 80
    Y_POS = 310
    PULO_VEL = 8.5

    def __init__(self, img=CORRENDO[0]):
        self.imagem = img
        self.dino_corre = True
        self.dino_pula = False
        self.pulo_vel = self.PULO_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
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
        if self.pulo_vel <= -self.PULO_VEL:
            self.dino_pula = False
            self.dino_corre = True
            self.pulo_vel = self.PULO_VEL

    def corre(self):
        self.imagem = CORRENDO[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, TELA):
        TELA.blit(self.imagem, (self.rect.x, self.rect.y))
        pygame.draw.rect(TELA, self.cor, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstaculo in obstaculos:
            pygame.draw.line(TELA, self.cor, (self.rect.x + 54, self.rect.y + 12), obstaculo.rect.center, 2)

class Obstaculos:
    def __init__(self, imagem, numero_de_cactos):
        self.imagem = imagem
        self.type = numero_de_cactos
        self.rect = self.imagem[self.type].get_rect()
        self.rect.x = ALTURA_TELA + 200

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstaculos.pop()

    def draw(self, TELA):
        TELA.blit(self.imagem[self.type], self.rect)

class PeqCacto(Obstaculos):
    def __init__(self, imagem, numero_de_cactos):
        super().__init__(imagem, numero_de_cactos)
        self.rect.y = 325

class GrdCacto(Obstaculos):
    def __init__(self, imagem, numero_de_cactos):
        super().__init__(imagem, numero_de_cactos)
        self.rect.y = 300

def remove(indice):
    dinos.pop(indice)
    ge.pop(indice)
    nets.pop(indice)

def distancia(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)

def eval_gnomes(genomes, config):
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
            game_speed += 1
        text = FONTE.render(f'Pontos: {str(pontos)}', True, (0, 0, 0))
        TELA.blit(text, (950, 50))

    def estatisticas():
        global dinos, game_speed, ge
        text_1 = FONTE.render(f'Dinossauros vivos: {str(len(dinos))}', True, (0, 0, 0))
        text_2 = FONTE.render(f'Geração: {pop.generation + 1}', True, (0, 0, 0))
        text_3 = FONTE.render(f'Velocidade do Jogo: {str(game_speed)}', True, (0, 0, 0))

        TELA.blit(text_1, (50, 450))
        TELA.blit(text_2, (50, 480))
        TELA.blit(text_3, (50, 510))

    def background():
        global x_pos_bg, y_pos_bg
        largura_imagem = BG.get_width()
        TELA.blit(BG, (x_pos_bg, y_pos_bg))
        TELA.blit(BG, (largura_imagem + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -largura_imagem:
            x_pos_bg = 0
        x_pos_bg -= game_speed

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
            break

        if len(obstaculos) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstaculos.append(PeqCacto(CACTO_PEQ, random.randint(0, 2)))
            elif rand_int == 1:
                obstaculos.append(GrdCacto(CACTO_GRD, random.randint(0, 2)))

        for obstaculo in obstaculos:
            obstaculo.draw(TELA)
            obstaculo.update()
            for i, dino in enumerate(dinos):
                if dino.rect.colliderect(obstaculo.rect):
                    ge[i].fitness -= 1
                    remove(i)

        # user_input = pygame.key.get_pressed()

        for i, dino in enumerate(dinos):
            output = nets[i].activate((dino.rect.y,
                                       distancia((dino.rect.x, dino.rect.y),
                                                 obstaculo.rect.midtop)))
            if output[0] > 0.6 and dino.rect.y == dino.Y_POS:
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
    pop.run(eval_gnomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
