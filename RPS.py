# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

import random
from collections import Counter, defaultdict

def player(prev_play, opponent_history=[], my_history=[], fail_count=[0]):
    beats = {'R': 'P', 'P': 'S', 'S': 'R'}
    moves = ['R', 'P', 'S']

    if prev_play:
        opponent_history.append(prev_play)

    # Si hay poco historial, jugar aleatorio
    if len(opponent_history) < 3:
        move = random.choice(moves)
        my_history.append(move)
        return move

    # Detectar si oponente juega siempre igual
    if len(set(opponent_history[-5:])) == 1:
        move = beats[opponent_history[-1]]
        my_history.append(move)
        return move

    # Detectar alternancia simple
    if len(opponent_history) >= 4:
        last4 = opponent_history[-4:]
        if last4[0] == last4[2] and last4[1] == last4[3] and last4[0] != last4[1]:
            predicted = last4[1]
            move = beats[predicted]
            my_history.append(move)
            return move

    # Predicción Markov de orden 1 (transiciones simples)
    trans_counts = defaultdict(Counter)
    for i in range(len(opponent_history)-1):
        trans_counts[opponent_history[i]][opponent_history[i+1]] += 1
    last_op = opponent_history[-1]
    if trans_counts[last_op]:
        predicted = trans_counts[last_op].most_common(1)[0][0]
    else:
        predicted = random.choice(moves)

    # Contar aleatoriedad del oponente
    recent = opponent_history[-10:]
    entropy = len(set(recent)) / 3  # 1 = muy variado, 1/3 = siempre igual

    # Si muy aleatorio, aumentar aleatoriedad propia
    if entropy > 0.8:
        if random.random() < 0.5:
            move = random.choice(moves)
        else:
            move = beats[predicted]
    else:
        # Si menos aleatorio, confiar en la predicción
        move = beats[predicted]

    # Evitar 3 jugadas propias iguales seguidas
    if len(my_history) >= 2 and my_history[-1] == my_history[-2] == move:
        alternatives = [m for m in moves if m != move]
        move = random.choice(alternatives)

    my_history.append(move)

    # Contar fallos para romper patrones si va mal
    if prev_play and len(my_history) >= 2:
        last_my = my_history[-2]
        if (last_my == 'R' and prev_play == 'P') or \
           (last_my == 'P' and prev_play == 'S') or \
           (last_my == 'S' and prev_play == 'R'):
            fail_count[0] += 1
        else:
            fail_count[0] = max(fail_count[0] - 1, 0)

    # Si demasiados fallos, jugar aleatorio para resetear
    if fail_count[0] > 4:
        move = random.choice(moves)
        fail_count[0] = 0
        my_history[-1] = move

    return move


