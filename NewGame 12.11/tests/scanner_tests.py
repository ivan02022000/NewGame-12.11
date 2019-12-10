import unittest
import sys
sys.path.append('/python_progs/NewGame 12.11/NewGame 12.11')
from scanner import find_tokens
from scanner import Token
from scanner import print_tokens

# Название файла со сканируемым текстом
F_NAME = "test.txt"
# Токены для сравнения с результатом работы модуля
tokens = []

def new_file(text):
    '''
    Открывает и записывает текст в файл
    Принимает текст
    '''
    file = open(F_NAME, "w")
    file.write(text)
    file.close()

def new_tokens(lis):
    '''
    Добавляет тоекны в список
    Принимает список с параметрами токенов
    '''
    global tokens
    tokens = []
    for line in lis:
        tokens_line = []
        for element in line:
            token = Token(element[0], element[1], element[2], element[3])
            tokens_line += [token]
        tokens += [tokens_line]

def equal_tokens(token1, token2):
    '''
    Функция для сравнения токенов
    Принимает два сравниваемых токена
    Если они одинаковые (их поля) то возвращает True
    иначе возвращает False
    '''
    if token1.type != token2.type:
        return False
    if token1.value != token2.value:
        return False
    if token1.line_num != token2.line_num:
        return False
    if token1.char_num != token2.char_num:
        return False
    return True
    
def are_equal(list1, list2):
    '''
    Функция для сравнения списка токенов
    Принимает два сравниваемых списка
    Если они одинаковые то возвращает True
    иначе возвращает False
    '''
    if len(list1) != len(list2):
        print("not equal len of lists: len1 = " + str(len(list1)) + " len2 = " + str(len(list2)))
        return False
    for i in range(len(list1)):
        if len(list1[i]) != len(list2[i]):
            print("not equal len[" + i +"] of lists: len1 = " + str(len(list1[i])) + " len2 = " + str(len(list2[i])))
            return False
        for j in range(len(list1[i])):
            if not equal_tokens(list1[i][j], list2[i][j]):
                print("found not equal tokens:\n" + str(list1[i][j]) + "\n" + str(list2[i][j]))
                return False
    return True

class TestScanner(unittest.TestCase):
    '''
    Класс для тестирования сканера
    '''
    def test_comments_symbols(self):
        '''
        Тестирует комментарии и символы
        '''
        print("\ntest_comments_symbols")
        new_file(': spam:: .# . : spam spam spam')
        lis = [[ # line 0
            [1, 1,   "COLON",       None],
            [1, 3,   "IDENTIFIER",  "spam"],
            [1, 7,   "COLON",       None],
            [1, 8,   "COLON",       None],
            [1, 10,   "DOT",         None],
            ]]
        new_tokens(lis)
        found_tokens = find_tokens(F_NAME)
        self.assertTrue(are_equal(found_tokens, tokens))
        print("test_comments_symbols passed")

    def test_string(self):
        '''
        Тестирует строки
        '''
        print("\ntest_string")
        new_file('"str"."str"' + '\n'+
                 '"str"a"str"' + '\n'+
                 '"str"5"str"' + '\n'+
                 '"str""st#r"#none"')
        lis = [[ # line 0
            [1, 1,   "STRING",      "str"],
            [1, 6,   "DOT",         None],
            [1, 7,   "STRING",      "str"],
            ],[ # line 1
            [2, 1,   "STRING",      "str"],
            [2, 6,   "IDENTIFIER",  "a"],
            [2, 7,   "STRING",      "str"],
            ],[ # line 2
            [3, 1,   "STRING",      "str"],
            [3, 6,   "NUMBER",      5],
            [3, 7,   "STRING",      "str"],
            ],[ # line 3
            [4, 1,   "STRING",      "str"],
            [4, 6,   "STRING",      "st#r"],
            ]]
        new_tokens(lis)
        found_tokens = find_tokens(F_NAME)
        self.assertTrue(are_equal(found_tokens, tokens))
        print("test_string passed")

    def test_words_numbers(self):
        '''
        Тестирует слова и цифры
        '''
        print("\ntest_words_numbers")
        new_file('no no  r2d2'       + '\n'+
                 'room   end '       + '\n'+
                 'height width'      + '\n'+
                 'left right up down'+ '\n'+
                 'img  1 22.333')
        lis = [[ # line 0
            [1, 1,   "IDENTIFIER", "no"],
            [1, 4,   "IDENTIFIER", "no"],
            [1, 8,   "IDENTIFIER", "r2d2"],
            ],[ # line 1
            [2, 1,   "ROOM" , None],
            [2, 8,   "END"  , None],
            ],[ # line 2
            [3, 1,   "HEIGHT" , None],
            [3, 8,   "WIDTH"  , None],
            ],[ # line 3
            [4, 1,   "LEFT" , None],
            [4, 6,   "RIGHT", None],
            [4, 12,  "UP"   , None],
            [4, 15,  "DOWN" , None],
            ],[ # line 4
            [5, 1,   "IMG"      , None],
            [5, 6,   "NUMBER"   , 1],
            [5, 8,   "NUMBER"   , 22],
            [5, 10,   "DOT"      , None],
            [5, 11,  "NUMBER"   , 333],
            ]]
        new_tokens(lis)
        found_tokens = find_tokens(F_NAME)
        self.assertTrue(are_equal(found_tokens, tokens))
        print("test_words_numbers passed")

    def test_error_wrong_symbol(self):
        '''
        Тестирует на ошибку неправильного символа
        '''
        print("\ntest_error_wrong_symbol")
        new_file('not4 5year old')
        print("should be wrong symbol error: line 1, char 6")
        found_tokens = find_tokens(F_NAME)
        self.assertEqual(found_tokens, None)
        print("test_error_wrong_symbol passed")

    def test_error_string(self):
        '''
        Тестирует на ошибку строки
        '''
        print("\ntest_error_string")
        new_file('not4"me')
        print("should be string error: line 1, char 7")
        found_tokens = find_tokens(F_NAME)
        self.assertEqual(found_tokens, None)
        print("test_error_string passed")

if __name__ == "__main__":
    print ("run scanner tests\n")
    unittest.main()
    input()