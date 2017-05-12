import sys
import math

while True:
    input_data = {'SHIP':[], 'BARREL':[]}
    my_ship_count = int(input())  # the number of remaining ships
    entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
    for i in range(entity_count):
        entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        if entity_type == 'SHIP':
            input_data[entity_type] += [[entity_id, x, y, arg_1, arg_2, arg_3, arg_4],]
        else:
            input_data[entity_type] += [[entity_id, x, y, arg_1],]
    for ship in input_data['SHIP']:
        distance = 99999999
        bx = 0
        by = 0
        if ship[6] == 1:
            xs = ship[1]
            ys = ship[2]
            for barrel in input_data['BARREL']:
                xb = barrel[1]
                yb = barrel[2]
                new_distance = ((xs-xb)**2) + ((ys-yb)**2)
                if distance > new_distance:
                    distance = new_distance
                    bx = xb
                    by = yb
            if distance <= 9:
                print('SLOWER')
            print('MOVE', bx, by)

