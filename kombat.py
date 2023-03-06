import json

import jq

# Carga los movimientos desde el archivo JSON
with open("moves_players.json") as f:
    players = json.load(f)

# Define las configuracion iniciales de cada jugador
players_config = {
    "player1": {
        "name": "Tonyn Stallone",
        "energy": 6,
        "special_blows": [
            {
                "movements": "DSD",
                "blow": "P",
                "damage": 3,
                "movement_name": "Taladoken",
            },
            {"movements": "SD", "blow": "K", "damage": 2, "movement_name": "Remuyuken"},
            {"movements": "", "blow": "K", "damage": 1, "movement_name": "Patada"},
            {"movements": "", "blow": "P", "damage": 1, "movement_name": "Puñetazo"},
        ],
    },
    "player2": {
        "name": "Arnaldor Shuatsneguer",
        "energy": 6,
        "special_blows": [
            {"movements": "SA", "blow": "K", "damage": 3, "movement_name": "Remuyuken"},
            {
                "movements": "ASA",
                "blow": "P",
                "damage": 2,
                "movement_name": "Taladoken",
            },
            {"movements": "", "blow": "K", "damage": 1, "movement_name": "Patada"},
            {"movements": "", "blow": "P", "damage": 1, "movement_name": "Puñetazo"},
        ],
    },
}


# Función para obtener el movimiento seleccionado por el jugador
def get_move(player: json):
    for i in range(len(players_config[player["player"]]["special_blows"])):
        move = player["movements"][i]
        punch = player["punching"][i]

        query = jq.compile(
            '.[] | select(.movements == "' + move + '" and .blow == "' + punch + '")'
        )
        result = query.input(players_config[player["player"]]["special_blows"]).all()

        if len(result) > 0:
            player["movements"].pop(i)
            player["punching"].pop(i)

            return result[0]

        elif len(result) == 0:
            if punch is not None:
                query = jq.compile(
                    '.[] | select(.movements == "" and .blow == "' + punch + '")'
                )
                result = query.input(
                    players_config[player["player"]]["special_blows"]
                ).all()

                if len(result) > 0:
                    player["movements"].pop(i)
                    player["punching"].pop(i)

                    return result[0]

            if punch == "" and move is not None:
                player["movements"].pop(i)
                player["punching"].pop(i)

                return None


# Función para aplicar el movimiento y actualizar la energia de los jugadores
def apply_move(attacker: json, defender: json, move: json):
    if move:
        damage = move["damage"]
        if damage == 0:
            return print(f"{defender['name']} bloquea el ataque de {attacker['name']}!")
        else:
            defender_energy = defender["energy"] - damage
            defender["energy"] = max(0, defender_energy)
            return print(
                f"{attacker['name']} usa {move['movement_name']} y causa {damage} de daño a {defender['name']}!"
            )

    return print(f"{attacker['name']} se mueve!")


# Funcion para validar quien inicia primero y se sincronizan los nombres y orden de pelea
def validate_who_initiates(first_player: json, second_player: json):
    players["player1"]["name"] = players_config["player1"]["name"]
    players["player2"]["name"] = players_config["player2"]["name"]

    sum_moves_one = sum(len(s) for s in first_player["movements"])
    sum_punch_one = sum(len(s) for s in first_player["punching"])
    total_moves_one = sum_moves_one + sum_punch_one

    sum_moves_two = sum(len(s) for s in second_player["movements"])
    sum_punch_two = sum(len(s) for s in second_player["punching"])
    total_moves_two = sum_moves_two + sum_punch_two

    if total_moves_one > total_moves_two:
        players["player2"]["player"] = "player1"
        players["player1"]["player"] = "player2"

        return players["player2"], players["player1"]
    elif total_moves_two > total_moves_one:
        players["player1"]["player"] = "player1"
        players["player2"]["player"] = "player2"

        return players["player1"], players["player2"]
    elif total_moves_one == total_moves_two:
        if sum_moves_one > sum_moves_two:
            players["player2"]["player"] = "player1"
            players["player1"]["player"] = "player2"

            return players["player2"], players["player1"]
        elif sum_moves_two > sum_moves_one:
            players["player1"]["player"] = "player1"
            players["player2"]["player"] = "player2"

            return players["player1"], players["player2"]
    else:
        return players["player1"], players["player2"]


# funcion para iniciar la pelea
def start_fight():
    fighter1, fighter2 = validate_who_initiates(players["player1"], players["player2"])

    # Ciclo del juego
    while fighter1["energy"] > 0 and fighter2["energy"] > 0:
        # Turno del jugador 1
        if fighter1["energy"] == 0 or len(fighter1["movements"]) == 0:
            fighter1["energy"] == 0
            break

        move_first_player = get_move(fighter1)
        apply_move(fighter1, fighter2, move_first_player)

        if fighter2["energy"] == 0 or len(fighter2["movements"]) == 0:
            fighter2["energy"] == 0
            break

        # Turno del jugador 2
        move_second_player = get_move(fighter2)
        apply_move(fighter2, fighter1, move_second_player)


start_fight()

# Determina el ganador
if players["player1"]["energy"] == 0 and players["player2"]["energy"] == 0:
    print("¡Es un empate!")
elif players["player1"]["energy"] == 0:
    print(
        f"{players['player2']['name']} gana la pelea y aun tiene {players['player2']['energy']} de energia"
    )
else:
    print(
        f"{players['player1']['name']} gana la pelea y aun tiene {players['player1']['energy']} de energia"
    )
