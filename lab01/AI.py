from pico2d import*
import random
import time
#시간함수
import numbers
 
class Boy:
    image = None
 
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0,1,2,3
    # 대문자는 enum의 개념
    def __init__(self):
        self.x,self.y = random.randint(100,700),random.randint(90,600)
        self.frame = random.randint(0,7)
        self.state=random.randint(0,1)
        self.index = 0
        self.time = time.time()
        
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')
            # 한장만 쓰기위해 여러번나올때마다 불러오면 낭비이므로 image==none사용
            # 객체별로 했을땐 self.image로 헀을터지만 같은 그림 여러장사용이므로 Boy.image사용
            
    def update(self):
        self.elapsed = time.time() - self.time
        if self.state==self.RIGHT_RUN:
            self.frame=(self.frame+1)%8
            self.x+= 5
            if(self.elapsed > 2.5):
                self.time = time.time()
                self.state = self.RIGHT_STAND
        elif self.state == self.LEFT_RUN:
            self.frame = (self.frame+1)%8
            self.x -=5
            if(self.elapsed > 4.0):
                self.time = time.time()
                self.state = self.LEFT_STAND
        elif self.state == self.RIGHT_STAND:
            self.frame = (self.frame+1)%8
            self.handle_right_stand()
        elif self.state == self.LEFT_STAND:
            self.frame = (self.frame+1)%8
            self.handle_left_stand()
 
        if self.x>800:
            self.x=800
            self.state=self.LEFT_RUN
        elif self.x<0:
            self.x=0
            self.state=self.RIGHT_RUN
            
    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*100,100,100,self.x,self.y)
        numbers.draw(self.index, self.x+20, self.y-20, 0.5)


    def handle_right_stand(self):
        if(self.elapsed>2.0):
           self.time=time.time()
           self.state = self.RIGHT_RUN
        
    def handle_left_stand(self):
        if(self.elapsed>2.0):
           self.time=time.time()
           self.state = self.LEFT_RUN
        
 
class Grass:
    def __init__(self):
        self.image=load_image('grass.png')
    def draw(self):
        self.image.draw(400,30)
 
def handle_events():
    global running
    global x,y
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            close_canvas()
            sys.exit(1)
        elif event.type == SDL_MOUSEMOTION:
            boy.x,boy.y=event.x,600-event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            close_canvas()
            sys.exit(1)

 
open_canvas()
grass = Grass()
boy=Boy()
team = [Boy() for i in range(10)]
 
global running
running = True
while(running):
    handle_events()
    for boy in team:
        boy.update()
 
    clear_canvas()
    grass.draw()
    for boy in team:
        boy.draw()
    update_canvas()
 
    delay(0.05)
 
