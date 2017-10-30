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

class Player:
    image = None

    LEFT, RIGHT = 1,2

    GUN_UP, RUN_STATE, IDLE_STATE = 0,1,2
    
    def __init__(self):
        self.x,self.y = 400,90
        self.frame = random.randint(0,2)
        self.state=2
        self.index = 0

        if Player.image==None:
            Player.image = load_image('player_sheet.png')

    def update(self):
        self.frame=(self.frame+1)%3
        if (self.index,self.state)==(self.LEFT,self.RUN_STATE):
            self.x = max(0, self.x-5)
        elif (self.index,self.state)==(self.RIGHT,self.RUN_STATE):
             self.x = min(1200, self.x+5)
        

    def draw(self):
        self.image.clip_draw(self.frame*100,self.state*150,100,150,self.x,self.y)
        
    def handle_event(self, event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.state = self.RUN_STATE
            self.index=self.LEFT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.state = self.RUN_STATE
            self.index=self.RIGHT
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            self.state = self.GUN_UP
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            self.state = self.IDLE_STATE
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.state = self.IDLE_STATE

class Boss:
    def __init__(self):
        self.x,self.y=0,300
        self.frame = 0
        self.image=load_image('boss_sheet.png')

    def update(self):
        self.frame=random.randint(0,8)
        self.x=self.x+1
                             
    def draw(self):
        self.image.clip_draw(self.frame*600,0,600,600,self.x,self.y)
        

class Background:
    def __init__(self):
        self.image=load_image('bg.png')
        self.x=0

    def update(self):
        self.x=self.x-2
        
    def draw(self):
        self.image.draw(600+self.x,300)
        self.image.draw(1800+self.x,300)
        self.image.draw(3000+self.x,300)

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
    global bg, boss, player, ruin, ruins
    player = Player()
    boss = Boss()
    bg = Background()
    ruin = Ruin()
    ruins = [Ruin() for i in range(1)]

def exit():
    global bg, boss, player, ruin, ruins
    del(bg)
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

def update():
    player.update()
    boss.update()
    bg.update()
    for ruin in ruins:
        ruin.update()
        
def draw():
    clear_canvas()
    bg.draw()
    player.draw()
    for ruin in ruins:
        ruin.draw()
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
