import unittest
import sys
sys.path.append('/python_progs/NewGame 12.11/NewGame 12.11')
from parser_ import build_tree
from parser_ import Room
from scanner import find_tokens

# Название файла со сканируемым текстом
F_NAME = "test.txt"

def create_tokens(text):
    '''
    Открывает и записывает текст в файл
    Скинирует файл и возвращает токены
    Принимает текст
    '''
    file = open(F_NAME, "w")
    file.write(text)
    file.close()
    return find_tokens(F_NAME)

def equal_rooms(room1, room2):
    '''
    Функция для сравнения комнат
    Принимает две сравниваемые комнаты
    Если они одинаковые (их поля) то возвращает True
    иначе возвращает False
    '''
    if room1.height != room2.height:
        return False
    if room1.width != room2.width:
        return False
    if room1.left != room2.left:
        return False
    if room1.right != room2.right:
        return False
    if room1.up != room2.up:
        return False
    if room1.down != room2.down:
        return False
    if room1.img != room2.img:
        return False
    return True

def are_equal(dict1, dict2):
    '''
    Функция для сравнения словарей комнат
    Принимает два сравниваемых словаря
    Если они одинаковые то возвращает True
    иначе возвращает False
    '''
    if len(dict1) != len(dict2):
        print("not equal len of lists: len1 = " + str(len(dict1)) + " len2 = " + str(len(dict2)))
        return False
    for key in dict1:
        if key not in dict2:
            print("room "+ key + " not found in dict2")
            return False
        if not equal_rooms(dict1[key], dict2[key]):
            print("found not equal rooms " + key + ":\n" + str(dict1[key]) + "\n" + str(dict2[key]))
            return False
    return True

class TestParser(unittest.TestCase):
    '''
    Класс для тестирования парсера
    '''
    def test_empty_room(self):
        '''
        Тестирование пустой комнаты
        '''
        print("\ntest_empty_room")
        tokens = create_tokens('room ask321_me:'+ "\n" +
                               ''               + "\n" +
                               'end'        )
        built_tree = build_tree(tokens)
        room1 = Room()
        tree = {"ask321_me" : room1}
        self.assertTrue(are_equal(tree, built_tree))
        print("test_empty_room passed")

    def test_all_poles(self):
        '''
        Тестирование всех полей комнаты
        '''
        print("\ntest_all_poles")
        tokens = create_tokens('room a1:'    + "\n" +
                               'height 123'  + "\n" +
                               'width 123'   + "\n" +
                               'left nice1'  + "\n" +
                               'right nice2' + "\n" +
                               'up nice3'    + "\n" +
                               'down nice4'  + "\n" +
                               'img "nice5"' + "\n" +
                               'end'        )
        built_tree = build_tree(tokens)
        room1 = Room()
        room1.height = tokens[1][1]
        room1.width  = tokens[2][1]
        room1.left   = tokens[3][1]
        room1.right  = tokens[4][1]
        room1.up     = tokens[5][1]
        room1.down   = tokens[6][1]
        room1.img    = tokens[7][1]
        tree = {"a1" : room1}
        self.assertTrue(are_equal(tree, built_tree))
        print("test_all_poles passed")

    def test_some_rooms(self):
        '''
        Тестирование нескольких комнат
        '''
        print("\ntest_some_rooms")
        tokens = create_tokens('room a1:'  + "\n" +
                               'end'       + "\n" +
                               'room a2:'  + "\n" +
                               'end'       + "\n" +
                               'room a3:'  + "\n" +
                               'end'       )
        built_tree = build_tree(tokens)
        room = Room()
        tree = {
            "a1" : room,
            "a2" : room,
            "a3" : room
            }
        self.assertTrue(are_equal(tree, built_tree))
        print("test_some_rooms passed")

    def test_no_colon(self):
        '''
        Тестирование синтаксической ошибки (нет двоеточия)
        '''
        print("\ntest_no_colon")
        tokens = create_tokens('room a1:'  + "\n" +
                               'end'       + "\n" +
                               'room a2'   + "\n" +
                               'end'       + "\n" +
                               'room a3:'  + "\n" +
                               'end'       )
        built_tree = build_tree(tokens)
        self.assertEqual(built_tree, None)
        print("test_no_colon passed")

    def test_room_end_error(self):
        '''
        Тестирование синтаксической ошибки (нет конца комнаты)
        '''
        print("\ntest_room_end_error")
        tokens = create_tokens('room a1:'  + "\n" +
                               'end'       + "\n" +
                               'room a2:'  + "\n" +
                               'room a3:'  + "\n" +
                               'end'       )
        built_tree = build_tree(tokens)
        self.assertEqual(built_tree, None)
        print("test_room_end_error passed")

    def test_room_reuse(self):
        '''
        Тестирование ошибки (повторение комнат)
        '''
        print("\ntest_room_reuse")
        tokens = create_tokens('room a1:'  + "\n" +
                               'end'       + "\n" +
                               'room a1:'  + "\n" +
                               'end'       )
        built_tree = build_tree(tokens)
        room1 = Room()
        self.assertEqual(built_tree, None)
        print("test_room_reuse passed")

if __name__ == "__main__":
    print ("run parser tests\n")
    unittest.main()
    input()