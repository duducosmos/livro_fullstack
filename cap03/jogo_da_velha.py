#!/usr/bin/env python3.6
# -*- coding: UTF-8 -*-
"""
Um jogo da velha simples.

Copyright 2017 E. S. Pereira

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software
without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

from curses import initscr, wrapper
from random import randint


def boas_vindas(stdscr):
    """
    Exibe a tela de boas vindas.
    """
    stdscr.addstr(1, 1, "Bem vindo ao Jogo da Velha.")
    stdscr.addstr(2, 1, "Digite q para sair e h para obter ajuda.")


def fim_de_jogo(stdscr, gan):
    "Mostra o vencedor"
    stdscr.addstr(6, 1, "O %s venceu..." % gan)
    stdscr.addstr(7, 1, "Precione y para jogar novamente ou q para sair.")


def creditos(stdscr):
    """
    Creditos e Licença
    """
    stdscr.addstr(16, 1, "Desenvovido por : E. S. Pereira.")
    stdscr.addstr(17, 1, "Licensa Nova BSD.")


def ajuda(stdscr):
    """
    Exibi as informações de ajuda do jogo.
    """
    stdscr.addstr(1, 1, "Digite q para sair e h para ajuda.")
    stdscr.addstr(2, 1, "Para mudar a posicao use as teclas: a,d,s,w")
    stdscr.addstr(3, 1, "Para definir uma posição do jogo digite: l")
    stdscr.addstr(4, 1, "Para reiniciar a partida digite: y")


def tela_do_jogo(stdscr, posicoes, x_center):
    """
    Recebe a lista com as posições atual de cada jogada e exibe o resultado na tela.
    """
    i = 9
    stdscr.addstr(10, x_center - 3, "------")
    stdscr.addstr(12, x_center - 3, "------")
    for linha in posicoes:
        tela = "%s|%s|%s " % tuple(linha)
        stdscr.addstr(i, x_center - 3, tela)
        i += 2


def limites(pos_x, pos_y):
    '''
    Verifica se cursor está no limite da tela do jogo.
    '''
    if pos_x > 2:
        pos_x = 0
    if pos_x < 0:
        pos_x = 2

    if pos_y > 2:
        pos_y = 0

    if pos_y < 0:
        pos_y = 2

    return pos_x, pos_y


def cursor(pos_x, pos_y, entrada):
    """
    Atualiza a posição do cursor de acordo com a tecla digitada.
    """
    if entrada == 'a':
        pos_x, pos_y = limites(pos_x - 1, pos_y)
    elif entrada == 'd':
        pos_x, pos_y = limites(pos_x + 1, pos_y)
    elif entrada == 's':
        pos_x, pos_y = limites(pos_x, pos_y + 1)
    elif entrada == 'w':
        pos_x, pos_y = limites(pos_x, pos_y - 1)
    else:
        pass

    return pos_x, pos_y


def blink(pos_x, pos_y, stdscr, x_center):
    """
    Atualiza a posição do blink na tela
    """
    y_blink = 9
    x_blink = x_center - 3
    if pos_y == 1:
        y_blink += 2

    if pos_y == 2:
        y_blink += 4

    if pos_x == 1:
        x_blink += 2

    if pos_x == 2:
        x_blink += 4

    stdscr.move(y_blink, x_blink)


def atualiza_jogada(pos_x, pos_y, posicoes, fixar):
    """
    Atualiza a lista contendo informações da jogada.
    """
    if fixar is True:
        posicoes[pos_y][pos_x] = "o"
    return posicoes


def computador(posicoes):
    """
    Jogada do computador
    """

    vazias = []
    for i in range(0, 3):
        for j in range(0, 3):
            if posicoes[j][i] == " ":
                vazias.append([j, i])
    n_escolhas = len(vazias)
    if n_escolhas != 0:
        j, i = vazias[randint(0, n_escolhas - 1)]
        posicoes[j][i] = "x"
    return posicoes


def total_alinhado(linha):
    """
    Retorna x ou o se o total desses elementos na linha for igual a 3.
    Do contrário retorna vazio
    """
    num_x = linha.count("x")
    num_o = linha.count("o")

    if num_x == 3:
        return "x"
    if num_o == 3:
        return "o"


def ganhador(posicoes):
    """
    Retorna x ou o ou None. Dependento de quem ganhou o jogo
    """

    diagonal1 = [posicoes[0][0], posicoes[1][1], posicoes[2][2]]
    diagonal2 = [posicoes[0][2], posicoes[1][1], posicoes[2][0]]

    transposta = [[], [], []]
    for i in range(3):
        for j in range(3):
            transposta[i].append(posicoes[j][i])

    gan = total_alinhado(diagonal1)
    if gan is not None:
        return gan

    gan = total_alinhado(diagonal2)

    if gan is not None:
        return gan

    velha = 9

    for i in range(3):
        gan = total_alinhado(posicoes[i])

        if gan is not None:
            return gan

        gan = total_alinhado(transposta[i])
        if gan is not None:
            return gan

        velha -= posicoes[i].count("x")
        velha -= posicoes[i].count("o")

    if velha == 0:
        return "velha"


def main(stdscr):
    """
    Programa principal
    """
    stdscr.clear()
    stdscr.border()
    boas_vindas(stdscr)
    creditos(stdscr)

    width = stdscr.getmaxyx()[1]
    x_center = (width - 1) // 2

    posicoes = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    tela_do_jogo(stdscr, posicoes, x_center)

    pos_x = 0
    pos_y = 0
    blink(pos_x, pos_y, stdscr, x_center)
    stdscr.refresh()

    gan = None

    while True:
        entrada = stdscr.getkey()
        if entrada == 'q':
            break

        if(entrada in ['a', 's', 'w', 'd', '\n']):
            stdscr.clear()

            pos_x, pos_y = cursor(pos_x, pos_y, entrada)
            atualiza_jogada(pos_x, pos_y, posicoes, False)

            if entrada == "\n":
                if posicoes[pos_y][pos_x] == " " and gan is None:
                    atualiza_jogada(pos_x, pos_y, posicoes, True)
                    computador(posicoes)

        if entrada == "y":
            stdscr.clear()
            gan = None
            posicoes = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

            tela_do_jogo(stdscr, posicoes, x_center)

            pos_x = 0
            pos_y = 0
            atualiza_jogada(pos_x, pos_y, posicoes, False)
            stdscr.border()
            boas_vindas(stdscr)
            tela_do_jogo(stdscr, posicoes, x_center)
            blink(pos_x, pos_y, stdscr, x_center)

        gan = ganhador(posicoes)

        if gan is not None:
            fim_de_jogo(stdscr, gan)
        stdscr.border()

        if entrada == 'h':
            ajuda(stdscr)
        else:
            boas_vindas(stdscr)
        creditos(stdscr)
        tela_do_jogo(stdscr, posicoes, x_center)
        blink(pos_x, pos_y, stdscr, x_center)

        stdscr.refresh()


if __name__ == "__main__":
    initscr()
    wrapper(main)
