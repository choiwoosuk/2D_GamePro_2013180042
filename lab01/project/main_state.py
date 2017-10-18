from pico2d import*
import random
import game_framework
import title_state

class Boy:
    image = None
    
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0,1,2,3
    
    def __init__(self):
        self.x,self.y = 400,90
        self.frame = random.randint(0,7)
        self.state=3
        self.index = 0
        
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

    def update(self):
        self.frame = (self.frame+1)%8
        if self.state == self.RIGHT_RUN:
            self.x = min(1200, self.x+5)
        elif self.state == self.LEFT_RUN:
            self.x = max(0, self.x-5)
            
    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*100,100,100,self.x,self.y)

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

class Boss:
    def __init__(self):
        self.x,self.y=0,300
        self.frame = 0
        self.image=load_image('boss_sheet.png')

    def update(self):
        self.frame=random.randint(0,8)
        self.x=self.x+1
                             
    def draw(self):
        #self.image.draw(300,300)
        self.image.clip_draw(self.frame*600,0,600,600,self.x,self.y)
        

class Background:
    def __init__(self):
        self.image=load_image('bg.png')
    def draw(self):
        self.image.draw(600,300)

def enter():
    global boy, bg, boss
    boy = Boy()
    boss = Boss()
    bg = Background()

def exit():
    global boy,bg, boss
    del(boy)
    del(bg)
    del(boss)
    
def handle_events():
    global running
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            boy.handle_event(event)

def update():
    boy.update()
    boss.update()

def draw():
    clear_canvas()
    bg.draw()
    boy.draw()
    boss.draw()
    update_canvas()
    delay(0.05)
