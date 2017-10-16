from pico2d import*
import random
import game_framework
import title_state

class Boy:
    def __init__(self):
        self.x,self.y = random.randint(100,700),90
        self.frame = 0
        self.image=load_image('run_animation.png')
    def update(self):
        self.frame = random.randint(0,7)
        self.x+=5
    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)

class Grass:
    def __init__(self):
        self.image=load_image('grass.png')
    def draw(self):
        self.image.draw(400,30)

def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()

def exit():
    global boy,grass
    del(boy)
    del(grass)
    
def handle_events():
    global running
    global x,y
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            boy.x,boy.y=event.x,600-event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)

def update():
    boy.update()

def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
    delay(0.05)
