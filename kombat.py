import json
import jq
import numpy as np


# Carga los movimientos desde el archivo JSON
with open('moves_players.json') as f:
    players = json.load(f)

# Define las estadísticas iniciales de cada jugador
players_config = {
    "player1": {
        "name": "Tonyn Stallone",
        "energy": 6,
        "special_blows": [
            {
                "movements": "DSD",
                "blow": "P",
                "damage": 3,
                "movement_name": "Taladoken"
            },
            {
                "movements": "SD",
                "blow": "K",
                "damage": 2,
                "movement_name": "Remuyuken"
            },
            {
                "movements": "",
                "blow": "K",
                "damage": 1,
                "movement_name": "Patada"
            },
            {
                "movements": "",
                "blow": "P",
                "damage": 1,
                "movement_name": "Puñetazo"
            }
        ]
    },
    "player2": {
        "name": "Arnaldor Shuatsneguer",
        "energy": 6,
        "special_blows": [
            {
                "movements": "SA",
                "blow": "K",
                "damage": 3,
                "movement_name": "Remuyuken"
            },
            {
                "movements": "ASA",
                "blow": "P",
                "damage": 2,
                "movement_name": "Taladoken"
            },
            {
                "movements": "",
                "blow": "K",
                "damage": 1,
                "movement_name": "Patada"
            },
            {
                "movements": "",
                "blow": "P",
                "damage": 1,
                "movement_name": "Puñetazo"
            }
        ]
    }
}

# Función para obtener el movimiento seleccionado por el jugador
def get_move(player):
    print("[1] Buscando movimiento")

    for i in range(len(players_config[player["player"]]["special_blows"])):
        move = player['movements'][i]
        punch = player['punching'][i]

        query = jq.compile('.[] | select(.movements == "'+ move +'" and .blow == "'+ punch +'")')
        result = query.input(players_config[player["player"]]["special_blows"]).all()

        if len(result) > 0:
            player['movements'].pop(i)
            player['punching'].pop(i)

            return result[0]
        
        elif len(result) == 0:
            if punch is not None:
                query = jq.compile('.[] | select(.movements == "" and .blow == "'+ punch +'")')
                result = query.input(players_config[player["player"]]["special_blows"]).all()
                
                if len(result) > 0:
                    player['movements'].pop(i)
                    player['punching'].pop(i)

                    return result[0]
            
            if punch == "" and move is not None:
                player['movements'].pop(i)
                player['punching'].pop(i)

                return None

# Función para aplicar el movimiento y actualizar las estadísticas de los jugadores
def apply_move(attacker, defender, move):
    print("[2] Aplicando movimiento")
    if move:
        damage = move["damage"]
        if damage == 0:
            return print(f"{defender['name']} bloquea el ataque de {attacker['name']}!")
        else:
            defender_energy = players[defender["player"]]['energy'] - damage
            players[defender["player"]]['energy'] = max(0, defender_energy)
            return print(f"{attacker['name']} usa {move['movement_name']} y causa {damage} de daño a {defender['name']}!")
        pass

    return print(f"{attacker['name']} se mueve!")

# Ciclo del juego
while players["player1"]["energy"] > 0 and players["player2"]["energy"] > 0:
    # config players / definir el jugador que ataca primero segun numero de movimientos
    # validate_who_initiates()

    players["player1"]["name"] = players_config["player1"]["name"]
    players["player1"]["player"] = "player1"

    players["player2"]["name"] = players_config["player2"]["name"]
    players["player2"]["player"] = "player2"
    
    # Turno del jugador 1
    move_first_player = get_move(players["player1"])

    apply_move(players["player1"], players["player2"], move_first_player)

    if players["player2"]["energy"] == 0:
        break

    # Turno del jugador 2
    move_second_player = get_move(players["player2"])
    apply_move(players["player2"], players["player1"], move_second_player)

# Determina el ganador
if players["player1"]["energy"] == 0 and players["player2"]["energy"] == 0:
    print("¡Es un empate!")
elif players["player1"]["energy"] == 0:
    print(f"{players['player2']['name']} gana la pelea y aun tiene {players['player2']['energy']} de energia")
else:
    print(f"{players['player1']['name']} gana la pelea y aun tiene {players['player1']['energy']} de energia")
