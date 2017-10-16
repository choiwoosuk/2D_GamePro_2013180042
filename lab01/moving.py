from pico2d import*
import random

class Boy:
    def __init__(self):
        self.x,self.y = random.randint(100,700),90
        self.frame = 0
        self.image=load_image('run_animation.png')
    def update(self):
        self.frame = random.randint(0,7)
        self.x+=2
    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)
 
 
def handle_events():
    global running
    global x,y
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            boy.x,boy.y=event.x,600-event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            close_canvas()
  
open_canvas()
grass = load_image('grass.png')
boy=Boy()
running=True

while(running):
    boy.update()
    clear_canvas()
    grass.draw(400,30)
    boy.draw()
    update_canvas()
    delay(0.05)
    handle_events()
