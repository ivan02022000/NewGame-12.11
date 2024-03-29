# scanner 26.11 - key words, colon, identifyer, endl
# scanner 27.11 - Number
# scanner 30.11 - tokens var became list of lines with tokens, added commets, added LOG, added print file function
# scanner 01.12 - string (one line with "")
# TODO inside (commands inside room), global identifier (with upper first letter)
from constants import *

# При ошибке в этом модуле, значение меняется на True и останавливает работу программы
error = False
# Если необходимо, чтобы программа описывала каждое действие, значение меняется на True
LOG = False
# Если необходимо, чтобы программа выписывала содержимое читаемого файла, значение меняется на True
lOG_FILE = False
# В этом списке хранятся все найденные в тексте тоекны, сгруппированные для удобства в строки (Lines)
tokens = []
# В этом списке временно хранятся токены, найденные на одной строке текста
tokens_line = []
# Это словарь ключевых слов, которые могут быть найдены в тексте
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

def print_file(source):
    '''
    Печатает файл, если LOG_FILE == True
    на вход передается файл
    '''
    if lOG_FILE == True:
        file = open(source, "r")
        line_num = 0
        for line in file:
            print(str(line_num) + ") " + line[0: len(line) - 1])
            line_num += 1
        file.close()
            
def print_log(line):
    '''
    Печатает текст, описывающий действия программы, если LOG == True
    на вход передается текст
    '''
    if LOG:
        print(line)
       
def print_error(name, line_num, char_num):
    '''
    Печатает ошибку и меняет значение error на True
    Входные параметры: текст ошибки, строка, на которой найдена, символ на котором найдена
    '''
    global error
    error = True
    print("Error: " + name + " (scanner) found at line: " + str(line_num + 1) + ", char: " + str(char_num + 1)) 

def tests():
    '''
    Функция для тестирования других функций
    '''
    print("scanner tests:")
    print_tokens()

def is_alfa(s):
    '''
    Возвращает True, если символ - латинская буква, иначе False
    на вход передается символ
    '''
    if ((s >= "a") & (s <= "z")) or ((s >= "A") & (s <= "Z")) or (s == "_"):
        return True
    else:
        return False

def is_digit(s):
    '''
    Возвращает True, если символ - цифра, иначе False
    на вход передается символ
    '''
    if ((s >= "0") & (s <= "9")):
        return True
    else:
        return False

def is_alfa_digit(s):
    '''
    Возвращает True, если символ - латинская буква или цифра, иначе False
    на вход передается символ
    '''
    return is_alfa(s) or is_digit(s)

def is_space(s):
    '''
    Возвращает True, если символ не учитывается модулем, иначе False
    на вход передается символ
    '''
    if (s == " ") or (s == "\t") or (s == "\n"):
        return True
    else:
        return False

class Token:
    '''
    Класс описывающий каждое слово сканируемого файла
    '''
    # Тип токена
    type = None
    # Значение токена
    value = None
    # Строка на которой токен найден в тексте
    line_num = 0
    # Номер символа на котором найден в тексте
    char_num = 0
    
    def __init__ (self, line_num, char_num, type_, value):
        '''
        Конструктор токена
        '''
        self.line_num = line_num
        self.char_num = char_num
        self.type = type_
        self.value = value

    def __str__(self):
        '''
        Возвращает информацию о токене (его поля) в строковом формате
        '''
        return 'token(line: '+ str(self.line_num) + ", char: " + str(self.char_num) + ") " + self.type + " = " + str(self.value)


def print_tokens():
    '''
    Печатает все найденные токены
    '''
    print("tokens:")
    line_num = 0
    for line in tokens:
        print("tokens line " + str(line_num))
        for token in line:
            print(token)
        line_num += 1

def add_token(line_num, char_num, type_, value = None):
    '''
    Добавляет найденный токен в token_line
    Параметры: номер строки, номер символа, тип токена, значение токена (по умолчанию None)
    '''
    global tokens_line
    tokens_line += [Token(line_num + 1, char_num + 1, type_, value)]
    print_log("added token: " + str(tokens_line[len(tokens_line)-1]))

def add_line():
    '''
    Добавляет составленную tokens_line в tokens и очищает содержимое tokens_line
    '''
    global tokens
    global tokens_line
    tokens += [tokens_line]
    tokens_line = []
    print_log("added token line")

def add_word(line_num, char_num, line, word_len):
    '''
    Добавляет найденное слово и определяет, является оно идентификатором или ключевым словом
    Параметры: номер строки, номер символа, строку (последнее слово в которой является найденным), длинну найденного слова
    '''
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
    '''
    Добавляет найденное число
    Параметры: номер строки, номер символа, строку (последнее слово в которой является найденным), длинну найденного слова
    '''
    num = int(line[char_num - word_len + 1: char_num + 1])
    add_token(line_num,  char_num - word_len + 1,
              "NUMBER", num)

def fresh():
    global tokens
    tokens = []
    global error
    error = []
    global tokens_line
    tokens_line = []


def find_tokens(source = "text.txt"):
    '''
    Ищет токены в тексте
    Входной параметр - название сканируемого файла
    На выход передает список токенов в случае успешного чтения файла
    В случае ошибки возвращает None
    '''
    try:
        file = open(source, "r")
    except FileNotFoundError:
        print("File not found!")
    else:
        global tokens
        fresh()
        file.close()
        print ("source: " + source)
        print_file(source)
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
                        add_token(line_num, char_num - string_len - 1, "STRING", line[char_num - string_len: char_num])
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
    print ("run scanner\n")
    find_tokens()
    tests()
    input()
else:
    print("added scanner [script]")