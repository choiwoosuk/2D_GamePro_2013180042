from pico2d import*
import random
import time
#시간함수
import numbers
import json

class Boy:
    image = None
 
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0,1,2,3
    # 대문자는 enum의 개념
    def __init__(self):
        self.x,self.y = 400,90
        self.frame = random.randint(0,7)
        self.state=3
        self.index = 0
        
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')
            # 한장만 쓰기위해 여러번나올때마다 불러오면 낭비이므로 image==none사용
            # 객체별로 했을땐 self.image로 헀을터지만 같은 그림 여러장사용이므로 Boy.image사용
            
    def update(self):
        self.frame = (self.frame+1)%8
        if self.state == self.RIGHT_RUN:
            self.x = min(800, self.x+5)
        elif self.state == self.LEFT_RUN:
            self.x = max(0, self.x-5)
            
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

def create_team():
    team_data_text ='{"Jarvis":{"StartState":"LEFT_RUN", "x":100, "y":100},"Damon":{"StartState":"RIGHT_RUN", "x":200, "y":200},"Brett":{"StartState":"LEFT_STAND", "x":300, "y":300},"Noel":{"StartState":"RIGHT_STAND", "x":400, "y":400}}'

    player_state_table={
            "LEFT_RUN": Boy.LEFT_RUN,
            "RIGHT_RUN":Boy.RIGHT_RUN,
            "LEFT_STAND":Boy.LEFT_STAND,
            "RIGHT_STAND":Boy.RIGHT_STAND
    }
    
    team_data = json.loads(team_data_text)
    
    team = []
    for name in team_data:
        player = Boy()
        player.name = name
        player.x = team_data[name]['x']
        player.y = team_data[name]['y']
        player.state = player_state_table[team_data[name]['StartState']]
        team.append(player)
    return team
 
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
        

 
open_canvas()
grass = Grass()
boy=Boy()
team = [Boy() for i in range(1)]
create_team()
 
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
 
