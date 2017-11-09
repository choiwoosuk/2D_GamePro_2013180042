from pico2d import*
import start_state
import game_framework
import main_state
import title_state

name="GameOverState"
image=None
char=None

class Dead:
    def __init__(self):
        self.image=load_image('dead.png')
        self.x,self.y=600,320
        self.frame = 0
    def update(self):
        self.frame = (self.frame+1)%2
    def draw(self):
        self.image.clip_draw(self.frame*150,0,150,100,self.x,self.y)

def enter():
    global image, char
    image=load_image('gameover.png')
    char=Dead()

def exit():
    global image, char
    del(image)
    del(char)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key)==(SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key)==(SDL_KEYDOWN,SDLK_SPACE):
                game_framework.change_state(main_state)

def update():
    char.update()

def draw():
    clear_canvas()
    image.draw(600,300)
    char.draw()
    delay(0.3)
    update_canvas()
