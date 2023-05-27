import time
import copy
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
        self.board = np.zeros(shape=(4, 4))
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

    def check_win(self):
        """
        verifica se algum jogador ganhou a partida, dado sua jogada
        """
        for i in range(4):
            possible = 0
            for j in range(4):
                possible += jogo.board[i][j]
            if abs(possible) == 4:
                return True

        for i in range(4):
            possible = 0
            for j in range(4):
                possible += jogo.board[j][i]
            if abs(possible) == 4:
                return True

        possible = 0
        for i in range(4):
            possible += jogo.board[i][i]
        if abs(possible) == 4:
            return True
        possible = 0
        for i in range(4):
            possible += jogo.board[i][3 - i]
        if abs(possible) == 4:
            return True

        return False

    def contar_jogada(self):
        self.plays_ocurred += 1
        print(f"Jogada nº {self.plays_ocurred}")

    def count_play(self, jogada : int, index : int):
        self.possible_plays.remove(jogada)
        self.board[(jogada) // 4][(jogada) % 4] = index
        self.contar_jogada()


class Jogador:

    def __init__(self, index):
        self.id = index

    def make_play(self, board: Board):
        """
        método para jogador realizar jogada e alterar estado do tabuleiro
        """


class Humano(Jogador):
    def __init__(self):
        super().__init__(index=1)

    @timer
    def make_play(self, tabuleiro: Board):
        """
        método para jogador realizar jogada e alterar estado do tabuleiro
        """
        play_not_made = True
        a = -1
        while play_not_made:
            a = int(input("Jogada (numpad) : 1...16 "))
            if tabuleiro.board[(a - 1) // 4][(a - 1) % 4] == 0:
                play_not_made = False
            else:
                print("Jogada " + str(a) + " não é possível. Tente outra jogada")
        return a - 1


POSSIBLE_TYPES = ["Random", "MiniMax", "MiniMaxAlphaBeta"]


class Maquina(Jogador):
    def __init__(self, index, type, max_depth):
        super().__init__(index)
        if type not in POSSIBLE_TYPES:
            print("Tipo do agente não reconhecido, escolha entre : " + POSSIBLE_TYPES)
        self.type = type
        self.nos_percorridos = 0

        if type == "Random":
            self.random = Random()
        else:
            self.max_depth = max_depth

    @timer
    def make_play(self, board: Board):
        """
        método para maquina realizar jogada
        """
        a = -1
        if self.type == "Random":
            play = board.possible_plays[self.random.randint(0, len(board.possible_plays) - 1)]
            a = play
        elif self.type == "MiniMax":
            copia = copy.deepcopy(board)
            minimax = self.minimax(copia, 1, self.id)
            #print(minimax)
            #print()
            play = minimax[0]
            a = play
            print("nós percorridos : ", self.nos_percorridos)
            self.nos_percorridos = 0
        else:
            copia = copy.deepcopy(board)
            alfabeta = self.alfa_beta(copia, 1, self.id, -np.Inf, np.Inf)
            play = alfabeta[0]
            a = play
            print("nós percorridos : ", self.nos_percorridos)
            self.nos_percorridos = 0
        assert a in range(16)
        return a

    def win_state(self,jogo, player):
        for i in range(4):
            possible = 0
            for j in range(4):
                possible += jogo.board[i][j]
            if possible == player * 4:
                return 1
            elif possible == -player * 4:
                return -1
        for i in range(4):
            possible = 0
            for j in range(4):
                possible += jogo.board[j][i]
            if possible == player * 4:
                return 1
            elif possible == -player * 4:
                return -1

        possible = 0
        for i in range(4):
            possible += jogo.board[i][i]
        if possible == player * 4:
            return 1
        elif possible == -player * 4:
            return -1
        possible = 0
        for i in range(4):
            possible += jogo.board[i][3 - i]
        if possible == player * 4:
            return 1
        elif possible == -player * 4:
            return -1
        return 0.0

    def possible_wins(self, jogo, player):
        n = 0

        for i in range(0,4):
            ally = 0
            enemy = 0
            empty = 0
            for j in range(0, 4):
                if jogo.board[i][j] == player:
                    ally += 1
                elif jogo.board[i][j] == 0:
                    empty += 1
                else:
                    enemy += 1

            if ally == 4:
                return np.inf
            elif enemy == 4:
                return -np.inf

            if ally + empty == 4:
                n += 1
            elif enemy + empty == 4:
                n -= 1

        for i in range(0, 4):
            ally = 0
            enemy = 0
            empty = 0
            for j in range(0, 4):
                if jogo.board[j][i] == player:
                    ally += 1
                elif jogo.board[j][i] == 0:
                    empty += 1
                else:
                    enemy += 1

            if ally == 4:
                return np.inf
            elif enemy == 4:
                return -np.inf

            if ally + empty == 4:
                n += ally
            elif enemy + empty == 4:
                n -= enemy

        ally = 0
        enemy = 0
        empty = 0
        for i in range(0, 4):
            if jogo.board[i][i] == player:
                ally += 1
            elif jogo.board[i][i] == 0:
                empty += 1
            else:
                enemy += 1

        if ally == 4:
            return np.inf
        elif enemy == 4:
            return -np.inf

        if ally + empty == 4:
            n += ally
        elif enemy + empty == 4:
            n -= enemy

        ally = 0
        enemy = 0
        empty = 0
        for i in range(0, 4):
            if jogo.board[i][3 - i] == player:
                ally += 1
            elif jogo.board[i][3 - i] == 0:
                empty += 1
            else:
                enemy += 1

        if ally == 4:
            return np.inf
        elif enemy == 4:
            return -np.inf

        if ally + empty == 4:
            n += ally
        elif enemy + empty == 4:
            n -= enemy

        return n

    def eval(self, jogo, player):
        """
        Heuristica de avaliação.

        """
        if player == 1:
            return self.possible_wins(jogo, 1) - self.possible_wins(jogo, -1)
        else:
            return self.possible_wins(jogo, -1) - self.possible_wins(jogo, 1)

    def minimax(self, state, depth, player):
        self.nos_percorridos += 1
        """

        """
        if depth % 2 == 1:  # depth ímpar
            agent = 'MAX'
        else:
            agent = 'MIN'  # depth par
        if len(state.possible_plays) == 1 or depth == self.max_depth:
            if agent == 'MAX':
                max_v = (-1, -np.Inf)
                for cell in state.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[cell // 4][cell % 4] = player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player)
                    if heuristica > max_v[1]:
                        max_v = (cell, heuristica, copia)
                    # print(max_v)
                return max_v
            else:
                min_v = (-1, +np.Inf)
                for cell in jogo.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[(cell) // 4][(cell) % 4] = player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player)
                    if heuristica < min_v[1]:
                        min_v = (cell, heuristica, copia)
                    # print(min_v)
                return min_v
        elif agent == 'MAX':
            return self.max_value(state, depth, player)
        elif agent == 'MIN':
            return self.min_value(state, depth, player)


    def max_value(self, jogo: Board, depth, player):
        max_v = (-1, -np.inf, 0)
        for cell in jogo.possible_plays:
            copia = copy.deepcopy(jogo)
            copia.board[(cell) // 4][(cell) % 4] = player
            copia.possible_plays.remove(cell)
            #heuristica = self.eval(copia, player)
            max_v = self.maximo(max_v, self.minimax(copia, depth + 1, player))
        return max_v

    def min_value(self, jogo: Board, depth, player):
        min_v = (-1, +np.inf, 0)
        for cell in jogo.possible_plays:
            copia = copy.deepcopy(jogo)
            copia.board[(cell) // 4][(cell) % 4] = player
            copia.possible_plays.remove(cell)
            #heuristica = self.eval(copia, player)
            min_v = self.minimo(min_v, self.minimax(copia, depth + 1, player))
        return min_v
    
    def alfa_beta(self, state: Board, depth: int, player : int, alpha = -np.Inf, beta = np.Inf): 
        self.nos_percorridos += 1
        """
            minimax com poda alfa beta
        """
        if depth % 2 == 1:  # depth ímpar
            agent = 'MAX'
        else:
            agent = 'MIN'  # depth par
        if len(state.possible_plays) == 1 or depth == self.max_depth:
            if agent == 'MAX':
                max_v = (-1, -np.Inf)
                for cell in state.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[cell // 4][cell % 4] = player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player)
                    if heuristica > max_v[1]:
                        max_v = (cell, heuristica, copia)
                    # print(max_v)
                return max_v
            else:
                min_v = (-1, +np.Inf)
                for cell in jogo.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[(cell) // 4][(cell) % 4] = player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player)
                    if heuristica < min_v[1]:
                        min_v = (cell, heuristica, copia)
                    # print(min_v)
                return min_v
        elif agent == 'MAX':
            return self.max_value_ab(state, depth, player,alpha, beta)
        elif agent == 'MIN':
            return self.min_value_ab(state, depth, player,alpha, beta)
        
    def max_value_ab(self, jogo: Board, depth, player,alpha, beta):
        max_v = (-1, -np.inf, 0)
        for cell in jogo.possible_plays:
            copia = copy.deepcopy(jogo)
            copia.board[(cell) // 4][(cell) % 4] = player
            copia.possible_plays.remove(cell)
            if self.win_state(copia, player) == 1:
                return (cell, +np.inf, copia)
            max_v = self.maximo(max_v, self.alfa_beta(copia, depth + 1, player,alpha, beta))
            if max_v[1] >= beta:
                return max_v
            alpha = max(max_v[1], alpha)
        return max_v

    def min_value_ab(self, jogo: Board, depth, player,alpha, beta):
        min_v = (-1, +np.inf, 0)
        for cell in jogo.possible_plays:
            copia = copy.deepcopy(jogo)
            copia.board[(cell) // 4][(cell) % 4] = -player
            copia.possible_plays.remove(cell)
            if self.win_state(copia, -player) == -1:
                return (cell, -np.inf, copia)
            min_v = self.minimo(min_v, self.alfa_beta(copia, depth + 1, player,alpha, beta))
            if min_v[1] <= alpha:
                return min_v
            beta = min(beta, min_v[1])
        return min_v

    def maximo(self, tuple_v, heuristic):
        if tuple_v[1] > heuristic[1]:
            return tuple_v
        else:
            return heuristic

    def minimo(self, tuple_v, heuristic):
        if tuple_v[1] < heuristic[1]:
            return tuple_v
        else:
            return heuristic


if __name__ == "__main__":
    """
    #Instanciamento de variáveis
    """
    inteligenca_bots = "MiniMaxAlphaBeta"
    jogo = Board()
    n_jogadas = 0
    maquina = Maquina(-1, inteligenca_bots, max_depth=5)
    modo = ""

    """
    #Seleção do modo de jogo
    """
    print("Selecione o modo de jogo:")
    print("-Jogador Versus Máquina (1)")
    print("-Máquina Versus Máquina (2)")
    print("-Máquina Versus Máquina (3)")

    while True:
        modo = input()
        if modo in ["1", "2"]:
            break
        raise Exception("Selecione um modo válido")

    if modo == "1":
        jogador = Humano()
    else:
        jogador = Maquina(1, inteligenca_bots, max_depth=5)

    """
    Início do jogo
    """
    while True:
        print()
        jogo.render()
        print()
        # if modo == "MxM":
        #    time.sleep(1)
        jogada = jogador.make_play(jogo)
        jogo.count_play(jogada, 1)
        if jogo.check_win():
            print("JOGADOR 1 GANHOU")
            break
        # jogo.clean()

        jogo.render()
        print()
        jogada = maquina.make_play(jogo)
        jogo.count_play(jogada, -1)
        if jogo.check_win():
            print("JOGADOR 2 GANHOU")
            break
        elif jogo.plays_ocurred == 16:
            print("EMPATE")
            break
        # jogo.clean()
    jogo.render()