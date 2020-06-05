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

WID = 11
HIG = 11
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

PICX = 4
CHZ = 16*PICX

mtmp = makemaze.MazeMaker(WID,HIG)
mtmp.makemz()
for y in range(HIG):
  for x in range(WID):
    masu = mtmp.getMap(x,y)
    mapd[y][x] = masu

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
    self.vx = 0
    self.vy = 0
    self.nx = 0
    self.ny = 0
    self.ox = x
    self.oy = y
    self.c = c
    self.r = r
    self.anif = [0,1,0,2]
    self.acnt = 0
    self.acntspd = 0
    self.dir4 = 0
    self.DIR_L = 0
    self.DIR_R = 1
    self.DIR_U = 2
    self.DIR_D = 3
  def move(self, vx, vy):
    if vx != 0:
      self.dir4 = self.DIR_R if vx > 0 else self.DIR_L
      self.x += vx
      return
    if vy != 0:
      self.dir4 = self.DIR_D if vy > 0 else self.DIR_U
      self.y += vy
      return
  def gomove(self):
    self.x = self.nx
    self.y = self.ny
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

p2 = Monst(1,2)
p2.x = 1
p2.y = 2

useswblitting = False

# bgimg = pygame.image.load("manga.png")

def dist(x,y,x2,y2):
  xx = (x-x2)**2
  yy = (y-y2)**2
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
        if dist(tchx, tchy, xx, yy) > 39:
          ox = p.x
          oy = p.y
          od4 = p.dir4
          dx = 1
          dy = 1
          vx = 0
          vy = 0
          if abs(tchx - xx) > abs(tchy - yy):
            vx = 1 if tchx > xx else -1
            p.dir4 = p.DIR_R if vx > 0 else p.DIR_L
          else: # if moving_for_y
            vy = 1 if tchy > yy else -1
            p.dir4 = p.DIR_D if vy > 0 else p.DIR_U
          for i in range(2):
            dx = p.x
            dy = p.y
            dx += vx
            dy += vy
            if dx < 0:
              dx = 0
            if dx >= WID - 1:
              dx = WID - 1
            if dy < 0:
              dy = 0
            if dy >= HIG - 1:
              dy = HIG - 1
            if mapd[dy][dx] == 0:
              ox = p.x
              oy = p.y
              p.x = dx
              p.y = dy
              p2.x = ox
              p2.y = oy
              p2.dir4 = p.dir4
              continue
            else:
              break
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
    SCREEN_blit(osurf[pk + 20 * p2.dir4 + 20*4], (p2.x*CHZ, p2.y*CHZ))
    
    pygame_display_update()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
