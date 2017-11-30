from pico2d import*
import start_state
import game_framework
import main_state

name="TitleState"
image=None

def enter():
    global image, bgm
    image=load_image('title.png')
    bgm=load_music('intro.mp3')
    bgm.set_volume(128)
    bgm.repeat_play()

def exit():
    global image, bgm
    del(image)
    del(bgm)

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

def draw():
    clear_canvas()
    image.draw(600,300)
    update_canvas()

def update(): pass
