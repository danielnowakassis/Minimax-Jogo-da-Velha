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
    def __init__(self, index, type, max_depth):
        super().__init__(index)
        if type not in POSSIBLE_TYPES:
            print("Tipo do agente não reconhecido, escolha entre : " + POSSIBLE_TYPES)
        self.type = type

        if type == "Random":
            self.random = Random()
        else:
          self.max_depth = max_depth
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
            a = play
            
        elif self.type == "MiniMax":
            copia = copy.deepcopy(board)
            play = self.minimax(copia, 1, -self.id)[0]
            assert play in range(16)
            board.possible_plays.remove(play)
            board.board[(play) // 4][(play) % 4] = self.id
            board.contar_jogada()
            a = play
        else:
            "TODO"
        
        return a

    def eval(self, jogo, player):
        """
        Heuristica de avaliação.
        
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

    def minimax(self,state, depth, player, jogada = (-1, np.inf)):
        """
        
        """
        if depth % 2 == 1: # depth ímpar
          agent = 'MAX'
        else:
          agent = 'MIN' # depth par
        if len(state.possible_plays) == 1 or depth == self.max_depth:
          if agent == 'MAX':
            max_v = (-1, -np.inf)
            for cell in state.possible_plays:
              copia = copy.deepcopy(jogo)
              copia.board[cell // 4][cell % 4] = player 
              copia.possible_plays.remove(cell)
              heuristica = self.eval(copia, player)
              if max_v[1] < heuristica:
                max_v = (cell, heuristica)
              #print(max_v)
              return max_v
          else:
            min_v = (-1, +np.inf)
            for cell in jogo.possible_plays:
              copia = copy.deepcopy(jogo)
              copia.board[(cell) // 4][(cell) % 4] = player 
              copia.possible_plays.remove(cell)
              heuristica = self.eval(copia, player)
              if min_v[1] > heuristica:
                min_v = (cell, heuristica)
              #print(min_v)
              return min_v
        elif agent == 'MAX':
          return self.max_value(state, depth,player, jogada)
        elif agent == 'MIN':
          return self.min_value(state, depth,-player, jogada)
      
    def max_value(self, jogo : Board, depth, player, jogada):
      max_v = (-1, -np.inf)
      for cell in jogo.possible_plays:
        copia = copy.deepcopy(jogo)
        copia.board[(cell) // 4][(cell) % 4] = player 
        copia.possible_plays.remove(cell)
        heuristica = self.eval(copia, player)
        max_v = self.maximo(max_v, self.minimax(copia, depth + 1, player, jogada))
      return max_v
      
        
    def min_value(self, jogo : Board, depth, player, jogada):
      min_v = (-1, +np.inf)
      for cell in jogo.possible_plays:
        copia = copy.deepcopy(jogo)
        copia.board[(cell) // 4][(cell) % 4] = player 
        copia.possible_plays.remove(cell)
        heuristica = self.eval(copia, player)
        min_v = self.minimo((cell, heuristica), self.minimax(copia, depth + 1, player, jogada))
      return min_v

    def maximo(self, tuple_v, heuristic):
      if tuple_v[1] < heuristic[1]:
        return heuristic
      else:
        return tuple_v

    def minimo(self, tuple_v, heuristic):
      if tuple_v[1] > heuristic[1]:
        return heuristic
      else:
        return tuple_v

    

if __name__ == "__main__":
    """
    #Instanciamento de variáveis
    """
    inteligenca_bots = "MiniMax"
    jogo = Board()
    n_jogadas = 0
    maquina = Maquina(-1, inteligenca_bots, 5)
    modo = ""

    """
    #Seleção do modo de jogo
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
        jogador = Maquina(1, inteligenca_bots, 5)

    """
    Início do jogo
    """
    while True:
        print()
        jogo.render()
        print()
        #if modo == "MxM":
        #    time.sleep(1)
        jogada = jogador.make_play(jogo)
        if jogo.check_win(jogada):
            print("JOGADOR 1 GANHOU")
            break
        jogo.clean()

        jogo.render()
        print()
        jogada = maquina.make_play(jogo)
        if jogo.check_win(jogada):
            print("JOGADOR 2 GANHOU")
            break
        elif jogo.plays_ocurred == 16:
            print("EMPATE")
            break
        #jogo.clean()
    jogo.render()