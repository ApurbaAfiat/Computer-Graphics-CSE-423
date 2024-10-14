
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width = 500
window_height = 500

raindrops = []
x=100
y = 350 #height of the raindrops
dx = 0
speed=0.4
background=[1,1,1]
house=[1,0,0]
rain=[0,0,1]
color=[background, house, rain] #storing the colors of objects

def draw_rain():
   glColor3f(*rain)
   glLineWidth(1.0)
   glBegin(GL_LINES)
   for x, y in raindrops:
       glVertex2f(x - dx, y)
       glVertex2f(x + dx, y - 10) #handling the length of raindrops
   glEnd()

def animate_rain():
   global x,y,speed
   x += 7 #handling the horizontal distance between raindrops
   if x > 400:
       x = 100 #adjustments within the given window
   y = 350
   raindrops.append((x, y)) #storing new raindrops
   for i in range(len(raindrops)):
       x, y = raindrops[i]
       y -= speed #handling the vertical distance between raindrops
       raindrops[i] = (x, y)
   for i in raindrops:
       x,y=i
       if y<100:
           raindrops.remove((x,y)) #removal is important to avoid the vertical joining of all raindrops

def specialKeyListener(key, x, y):
   global speed,dx,color
   light_speed = 0.125
   if key==GLUT_KEY_LEFT:
       dx-=1
       print('Bending Left')
   elif key== GLUT_KEY_RIGHT:
       dx+=1
       print('Bending Right')
   elif key== GLUT_KEY_UP:
       for i in range(3):
           background[i]+=light_speed
           if background[i]>1:
               background[i]=1
       rain[2]+=light_speed
       if rain[2]>1:
           rain[2]=1
       house[0]+=light_speed
       if house[0]>1:
           house[0]=1
       print('Light Increased')
   elif key== GLUT_KEY_DOWN:
       for i in range(3):
           background[i]-=light_speed
           if background[i]<0:
               background[i]=0
           rain[i]-=light_speed
           if rain[i]<0:
               rain[i]=0
           house[i]-=light_speed
           if house[i]<0:
               house[i]=0
       print('Light Decreased')

   glutPostRedisplay()

def keyboardListener(key, x, y):
   global speed
   if key==b'w':
       speed*=1.25
       print('Speed Increased')
   if key==b's':
       speed/=1.25
       print('Speed Decreased')
   glutPostRedisplay()

def draw_points(x, y):
   glPointSize(3)
   glBegin(GL_POINTS)
   glVertex2f(x,y)
   glEnd()

def draw_triangle(x1,x2,y1,y2):
   glBegin(GL_TRIANGLES)

   glVertex2f(x1,y1)
   glVertex2f((x1+x2)/2, y2)
   glVertex2f(x2,y1)

   glEnd()

def draw_rectangle(x1, x2, y1, y2):
   glBegin(GL_LINES)

   glVertex2f(x1, y1)
   glVertex2f(x2, y1)

   glVertex2f(x2, y1)
   glVertex2f(x2, y2)

   glVertex2f(x2, y2)
   glVertex2f(x1, y2)

   glVertex2f(x1, y2)
   glVertex2f(x1, y1)

   glEnd()

def draw_door(x1,x2,y1,y2):
   draw_rectangle(x1, x2, y1, y2)
   m_x=(x1+x2)/2
   m_y=(y1+y2)/2
   draw_points((m_x+x2)/2, m_y)

def draw_window(x1,x2,y1,y2):
   draw_rectangle(x1, x2, y1, y2)
   glBegin(GL_LINES)
   m_x = (x1 + x2) / 2
   m_y = (y1 + y2) / 2
   glVertex2f(x1, m_y)
   glVertex2f(x2, m_y)
   glVertex2f(m_x, y2)
   glVertex2f(m_x, y1)
   glEnd()

def iterate():
   global color
   glViewport(0, 0, 500, 500)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
   glMatrixMode (GL_MODELVIEW)
   glLoadIdentity()
   glClearColor(background[0],background[1],background[2],0)  #background color becomes black

def showScreen():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glLoadIdentity()
   iterate()
   glColor3f(house[0],house[1],house[2]) #color of the house becomes red
   glLineWidth(2)
   draw_triangle(140,360,200,250)
   draw_rectangle(150, 350, 100, 200)
   draw_door(175, 210, 100, 160)
   draw_window(325, 295, 180, 150)
   draw_rain()
   animate_rain()
   glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()
