import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window
window_height = 600
window_width = 600

# Cross button
cross_size = 20.0
cross_x = window_width - cross_size - 15.0
cross_y = 0

# Restart
restart_x = 15.0
restart_y = 1.0
restart_size = 20.0
reset = False

score = 0
game_over = False
initial_time = time.time()
current_level = 1
max_pigeons = 10 
level_requirements = {
    1: {'pigeon_count': 10, 'time_limit': 30},
    2: {'pigeon_count': 15, 'time_limit': 40},
    3: {'pigeon_count': 20, 'time_limit': 50} , 
}

# Pigeon
num = max_pigeons
size = 15
speed = 0.5
pigeons = []

# Gun
gun_x = 250
gun_y = 50
gun_width = 50
gun_height = 100
gun_speed = 10

# Bullet
bullet_width = 2
bullet_height = 10
bullet_speed = 5
bullets = []

class Pigeon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)
        self.color = (1.0, 1.0, 1.0) 

    def draw(self):
        glColor3f(*self.color)
        draw_line(self.x, self.y, self.x + size, self.y)
        draw_line(self.x + size, self.y, self.x + size, self.y + size)
        draw_line(self.x + size, self.y + size, self.x, self.y + size)
        draw_line(self.x, self.y + size, self.x, self.y)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if (self.x <= 0) or (self.x >= window_width - size):
            self.speed_x = -self.speed_x
        if (self.y <= window_height // 2) or (self.y >= window_height - size):
            self.speed_y = -self.speed_y

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)
        draw_line(self.x, self.y, self.x, self.y + bullet_height)

    def move(self):
        self.y += bullet_speed

def draw_bullets():
    for bullet in bullets:
        bullet.draw()
        bullet.move()

def shoot_bullet():
    global gun_x, gun_y
    bullet = Bullet(gun_x + gun_width // 2, gun_y + gun_height)
    bullets.append(bullet)

def quit_game():
    global game_over
    game_over = True

def restart_game():
    global score, initial_time, pigeons, bullets, game_over, pause, current_level
    score = 0
    initial_time = time.time()
    pigeons = []
    bullets = []
    game_over = False
    pause = False
    current_level = 1
    initialize_pigeons()

def collision_detection():
    global bullets, pigeons, score, current_level
    for bullet in bullets:
        for pigeon in pigeons:
            if (
                bullet.x >= pigeon.x
                and bullet.x <= pigeon.x + size
                and bullet.y >= pigeon.y
                and bullet.y <= pigeon.y + size
            ):
                bullets.remove(bullet)
                pigeons.remove(pigeon)
                score += 1
                if score >= level_requirements[current_level]['pigeon_count']:
                    level_up()
                return

current_level = 1
level_up_conditions = [(10, 20), (15, 25), (20, 15)]  #pigeon, time

def level_up():
    global current_level, pigeons, initial_time, score

   #level_up er jonno condition
    pigeons_to_shoot, time_limit = level_requirements[current_level]['pigeon_count'], level_requirements[current_level]['time_limit']
    if score >= pigeons_to_shoot and int(time.time() - initial_time) <= time_limit:
        current_level += 1
        initial_time = time.time() 
        score=0
        initialize_pigeons()

def draw_line(x1, y1, x2, y2):
    glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    step_x = 1 if x1 < x2 else -1
    step_y = 1 if y1 < y2 else -1
    x, y = x1, y1
    count = 0
    if dx > dy:
        p = 2 * dy - dx
        while dx > count:
            glVertex2f(x, y)
            x += step_x
            if p >= 0:
                y += step_y
                p -= 2 * dx
            p += 2 * dy
            count += 1
    else:
        p = 2 * dx - dy
        while dy > count:
            glVertex2f(x, y)
            y += step_y
            if p >= 0:
                x += step_x
                p -= 2 * dy
            p += 2 * dx
            count += 1
    glEnd()

def draw_pigeons():
    for pigeon in pigeons:
        pigeon.draw()
        pigeon.move()

def draw_restart():
    global restart_x, restart_y, restart_size
    glColor3f(1, 0, 0)
    draw_line(int(restart_x), int(restart_y + restart_size / 2), int(restart_x + restart_size),
              int(restart_y + restart_size / 2))
    draw_line(int(restart_x), int(restart_y + restart_size / 2), int(restart_x + restart_size / 2),
              int(restart_y + restart_size))
    draw_line(int(restart_x), int(restart_y + restart_size / 2), int(restart_x + restart_size / 2),
              int(restart_y))

def draw_cross():
    global cross_x, cross_y, cross_size
    glColor3f(1.0, 0.0, 0.0)
    draw_line(cross_x, cross_y, cross_x + cross_size, cross_y + cross_size)
    draw_line(cross_x, cross_y + cross_size, cross_x + cross_size, cross_y)
    glColor3f(1.0, 1.0, 1.0)

def draw_gun():
    draw_line(gun_x, gun_y, gun_x + gun_width, gun_y)
    draw_line(gun_x + gun_width, gun_y, gun_x + gun_width, gun_y + gun_height)
    draw_line(gun_x + gun_width, gun_y + gun_height, gun_x, gun_y + gun_height)
    draw_line(gun_x, gun_y + gun_height, gun_x, gun_y)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ctypes.c_int(ord(char)))

def draw_timer_score():
    global initial_time, score, current_level
    elapsed_time = int(time.time() - initial_time)
    glColor3f(1.0, 1.0, 1.0) 
    draw_text(window_width - 100, window_height - 20, f"Time: {elapsed_time}s")
    draw_text(10, window_height - 20, f"Score: {score}")
    draw_text(10, window_height - 40, f"Level: {current_level}") 


def display():
    global game_over
    glClear(GL_COLOR_BUFFER_BIT)
    draw_pigeons()
    draw_gun()
    draw_bullets()
    draw_timer_score()
    draw_restart()
    draw_cross()
    glFlush()
    glutSwapBuffers()
    collision_detection()

    elapsed_time = int(time.time() - initial_time)
    time_limit = level_requirements[current_level]['time_limit']
    pigeons_to_shoot = level_requirements[current_level]['pigeon_count']
    
    if elapsed_time >= time_limit and score < pigeons_to_shoot:
        game_over = True
        print("LOST THE GAME HAHA")
    if not game_over:
        glutPostRedisplay()


def initialize_pigeons():
    global num, pigeons
    pigeons = []
    if current_level==1:
        j=10
    elif current_level==2:
        j=15
    elif current_level==3:
        j=20
    for i in range(j):
        x = random.randint(0, window_width - size)
        y = random.randint(window_height // 2, window_height - size)
        new_pigeon = Pigeon(x, y)
        pigeons.append(new_pigeon)

def keyboard_pressed(key, x, y):
    global pause, game_over, reset
    if key == b' ':
        shoot_bullet()
    elif key == b'q' or key == b'Q':
        quit_game()
        print("Quit")
        glutPostRedisplay()

def special_key_pressed(key, x, y):
    global gun_x, window_width, gun_width, gun_speed
    if key == GLUT_KEY_LEFT:
        gun_x = max(0, gun_x - gun_speed)
    elif key == GLUT_KEY_RIGHT:
        gun_x = min(window_width - gun_width, gun_x + gun_speed)

    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global pause, game_over, reset

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            restart_game()
            print("Restarting the game")

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Pigeon")
gluOrtho2D(0, window_width, 0, window_height)
glutDisplayFunc(display)
glutSpecialFunc(special_key_pressed)
glutKeyboardFunc(keyboard_pressed)
glutMouseFunc(mouse_click)
glClearColor(0, 0, 0, 0)
initialize_pigeons()
glutMainLoop()
