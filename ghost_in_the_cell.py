'''
        Codingame Gost in the shell contest
'''
def initialization_input():
    '''
        Takes Intialisation input data and convert into dictionaries
    '''
    distance_data = {}
    link_count = int(input())  # the number of links between factories
    for _ in range(link_count):
        factory_1, factory_2, distance = [int(j) for j in input().split()]
        distance_data[(factory_1, factory_2)] = distance
        distance_data[(factory_2, factory_1)] = distance
    return distance_data

def best_neutral(game_data, distance_data, factory_id, safe_data_level):
    '''
        Calculate the best neutral according to distance and production
    '''
    if factory_id == -1:
        return -1, 0
    score = 0
    best_neutral_id = -1
    for factory in game_data[('FACTORY', 0)]:
        dist = distance_data[(factory_id, factory[0])]
        new_score = (2*factory[2])/(3*dist) + ((safe_data_level[factory[0]])/30)
        if score <= new_score:
            score = new_score
            best_neutral_id = factory[0]
    return best_neutral_id, score

def best_enemy(game_data, distance_data, factory_id, safe_data_level):
    '''
        Calculate the best enemy to attack according to the distance and production
    '''
    if factory_id == -1:
        return -1, 0
    score = 0
    best_enemy_id = -1
    for factory in game_data[('FACTORY', -1)]:
        dist = distance_data[(factory_id, factory[0])]
        new_score = (2*factory[2])/(3*dist) + ((safe_data_level[factory[0]])/30)
        if score <= new_score:
            score = new_score
            best_enemy_id = factory[0]
    return best_enemy_id, score

def final_factory(game_data, distance_data, factory_id, safe_data_level):
    '''
        Gives best factory among neutral and enemy by comparing the scores
    '''
    neutral_id, neutral_score = best_neutral(game_data, distance_data, factory_id, safe_data_level)
    enemy_id, enemy_score = best_enemy(game_data, distance_data, factory_id, safe_data_level)
    if neutral_score > enemy_score:
        return 0, neutral_id
    else:
        return -1, enemy_id
def best_bomb_enemy(game_data):
    '''
        Calculate and gives the best enemy id and his score and
        his no of cyborgs to decide to drop the bomb
    '''
    best_bomb_enemy_id = -1
    score = 0
    for enemy in game_data[('FACTORY', -1)]:
        new_score = (5*enemy[2]) + enemy[1]
        if score <= new_score and ((game_data[('BOMB', 1)] and
                                    game_data[('BOMB', 1)][0][2] != enemy[0]) or
                                   not game_data[('BOMB', 1)]):
            score = new_score
            best_bomb_enemy_id = enemy[0]
    return best_bomb_enemy_id, score
def best_bomb_factory(game_data, distance_data, best_bomb_enemy_id):
    '''
        Calculate the best factory to attack the best enemy by the distance between the factories
    '''
    score = 9999999
    best_bomb_factory_id = -1
    for factory in game_data[('FACTORY', 1)]:
        new_score = distance_data[(factory[0], best_bomb_enemy_id)]
        if score >= new_score:
            score = new_score
            best_bomb_factory_id = factory[0]
    return best_bomb_factory_id

def bomb_decision(game_data, distance_data, bomb_count):
    '''
        Decide to deliver bomb or not by the count of bomb and the enemy factory score
    '''
    bomb_msg = ''
    if bomb_count > 0:
        best_bomb_enemy_id, bomb_enemy_score = best_bomb_enemy(game_data)
        if bomb_enemy_score > 35:
            best_bomb_factory_id = best_bomb_factory(game_data, distance_data, best_bomb_enemy_id)
            bomb_msg += 'BOMB ' + str(best_bomb_factory_id) + ' ' + str(best_bomb_enemy_id)
            bomb_msg += (';MOVE ' + str(best_bomb_factory_id) + ' ' + str(best_bomb_enemy_id)
                         + ' '+str(2))
    return bomb_msg
def safe_data(game_data):
    '''
        Calculte the threat level to our factories using troop DATA
    '''
    safe_data_level = {}
    for troop in game_data[('TROOP', -1)]:
        try:
            safe_data_level[troop[2]] -= troop[3]/troop[4]
        except KeyError:
            safe_data_level[troop[2]] = -troop[3]/troop[4]
    for troop in game_data[('TROOP', 1)]:
        try:
            safe_data_level[troop[2]] += troop[3]/troop[4]
        except KeyError:
            safe_data_level[troop[2]] = troop[3]/troop[4]
    for factory in game_data[('FACTORY', 1)]:
        try:
            safe_data_level[factory[0]] += factory[1]
        except KeyError:
            safe_data_level[factory[0]] = factory[1]
    for factory in game_data[('FACTORY', 0)]:
        try:
            safe_data_level[factory[0]] += factory[1]
        except KeyError:
            safe_data_level[factory[0]] = factory[1]
    for factory in game_data[('FACTORY', -1)]:
        try:
            safe_data_level[factory[0]] += factory[1]
        except KeyError:
            safe_data_level[factory[0]] = factory[1]
    return safe_data_level
def factory_remain_cyborgs_data(game_data):
    '''
        Calculate the remain cyborgs in every factory after a command
    '''
    factory_remain_cyborgs = {}
    for factory in game_data['FACTORY', -1]:
        try:
            factory_remain_cyborgs[factory[0]] += factory[1]
        except KeyError:
            factory_remain_cyborgs[factory[0]] = factory[1]
    for factory in game_data['FACTORY', 1]:
        try:
            factory_remain_cyborgs[factory[0]] += factory[1]
        except KeyError:
            factory_remain_cyborgs[factory[0]] = factory[1]
    return factory_remain_cyborgs
def best_source_factory(game_data, distance_data, safe_data_level,
                        threat_factory, remain_cyborgs_data):
    '''
        Calculate the best source to send cyborgs to make safe
    '''
    dist = 99
    best_source_factory_id = -1
    count = 0
    for factory in game_data[('FACTORY', 1)]:
        if threat_factory != factory[0] and (dist > distance_data[(threat_factory, factory[0])]
                                             and (remain_cyborgs_data[factory[0]]-2) > 0):
            dist = distance_data[(threat_factory, factory[0])]
            best_source_factory_id = factory[0]
            if -safe_data_level[factory[0]] > remain_cyborgs_data[factory[0]]-2:
                count += remain_cyborgs_data[factory[0]]-2
            else:
                count -= safe_data_level[factory[0]]
    return best_source_factory_id, count

def game_loop(distance_data):
    '''
            Run the game loop
    '''
    bomb_count = 2
    while True:
        output = ''
        game_data = {('FACTORY', 1): [], ('FACTORY', 0): [], ('FACTORY', -1): [],
                     ('TROOP', 1): [], ('TROOP', -1): [], ('BOMB', -1): [], ('BOMB', 1): []}
        entity_count = int(input())  # the number of entities (e.g. factories and troops)
        for _ in range(entity_count):
            entity_id, entity_type, owner, arg_2, arg_3, arg_4, arg_5 = input().split()
            entity_id = int(entity_id)
            owner = int(owner)
            arg_2 = int(arg_2)
            arg_3 = int(arg_3)
            arg_4 = int(arg_4)
            arg_5 = int(arg_5)
            game_data[(entity_type, owner)] += [[entity_id, arg_2, arg_3, arg_4, arg_5],]
        safe_data_level = safe_data(game_data)
        remain_cyborgs_data = factory_remain_cyborgs_data(game_data)
        for factory in game_data[('FACTORY', 1)]:
            if factory[2] < 3 and factory[1] > 10:
                output += ';INC ' + str(factory[0])
                remain_cyborgs_data[factory[0]] -= 10
            if safe_data_level[factory[0]] < 0:
                status = False
                while status:
                    if safe_data_level[factory[0]] >= 0:
                        status = True
                    else:
                        b_s_f_i, _ = best_source_factory(game_data, distance_data, safe_data_level,
                                                         factory[0], remain_cyborgs_data)
                        output += ';MOVE '+str(b_s_f_i)+' '+str(factory[0])+' '+str(_)
                        safe_data_level[factory[0]] += _
                        remain_cyborgs_data[b_s_f_i] -= _
        bomb_msg = bomb_decision(game_data, distance_data, bomb_count)
        if bomb_msg:
            output += ';' + bomb_msg
            bomb_count -= 1
        for factory in game_data[('FACTORY', 1)]:
            factory_id = factory[0]
            final_owner, final_factory_id = final_factory(game_data, distance_data, factory_id,
                                                          safe_data_level)
            if final_owner == -1 and (safe_data_level[factory[0]]+
                                      remain_cyborgs_data[factory[0]]) >= 0:
                for factory in game_data[('FACTORY', final_owner)]:
                    if factory[0] == final_factory_id:
                        final_factory_data = factory[:]
                        break
                output += ';MOVE ' + str(factory_id) + ' ' + str(final_factory_id) + ' '
                if (factory[1]-1) > final_factory_data[1]:
                    output += str(final_factory_data[1]+1)
                    remain_cyborgs_data[factory[0]] -= final_factory_data[1]+1
                else:
                    output += str(max(factory[1]-(4-factory[2]), 0))
                    remain_cyborgs_data[factory[0]] -= max(factory[1]-(4-factory[2]), 0)
            elif final_owner == 0 and (safe_data_level[factory[0]]+
                                       remain_cyborgs_data[factory[0]]) >= 0:
                output += (';MOVE ' + str(factory_id) + ' ' + str(final_factory_id) + ' ' +
                           str(int((factory[1]+2)/2)))
                remain_cyborgs_data[factory[0]] -= int((factory[1]+2)/2)
            else:
                pass
        if final_factory_id != -1 and output:
            print(output[1:])
        else:
            print('WAIT')
input()
DISTANCE_DATA = initialization_input()
game_loop(DISTANCE_DATA)
