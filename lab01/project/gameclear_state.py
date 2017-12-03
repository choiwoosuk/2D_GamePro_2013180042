from pico2d import*
import start_state
import game_framework
import main_state
import title_state

name="GameClearState"

class Ending:
    def __init__(self):
        self.image=load_image('clear.png')
        self.bgm=load_music('clear.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()
        self.frame = 0
    def update(self):
        self.frame = (self.frame+1)%2
    def draw(self):
        self.image.clip_draw(self.frame*1200,0,1200,600,600,300)

def enter():
    global ending
    ending = Ending()

def exit():
    global ending
    del(ending)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key)==(SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key)==(SDL_KEYDOWN,SDLK_SPACE):
                game_framework.change_state(title_state)

def update():
    ending.update()

def draw():
    clear_canvas()
    ending.draw()
    delay(0.3)
    update_canvas()
