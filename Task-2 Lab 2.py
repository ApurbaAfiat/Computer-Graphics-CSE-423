from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width = 500
window_height = 500
points = []
blink=False
freeze=False
speed=0.01
def generate_point(x, y):
   color = (random.random(), random.random(), random.random())
   direction=(random.choice([-1, 1]),random.choice([-1, 1]))
   points.append({'position':(x,y), 'color':color, 'direction':direction, 'background':(0,0,0)})

def mouseListener(button, state, x, y):
   global blink
   if button == GLUT_RIGHT_BUTTON:
       if state == GLUT_DOWN:
           x = x - (window_width / 2)
           y = (window_height / 2) - y
           generate_point(x, y)

   if button == GLUT_LEFT_BUTTON:
       if (state == GLUT_DOWN):
           if blink==False:
               blink = True
               print('Blinking')
           else:
               blink = False
               print('Not Blinking')
   glutPostRedisplay()

def draw_points():
   glPointSize(4)
   glBegin(GL_POINTS)
   for i in points:
       color=i['color']
       glColor3f(*color)
       position=i['position']
       glVertex2f(*position)
   glEnd()

def animate_points():
   global blink,freeze,speed
   glutPostRedisplay()
   if not freeze:
       for i in points:
           x,y=i['position']
           dx,dy=i['direction']
           if x>180 or x<0:
               dx=-dx
           x += dx * speed
           if y>180 or y<0:
               dy=-dy
           y += dy * speed
           i['position']=(x,y)
           i['direction']=(dx,dy)
           if blink==True:
               i['color'],i['background']=i['background'],i['color']

def specialKeyListener(key, x, y):
   global speed
   if key==GLUT_KEY_UP:
       speed *= 2
       print("Speed Increased")
   if key== GLUT_KEY_DOWN:
       speed /= 2
       print("Speed Decreased")
   glutPostRedisplay()

def keyboardListener(key, x, y):
   global freeze
   if key==b' ':
       if freeze==False:
           freeze=True
       else:
           freeze=False

def display():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glClearColor(0, 0, 0, 0);  # background color is black
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
   glMatrixMode(GL_MODELVIEW)

   glColor3f(1,1,1)
   glBegin(GL_LINES)
   glVertex2d(180, 0)
   glVertex2d(180, 180)
   glVertex2d(180, 180)
   glVertex2d(0, 180)
   glVertex2d(0, 0)
   glVertex2d(0, 180)
   glVertex2d(0, 0)
   glVertex2d(180,0)
   glEnd()
   draw_points()
   glutSwapBuffers()


def init():
   glClearColor(0, 0, 0, 0)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(window_width, window_width)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()
glutDisplayFunc(display)
glutIdleFunc(animate_points)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()

