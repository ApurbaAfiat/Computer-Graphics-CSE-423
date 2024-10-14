from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

window_width = 500
window_height = 500

r_shooter=10 #shooter radius
c_shooter=[window_width/2,20] #shooter center
pause = False
game_over = False
score = 0
bubble=[]
fire=[]
misfire=[]
fire_speed=5
bubble_speed=0.5

def draw_point(x, y):
  glPointSize(2)
  glBegin(GL_POINTS)
  glVertex2f(x, y)
  glEnd()

def draw_circle(r,c):
   d=1-r
   x=0
   y=r
   circle_point(x,y,c)
   while x<y:
       if d<0:
           d+=2*x+3
           x+=1
       else:
           d+=2*x-2*y+5
           x+=1
           y-=1
       circle_point(x, y, c)

def circle_point(x,y,c):
   c_x,c_y=c
   draw_point(c_x+x, c_y+y)
   draw_point(c_x+y, c_y+x)
   draw_point(c_x+y, c_y-x)
   draw_point(c_x+x, c_y-y)
   draw_point(c_x-x, c_y-y)
   draw_point(c_x-y,c_y-x)
   draw_point(c_x-y, c_y+x)
   draw_point(c_x-x, c_y+y)

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

def draw_shooter(r,c):
   glColor3f(1, 0.75, 0)
   draw_circle(r,c)

def generate_fire():
   global fire,r_shooter,c_shooter
   r=r_shooter/2 #fire has half the radius of shooter
   c=[c_shooter[0],c_shooter[1]+30] #initial center of fire
   fire.append([r, c]) #handle multiple fires

def draw_fire():
   global fire
   glColor3f(1, 0.75, 0)
   for r,c in fire: #fires are drawn from the stored radius and center
       draw_circle(r,c)

def generate_bubble(r,c):
   bubble.append([r, c])

for i in range(5): #there can has to be exactly 5 bubbles
   r = random.uniform(0.75 * r_shooter, 2 * r_shooter) #radius of bubbles are close to radius of shooter
   c = [random.uniform(r,window_width-r), window_height+i*40] #x coordinate is within the window
   #y coordinate is divided into 5 segments with difference of the maximum diameter
   generate_bubble(r,c) #handle multiple bubbles

def draw_bubble():
   global bubble
   glColor3f(1, 0.75, 0)
   for r, c in bubble: #bubbles are drawn from the stored radius and center
       draw_circle(r, c)

def keyboardListener(key, x, y):
  global c_shooter
  if not game_over:
      if not pause:
          if key == b'a':
              c_shooter[0] -= 15 #shooter moves left with 'a'
              if c_shooter[0] < 20:
                  c_shooter[0] = 20 #shooter cannot move left beyond the window
          elif key == b'd':
              c_shooter[0] += 15 #shooter moves right with 'd'
              if c_shooter[0] + r_shooter > window_width - 10:
                  c_shooter[0] = (window_width - 10) - r_shooter #shooter cannot move right beyond the window

          elif key == b' ':
              if not pause:
               generate_fire() #fires with spacebar
  glutPostRedisplay()

def mouseListener(button, state, x, y):
  global pause, score, game_over, fire_speed, bubble_speed, r_shooter, c_shooter, bubble, fire, misfire
  if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
      y = window_height - y
      n = 30
      if window_height - n - 10 <= y <= window_height - n + 10: #handles restart button
          if n <= x <= 2 * n:
              r_shooter = 10
              c_shooter = [window_width / 2, 20]
              pause = False
              game_over = False
              score = 0
              bubble = []
              fire = []
              misfire = []
              fire_speed = 5
              bubble_speed = 0.5
              for i in range(5):
                  r = random.uniform(0.75 * r_shooter, 2 * r_shooter)
                  c = [random.uniform(r, window_width - r), window_height+i*40]
                  generate_bubble(r, c)
              print('Starting Over')

          elif window_width / 2 - 15 <= x <= window_width / 2 + 15: #handles pause button
              if not pause:
                  pause = True
              else:
                  pause = False

          elif (window_width - 2 * n <= x <= window_width - n): #handles cross button
              print(f'Goodbye! Final Score: {score}')
              glutLeaveMainLoop()

def animate(x):
  global score, pause, game_over, fire, fire_speed, r_shooter, c_shooter, fire_speed, bubble_speed, bubble
  if not pause and not game_over:
      for r,c in bubble:
          c[1] -= bubble_speed #bubbles move downward

          bubble_x = c[0] #center x coordinate of bubble
          shooter_x=c_shooter[0] #center x coordinate of shooter
          bubble_y=c[1]-r #downward y coordinate of bubble
          shooter_y=c_shooter[1]+r_shooter #upward y coordinate of shooter

          if bubble_x-r<=shooter_x<=bubble_x+r and bubble_y<=shooter_y:
          #if bubble touches shooter then game over
              game_over=True
              print(f'Game Over! Final Score: {score}')

          if not (bubble_x-r<=shooter_x<=bubble_x+r) and bubble_y<=0:
          #if 3 bubbles are removed then game over
              bubble.remove([r,c])
              if len(bubble)==2:
                  game_over=True
                  print(f'Game Over! Final Score: {score}')

      for r, c in fire:
          c[1] += fire_speed #fire moves upwards
          if c[1]>=window_height: #if fire goes beyond the screen it is removed and stored in misfire
              misfire.append([r,c])
              fire.remove([r,c])
              if len(misfire)==3: #if 3 misfires then game over
                  game_over=True
                  print(f'Game Over! Final Score: {score}')

      remove=[]
      for i in range(len(fire)):
          for j in range(len(bubble)):
              r,c=fire[i]
              r2,c2=bubble[j]
              if c2[0]-r2<=c[0]<=c2[0]+r2 and c[1]>=c2[1]-r2:
              #if fire touches bubble then those fire and bubble are stored
                  remove.append([i,j])

      for i,j in remove:
          bubble.pop(j) #touching bubble removed
          fire.pop(i) #touching fire removed
          score+=1
          print(f'Score: {score}')
          r = random.uniform(0.75 * r_shooter, 3 * r_shooter)
          c = [random.uniform(r,window_width-r), random.uniform(window_height, window_height+200)]
          generate_bubble(r,c) #new bubble generated if one is already hit by fire

  elif game_over==True: #bubbles and fires are removed when game is over
      bubble=[]
      fire=[]

def display():
  glClear(GL_COLOR_BUFFER_BIT)
  draw_arrow()
  draw_pause()
  draw_cross()
  draw_shooter(r_shooter,c_shooter)
  draw_fire()
  draw_bubble()
  animate(0)
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
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()