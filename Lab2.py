from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

window_width = 500
window_height = 500

x_diamond = random.randint(10, window_width - 30)
y_diamond = window_height
speed_diamond = 2
color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))

x_catcher = (window_width - 100) / 2
y_catcher = 10

pause = False
score = 0
game_over = False


def draw_point(x, y):
   glPointSize(2)
   glBegin(GL_POINTS)
   glVertex2f(x, y)
   glEnd()


def draw_line(x1, y1, x2, y2, color):
   glColor3f(*color)
   dx = x2 - x1
   dy = y2 - y1
   if abs(dx) > abs(dy):
       if dx > 0 and dy > 0:
           zone = 0
       elif dx < 0 and dy > 0:
           zone = 3
       elif dx < 0 and dy < 0:
           zone = 4
       else:
           zone = 7
   else:
       if dx > 0 and dy > 0:
           zone = 1
       elif dx < 0 and dy > 0:
           zone = 2
       elif dx < 0 and dy < 0:
           zone = 5
       else:
           zone = 6

   x1, y1 = zone_0(x1, y1, zone)
   x2, y2 = zone_0(x2, y2, zone)

   dx = x2 - x1
   dy = y2 - y1
   d = 2 * dy - dx
   incE = 2 * dy
   incNE = 2 * (dy - dx)
   y = y1

   for x in range(int(x1), int(x2)):
       original_x, original_y = original(x, y, zone)
       draw_point(original_x, original_y)
       if d > 0:
           d += incNE
           y += 1
       else:
           d += incE


def zone_0(x, y, zone):
   if zone == 0:
       return x, y
   elif zone == 1:
       return y, x
   elif zone == 2:
       return y, -x
   elif zone == 3:
       return -x, y
   elif zone == 4:
       return -x, -y
   elif zone == 5:
       return -y, -x
   elif zone == 6:
       return -y, x
   elif zone == 7:
       return x, -y


def original(x, y, zone):
   if zone == 0:
       return x, y
   elif zone == 1:
       return y, x
   elif zone == 2:
       return -y, x
   elif zone == 3:
       return -x, y
   elif zone == 4:
       return -x, -y
   elif zone == 5:
       return -y, -x
   elif zone == 6:
       return y, -x
   elif zone == 7:
       return x, -y

def draw_arrow():
   n = 30
   teal = (0, 0.8, 0.8)
   draw_line(n, window_height - n, 2 * n, window_height - n, teal)
   draw_line(n, window_height - n, 1.5 * n, window_height - n + 10, teal)
   draw_line(n, window_height - n, 1.5 * n, window_height - n - 10, teal)

def draw_pause():
   n = 30
   amber = (1, 0.749, 0)
   if not pause:
       draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 - 5, window_height - n - 10, amber)
       draw_line(window_width / 2 + 5, window_height - n + 10, window_width / 2 + 5, window_height - n - 10, amber)
   else:
       draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 - 5, window_height - n - 10, amber)
       draw_line(window_width / 2 - 5, window_height - n - 10, window_width / 2 + 15, window_height - n, amber)
       draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 + 15, window_height - n, amber)

def draw_cross():
   n = 30
   red = (1, 0, 0)
   draw_line(window_width - n, window_height - n + 10, window_width - 2 * n, window_height - n - 10, red)
   draw_line(window_width - n, window_height - n - 10, window_width - 2 * n, window_height - n + 10, red)

def draw_diamond(x, y):
   global color_diamond
   draw_line(x, y, x + 10, y + 10, color_diamond)
   draw_line(x, y, x + 10, y - 10, color_diamond)
   draw_line(x + 10, y + 10, x + 20, y, color_diamond)
   draw_line(x + 10, y - 10, x + 20, y, color_diamond)


def draw_catcher(x, y):
   global game_over, color_diamond
   if not game_over:
       color = [1, 1, 1]
   else:
       color = [1, 0, 0]
       color_diamond = [0, 0, 0]
   draw_line(x, y + 20, x + 100, y + 20, color)
   draw_line(x + 10, y, x + 90, y, color)
   draw_line(x, y + 20, x + 10, y, color)
   draw_line(x + 90, y, x + 100, y + 20, color)


def specialKeyListener(key, x, y):
   global x_catcher
   if not pause and not game_over:
       if key == GLUT_KEY_LEFT:
           x_catcher -= 15
           if x_catcher < 10:
               x_catcher = 10
       elif key == GLUT_KEY_RIGHT:
           x_catcher += 15
           if x_catcher + 100 > window_width - 10:
               x_catcher = (window_width - 10) - 100


def mouseListener(button, state, x, y): #############################
   global x_diamond, y_diamond, speed_diamond, color_diamond, x_catcher, y_catcher,pause, score, game_over
   if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       y = window_height - y
       n = 30
       if window_height - n - 10 <= y <= window_height - n + 10:
           if n <= x <= 2 * n:
               print('Starting Over')
               x_diamond = random.randint(10, window_width - 30)
               y_diamond = window_height
               speed_diamond = 2
               color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))

               x_catcher = (window_width - 100) / 2
               y_catcher = 10

               pause = False
               score = 0
               game_over = False

           elif window_width / 2 - 15 <= x <= window_width / 2 + 15:
               if not pause:
                   pause = True
               else:
                   pause = False

           elif (window_width - 2 * n <= x <= window_width - n):
               print(f'Goodbye! Score: {score}')
               glutLeaveMainLoop()


def animate(x):
   global x_diamond, y_diamond, speed_diamond, color_diamond, score, pause, game_over
   if not pause and not game_over:
       y_diamond -= speed_diamond
       if x_catcher <= x_diamond <= x_catcher + 100 and y_catcher <= y_diamond <= y_catcher + 20:
           score += 1
           print(f'Score: {score}')
           x_diamond = random.randint(10, window_width - 30)
           y_diamond = window_height
           speed_diamond += 0.5
           color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))

       if y_diamond < 0:
           game_over = True
           print(f'Game Over! Score: {score}')

   glutTimerFunc(10, animate, 0)


def display():
   glClear(GL_COLOR_BUFFER_BIT)
   draw_arrow()
   draw_pause()
   draw_cross()
   draw_diamond(x_diamond, y_diamond)
   draw_catcher(x_catcher, y_catcher)
   glutSwapBuffers()


glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glOrtho(0, window_width, 0, window_height, -1, 1)
glClearColor(0, 0, 0, 0)
glutDisplayFunc(display)
glutIdleFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutTimerFunc(10, animate, 0)
glutMainLoop()
