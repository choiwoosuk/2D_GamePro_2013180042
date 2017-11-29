from pico2d import*
import random
import game_framework
import title_state
import gameover_state

class Player:
    
    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    
    image = None

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
    
    def __init__(self,x,y):
        self.x,self.y=x,y
        if Bullet.image==None:
            Bullet.image = load_image('bullet.png')

    def update(self,frame_time,angleOn):    
        distance = self.RUN_SPEED_PPS * frame_time
        if(angleOn==False):
            self.x -= distance
        elif(angleOn == True):
            self.x -=distance
            self.y +=distance
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
        self.image=load_image('boss_sheet2.png')

    def update(self,frame_time):
        distance = Boss.RUN_SPEED_PPS*frame_time
        self.frame=random.randint(0,8)
        
        if(self.index == self.LEFT):
            self.x = max(0, self.x+1+distance)
        elif(self.index == self.RIGHT):
            self.x = max(0, self.x+14-distance)
        else:
            self.x=self.x+10
                             
    def draw(self):
        self.image.clip_draw(self.frame*600,0,600,600,self.x,self.y)

    def get_bb(self):
        return self.x-300, self.y-300, self.x+250, self.y+300

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
    SCROLL_SPEED_PPS = 200
    
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

    def __init__(self,x,y):
        self.temp = 0
        #self.x,self.y=random.randint(800,1200),80
        self.x,self.y= x,y
        self.speed=0
        self.index=0
        self.frame=random.randint(0,2)*300;
        if Car.image==None:
            Car.image = load_image('cars.png')

    def explosion(self):
        self.explo.play()

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
        
def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

bullet = None
BULLET = None
bulletOn = False
bulletTime = 0

def enter():
    global bg, road, boss, player, car, cars
    global BULLET
    
    player = Player()
    boss = Boss()
    bg = Background()
    road = Road()
    car = Car(1200,80)
    cars = [Car(i*1200,80) for i in range(30)]

    BULLET = []
    #for i in range(30):
        #car = Car(i*1200,80)

def exit():
    global bg, road, boss, player, car, cars
    global BULLET
    
    del(bg)
    del(road)
    del(boss)
    del(player)
    del(car)
    del(cars)

    del(BULLET)
    
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
    global bulletTime
    frame_time = get_frame_time()

    bulletTime +=frame_time*10
    
    player.update(frame_time)
    boss.update(frame_time)
    bg.update(frame_time)
    road.update(frame_time)    
    for car in cars:
        car.update(frame_time)


    if bulletOn and bulletTime > 3:
        bullet = Bullet(player.x,player.y)
        BULLET.append(bullet)
        bulletTime = 0

    for bullet in BULLET:
        isDel = bullet.update(frame_time,player.angle)
        if isDel == True:
            BULLET.remove(bullet)

    for car in cars:
        if collide(player, car):
            player.life=player.life-1
            print("부딪힘. 남은 라이프:", player.life)
            cars.remove(car)
    for bullet in BULLET:
        if collide(bullet,boss):
            BULLET.remove(bullet)
    
    if collide(player, boss) or player.life<=0:
        game_framework.change_state(gameover_state)
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
    #player.draw_bb()
    for car in cars:
        car.draw()
    #for car in cars:
    #    car.draw_bb()
    boss.draw()
    #boss.draw_bb()
    update_canvas()
    delay(0.05)
