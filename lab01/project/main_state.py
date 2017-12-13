from pico2d import*
import random
import game_framework
import title_state
import gameover_state
import gameclear_state

class Player:
    
    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    
    image = None
    scream = None

    LEFT, RIGHT = 1,2

    UP_RUN_STATE, UP_IDLE_STATE, RUN_STATE, IDLE_STATE = 0,1,2,3
    
    def __init__(self):
        self.x,self.y = 500,90
        self.frame = random.randint(0,2)
        self.state= 3
        self.index = 0
        self.dir=30
        self.jumpTime=0
        self.jump = False
        self.total_frames=0
        self.life = 4
        self.angle = False
  
        if Player.image==None:
            Player.image = load_image('player_sheet.png')

        if Player.scream == None:
            Player.scream = load_wav('scream.wav')
            Player.scream.set_volume(64)

    def Scream(self):
        self.scream.play()

    def update(self,frame_time):
        distance = Player.RUN_SPEED_PPS*frame_time
        self.total_frames += 1.0
        self.frame = (self.frame+1)%3

        if (self.index,self.state)==(self.LEFT,self.RUN_STATE):
            self.x = max(0, self.x-distance)
        elif(self.index,self.state)==(self.LEFT,self.UP_RUN_STATE):
            self.x = max(0, self.x-distance)
        elif (self.index,self.state)==(self.RIGHT,self.RUN_STATE):
            self.x = min(1000, self.x+distance)
        elif (self.index,self.state)==(self.RIGHT,self.UP_RUN_STATE):
            self.x = min(1000, self.x+distance)

        if(self.jump==True):
            self.jumpTime +=frame_time
            if(self.jumpTime<0.4):
                self.y += self.dir
                self.y += 10
                self.dir-= 1
            elif (self.jumpTime>=0.4):
                self.jump=False
                
        if(self.jump==False):
            if(self.y>90):
                self.y += self.dir
                self.dir-= 4
            if (self.y<=90):
                self.jumpTime=0
                self.y=90
                self.dir=30
            
    def get_bb(self):
        return self.x-25, self.y-75, self.x+50, self.y+50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        
    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*150,100,150,self.x,self.y)
        
    def handle_event(self, event):
                                                                            #좌우 이동
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):                
            if self.state in (self.UP_IDLE_STATE, self.IDLE_STATE):
                if(self.state==3):
                    self.state = self.RUN_STATE
                    self.angle=False
                    #print("전진")
                elif(self.state==1):
                    self.state = self.UP_RUN_STATE
                    self.angle=True
                    #print("총구 올리고 전진")
                self.index = self.LEFT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.UP_IDLE_STATE, self.IDLE_STATE):
                if(self.state==3):
                    self.state = self.RUN_STATE
                    self.angle=False
                    #print("후퇴")
                elif(self.state==1):
                    self.state = self.UP_RUN_STATE
                    self.angle=True
                    #print("총구 올리고 후퇴")
                self.index = self.RIGHT
                                                                            #위아래 총구 변경        
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
                  if self.state in (self.IDLE_STATE, self.RUN_STATE):
                     self.state = self.UP_IDLE_STATE
                     self.angle=True
                     #print("총구위로올려")
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if (self.state==1):
                self.state = self.IDLE_STATE
            elif self.state in (self.UP_IDLE_STATE, self.RUN_STATE):
                self.state = self.RUN_STATE
                self.angle=False
                #print("총구내려")
                                                                            #좌우 이동시 키를 땔경우            
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.UP_RUN_STATE, self.RUN_STATE):
                if(self.state==0):
                    self.state = self.UP_IDLE_STATE
                    self.angle=True
                    #print("총구 올리고 멈춰")
                elif(self.state==2):
                    self.state = self.IDLE_STATE
                    self.angle=False
                    #print("멈춰")
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.UP_RUN_STATE, self.RUN_STATE):
                if(self.state==0):
                    self.state = self.UP_IDLE_STATE
                    self.angle=True
                    #print("총구 올리고 멈춰")
                elif(self.state==2):
                    self.state = self.IDLE_STATE
                    self.angle=False
                    #print("멈춰")

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                  if(self.state==2):
                     self.state = self.UP_RUN_STATE
                     self.angle=True
                     #print("총구위로올리고 전진")
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                  if (self.state==0):
                     self.state = self.RUN_STATE
                     self.angle=False
                     #print("총구내리고 전진")
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            self.jump = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z):
            self.jump=False

class Bullet:

    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 105.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    gun_sound = None
    
    def __init__(self,x,y,angle):
        self.x,self.y=x,y
        if(angle==1):
            self.gunUp = 0
        elif(angle==0):
            self.gunUp = 50
        if Bullet.image==None:
            Bullet.image = load_image('bullet.png')
        if Bullet.gun_sound == None:
            Bullet.gun_sound = load_wav('gun_shoot_sound.wav')
            Bullet.gun_sound.set_volume(64)

    def shoot(self):
        self.gun_sound.play()

    def update(self,frame_time,angleOn):    
        distance = self.RUN_SPEED_PPS * frame_time
        self.x -=distance
        self.y +=self.gunUp
        if self.x < 0:
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x-10, self.y-10, self.x+10, self.y+10
                    
class Boss:
    
    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    LEFT, RIGHT = 1,2
    
    def __init__(self):
        self.x,self.y=0,300
        self.frame = 0
        self.index = 0
        self.life = 140
        self.image=load_image('boss_sheet2.png')

    def update(self,frame_time):
        distance = Boss.RUN_SPEED_PPS*frame_time

        self.frame=random.randint(0,8)
        if(self.index == self.LEFT):
            self.x = max(0, self.x+1+distance)
        elif(self.index == self.RIGHT):
            self.x = max(0, self.x+16-distance)
            #16주면 보스가 더 빨라지고 14주면 캐릭터가 더 빨라짐
        else:
            self.x=self.x+10
                             
    def draw(self):
        self.image.clip_draw(self.frame*600,0,600,600,self.x,self.y)

    def get_bb(self):
        return self.x-300, self.y-300, self.x+250, self.y+200

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.index = self.LEFT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.index = self.RIGHT                                                     
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
                self.index = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
                self.index = 0

class BossBullet:
    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 75.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    shoot = None
    
    def __init__(self,x,y):
        self.x,self.y=x,y
        if BossBullet.image==None:
            BossBullet.image = load_image('boss_bullet.png')
        if BossBullet.shoot == None:
            BossBullet.shoot = load_wav('bossShoot.wav')
            BossBullet.shoot.set_volume(64)

    def Shoot(self):
        self.shoot.play()

    def update(self,frame_time):    
        distance = self.RUN_SPEED_PPS * frame_time
        self.x +=distance
        if self.x > 1200:
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x-25, self.y-25, self.x+25, self.y+25
      
class Background:
    SCROLL_SPEED_PPS = 10
    
    def __init__(self):
        self.image=load_image('bg2.png')
        self.x=0
        self.speed=0
        self.left=0
        self.screen_width = 1200
        self.screen_height = 600
        self.bgm=load_music('contra.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def update(self, frame_time):
        self.left = (self.left+frame_time*self.speed)%self.image.w
        
    def draw(self):
        x= int(self.left)
        w= min(self.image.w-x,self.screen_width)
        self.image.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

    def handle_event(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.speed-=Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT:self.speed+=Background.SCROLL_SPEED_PPS
        if event.type==SDL_KEYUP:
            if event.key == SDLK_LEFT:self.speed+=Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT:self.speed-=Background.SCROLL_SPEED_PPS

class Road:
    SCROLL_SPEED_PPS = 250
    
    def __init__(self):
        self.image=load_image('road.png')
        self.x=0
        self.speed=0
        self.left=0
        self.screen_width = 1200
        self.screen_height = 600

    def update(self, frame_time):
        self.left = (self.left+frame_time*self.speed)%self.image.w
        
    def draw(self):
        x= int(self.left)
        w= min(self.image.w-x,self.screen_width)
        self.image.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

    def handle_event(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.speed-=Road.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT:self.speed+=Road.SCROLL_SPEED_PPS
        if event.type==SDL_KEYUP:
            if event.key == SDLK_LEFT:self.speed+=Road.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT:self.speed-=Road.SCROLL_SPEED_PPS

class Car:

    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    LEFT, RIGHT = 1,2

    image = None
    explo_sound = None

    def __init__(self,x,y):
        self.temp = 0
        #self.x,self.y=random.randint(800,1200),80
        self.x,self.y= x,y
        self.speed=0
        self.index=0
        self.frame=random.randint(0,2)*300;
        if Car.image==None:
            Car.image = load_image('cars.png')
        if Car.explo_sound == None:
            Car.explo_sound = load_wav('explosion.wav')
            Car.explo_sound.set_volume(64)

    def explosion(self,player):
        self.explo_sound.play()

    def update(self, frame_time):
        distance = Car.RUN_SPEED_PPS*frame_time
        
        if(self.index == self.LEFT):
            self.x = self.x+distance
        elif(self.index == self.RIGHT):
            self.x = self.x-distance

    def draw(self):
        self.image.clip_draw(self.frame,0,300,150,self.x,self.y)
        #dist = 0
        #frame = 0
        #for i in range (30):
        #    self.image.clip_draw(frame,0,300,150,self.x+dist,self.y)
        #    dist=dist+1600
        #    frame=frame+300
        #    if(frame==900):
        #        frame=0
            
    def handle_event(self,event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.index = self.LEFT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.index = self.RIGHT                                                     
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            self.index = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.index = 0
        
    def get_bb(self):
        return self.x-100, self.y-75,self.x+100,self.y+50
            
    
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class UI:
    image = None

    def __init__(self,x):
        self.x,self.y= x,550
        self.index=0
        self.frame=0
        if UI.image==None:
            UI.image = load_image('heart.png')

    def update(self, frame_time):
        if(frame_time%10 > 5):
            self.frame = (self.frame+1)%2

    def draw(self):
        self.image.clip_draw(self.frame*50,0,50,50,self.x,self.y)

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

bullet = None
bullet2 = None
BULLET = None
BULLET2 = None
bulletOn = False
bulletTime = 0
bullet2Time = 0
heartBeat = 0

def enter():
    global bg, road, boss, player, cars, life
    global BULLET, BULLET2
    
    player = Player()
    boss = Boss()
    bg = Background()
    road = Road()
    #car = Car(1200,80)
    cars = [Car(i*1200,80) for i in range(30)]

    BULLET = []
    BULLET2 = []
    life = [UI(50+i*60) for i in range(4)]
    #for i in range(30):
        #car = Car(i*1200,80)

def exit():
    global bg, road, boss, player, cars, life
    global BULLET, BULLET2
    
    del(bg)
    del(road)
    del(boss)
    del(player)
    del(cars)
    del(life)

    del(BULLET)
    del(BULLET2)
    
def handle_events():
    global bulletOn
    
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            bulletOn = True
        elif event.type == SDL_KEYUP and event.key == SDLK_x:
            bulletOn = False
        else:
            player.handle_event(event)
            boss.handle_event(event)
            bg.handle_event(event)
            road.handle_event(event)
            for car in cars:
                car.handle_event(event)

start_time = 0.0

def get_frame_time():
    global start_time

    frame_time = get_time() - start_time
    start_time += frame_time
    return frame_time   

def update():
    global bullet, bulletOn
    global bulletTime, bullet2Time, heartBeat
    frame_time = get_frame_time()

    bulletTime +=frame_time*10
    heartBeat +=frame_time*10

    bullet2Time +=frame_time*10
    
    player.update(frame_time)
    boss.update(frame_time)
    bg.update(frame_time)
    road.update(frame_time)
    for heart in life:
        heart.update(heartBeat)
    #life.update(frame_time)
    for car in cars:
        car.update(frame_time)

    if bullet2Time > 100:
        bullet2 = BossBullet(boss.x,random.randint(3,6)*60)
        BULLET2.append(bullet2)
        bullet2.Shoot()
        bullet2Time = 0

    for bullet2 in BULLET2:
        isDel = bullet2.update(frame_time)
        if isDel == True:
            BULLET2.remove(bullet2)


    if bulletOn and bulletTime > 3:
        if(player.angle==False):
            bullet = Bullet(player.x,player.y,1)
        elif(player.angle==True):
            bullet = Bullet(player.x,player.y,0)
        BULLET.append(bullet)
        bullet.shoot()
        bulletTime = 0

    for bullet in BULLET:
        isDel = bullet.update(frame_time,player.angle)
        if isDel == True:
            BULLET.remove(bullet)

    for car in cars:
        if collide(player, car):
            player.life=player.life-1
            life.remove(heart)
            #print("부딪힘. 남은 라이프:", player.life)
            car.explosion(player)
            player.Scream()
            cars.remove(car)

    for bullet2 in BULLET2:
        if collide(bullet2,player):
            player.life=player.life-1
            life.remove(heart)
            player.Scream()
            #print("부딪힘. 남은 라이프:", player.life)
            BULLET2.remove(bullet2)

    for bullet in BULLET:
        if collide(bullet,boss):
            BULLET.remove(bullet)
            if(player.angle == False):
                boss.life = boss.life -1
            elif(player.angle == True):
                boss.life = boss.life -2
            #print("보스 체력: ",boss.life)
    
    if collide(player, boss) or player.life<=0:
        game_framework.change_state(gameover_state)
        return 0

    if boss.life < 0:
        game_framework.change_state(gameclear_state)
        
    #if collide(player, car):
    #    game_framework.change_state(gameover_state)
    #for ruin in ruins:
    #    ruin.update()
        
def draw():
    clear_canvas()
    bg.draw()
    road.draw()
    player.draw()
    for bullet in BULLET:
        bullet.draw()
    for bullet2 in BULLET2:
        bullet2.draw()
    #player.draw_bb()
    for car in cars:
        car.draw()
    #for car in cars:
    #    car.draw_bb()
    boss.draw()
    for heart in life:
        heart.draw()
    #life.draw()
    #boss.draw_bb()
    update_canvas()
    delay(0.05)
