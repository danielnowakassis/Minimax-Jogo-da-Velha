import time
import copy
import numpy as np
import platform
import functools
from os import system
from random import Random


def timer(func):
    '''
    Função para contar tempo da jogada
    '''
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
            for cell in copia.possible_plays:
                copia = copy.deepcopy(jogo)
                copia.board[cell // 4][cell % 4] = self.id
                copia.possible_plays.remove(cell)
                if self.win_state(copia, self.id) == self.id:
                    a = cell
                if self.avoid_win(cell, copia, self.id):
                    a = cell
            if a == -1:
                copia = copy.deepcopy(board)
                minimax = self.minimax(copia, 1, self.id)
                play = minimax[0]
                a = play
                print("nós percorridos : ", self.nos_percorridos)
                self.nos_percorridos = 0
        else:
            copia = copy.deepcopy(board)
            for cell in copia.possible_plays:
                copia = copy.deepcopy(jogo)
                copia.board[cell // 4][cell % 4] = self.id
                copia.possible_plays.remove(cell)
                if self.win_state(copia, self.id) == self.id:
                    a = cell
                    break
                if self.avoid_win(cell, copia, self.id):
                    a = cell
            if a == -1:
                copia = copy.deepcopy(board)
                alfabeta = self.alfa_beta(copia, 1, self.id, -np.Inf, np.Inf)
                play = alfabeta[0]
                a = play
                print("nós percorridos : ", self.nos_percorridos)
                self.nos_percorridos = 0
        assert a in range(16)
        return a

    def avoid_win(self,jogada,jogo, player):
        '''
        Dado uma jogada, verifica se essa evita ganho do oponente
        '''
        if jogada in [0,15]:
            score_player = 0
            score_oponent = 0
            for i in range(4):
                if jogo.board[i][i] == player:
                    score_player += 1
                if jogo.board[i][i] == -player:
                    score_oponent += 1
            if score_player == 1 and score_oponent == 3:
                return True
        if jogada in [3,11]:
            score_player = 0
            score_oponent = 0
            for i in range(4):
                if jogo.board[i][3 - i] == player:
                    score_player += 1
                if jogo.board[i][3 - i] == -player:
                    score_oponent += 1
            if score_player == 1 and score_oponent == 3:
                return True
        score_player = 0
        score_oponent = 0
        for i in range(4):
            if jogo.board[i][jogada % 4] == player:
                    score_player += 1
            if jogo.board[i][jogada % 4] == -player:
                score_oponent += 1
        if score_player == 1 and score_oponent == 3:
            return True
        score_player = 0
        score_oponent = 0
        for i in range(4):
            if jogo.board[jogada // 4][i] == player:
                    score_player += 1
            if jogo.board[jogada // 4][i] == -player:
                score_oponent += 1
        if score_player == 1 and score_oponent == 3:
            return True
        return False

    def win_state(self,jogo, player):
        '''
        Retorna 1 caso o player ganhou dado o estado do jogo,
        Retorna 0 caso houve empate ou nenhum dos jogadores ganhou dado o estado do tabuleiro,
        Retorna -1 caso o player perdeu dado o estado do jogo.
        '''
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
        """
        dado um jogador, retorna o número de jogadas possíveis com ganho
        """
        n = 0
        for i in range(4):
            possible = 0
            for j in range(4):
                if jogo.board[i][j] == 0 or jogo.board[i][j] == player:
                    possible += 1
            if possible == 4:
                n += 1

        for i in range(4):
            possible = 0
            for j in range(4):
                if jogo.board[j][i] == 0 or jogo.board[j][i] == player:
                    possible += 1
            if possible == 4:
                n += 1

        possible = 0
        for i in range(4):
            if jogo.board[i][i] == 0 or jogo.board[i][i] == player:
                possible += 1
        if possible == 4:
            n += 1
        possible = 0

        for i in range(4):
            if jogo.board[i][3 - i] == 0 or jogo.board[i][3 - i] == player:
                possible += 1
        if possible == 4:
            n += 1

        return n

    def eval(self, jogo, player, agent_type):
        """
        Heuristica de avaliação.

        """
        if player == 1:
            if agent_type == 'MAX':
                return self.possible_wins(jogo, 1) - self.possible_wins(jogo, -1)
            else:
                return self.possible_wins(jogo, -1) - self.possible_wins(jogo, 1)
        else:
            if agent_type == 'MAX':
                return self.possible_wins(jogo, -1) - self.possible_wins(jogo, 1)
            else:
                return self.possible_wins(jogo, 1) - self.possible_wins(jogo, -1)
        
    def minimax(self, state, depth, player):
        self.nos_percorridos += 1
        """
        Algoritmo minimax sem poda alfa beta
        """
        if depth % 2 == 1:  # depth ímpar
            agent = 'MAX'
        else:
            agent = 'MIN'  # depth par
        #Nós terminais
        if len(state.possible_plays) == 1 or depth == self.max_depth:
            if agent == 'MAX':
                max_v = (-1, -np.Inf)
                for cell in state.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[cell // 4][cell % 4] = player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player, 'MAX')
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
                    heuristica = self.eval(copia, player, 'MIN')
                    if heuristica < min_v[1]:
                        min_v = (cell, heuristica, copia)
                    # print(min_v)
                return min_v
        #MAX
        elif agent == 'MAX':
            return self.max_value(state, depth, player)
        #MIN
        elif agent == 'MIN':
            return self.min_value(state, depth, player)


    def max_value(self, jogo: Board, depth, player):
        '''
        max value para minimax
        '''
        max_v = (-1, -np.inf, 0)
        for cell in jogo.possible_plays:
            copia = copy.deepcopy(jogo)
            copia.board[(cell) // 4][(cell) % 4] = player
            copia.possible_plays.remove(cell)
            max_v = self.maximo(max_v, self.minimax(copia, depth + 1, player))
        return max_v

    def min_value(self, jogo: Board, depth, player):
        '''
        min value para minimax
        '''
        min_v = (-1, +np.inf, 0)
        for cell in jogo.possible_plays:
            copia = copy.deepcopy(jogo)
            copia.board[(cell) // 4][(cell) % 4] = -player
            copia.possible_plays.remove(cell)
            if self.win_state(copia, player) == -1:
                return (cell, +np.inf, copia)
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
        #nós terminais
        if len(state.possible_plays) == 1 or depth == self.max_depth:
            if agent == 'MAX':
                max_v = (-1, -np.Inf)
                for cell in state.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[cell // 4][cell % 4] = player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player, 'MAX')
                    if heuristica > max_v[1]:
                        max_v = (cell, heuristica, copia)
                    # print(max_v)
                return max_v
            else:
                min_v = (-1, +np.Inf)
                for cell in jogo.possible_plays:
                    copia = copy.deepcopy(jogo)
                    copia.board[(cell) // 4][(cell) % 4] = -player
                    copia.possible_plays.remove(cell)
                    heuristica = self.eval(copia, player, 'MIN')
                    if heuristica < min_v[1]:
                        min_v = (cell, heuristica, copia)
                    # print(min_v)
                return min_v
        #MAX
        elif agent == 'MAX':
            return self.max_value_ab(state, depth, player,alpha, beta)
        #MIN
        elif agent == 'MIN':
            return self.min_value_ab(state, depth, player,alpha, beta)
        
    def max_value_ab(self, jogo: Board, depth, player,alpha, beta):
        '''
        max value para minimax com poda alfa beta
        '''
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
        '''
        min value para minimax com poda alfa beta
        '''
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

    """
    Funções que comparam max para elementos especificos de tuplas e retornam a tupla desejada
    """
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
   
    jogo = Board()
    n_jogadas = 0
    
    modo = ""

    """
    #Seleção do modo de jogo
    """
    print("Selecione o modo de jogo:")
    print("-Jogador Versus Máquina (1)")
    print("-Máquina Versus Máquina (2)")
    while True:
        modo = input()
        if modo in ["1", "2"]:
            break
        raise Exception("Selecione um modo válido")
    print('Selecione o número de jogadas a frente que o(s) computador(es) deve(m) computar : ')
    max_depth = int(input())
    print("Selecione a inteligencia do Bot")
    print("1 - Random")
    print("2 - MiniMax")
    print("3 - MiniMaxAlphaBeta")
    inteligencia = input()
    if inteligencia == "1":
        inteligenca_bots = "Random"
    elif inteligencia == "2":
        inteligenca_bots = "MiniMax"
    elif inteligencia == "3":
        inteligenca_bots = "MiniMaxAlphaBeta"
    else:
        raise Exception("Selecione um modo válido")

    if modo == "1":
        jogador = Humano()
        maquina = Maquina(-1, inteligenca_bots, max_depth=max_depth)
    else:
        jogador = Maquina(1, inteligenca_bots, max_depth=max_depth)
        print("Selecione a inteligencia do Bot")
        print("1 - Random")
        print("2 - MiniMax")
        print("3 - MiniMaxAlphaBeta")
        inteligencia = input()
        if inteligencia == "1":
            inteligenca_bots = "Random"
        elif inteligencia == "2":
            inteligenca_bots = "MiniMax"
        elif inteligencia == "3":
            inteligenca_bots = "MiniMaxAlphaBeta"
        else:
            raise Exception("Selecione um modo válido")
        maquina = Maquina(-1, inteligenca_bots, max_depth=max_depth)

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
        if maquina.possible_wins(jogo, 1) == 0 and maquina.possible_wins(jogo, -1) == 0:
            print("EMPATE")
            break
        # jogo.clean()

        jogo.render()
        print()
        jogada = maquina.make_play(jogo)
        jogo.count_play(jogada, -1)
        if jogo.check_win():
            print("JOGADOR 2 GANHOU")
            break
        if maquina.possible_wins(jogo, 1) == 0 and maquina.possible_wins(jogo, -1) == 0:
            print("EMPATE")
            break
        # jogo.clean()
    jogo.render()