import json

def create_team():
    team_data_text ='{
        "Jarvis":{"StartState":"LEFT_RUN", "x":100, "y":100},
        "Damon":{"StartState":"RIGHT_RUN", "x":200, "y":200},
        "Brett":{"StartState":"LEFT_STAND", "x":300, "y":300},
        "Noel":{"StartState":"RIGHT_STAND", "x":400, "y":400}
    }'

    player_state_table={
            "LEFT_RUN": Boy.LEFT_RUN,
            "RIGHT_RUN":Boy.RIGHT_RUN,
            "LEFT_STAND":Boy.LEFT_STAND,
            "RIGHT_STAND":Boy.RIGHT_STAND
        }
    team_data = json.loads(team_data_text)
    team = []
    for name in team data:
        player = Boy()
        player.name = name
        player.x=team_data[name]['x']
        player.y=team_data[name]['y']
        player.state=player_state_table[team_data[name]['StartState']]
        team.append(player)

    return team
