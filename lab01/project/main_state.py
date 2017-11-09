from pico2d import*
import random
import game_framework
import title_state

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
        self.x,self.y = 400,90
        self.frame = random.randint(0,2)
        self.state= 3
        self.index = 0
        self.total_frames=0

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
        

    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*150,100,150,self.x,self.y)
        
    def handle_event(self, event):
                                                                            #좌우 이동
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.UP_IDLE_STATE, self.IDLE_STATE):
                if(self.state==3):
                    self.state = self.RUN_STATE
                    #print("전진")
                elif(self.state==1):
                    self.state = self.UP_RUN_STATE
                    #print("총구 올리고 전진")
                self.index = self.LEFT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
               if self.state in (self.UP_IDLE_STATE, self.IDLE_STATE):
                if(self.state==3):
                    self.state = self.RUN_STATE
                    #print("후퇴")
                elif(self.state==1):
                    self.state = self.UP_RUN_STATE
                    #print("총구 올리고 후퇴")
                self.index = self.RIGHT
                                                                            #위아래 총구 변경        
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
                  if self.state in (self.IDLE_STATE, self.RUN_STATE):
                     self.state = self.UP_IDLE_STATE
                     #print("총구위로올려")
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
                  if self.state in (self.UP_IDLE_STATE, self.RUN_STATE):
                     self.state = self.IDLE_STATE
                     #print("총구내려")
                                                                            #좌우 이동시 키를 땔경우            
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.UP_RUN_STATE, self.RUN_STATE):
                if(self.state==0):
                    self.state = self.UP_IDLE_STATE
                    #print("총구 올리고 멈춰")
                elif(self.state==2):
                    self.state = self.IDLE_STATE
                    #print("멈춰")
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.UP_RUN_STATE, self.RUN_STATE):
                if(self.state==0):
                    self.state = self.UP_IDLE_STATE
                    #print("총구 올리고 멈춰")
                elif(self.state==2):
                    self.state = self.IDLE_STATE
                    #print("멈춰")

class Boss:
    def __init__(self):
        self.x,self.y=0,300
        self.frame = 0
        self.image=load_image('boss_sheet2.png')

    def update(self):
        self.frame=random.randint(0,8)
        self.x=self.x+1
                             
    def draw(self):
        self.image.clip_draw(self.frame*600,0,600,600,self.x,self.y)
        

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
    SCROLL_SPEED_PPS = 100
    
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

class Ruin:
    image = None

    def __init__(self):
        self.x,self.y=random.randint(800,1200),90
        self.frame=random.randint(0,3)
        
        if Ruin.image == None:
            Ruin.image=load_image('ruins.png')

    def update(self):
        self.x=self.x-2

    def draw(self):
        self.image.clip_draw(self.frame*80,0,80,100,self.x,self.y)
        

    def get_bb(self):
        return self.x-40, self.y-50,self.x+40,self.y+50
        

def enter():
    global bg, road, boss, player, ruin, ruins
    player = Player()
    boss = Boss()
    bg = Background()
    road = Road()
    ruin = Ruin()
    ruins = [Ruin() for i in range(1)]

def exit():
    global bg, road, boss, player, ruin, ruins
    del(bg)
    del(road)
    del(boss)
    del(player)
    del(ruin)
    del(ruins)
    
def handle_events():
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            player.handle_event(event)
            bg.handle_event(event)
            road.handle_event(event)

start_time = 0.0
def get_frame_time():
    global start_time

    frame_time = get_time() - start_time
    start_time += frame_time
    return frame_time   

def update():
    frame_time = get_frame_time()
    player.update(frame_time)
    boss.update()
    bg.update(frame_time)
    road.update(frame_time)
    #for ruin in ruins:
    #    ruin.update()
        
def draw():
    clear_canvas()
    bg.draw()
    road.draw()
    player.draw()
    #for ruin in ruins:
    #    ruin.draw()
    boss.draw()
    update_canvas()
    delay(0.05)

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
