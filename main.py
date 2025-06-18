import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
import json


pygame.init()
inicializarBancoDeDados()


tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Foge do Zagueiro - Neymar Edition")


relogio = pygame.time.Clock()


branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
amarelo = (255, 255, 0)


icone = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)

neymar = pygame.image.load("assets/Neymar.png")
zagueiro = pygame.image.load("assets/zuniga.png")
fundoStart = pygame.image.load("assets/FotoSoccer.jpg")
fundoJogo = pygame.image.load("assets/FotoSoccer.jpg")
fundoDead = pygame.image.load("assets/fundoDead.png")

# Tamanho dos bonecos
larguraNeymar = int(tamanho[0] * 0.25)
alturaNeymar = int(tamanho[1] * 0.30)

larguraZagueiro = int(tamanho[0] * 0.20)
alturaZagueiro = int(tamanho[1] * 0.28)


neymar = pygame.transform.scale(neymar, (larguraNeymar, alturaNeymar))
zagueiro = pygame.transform.scale(zagueiro, (larguraZagueiro, alturaZagueiro))
fundoStart = pygame.transform.scale(fundoStart, tamanho)
fundoJogo = pygame.transform.scale(fundoJogo, tamanho)
fundoDead = pygame.transform.scale(fundoDead, tamanho)

# Sons
explosaoSound = pygame.mixer.Sound("assets/Gta 5 Tela de Morte.wav")
pygame.mixer.music.load("assets/Batucada Futbolera de Boca.mp3")

# Fontes
fonteMenu = pygame.font.SysFont("comicsans", 24)
fonteTexto = pygame.font.SysFont("arial", 24)
fonteMorte = pygame.font.SysFont("arial", 100)
fonteBoasVindas = pygame.font.SysFont("arial", 32)




def jogar():
    pygame.mixer.music.play(-1)

    global nome

    # Obter nome do jogador
    root = tk.Tk()
    root.withdraw()

    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root.deiconify()
    largura_janela = 300
    altura_janela = 50
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    root.mainloop()

    tela_boas_vindas()

    posicaoXNeymar = 400
    posicaoYNeymar = 500
    movimentoXNeymar = 0
    movimentoYNeymar = 0

    posicaoXZagueiro = random.randint(0, tamanho[0] - larguraZagueiro)
    posicaoYZagueiro = -alturaZagueiro
    velocidadeZagueiro = 4

    pontos = 0
    pausado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                if not pausado:
                    if evento.key == pygame.K_RIGHT:
                        movimentoXNeymar = 15
                        movimentoYNeymar = 0
                    if evento.key == pygame.K_LEFT:
                        movimentoXNeymar = -15
                        movimentoYNeymar = 0
                    if evento.key == pygame.K_UP:
                        movimentoYNeymar = -15
                        movimentoXNeymar = 0
                    if evento.key == pygame.K_DOWN:
                        movimentoYNeymar = 15
                        movimentoXNeymar = 0

            elif evento.type == pygame.KEYUP:
                if not pausado:
                    movimentoXNeymar = 0
                    movimentoYNeymar = 0

        if not pausado:
            posicaoXNeymar += movimentoXNeymar
            posicaoYNeymar += movimentoYNeymar

            posicaoXNeymar = max(0, min(posicaoXNeymar, tamanho[0] - larguraNeymar))
            posicaoYNeymar = max(0, min(posicaoYNeymar, tamanho[1] - alturaNeymar))

            posicaoYZagueiro += velocidadeZagueiro
            if posicaoYZagueiro > tamanho[1]:
                posicaoYZagueiro = -alturaZagueiro
                pontos += 1
                velocidadeZagueiro += 0.5
                posicaoXZagueiro = random.randint(0, tamanho[0] - larguraZagueiro)

        tela.blit(fundoJogo, (0, 0))
        tela.blit(neymar, (posicaoXNeymar, posicaoYNeymar))
        tela.blit(zagueiro, (posicaoXZagueiro, posicaoYZagueiro))

        texto = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto, (15, 15))

        pauseMsg = fonteMenu.render("Press Space to Pause Game", True, branco)
        tela.blit(pauseMsg, (15, 45))

        jogador_rect = pygame.Rect(
            posicaoXNeymar + 30, posicaoYNeymar + 30,
            larguraNeymar - 60, alturaNeymar - 60
        )
        zagueiro_rect = pygame.Rect(
            posicaoXZagueiro + 20, posicaoYZagueiro + 20,
            larguraZagueiro - 40, alturaZagueiro - 40
        )

        if jogador_rect.colliderect(zagueiro_rect) and not pausado:
            escreverDados(nome, pontos)
            dead()

        if pausado:
            pause_text = fonteMorte.render("PAUSE", True, amarelo)
            tela.blit(pause_text, (350, 250))

        pygame.display.update()
        relogio.tick(60)
        
def start():
    pygame.mixer.music.play(-1)

    larguraButtonStart = 200
    alturaButtonStart = 50
    larguraButtonQuit = 200
    alturaButtonQuit = 50

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 180
                    alturaButtonStart = 45
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 180
                    alturaButtonQuit = 45

            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 200
                    alturaButtonStart = 50
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 200
                    alturaButtonQuit = 50
                    pygame.quit()
                    quit()

        tela.blit(fundoStart, (0, 0))

        startButton = pygame.draw.rect(tela, branco, (50, 50, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (70, 60))

        quitButton = pygame.draw.rect(tela, branco, (50, 120, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (70, 130))

        pygame.display.update()
        relogio.tick(60)


        
def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    tela.blit(fundoDead, (0, 0))

    with open("base.atitus", "r") as f:
        log_partidas = json.load(f)

    texto_morte = fonteMorte.render("GAME OVER", True, vermelho)
    tela.blit(texto_morte, (200, 100))

    logs = list(log_partidas.items())[-5:]

    y_offset = 300
    for jogador, dados in logs:
        texto = fonteTexto.render(f"{jogador}: {dados[0]} pontos em {dados[1]}", True, preto)
        tela.blit(texto, (100, y_offset))
        y_offset += 40

    pygame.display.update()
    pygame.time.delay(5000)
    start()


start()


        