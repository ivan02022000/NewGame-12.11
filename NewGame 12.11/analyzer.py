# 01.12 - check room names in doors, check values of rooms size
# 02.12 - check if room has door to itself or to some similar rooms
from constants import *
import os.path
import re

# При ошибке в этом модуле, значение меняется на True и останавливает работу программы
error = False
# Если необходимо, чтобы программа описывала каждое действие, значение меняется на True
LOG = False

def print_error(name, token):
    '''
    Печатает ошибку и меняет значение error на True
    Входные параметры: текст ошибки, токен, нарушающий логику программы
    '''
    global error
    error = True
    print("Error: " + name + " (analyzer) found at line: " + str(token.line_num) + ", char: " + str(token.char_num)) 

def print_log(line):
    '''
    Печатает текст, описывающий действия программы, если LOG == True
    на вход передается текст
    '''
    if LOG:
        print(line)

def check_names_error(cur_name, doors):
    '''
    Проверяет, есть ли в комнате двери в одну и ту же комнату или двери в эту комнату
    Параметры: название данной комнаты, двери комнаты
    '''
    names = [cur_name]
    for door in doors:
        if door.value in names:
            print_error("door to room '" + door.value +
                       "' was already made in the room '" + cur_name +
                       "' or it leads to itself", door)
        else:
            names += [door.value]

def fresh():
    global error 
    error = False

def analyse_all_errors(tree):
    '''
    Анализирует на наличие логических ошибок
    Входной параметр: дерево, в котором нужно найти ошибки
    возвращает False если ошибок нет, иначе возвращает True
    '''
    print("analyzing tree:")
    for name in tree:
        print_log("analysing room: " + name)
        room = tree[name]
        # var for all rooms mentioned in current room
        doors_in_room = []

        if room.height.value < HEIGHT:
            print_error("room height must be not less then " + str(HEIGHT), room.height)
        if room.width.value < WIDTH:
            print_error("room width must be not less then " + str(WIDTH), room.width)

        if room.up != None:
            if room.up.value not in tree:
                print_error("room " + room.up.value + " not found", room.up)
            else:
                doors_in_room += [room.up]
                print_log("analyzed up")

        if room.right != None:
            if room.right.value not in tree:
                print_error("room " + room.right.value + " not found", room.right)
            else:
                doors_in_room += [room.right]
                print_log("analyzed right")

        if room.down != None:
            if room.down.value not in tree:
                print_error("room " + room.down.value + " not found", room.down)
            else:
                doors_in_room += [room.down]
                print_log("analyzed down")

        if room.left != None:
            if room.left.value not in tree:
                print_error("room " + room.left.value + " not found", room.left)
            else:
                doors_in_room += [room.left]
                print_log("analyzed left")

        if room.img != None:
            if re.fullmatch(r"\w+\.jpg", room.img.value) or re.fullmatch(r"\w+\.png", room.img.value) or re.fullmatch(r"\w+\.gif", room.img.value):
                if os.path.isfile(IMG_DIR + room.img.value):
                    print_log("analyzed img")
                else:
                    print_error(room.img.value + " file not found", room.img)
            else:
                print_error(room.img.value + ' is not ".jpg" or ".png"', room.img)

        # checking for similar names in room
        check_names_error(name, doors_in_room)
    return error

if __name__ == "__main__":
    print ("run analyzer\n")
else:
    print("added analyzer [script]")