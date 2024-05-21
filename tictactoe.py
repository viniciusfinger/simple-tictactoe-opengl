import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

GAME_SIZE = 600
GRID_SIZE = 3
SQUARE_SIZE = GAME_SIZE // GRID_SIZE
DRAW = 0

# Player 1 = X, player 2 = O
board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
current_player = 1
game_over = False
player1_score = 0
player2_score = 0
draws = 0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, GAME_SIZE, 0, GAME_SIZE)

def draw_grid():
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)

    for i in range(1, GRID_SIZE):
        glBegin(GL_LINES)
        glVertex2f(i * SQUARE_SIZE, 0)
        glVertex2f(i * SQUARE_SIZE, GAME_SIZE)
        glEnd()
        
        glBegin(GL_LINES)
        glVertex2f(0, i * SQUARE_SIZE)
        glVertex2f(GAME_SIZE, i * SQUARE_SIZE)
        glEnd()

def draw_x(x, y):
    padding = 20
    glColor3f(1.0, 0.0, 0.0) # red
    glLineWidth(5)
    
    glBegin(GL_LINES)
    glVertex2f(x * SQUARE_SIZE + padding, y * SQUARE_SIZE + padding)
    glVertex2f((x + 1) * SQUARE_SIZE - padding, (y + 1) * SQUARE_SIZE - padding)
    glEnd()
    
    glBegin(GL_LINES)
    glVertex2f((x + 1) * SQUARE_SIZE - padding, y * SQUARE_SIZE + padding)
    glVertex2f(x * SQUARE_SIZE + padding, (y + 1) * SQUARE_SIZE - padding)
    glEnd()

def draw_o(x, y):
    padding = 20
    radius = (SQUARE_SIZE - 2 * padding) // 2
    center_x = x * SQUARE_SIZE + SQUARE_SIZE // 2
    center_y = y * SQUARE_SIZE + SQUARE_SIZE // 2
    
    glColor3f(0.0, 0.0, 1.0) # blue
    glLineWidth(5)
    
    glBegin(GL_LINE_LOOP)

    for i in range(360):
        angle = np.deg2rad(i)
        glVertex2f(center_x + np.cos(angle) * radius, center_y + np.sin(angle) * radius)
    glEnd()

def draw_board():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y, x] == 1:
                draw_x(x, y)
            elif board[y, x] == 2:
                draw_o(x, y)

def draw_score():
    glColor3f(1.0, 1.0, 1.0) # white
    glRasterPos2f(10, GAME_SIZE - 20)
    score_text = f"Jogador 1 (X): {player1_score}   Jogador 2 (O): {player2_score}   Empates: {draws}   Aperte R para reiniciar"
    for ch in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def check_winner():
    global game_over, player1_score, player2_score, draws
    
    for i in range(GRID_SIZE):
        if np.all(board[i, :] == current_player) or np.all(board[:, i] == current_player):
            game_over = True
            return current_player

    if np.all(np.diag(board) == current_player) or np.all(np.diag(np.fliplr(board)) == current_player):
        game_over = True
        return current_player

    if np.all(board != 0):
        game_over = True
        return DRAW

    return None

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()
    draw_board()
    draw_score()
    glutSwapBuffers()

def switch_player():
    global current_player
    current_player = 3 - current_player

def mouse_click(button, state, x, y):
    global current_player, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        grid_x = x // SQUARE_SIZE
        grid_y = (GAME_SIZE - y) // SQUARE_SIZE
        
        if board[grid_y, grid_x] == 0:
            board[grid_y, grid_x] = current_player
            winner = check_winner()
            if winner is not None:
                if winner == 0:
                    global draws
                    draws += 1
                    print("Empate!")
                else:
                    if winner == 1:
                        global player1_score
                        player1_score += 1
                    else:
                        global player2_score
                        player2_score += 1
                    print(f"Jogador {winner} ganhou!")
            switch_player()
        glutPostRedisplay()

def restart_game():
    global board, current_player, game_over
    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    current_player = 1
    game_over = False
    glutPostRedisplay()

def key_is_r(key):
    return key == b'r'

def keyboard(key, x, y):
    if key_is_r(key):
        restart_game()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(GAME_SIZE, GAME_SIZE)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Jogo da Velha Raiz em OpenGL")
    
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()