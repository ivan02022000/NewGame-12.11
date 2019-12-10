import unittest
import sys
sys.path.append('/python_progs/NewGame 12.11/NewGame 12.11')
from parser_ import build_tree
from scanner import find_tokens
from analyzer import analyse_all_errors

# Название файла со сканируемым текстом
F_NAME = "test.txt"

def create_tree(text):
    '''
    Создает словарь с комнатами из входного текста
    '''
    file = open(F_NAME, "w")
    file.write(text)
    file.close()
    tokens = find_tokens(F_NAME)
    tree = build_tree(tokens)
    return tree

class TestAnalyzer(unittest.TestCase):
    '''
    Класс для тестирования анализатора
    '''
    def test_all(self):
        '''
        Тест проверяет все возможности анализатора
        '''
        print("\ntest_all")
        tree = create_tree( 'room a:'           + "\n" +
                            'height 2000'       + "\n" +
                            'width 2000'        + "\n" +
                            'left a1'           + "\n" +
                            'right a2'          + "\n" +
                            'up a3'             + "\n" +
                            'down a4'           + "\n" +
                            'img "Bubbles.jpg"' + "\n" +
                            'end'               + "\n" +
                            'room a1:'          + "\n" +
                            'img "Love.gif"'    + "\n" +
                            'end'               + "\n" +
                            'room a2:'          + "\n" +
                            'end'               + "\n" +
                            'room a3:'          + "\n" +
                            'end'               + "\n" +
                            'room a4:'          + "\n" +
                            'end'               )
        print("0 errors")
        self.assertFalse(analyse_all_errors(tree))
        print("test_all passed")

    def test_size_errors(self):
        '''
        Тест на ошибки размера комнаты
        '''
        print("\ntest_size_errors")
        tree = create_tree( 'room a:'           + "\n" +
                            'height 12'         + "\n" +
                            'width 12'          + "\n" +
                            'end'               )
        print("2 errors: size")
        self.assertTrue(analyse_all_errors(tree))
        print("test_size_errors passed")

    def test_room_not_exist_errors(self):
        '''
        Тест на ошибки дверей
        '''
        print("\ntest_room_not_exist_errors")
        tree = create_tree( 'room a:'           + "\n" +
                            'left a1'           + "\n" +
                            'right a2'          + "\n" +
                            'up a3'             + "\n" +
                            'down a4'           + "\n" +
                            'end'               )
        print("4 errors: doors")
        self.assertTrue(analyse_all_errors(tree))
        print("test_room_not_exist_errors passed")

    def test_img_errors(self):
        '''
        Тест на ошибки изображений
        '''
        print("\ntest_img_errors")
        tree = create_tree( 'room a:'           + "\n" +
                            'img "Bubbles.jp"'  + "\n" +
                            'end'               + "\n" + 
                            'room b:'           + "\n" +
                            'img "Bubblesjp"'   + "\n" +
                            'end'               + "\n" +
                            'room c:'           + "\n" +
                            'img "Bubble.jpg"'  + "\n" +
                            'end'               )
        print("3 errors: 2 - wrong image name, 1 - image not found")
        self.assertTrue(analyse_all_errors(tree))
        print("test_img_errors passed")

    def test_doors_reuse_errors(self):
        '''
        Тест на ошибки дверей
        '''
        print("\ntest_doors_reuse_errors")
        tree = create_tree( 'room a:'           + "\n" +
                            'right a'           + "\n" +
                            'down b'            + "\n" +
                            'left b'            + "\n" +
                            'end'               + "\n" + 
                            'room b:'           + "\n" +
                            'end'               )
        print("2 errors: dors already made in the room")
        self.assertTrue(analyse_all_errors(tree))
        print("test_doors_reuse_errors passed")

if __name__ == "__main__":
    print ("run analyzer tests\n")
    unittest.main()
    input()