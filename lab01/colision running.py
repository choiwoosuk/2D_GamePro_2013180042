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
        #    print("Change Time:%f, Total Frames: %d"%(get_time(),self.total_frames))
        elif self.state == self.LEFT_RUN:
            self.x = max(0, self.x-distance)
        #    print("Change Time:%f, Total Frames: %d"%(get_time(),self.total_frames))
    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*100,100,100,self.x,self.y)
        numbers.draw(self.index, self.x+20, self.y-20, 0.5)

    def get_bb(self):
        return self.x-10, self.y-50, self.x+17, self.y+50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

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
        self.x,self.y = 400,30
        
    def draw(self):
        self.image.draw(400,30)
        
    def get_bb(self):
        return self.x-400,self.y-30,self.x+400,self.y+30

class Ball:
    image = None

    def __init__(self):
        self.x,self.y=random.randint(200,790),60
        if Ball.image == None:
            Ball.image=load_image('ball21x21.png')

    def update(self,frame_time):
        pass

    def draw(self):
        self.image.draw(self.x,self.y)

    def get_bb(self):
        return self.x-10, self.y-10, self.x+10, self.y+10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class BigBall(Ball):
    image = None
    def __init__(self):
        self.x,self.y=random.randint(100,700),500
        self.fall_speed = random.randint(50,120)
        if BigBall.image == None:
            BigBall.image = load_image('ball41x41.png')

    def update(self, frame_time):
        self.y-=frame_time*self.fall_speed

    def stop(self):
        self.fall_speed = 0

    def get_bb(self):
        return self.x-20, self.y-20,self.x+20,self.y+20
    
 
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

start_time = 0.0
def get_frame_time():
    global start_time

    frame_time = get_time() - start_time
    start_time += frame_time
    return frame_time    

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

open_canvas()
global boy, grass, ball
grass = Grass()
boy = Boy()
big_balls = [BigBall() for i in range(10)]
balls = [Ball() for i in range(10)]
balls = big_balls+balls
team = [Boy() for i in range(1)]

 
global running
running = True

start_time=get_time()

while(running):
    frame_time = get_frame_time()
    handle_events()
    for boy in team:
        boy.update(frame_time)
    #boy.update(frame_time)
    for ball in balls:
        ball.update(frame_time)
    for ball in balls:
        if collide(boy, ball):
            balls.remove(ball)
    for ball in big_balls:
        if collide(grass,ball):
            ball.stop()

    #ball.update(frame_time)
    #if collide(boy,ball):
        #print("aaaaa")
        #ball.remove(ball)
 
    clear_canvas()
    grass.draw()
    for ball in balls:
        ball.draw()
    #ball.draw()
    for boy in team:
        boy.draw()
    #boy.draw()
    boy.draw_bb()
    for ball in balls:
        ball.draw_bb()
    update_canvas()
    delay(0.03)
