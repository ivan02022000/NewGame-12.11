# scaner 26.11 - key words, colon, identifyer, endl
# scaner 27.11 - Number
# scaner 30.11 - tokens var became list of lines with tokens, added commets, added log, added print file function
# scaner 01.12 - string (one line with "")
# TODO inside (commands inside room), global identifier (with upper first letter)
from constants import *
error = False

log = False
log_file = False

tokens = []
tokens_line = []

KEY_WORDS = {
    "room"  : "ROOM",
    "end"   : "END",
    "height": "HEIGHT",
    "width" : "WIDTH",
    "left"  : "LEFT",
    "right" : "RIGHT",
    "up"    : "UP",
    "down"  : "DOWN",
    "img"   : "IMG"
    }

def print_file(file):
    if log_file == True:
        line_num = 0
        for line in file:
            print(str(line_num) + ") " + line[0: len(line) - 1])
            line_num += 1
            
def print_log(line):
    if log:
        print(line)
        
def tests():
    print("scaner tests:")
    print_tokens()

def is_alfa(s):
    if ((s >= "a") & (s <= "z")) or ((s >= "A") & (s <= "Z")) or (s == "_"):
        return True
    else:
        return False

def is_digit(s):
    if ((s >= "0") & (s <= "9")):
        return True
    else:
        return False

def is_alfa_digit(s):
    return is_alfa(s) or is_digit(s)

def is_space(s):
    if (s == " ") or (s == "\t") or (s == "\n"):
        return True
    else:
        return False

class Token:
    type = None
    value = None
    line_num = 0
    char_num = 0
    
    def __init__ (self, line_num, char_num, type_, value):
        self.line_num = line_num
        self.char_num = char_num
        self.type = type_
        self.value = value

    def __str__(self):
        return 'token(line: '+ str(self.line_num) + ", char: " + str(self.char_num) + ") " + self.type + " = " + str(self.value)


def print_tokens():
    print("tokens:")
    line_num = 0
    for line in tokens:
        print("tokens line " + str(line_num))
        for token in line:
            print(token)
        line_num += 1

def add_token(line_num, word_num, type_, value = None):
    global tokens_line
    tokens_line += [Token(line_num, word_num, type_, value)]
    print_log("added token: " + str(tokens_line[len(tokens_line)-1]))

def add_line():
    global tokens
    global tokens_line
    tokens += [tokens_line]
    tokens_line = []
    print_log("added token line")

def add_word(line_num, char_num, line, word_len):
    word = line[char_num - word_len + 1: char_num + 1]
    # KEYWORD
    if word in KEY_WORDS:
         add_token(line_num,  char_num - word_len + 1,
                  KEY_WORDS[word], None)
    # IDENTIFYER
    else:
         add_token(line_num,  char_num - word_len + 1,
                  "IDENTIFIER", word)

def add_num(line_num, char_num, line, word_len):
    num = int(line[char_num - word_len + 1: char_num + 1])
    add_token(line_num,  char_num - word_len + 1,
              "NUMBER", num)

def print_error(name, line_num, char_num):
    global error
    error = True
    print("Error: " + name + " (scaner) found at line: " + str(line_num) + ", char: " + str(char_num)) 

def find_tokens(source = "text.txt"):
    try:
        file = open(source, "r")
    except FileNotFoundError:
        print("Искомый файл не найден!")
    else:
        print ("source: " + source)
        print_file(file)
        file = open(source, "r")
        line_num = 0
        for line in file:
            if error:
                break
            line += " "
            char_num = 0
            word_len = 0
            num_len = 0
            string_len = -1
            for char in line:
                # STRING
                if (char == '"') or (string_len != -1):
                    if string_len == -1:
                        string_len = 0
                    elif char == '"':
                        add_token(line_num, char_num, "STRING", line[char_num - string_len: char_num])
                        string_len = -1
                    else:
                        if char_num == len(line) - 1:
                            print_error('found end of line (expected ")',line_num, char_num)
                            break
                        else:
                            string_len += 1
                # SYMBOLS
                elif char == ":":
                    add_token(line_num, char_num, "COLON")
                elif char == ".":
                    add_token(line_num, char_num, "DOT")
                # COMMENTS
                elif char == "#":
                    print_log("Comment found at line:" + str(line_num) + ", char: " + str(char_num))
                    break
                # WORDS (IDENTIFIERS, KEYWORDS)
                elif is_alfa(char) or (word_len > 0):
                    word_len += 1
                    if is_alfa_digit(line[char_num + 1]):
                        pass
                    else:
                        add_word(line_num, char_num, line, word_len)
                        word_len = 0
                # NUMBERS
                elif is_digit(char) or (num_len > 0):
                    num_len += 1
                    if is_digit(line[char_num + 1]):
                        pass
                    else:
                        if is_alfa(line[char_num + 1]):
                            print_error("wrong symbol", line_num, char_num)
                            break
                        else:
                            add_num(line_num, char_num, line, num_len)
                            num_len = 0
                # ERRORS and spare
                elif is_space(char):
                    pass
                else:
                    print_error("wrong symbol", line_num, char_num)
                    break
                char_num += 1
            if tokens_line != []:
                add_line()
            line_num += 1
        file.close()
        if error:
            return None
        else:
            print("The file was scanned")
            return tokens

if __name__ == "__main__":
    print ("run scaner\n")
    find_tokens()
    tests()
    input()
else:
    print("added scaner [script]")
