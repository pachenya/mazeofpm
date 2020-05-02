import random
'''
This file is made by Becky42.
Let me know if you want to use this code.
Twitter -> @alicebecky10
'''

class CPos:
 def __init__(self, x = 0, y = 0, n = 0):
   self.x = x
   self.y = y
   self.n = n
   self.k = True

class MazeMaker:
  def __init__(self, w = 21, h = 21):
    self.w = w
    self.h = h
    self.WID = w
    self.HIG = h
    self.WT_W = 1
    self.WT_N = 0
    self.WT_B = 2
    self.mapdr = [[self.WT_W for i in range(self.WID)] for j in range(self.HIG)]
    self.p = CPos(1,1)
    self.sutakku = []

  def horu(self, p,attr=0):
    self.mapdr
    x = self.p.x
    y = self.p.y
    w = self.WID
    h = self.HIG
    if x >= 0 and x <= w -1 and y >= 0 and y <= h:
      if self.mapdr[y][x] == self.WT_W:
        return False
      self.mapdr[y][x] = self.WT_N
      return True

  def makemz_aux(self, s):
    self.mapdr[s.y][s.x] = self.WT_N
    xxx = [-1,0, 0,1]
    yyy = [ 0,1,-1,0]
    trnd = [0,1,2,3]
    for i in range(4):
      rni = random.randint(0,3)
      trnd[rni], trnd[i] = trnd[i], trnd[rni]
  
    for i in trnd:
      xx = s.x + xxx[i]
      yy = s.y+ yyy[i]
      xx2 = s.x + xxx[i]*2
      yy2 = s.y + yyy[i]*2
      if xx2 < 0 or xx2 >= self.WID or yy2 < 0 or yy2 >=self.HIG:
        continue
      if self.mapdr[yy2][xx2] == self.WT_N:
        continue
      self.mapdr[yy][xx] = self.WT_N
      self.mapdr[yy2][xx2] = self.WT_N
      self.mapdr[yy][xx] = self.WT_N
      return CPos(xx2,yy2)
    return None
    
  def makemz(self):
    self.sutakku.append(CPos(1, 1, self.WT_N))
    done = False
    while not done:
      for s in self.sutakku:
        rval = self.makemz_aux(s)
        if rval == None:
          s.k = False
        else:
          self.sutakku.append(rval)
      self.sutakku = [suta for suta in self.sutakku if suta.k == True]
      if len(self.sutakku) == 0:
        done = True
        
  def getMap(self, x, y):
    if y < 0 or x < 0 or y > self.h - 1 or x > self.w - 1:
      return self.WT_W
    return self.mapdr[y][x]
  def draw_cons(self):
    for y in range(self.HIG):
      for x in range(self.WID):
        if self.mapdr[y][x] == self.WT_N:
          print('.',end='')
        elif self.mapdr[y][x] == self.WT_W:
          print('#',end='')
        elif self.mapdr[y][x] == self.WT_B:
          print('*',end='')
      print('')

'''
# test
def makemazetesttest():
  m = MazeMaker()
  m.makemz()
  m.draw_cons()

makemazetesttest()
'''
