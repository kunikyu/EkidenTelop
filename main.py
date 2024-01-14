import time as t
import PySimpleGUI as sg
# import json
import pygame
from pygame.locals import *
import sys
# import tkinter as tk
pygame.font.init()

class 時間():
  def __init__(self) :
    self.time_start = t.time()
    self.skip_time = 0
    self.elapsed_time = 0
    self.running = False
  def reset(self):
    self.time_start = t.time()
    self.skip_time = 0
    self.elapsed_time = 0
  def stopstart(self):
    self.running = not self.running
  def disp(self, screen):
    if self.running:
      self.elapsed_time = int(t.time() - self.time_start - self.skip_time)
    else:
      self.skip_time = int(t.time() - self.time_start - self.elapsed_time)
    self.elapsed_hour = self.elapsed_time // 3600
    self.elapsed_minute = (self.elapsed_time % 3600) // 60
    self.elapsed_second = (self.elapsed_time % 3600 % 60)
    font = pygame.font.SysFont("hg正楷書体pro", 50)
    self.time = str(self.elapsed_hour).zfill(2) + ":" + str(self.elapsed_minute).zfill(2) + ":" + str(self.elapsed_second).zfill(2)
    text = font.render(self.time, True, (0, 0, 0))
    screen.blit(text, (1050, 0))

class 順位():
  def __init__(self) -> None:
    self.img = pygame.image.load("img/rank.png")
    self.font1 = pygame.font.SysFont("yugothicuisemibold", 30)
    self.font2 = pygame.font.SysFont("ebrima", 30)
    self.time = 200
    self.len = 1
    self.page = 1
    self.pagemax = 1
    self.now = 0
    self.height = 24
  def disp(self, datalist:dict, screen, now):
    if (len(datalist) - 1) % self.height != 0:
      self.pagemax = (len(datalist) - 1) // self.height + 1
    else:
      self.pagemax = (len(datalist)) // self.height
    if len(datalist) != self.len:
      self.len = len(datalist)
      self.page = self.pagemax
      self.time = 150
    if self.now == now and self.time != 0:
      self.time -= 1
    elif self.now == now and self.time == 0:
      self.time = 200
      if self.page >= self.pagemax:
        self.page = 1
      else:
        self.page += 1
    else:
      self.time = 200
      self.page = 1
      self.now = now
    for i, data in enumerate(datalist):
      if type(datalist[data]) is str:
        break
      if data == 'top+':
        continue
        # pass
      if (self.page - 1)*self.height < i <= self.page*self.height:
        text1 = self.font1.render(data, True, (0, 0, 0))
        timestr = str(datalist[data]//60)+":"+str(datalist[data]%60).zfill(2)
        text2 = self.font2.render(timestr, True, (255, 200, 0))
        ranktext = self.font2.render(str(i), True, (255, 255, 255))
        screen.blit(self.img, (995, (i-(self.page-1)*self.height)*36+50))
        screen.blit(ranktext, (1008-(len(str(i))-1)*8, (i-(self.page-1)*self.height)*36+45))
        screen.blit(text1, (1040, (i-(self.page-1)*self.height)*36+50))
        screen.blit(text2, (1275-(len(timestr)-1)*20, (i-(self.page-1)*self.height)*36+45))

class チーム():
  def __init__(self) -> None:
    self.font = pygame.font.SysFont("yumincho", 30)
    self.image1 = pygame.image.load("img/tile.png")
    self.image2 = pygame.image.load("img/tile2.png")
  def disp(self, screen, datalist):
    f = open('doc/teamlist.txt', 'r', encoding='UTF-8')
    self.team_list = f.readlines()
    self.data = []
    self.datapos = []
    for i, team in enumerate(self.team_list):
      self.data.append(team.rstrip('\n')[:5])
      self.datapos.append(pygame.Vector2((i%5)*160+10, int(i/5)*40+500))
      self.text = self.font.render(self.data[i], True, (0, 0, 0))
      for data_key in datalist:
        if data_key == self.data[i]:
          screen.blit(self.image2, self.datapos[i])
          break
      else:
        screen.blit(self.image1, self.datapos[i])
      screen.blit(self.text, ((i%5)*160+15, int(i/5)*40+505))
    f.close()
    return self.data, self.datapos

class チェックポイント():
  def __init__(self) -> None:
    self.font = pygame.font.SysFont("yumincho", 30)
    self.image1 = pygame.image.load("img/tile.png")
    self.image2 = pygame.image.load("img/tile2.png")
    self.cp_list = []
    self.data = []
    self.datapos = []
  def disp(self, screen, now):
    f = open('doc/cplist.txt', 'r', encoding='UTF-8')
    self.data = []
    self.datapos = []
    self.cp_list = f.readlines()
    for i in range(len(self.cp_list)):
      self.data.append(self.cp_list[i].rstrip('\n')[:5])
      self.datapos.append(pygame.Vector2((i%5)*160+10, int(i/5)*40+60))
      self.text = self.font.render(self.data[i], True, (0, 0, 0))
      if i == now:
        screen.blit(self.image2, self.datapos[i])
      else:
        screen.blit(self.image1, self.datapos[i])
      screen.blit(self.text, ((i%5)*160+15, int(i/5)*40+65))
    f.close()
    return self.data , self.datapos

class 設定():
  def __init__(self) -> None:
    self.team = [
      [sg.Text('下にチーム名を記入')], 
      [sg.Text('注意事項\n ・5文字以内\n ・改行で区切る\n ・同一の名称を使用しない')], 
      [sg.Multiline(key='-Input_t-', default_text="", size=(20, 10))], 
      [sg.Button('入力を登録します', key='-Btn_t-')]
    ]
    self.cp = [
      [sg.Text('下に計測地点名を記入')], 
      [sg.Text('注意事項\n ・5文字以内\n ・改行で区切る\n ・同一の名称を使用しない')], 
      [sg.Multiline(key='-Input_cp-', default_text="", size=(20, 10))], 
      [sg.Button('入力を登録します', key='-Btn_cp-')]
    ]
  def setting(self):
    # while True:
      window1 = sg.Window('チーム設定', self.team, size=(250, 400))
      event, value = window1.read()  # イベントの入力を待つ
      if event == '-Btn_t-':
        output = value['-Input_t-']
        f = open("doc/teamlist.txt", "w", encoding="UTF-8")
        f.write(output)
        f.close()
        window1.close()
        # break
      elif event is None:
        window1.close()
        sys.exit()
    # while True:
      window2 = sg.Window('計測地点設定', self.cp, size=(250, 400))
      event, value = window2.read()  # イベントの入力を待つ
      if event == '-Btn_cp-':
        output = value['-Input_cp-']
        f = open("doc/cplist.txt", "w", encoding="UTF-8")
        f.write(output)
        f.close()
        window2.close()
        # break
      elif event is None:
        window2.close()
        sys.exit()

class ヘッダー():
  def __init__(self) -> None:
    self.font = pygame.font.SysFont("yugothic",28)
  def disp(self,screen):
    text=self.font.render("Esc:終了　Space:スタート、ストップ", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def main():
  time = 時間()
  cp_now = 0
  timedata = {}
  setting = 設定()
  team = チーム()
  cp = チェックポイント()
  rank = 順位()
  header =ヘッダー()
  # fullscreen = True
  firsttime = True
  # 設定
  setting.setting()
  # 以下メイン実行
  pygame.init()
  screen = pygame.display.set_mode((1280, 960))
  pygame.display.set_caption("テロップ作成")
  font = pygame.font.SysFont("yugothicuiregular", 30)
  # text_cp = font.render("", True, (0, 0, 0))
  image_cp = pygame.image.load("img/cp.png")
  while (1):
    screen.fill("GREEN")
    menu_area = pygame.Rect(pygame.Vector2(0, 0), pygame.Vector2(820, 960))
    screen.fill("WHITE", menu_area)
    time.disp(screen)
    header.disp(screen)
    cp_list, cp_pos_list = cp.disp(screen, cp_now)
    while firsttime:
      for k in cp_list:
        timedata.update([(k, {"top+":""})])
      # print(timedata)
      firsttime = False
    team_list, team_pos_list = team.disp(screen, timedata[cp_list[cp_now]])
    rank.disp(timedata[cp_list[cp_now]], screen, cp_now)
    text_cp = font.render(cp_list[cp_now], True, (0, 0, 0))
    screen.blit(image_cp, (830, 48))
    screen.blit(text_cp, (835, 51))
    if 1 < len(timedata[cp_list[cp_now]]) < len(team_list)+1:
      lag = time.elapsed_time-timedata[cp_list[cp_now]]['top+']
      lag_text = str(lag//60)+":"+str(lag%60).zfill(2)
      screen.blit(pygame.font.SysFont("ebrima", 30).render(lag_text, True, (255, 255, 0)),(1275-(len(lag_text)-1)*20,45))
      screen.blit(pygame.font.SysFont("yugothicuiregular",24).render("一位とのタイム差", True, (0,0,0)),(1000,55))
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
      if event.type == QUIT:
        pygame.quit()
        # with open('data.json', 'w', encoding='UTF-8') as f:
        #   json.dump(timedata, f, indent=2, ensure_ascii=False)
        sys.exit()
      elif event.type == KEYDOWN:
        if event.key == K_SPACE:
          time.stopstart()
        elif event.key == K_RETURN:
          # time.reset()
          pass
        # elif event.key == K_F11:
        #   if fullscreen:
        #     screen = pygame.display.set_mode((1280, 720))
        #   else:
        #     screen = pygame.display.set_mode((1280, 720), FULLSCREEN)
        #   fullscreen = not fullscreen
        elif event.key == K_ESCAPE:
          pygame.quit()
          # with open('data.json', 'w', encoding='UTF-8') as f:
          #   json.dump(timedata, f, indent=2, ensure_ascii=False)
          sys.exit()
        elif event.key == K_RIGHT and cp_now != len(cp_list)-1:
          cp_now += 1
        elif event.key == K_LEFT and cp_now != 0:
          cp_now -= 1
      elif event.type == MOUSEBUTTONDOWN:
        x, y = event.pos
        mousepos = pygame.Rect(pygame.Vector2(x, y), pygame.Vector2(1, 1))
        tile = pygame.Vector2(160, 40)
        for i in range(len(cp_pos_list)):
          if pygame.Rect(cp_pos_list[i], tile).colliderect(mousepos):
            cp_now = i
            # text_cp = font.render(cp_list[cp_now], True, (0, 0, 0))
            break
        else:
          if time.running:
            for i in range(len(team_pos_list)):
              if pygame.Rect(team_pos_list[i], tile).colliderect(mousepos):
                for t in timedata[cp_list[cp_now]]:
                  if t == 'top+' and timedata[cp_list[cp_now]]['top+'] == "":
                    timedata[cp_list[cp_now]]['top+'] = time.elapsed_time
                  if t == team_list[i]:
                    break
                else:
                  data = (team_list[i], time.elapsed_time-timedata[cp_list[cp_now]]["top+"])
                  timedata[cp_list[cp_now]].update([data])
              # print(team_list[i], time.time)
        # if mousepos ==



if __name__ == "__main__":
  main()
