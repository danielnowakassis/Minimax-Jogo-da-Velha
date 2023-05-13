import time

import numpy as np
import platform
import functools
from os import system
from random import Random


def timer(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        t1 = time.perf_counter()
        res = func(self, *args, **kwargs)
        t2 = round(time.perf_counter() - t1, 6)
        print("Tempo da jogada: " + str(t2))
        return res
    return wrapper

class Board:
    def __init__(self):
        self.board = np.zeros(shape = (4,4))
        self.possible_plays = [a for a in range(16)]
        self.plays_ocurred = 0
    
    def render(self):
        """
        Plota o tabuleiro
        """
        simbolo = {
            1: "X",
            -1: "O",
            0: " "
        }
        str_line = '--------------------'
        cont = 1
        print('\n' + str_line)
        for linha in self.board:
            for cell in linha:
                symbol = simbolo[cell]
                symbol = str(cont) if symbol == ' ' else symbol
                print(f'| {symbol} |', end='')
                cont += 1
            print('\n' + str_line)

    def clean(self):
        """
        Limpa o console
        """
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')
    
    def check_win(self, jogada):
        """
        verifica se algum jogador ganhou a partida, dado sua jogada
        """
        if (jogada-1) // 4 in [0,3] and (jogada-1) % 4 in [0, 3]:  # Verifica diagonal para os cantos
            possible = 0
            if (jogada - 1) % 5 == 0:
                for i in range(4):
                    possible += self.board[i][i]       
            else:
                for i in range(4):
                    possible += self.board[i][3 - i]       
            if abs(possible) == 4:
                return True
        #verfica horizontal
        possible = 0
        for i in range(4):
            possible += self.board[(jogada-1) // 4][i]  
        if abs(possible) == 4:
            return True
        #verfica vertical
        possible = 0
        for i in range(4):
            possible += self.board[i][(jogada-1) % 4]
        return abs(possible) == 4   

    def contar_jogada(self):
        self.plays_ocurred += 1
        print(f"Jogada nº {self.plays_ocurred}")

class Jogador:

    def __init__(self, index):
        self.id = index


    def make_play(self, board : Board):
        """
        método para jogador realizar jogada e alterar estado do tabuleiro
        """

class Humano(Jogador):
    def __init__(self):
        super().__init__(index = 1)

    @timer
    def make_play(self, tabuleiro : Board):
        """
        método para jogador realizar jogada e alterar estado do tabuleiro
        """
        play_not_made = True
        a = -1
        while play_not_made:
            a = int(input("Jogada (numpad) : 1...16 "))
            if tabuleiro.board[(a-1) // 4][(a-1) % 4] == 0:
                tabuleiro.board[(a-1) // 4][(a-1) % 4] = self.id
                tabuleiro.possible_plays.remove(a - 1)
                play_not_made = False
                tabuleiro.contar_jogada()
            else:
                print("Jogada" + str(a) + "não é possível. Tente outra jogada")
        return a

POSSIBLE_TYPES = ["Random", "MiniMax", "MiniMaxAlphaBeta" ]
class Maquina(Jogador):
    def __init__(self, index, type):
        super().__init__(index)
        if type not in POSSIBLE_TYPES:
            print("Tipo do agente não reconhecido, escolha entre : " + POSSIBLE_TYPES)
        self.type = type

        if type == "Random":
            self.random = Random()

    @timer
    def make_play(self, board : Board):
        """
        método para maquina realizar jogada e alterar estado do tabuleiro
        """
        a = -1
        if self.type == "Random":
            play = board.possible_plays[self.random.randint(0, len(board.possible_plays)-1)]
            board.possible_plays.remove(play)
            board.board[(play) // 4][(play) % 4] = self.id
            board.contar_jogada()
            
        elif self.type == "MiniMax":
            "TODO"
        else:
            "TODO"

        return a

if __name__ == "__main__":
    """
    #Instanciamento de variáveis
    """
    inteligenca_bots = "Random"
    jogo = Board()
    n_jogadas = 0
    maquina = Maquina(-1, inteligenca_bots)
    modo = ""

    """
    #Seleção do momdo de jogo
    """
    print("Selecione o modo de jogo:")
    print("-Jogador Versus Máquina (JxM)")
    print("-Máquina Versus Máquina (MxM)")

    while True:
        modo = input()
        if modo in ["JxM", "MxM"]:
            break
        raise Exception("Selecione um modo válido")

    if modo == "JxM":
        jogador = Humano()
    else:
        jogador = Maquina(1, inteligenca_bots)

    """
    Início do jogo
    """
    while True:
        print()
        jogo.render()
        print()
        jogada = jogador.make_play(jogo)
        if jogo.check_win(jogada):
            print("JOGADOR 1 GANHOU")
            break
        #jogo.clean()

        jogo.render()
        print()
        jogada = maquina.make_play(jogo)
        if jogo.check_win(jogada):
            print("JOGADOR 2 GANHOU")
            break
        #jogo.clean()
    jogo.render()