import json
import random

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/kombat/start')
def kombat_start():
    # Carga los movimientos desde el archivo JSON
    with open('moves.json') as f:
        moves = json.load(f)

    # Define las estadísticas iniciales de cada jugador
    players = {
        "Player 1": {
            "energy": 100
        },
        "Player 2": {
            "energy": 100
        }
    }

    # Función para obtener el movimiento seleccionado por el jugador
    def get_move(player):
        print(f"{player}, elige tu movimiento:")
        for i, move in enumerate(moves):
            print(f"{i+1}. {move} ({moves[move]['description']})")
        while True:
            try:
                move_index = int(input("> "))
                if move_index not in range(1, len(moves)+1):
                    raise ValueError
                break
            except ValueError:
                print("Ingresa un número válido.")
        return list(moves.keys())[move_index-1]

    # Función para aplicar el movimiento y actualizar las estadísticas de los jugadores
    def apply_move(attacker, defender, move):
        damage = moves[move]['damage']
        if damage == 0:
            print(f"{defender} bloquea el ataque de {attacker}!")
        else:
            print(f"{attacker} usa {move} y causa {damage} de daño a {defender}!")
            defender_energy = players[defender]['energy'] - damage
            players[defender]['energy'] = max(0, defender_energy)

    # Ciclo del juego
    while players["Player 1"]["energy"] > 0 and players["Player 2"]["energy"] > 0:
        # Turno del jugador 1
        move1 = get_move("Player 1")
        apply_move("Player 1", "Player 2", move1)
        if players["Player 2"]["energy"] == 0:
            break
        # Turno del jugador 2
        move2 = get_move("Player 2")
        apply_move("Player 2", "Player 1", move2)

    # Determina el ganador
    if players["Player 1"]["energy"] == 0 and players["Player 2"]["energy"] == 0:
        print("¡Es un empate!")
    elif players["Player 1"]["energy"] == 0:
        print("¡Player 2 gana!")
    else:
        print("¡Player 1 gana!")


if __name__ == '__main__':
    app.run()