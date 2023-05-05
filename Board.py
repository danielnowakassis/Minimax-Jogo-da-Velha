import numpy as np
import platform
from os import system

class Board:
    def __init__(self):
        self.board = np.zeros(shape = (4,4))
    
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
        if (jogada-1) // 4 in [0,3] and (jogada-1) % 4 in [0,3]: #verifica diagonal para os cantos
            possible = 0
            if (jogada - 1) % 5 == 0:
                for i in range(4):
                    possible += self.board[i][i]       
            else:
                for i in range(4):
                    possible += self.board[i][3 - i]       
            return abs(possible) == 4
        #verfica horizontal
        possible = 0
        for i in range(4):
            possible += self.board[(a-1) // 4][i]  
        if abs(possible) == 4:
            return True
        #verfica vertical
        possible = 0
        for i in range(4):
            possible += self.board[i][(a-1) % 4]
        return abs(possible) == 4   

jogo = Board()

while True:
    print()
    jogo.render()
    a = int(input("Jogada (numpad) : 1...16 "))
    jogo.board[(a-1) // 4][(a-1) % 4] = -1
    if jogo.check_win(a):
        break
    jogo.clean()
jogo.render()