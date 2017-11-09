from pico2d import*
import random
import time
#시간함수
import numbers
 
class Boy:

    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    
    image = None
 
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0,1,2,3
    # 대문자는 enum의 개념
    def __init__(self):
        self.x,self.y = 400,90
        self.frame = random.randint(0,7)
        self.state=3
        self.index = 0
        self.total_frames=0
        
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')
            # 한장만 쓰기위해 여러번나올때마다 불러오면 낭비이므로 image==none사용
            # 객체별로 했을땐 self.image로 헀을터지만 같은 그림 여러장사용이므로 Boy.image사용
            
    def update(self,frame_time):
        distance = Boy.RUN_SPEED_PPS*frame_time
        self.total_frames += 1.0
        self.frame = (self.frame+1)%8
        
        if self.state == self.RIGHT_RUN:
            self.x = min(800, self.x+distance)
            print("Change Time:%f, Total Frames: %d"%(get_time(),self.total_frames))
        elif self.state == self.LEFT_RUN:
            self.x = max(0, self.x-distance)
            print("Change Time:%f, Total Frames: %d"%(get_time(),self.total_frames))
    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*100,100,100,self.x,self.y)
        numbers.draw(self.index, self.x+20, self.y-20, 0.5)

    def handle_event(self, event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in(self.RIGHT_STAND, self.LEFT_STAND):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in(self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in(self.RIGHT_RUN, self.LEFT_RUN):
                self.state = self.RIGHT_STAND
 
class Grass:
    def __init__(self):
        self.image=load_image('grass.png')
    def draw(self):
        self.image.draw(400,30)


class Background:

    SCROLL_SPEED_PPS = 100
    
    def __init__(self):
        self.image=load_image('background.png')
        self.x=0
        self.speed=0
        self.left=0
        self.screen_width=800
        self.screen_height=600

    def draw(self):
        x= int(self.left)
        w= min(self.image.w-x,self.screen_width)
        self.image.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

    def update(self, frame_time):
        self.left = (self.left+frame_time*self.speed)%self.image.w

    def handle_event(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:self.speed-=Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT:self.speed+=Background.SCROLL_SPEED_PPS
        if event.type==SDL_KEYUP:
            if event.key == SDLK_LEFT:self.speed+=Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT:self.speed-=Background.SCROLL_SPEED_PPS

 
def handle_events():
    global running
    global x,y
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            close_canvas()
            sys.exit(1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            close_canvas()
            sys.exit(1)
        else:
            boy.handle_event(event)
            bg.handle_event(event)

start_time = 0.0
def get_frame_time():
    global start_time

    frame_time = get_time() - start_time
    start_time += frame_time
    return frame_time    
 
open_canvas()
grass = Grass()
boy=Boy()
bg = Background()
team = [Boy() for i in range(1)]
 
global running
running = True

start_time=get_time()

while(running):
    frame_time = get_frame_time()
    handle_events()
    for boy in team:
        boy.update(frame_time)
    bg.update(frame_time)
 
    clear_canvas()
    bg.draw()
    grass.draw()
    for boy in team:
        boy.draw()
    update_canvas()
    delay(0.03)
 
