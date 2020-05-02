import pygame_sdl2
pygame_sdl2.import_as_pygame()

from plyer import orientation
orientation.set_portrait()

import makemaze

def SCREEN_blit(src, dest):
  global RENDERER, spritecache
  Sprite(RENDERER.load_texture(src)).render(dest)

def pygame_display_update():
  RENDERER.render_present()
  RENDERER.clear((1, 1, 1))

import random
import sys
import math

import pygame
from pygame.locals import *
from pygame.render import *

WID = 17
HIG = 17
mapd = [[0 for i in range(WID)] for j in range(HIG)]

class CPosi:
  def __init__(self, x, y, idx):
    self.x = x
    self.y = y
    self.idx = idx
  def draw():
    return
    
IMGS = []
FPS = 30
SW = 240*2
SH = 320*2

CHZ = 16*3

mtmp = makemaze.MazeMaker(WID,HIG)
mtmp.makemz()
for y in range(HIG):
  for x in range(WID):
    masu = mtmp.getMap(x,y)
    mapd[y][x] = masu

DIR_L = 0
DIR_R = 1
DIR_U = 2
DIR_D = 3

class Monst:
  def __init__(self, k = 1, n =1, hp = 10, mp = 10, x = 4, y = -2, c = 1, r = 0):
    self.k = k
    self.n = n
    self.hp = hp
    self.mp = mp
    self.mhp = hp
    self.mmp = mp
    self.x = x
    self.y = y
    self.ox = x
    self.oy = y
    self.c = c
    self.r = r
    self.anif = [0,1,0,2]
    self.acnt = 0
    self.acntspd = 0
    self.dir4 = 0
  def getpos(self):
    return (self.x,self.y)

class Piicts:
  def __init__(self, id):
    self.id = id
  def draw(posx, posy):
    return

p = Monst(1,1)
p.x = 1
p.y = 1
useswblitting = False

# bgimg = pygame.image.load("manga.png")

def dist(x,y,x2,y2):
  xx = x**2
  yy = y**2
  return math.sqrt(xx+yy)

def main():
  global SCREEN, FPSCLOCK, RENDERER
  global p
  pygame.init()
  FPSCLOCK = pygame.time.Clock()
  SCREEN = pygame.display.set_mode((SW,SH))
  RENDERER = Renderer(None)
  pygame.display.set_caption('PMPM')
  ball = pygame.image.load("pacmano.png")
  ballrect = ball.get_rect()
  NUM = 12*20
  # source bmp rects in int.
  srct = []
  osurf = []
  for i in range(NUM):
    srct.append(pygame.Rect((i % 20) * 16, (i // 20) * 16, 16, 16))
  for i in range(NUM):
    stmp = pygame.Surface((16, 16))
    stmp.convert(stmp)
    stmp.blit(ball, pygame.Rect(0,0,16,16), srct[i])

    stmp = pygame.transform.scale(stmp, (CHZ, CHZ))
    stmp.set_colorkey((71,108, 108))
    osurf.append(stmp)
  touched = False
  tchx = 0
  tchy = 0

  if useswblitting:
    global SCREEN_blit, pygame_display_update
    SCREEN_blit = SCREEN.blit
    pygame_display_update = pygame.display.update

  while True:
    for ev in pygame.event.get():
      if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
      if ev.type == MOUSEBUTTONDOWN and touched == False:
        tchx = ev.pos[0]
        tchy = ev.pos[1]
        touched = True
      elif ev.type == pygame.MOUSEBUTTONUP:
        xx = ev.pos[0]
        yy = ev.pos[1]
        p.ox = p.x
        p.oy = p.y
        ox = p.x
        oy = p.y
        if dist(tchx, tchy, xx, yy) > 40:
          if abs(tchx - xx) > abs(tchy - yy):
            if tchx < xx:
              p.x += 1
              p.dir4 = DIR_R
            elif tchx > xx:
              p.x -= 1
              p.dir4 = DIR_L
          else:
            if tchy < yy:
              p.y += 1
              p.dir4 = DIR_D
            elif tchy > yy:
              p.y -= 1
              p.dir4 = DIR_U
          
          if mapd[p.y][p.x] != 0 or p.y < 0 or p.x < 0 or \
          p.y >= HIG-1 or p.x >= HIG-1:
            p.x = ox
            p.y = oy
          
        touched = False
    for y in range(HIG):
      for x in range(WID):
        xx = x * CHZ
        yy = y * CHZ
        if mapd[y][x] == 0:
          SCREEN_blit(osurf[167],(xx,yy))
        elif mapd[y][x] == 1:
          SCREEN_blit(osurf[164],(xx,yy))
        elif mapd[y][x] == 2:
          SCREEN_blit(osurf[167],(xx,yy))
          SCREEN_blit(osurf[208],(xx,yy))
    # do player
    pkoma = (0,1,0,2)
    pkomacnt = 4
    pkomawait = 6
    p.acnt += 1
    if p.acnt >= pkomawait * pkomacnt:
      p.acnt = 0
    pk = pkoma[p.acnt // pkomawait] 
    SCREEN_blit(osurf[pk + 20 * p.dir4], (p.x*CHZ, p.y*CHZ))
    
    pygame_display_update()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
