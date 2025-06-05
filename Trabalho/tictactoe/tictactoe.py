"""
Jogador de Tic Tac Toe (Jogo da Velha)

Este trabalho implementa uma IA para o jogo da velha(Tic Tac Toe) utilizando o algoritmo MINIMAX.
A IA consegue determinar qual é o movimento ideial para qualquer um dos players(X ou O) para qualquer configuração válida do tabuleiro.
"""

import math
import copy

# Define constantes para os jogadores e células vazias
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Retorna o estado inicial do tabuleiro.
    O estado inicial é uma grade 3x3 com todas as células vazias (EMPTY).
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Retorna o jogador que tem a próxima vez de jogar no tabuleiro.
    O jogador 'X' sempre começa. O próximo jogador é determinado contando o número
    de 'X's e 'O's no tabuleiro. Se houver mais 'X's do que 'O's, é a vez de 'O'.
    Caso contrário, é a vez de 'X'.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Retorna um conjunto de todas as ações possíveis (i, j) disponíveis no tabuleiro.
    Uma ação é uma tupla (linha, coluna) que representa uma célula vazia onde um
    jogador pode fazer uma jogada.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Retorna o tabuleiro resultante de fazer a jogada (i, j) no tabuleiro.
    
    Args:
        board (list of lists): O estado atual do tabuleiro do Jogo da Velha.
        action (tuple): Uma tupla (i, j) representando a linha e a coluna
                        onde o jogador atual deseja fazer uma jogada.
    
    Returns:
        list of lists: Um novo estado do tabuleiro após aplicar a ação.
        
    Raises:
        Exception: Se a ação for inválida (fora dos limites ou célula não vazia).
    """
    # Extrai a linha e coluna da ação
    i, j = action

    # Verifica se a ação é válida
    if i < 0 or i >= 3 or j < 0 or j >= 3 or board[i][j] is not EMPTY:
        raise Exception("Invalid action")

    # Cria uma cópia profunda do tabuleiro para não modificar o original
    new_board = copy.deepcopy(board)
    
    # Aplica a jogada na cópia do tabuleiro
    new_board[i][j] = player(board)
    
    return new_board


def winner(board):
    """
    Retorna o vencedor do jogo, se houver um.
    Verifica se há um vencedor nas linhas, colunas e em ambas as diagonais.
    Retorna 'X' se 'X' vencer, 'O' se 'O' vencer, e None caso contrário.
    """
    # Checa linhas horizontais
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]

    # Checa colunas verticais
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

    # Checa diagonal principal (canto superior esquerdo ao inferior direito)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]

    # Checa diagonal secundária (canto superior direito ao inferior esquerdo)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # Se não houver vencedor
    return None


def terminal(board):
    """
    Retorna True se o jogo terminou, False caso contrário.
    O jogo termina se houver um vencedor ou se não houver mais
    ações possíveis (ou seja, o tabuleiro está cheio, resultando em um empate).
    """
    if winner(board) is not None or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Retorna 1 se 'X' venceu o jogo, -1 se 'O' venceu, 0 caso contrário.
    Esta função é usada para atribuir uma pontuação aos estados terminais no
    algoritmo minimax.
    """
    # Obtém o vencedor do jogo
    win = winner(board)

    # Atribui a utilidade com base no vencedor
    if win == X:
        return 1
    elif win == O: 
        return -1
    else:
        return 0

# Funções auxiliares para o algoritmo Minimax
def max_value(board):
    """
    Função auxiliar para o minimax. Calcula a utilidade máxima que o
    jogador maximizador ('X') pode alcançar a partir do estado atual do tabuleiro.
    
    Args:
        board (list of lists): O estado atual do tabuleiro do Jogo da Velha.
        
    Returns:
        int: A pontuação de utilidade máxima alcançável.
    """
    if terminal(board):
        return utility(board)
    v = -math.inf  # Inicializa com infinito negativo
    for action in actions(board):
        # Chama recursivamente min_value para a jogada do oponente
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    """
    Função auxiliar para o minimax. Calcula a utilidade mínima que o
    jogador minimizador ('O') pode alcançar a partir do estado atual do tabuleiro.
    
    Args:
        board (list of lists): O estado atual do tabuleiro do Jogo da Velha.
        
    Returns:
        int: A pontuação de utilidade mínima alcançável.
    """
    if terminal(board):
        return utility(board)
    v = math.inf  # Inicializa com infinito positivo
    for action in actions(board):
        # Chama recursivamente max_value para a jogada do oponente
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Retorna a ação ideal para o jogador atual no tabuleiro.
    Esta função implementa o algoritmo minimax para determinar a melhor
    jogada possível. Ela avalia todas as jogadas futuras possíveis e escolhe a
    que leva ao melhor resultado para o jogador atual, assumindo
    uma jogada ótima do oponente.
    
    Args:
        board (list of lists): O estado atual do tabuleiro do Jogo da Velha.
        
    Returns:
        tuple: A ação ideal (linha, coluna) para o jogador atual,
               ou None se o jogo já terminou.
    """
    # Se o jogo acabou, não há jogada a ser feita
    if terminal(board):
        return None

    current_player = player(board)

    # Se o jogador atual é 'X' (jogador maximizador)
    if current_player == X:
        best_score = -math.inf
        best_move = None
        for action in actions(board):
            # Calcula o valor da jogada chamando a função do minimizador
            # Isso simula a melhor resposta do oponente
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    # Se o jogador atual é 'O' (jogador minimizador)
    elif current_player == O:
        best_score = math.inf
        best_move = None
        for action in actions(board):
            # Calcula o valor da jogada chamando a função do maximizador
            # Isso simula a melhor resposta do oponente
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action
        return best_move