# parser 26.11
# parser 30.11 - Room class, add room function, other adding functions, LOG
# parser 01.12 - Room poles are now tokens
from constants import *
from scanner import Token
from constants import *

# При ошибке в этом модуле, значение меняется на True и останавливает работу программы
error = False
# Если необходимо, чтобы программа описывала каждое действие, значение меняется на True
LOG = False
# Словарь, ключами ктророго являются комнаты
tree = {}
# Имя комнаты, в которую добавляют элементы
cur_room_name = ""

def print_error(name, line_num, char_num):
    '''
    Печатает ошибку и меняет значение error на True
    Входные параметры: текст ошибки, строка, на которой найдена, символ на котором найдена
    '''
    global error
    error = True
    print("Error: " + name + " (parser) found at line: " + str(line_num) + ", char: " + str(char_num)) 

def print_log(line):
    '''
    Печатает текст, описывающий действия программы, если LOG == True
    на вход передается текст
    '''
    if LOG:
        print(line)
    
def tests():
    '''
    Функция для тестирования других функций
    '''
    print("parser tests:")
    print_tree()

def print_tree():
    '''
    Печатает все построенные комнаты
    '''
    print("tree:")
    for name in tree:
        print(name + ":")
        print(tree[name])

class Room:
    '''
    Класс для всех построенных комнат
    '''
    # Высота комнаты
    height  = Token(0, 0, "HEIGHT", HEIGHT)
    # Ширина комнаты
    width   = Token(0, 0, "WIDTH", WIDTH)
    # Левая дверь
    left    = None
    # Правая дверь
    right   = None
    # Верхняя дверь
    up      = None
    # Нижняя дверь
    down    = None
    # Название картинки
    img     = None

    def __str__ (self):
        '''
        Возвращает строку с описанием комнаты
        '''
        string = "height: " + str(self.height.value) + ", width: " + str(self.width.value)
        if self.left != None:
            string += ", left: " + self.left.value
        if self.right != None:
            string += ", right: " + self.right.value
        if self.up != None:
            string += ", up: " + self.up.value
        if self.down != None:
            string += ", down: " + self.down.value
        if self.img != None:
            string += ", img: " + self.img.value
        return string


def matches(tokens, match):
    '''
    Параметры: последовательность токенов и последовательность типов
    Если входящая последовательность токенов соответствует последовательности типов
    возвращает True, иначе возвращает False
    '''
    for i in range(len(tokens)):
        if i == len(match):
            print_error("unexpected " + tokens[i].type,
                        tokens[i].line_num, tokens[i].char_num)
            break
        elif match[i] != tokens[i].type:
            if i == 0:
                return False
            else:
                print_error("Unexpected " + tokens[i].type + " (expected " + match[i] + ")",
                            tokens[i].line_num, tokens[i].char_num)
                break
    if len(match) > len(tokens):
        print_error("not found " + match[len(tokens)] + " at the end of line",
                    tokens[0].line_num, 1)
    return True

def room_closed():
    '''
    Если cur_room_name == "" 
    то комната считается закрытой и функция возвращает True
    иначе возвращает False
    '''
    if cur_room_name == "":
        return True
    else:
        return False

def add_room(name_token):
    '''
    Добавляет новую комнату в tree и меняет cur_room
    Параматр: токен с названием комнаты
    '''
    global cur_room_name
    global tree
    if not room_closed():
        print_error("room not closed with END", name_token.line_num, 1)
    elif name_token.value in tree:
        print_error("reuse room name", name_token.line_num, name_token.char_num)
    else:
        cur_room_name = name_token.value
        tree[cur_room_name] = Room()
        print_log("added room " + cur_room_name)
    
def match_room(tokens):
    '''
    Если входящие токены соответствуют синтаксису создания комнаты, 
    возвращает True, иначе возвращает False
    '''
    match = ["ROOM", "IDENTIFIER", "COLON"]
    if matches(tokens, match):
        if not error:
            print_log("match room")
            add_room(tokens[1])
        return True
    else:
        return False

def end_room(end_token):
    '''
    Закрывает комнату (очищает cur_room)
    Параматр: токен завершающий комнату
    '''
    global cur_room_name
    if room_closed():
        print_error("unexpected END", end_token.line_num, 0)
    else:
        cur_room_name = ""
        print_log("room closed")

def match_end(tokens):
    '''
    Если входящие токены соответствуют синтаксису завершения комнаты, 
    возвращает True, иначе возвращает False
    '''
    match = ["END"]
    if matches(tokens, match):
        if not error:
            print_log("match end")
            end_room(tokens[0])
        return True
    else:
        return False

def set_height(token):
    '''
    Меняет высоту комнаты
    Параматр: токен со значением высоты
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].height = token
        print_log("height added")

def match_height(tokens):
    '''
    Если входящие токены соответствуют синтаксису изменения высоты, 
    возвращает True, иначе возвращает False
    '''
    match = ["HEIGHT", "NUMBER"]
    if matches(tokens, match):
        if not error:
            print_log("match height")
            set_height(tokens[1])
        return True
    else:
        return False

def set_width(token):
    '''
    Меняет ширину комнаты
    Параматр: токен со значением ширины
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].width = token
        print_log("width added")

def match_width(tokens):
    '''
    Если входящие токены соответствуют синтаксису изменения ширины, 
    возвращает True, иначе возвращает False
    '''
    match = ["WIDTH", "NUMBER"]
    if matches(tokens, match):
        if not error:
            print_log("match width")
            set_width(tokens[1])
        return True
    else:
        return False

def set_left(token):
    '''
    Меняет левую дверь комнаты
    Параматр: токен с названием комнаты на выходе из двери
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].left = token
        print_log("left added")

def match_left(tokens):
    '''
    Если входящие токены соответствуют синтаксису создания левой двери, 
    возвращает True, иначе возвращает False
    '''
    match = ["LEFT", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match left")
            set_left(tokens[1])
        return True
    else:
        return False

def set_right(token):
    '''
    Меняет правую дверь комнаты
    Параматр: токен с названием комнаты на выходе из двери
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].right = token
        print_log("right added")

def match_right(tokens):
    '''
    Если входящие токены соответствуют синтаксису создания правой двери, 
    возвращает True, иначе возвращает False
    '''
    match = ["RIGHT", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match right")
            set_right(tokens[1])
        return True
    else:
        return False

def set_up(token):
    '''
    Меняет верхнюю дверь комнаты
    Параматр: токен с названием комнаты на выходе из двери
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].up = token
        print_log("up added")

def match_up(tokens):
    '''
    Если входящие токены соответствуют синтаксису создания верхней двери, 
    возвращает True, иначе возвращает False
    '''
    match = ["UP", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match up")
            set_up(tokens[1])
        return True
    else:
        return False

def set_down(token):
    '''
    Меняет нижню дверь комнаты
    Параматр: токен с названием комнаты на выходе из двери
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].down = token
        print_log("down added")

def match_down(tokens):
    '''
    Если входящие токены соответствуют синтаксису создания нижней двери, 
    возвращает True, иначе возвращает False
    '''
    match = ["DOWN", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match down")
            set_down(tokens[1])
        return True
    else:
        return False

def set_img(token):
    '''
    Меняет название изображения
    Параматр: токен с именем изображения
    '''
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].img = token
        print_log("img added")

def match_img(tokens):
    '''
    Если входящие токены соответствуют синтаксису добавления изображения, 
    возвращает True, иначе возвращает False
    '''
    match = ["IMG", "STRING"]
    if matches(tokens, match):
        if not error:
            print_log("match img")
            set_img(tokens[1])
        return True
    else:
        return False

def fresh():
    global error
    error = False
    global tree
    tree = {}
    global cur_room_name
    cur_room_name = ""

def build_tree(tokens):
    '''
    Строит из входящих токенов дерево
    В случае успешного создния дерева возвращает tree
    В случае ошибки возвращает None
    '''
    fresh()
    print("building tree:")
    for line in tokens:
        if error:
            break
        elif match_room(line):
            pass
        elif match_end(line):
            pass
        elif match_height(line):
            pass
        elif match_width(line):
            pass
        elif match_left(line):
            pass
        elif match_right(line):
            pass
        elif match_up(line):
            pass
        elif match_down(line):
            pass
        elif match_img(line):
            pass
        else:
            print_error("syntax error", line[0].line_num, line[0].char_num)
    if (not room_closed()) and (not error):
        print_error("room not closed with END", tokens[len(tokens) - 1][0].line_num, 1)
        return None
    elif error:
        return None
    else:
        print("The tree was built")
        return tree

if __name__ == "__main__":
    print ("run parser\n")
    from scanner import find_tokens
    from scanner import print_tokens
    from scanner import error as scaner_error
    tokens = find_tokens()
    #print_tokens()
    print()
    build_tree(tokens)
    print()
    tests()
else:
    print("added parser [script]")