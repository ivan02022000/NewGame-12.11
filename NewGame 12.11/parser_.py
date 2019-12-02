# parser 26.11
# parser 30.11 - Room class, add room function, other adding functions, log
# parser 01.12 - Room poles are now tokens
from constants import *
from scaner import Token
from constants import *
error = False

log = False

tree = {}
cur_room_name = ""

def print_error(name, line_num, char_num):
    global error
    error = True
    print("Error: " + name + " (parser) found at line: " + str(line_num) + ", char: " + str(char_num)) 

def print_log(line):
    if log:
        print(line)
    
def tests():
    print("parser tests:")
    print_tree()

def print_tree():
    print("tree:")
    for name in tree:
        print(name + ":")
        print(tree[name])

class Room:
    height  = Token(0, 0, "HEIGHT", HEIGHT)
    width   = Token(0, 0, "WIDTH", WIDTH)
    left    = None
    right   = None
    up      = None
    down    = None
    img     = None

    def __str__ (self):
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
                    tokens[0].line_num, 0)
    return True

def room_closed():
    if cur_room_name == "":
        return True
    else:
        return False

def add_room(name_token):
    global cur_room_name
    global tree
    if not room_closed():
        print_error("room not closed with END", name_token.line_num, 0)
    elif name_token.value in tree:
        print_error("reuse room name", name_token.line_num, name_token.char_num)
    else:
        cur_room_name = name_token.value
        tree[cur_room_name] = Room()
        print_log("added room " + cur_room_name)
    
def match_room(tokens):
    match = ["ROOM", "IDENTIFIER", "COLON"]
    if matches(tokens, match):
        if not error:
            print_log("match room")
            add_room(tokens[1])
        return True
    else:
        return False

def end_room(end_token):
    global cur_room_name
    if room_closed():
        print_error("unexpected END", end_token.line_num, 0)
    else:
        cur_room_name = ""
        print_log("room closed")

def match_end(tokens):
    match = ["END"]
    if matches(tokens, match):
        if not error:
            print_log("match end")
            end_room(tokens[0])
        return True
    else:
        return False

def set_height(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].height = token
        print_log("height added")

def match_height(tokens):
    match = ["HEIGHT", "NUMBER"]
    if matches(tokens, match):
        if not error:
            print_log("match height")
            set_height(tokens[1])
        return True
    else:
        return False

def set_width(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].width = token
        print_log("width added")

def match_width(tokens):
    match = ["WIDTH", "NUMBER"]
    if matches(tokens, match):
        if not error:
            print_log("match width")
            set_width(tokens[1])
        return True
    else:
        return False

def set_left(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].left = token
        print_log("left added")

def match_left(tokens):
    match = ["LEFT", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match left")
            set_left(tokens[1])
        return True
    else:
        return False

def set_right(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].right = token
        print_log("right added")

def match_right(tokens):
    match = ["RIGHT", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match right")
            set_right(tokens[1])
        return True
    else:
        return False

def set_up(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].up = token
        print_log("up added")

def match_up(tokens):
    match = ["UP", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match up")
            set_up(tokens[1])
        return True
    else:
        return False

def set_down(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].down = token
        print_log("down added")

def match_down(tokens):
    match = ["DOWN", "IDENTIFIER"]
    if matches(tokens, match):
        if not error:
            print_log("match down")
            set_down(tokens[1])
        return True
    else:
        return False

def set_img(token):
    global tree
    if room_closed():
        print_error("this command must be inside room", token.line_num, 0)
    else:
        tree[cur_room_name].img = token
        print_log("img added")

def match_img(tokens):
    match = ["IMG", "STRING"]
    if matches(tokens, match):
        if not error:
            print_log("match img")
            set_img(tokens[1])
        return True
    else:
        return False

def build_tree(tokens):
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
        print_error("room not closed with END", tokens[len(tokens) - 1][0].line_num, 0)
        return None
    elif error:
        return None
    else:
        print("The tree was built")
        return tree

if __name__ == "__main__":
    print ("run parser\n")
    from scaner import find_tokens
    from scaner import print_tokens
    from scaner import error as scaner_error
    tokens = find_tokens()
    #print_tokens()
    print()
    build_tree(tokens)
    print()
    tests()
else:
    print("added parser [script]")
