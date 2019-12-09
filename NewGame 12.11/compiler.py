from scanner import find_tokens
from scanner import print_tokens
from scanner import tests as scaner_tests
from parser_ import build_tree
from parser_ import print_tree
from parser_ import tests as parser_tests
from analyzer import analyse_all_errors
from constants import *

def tests():
    '''
    Функция для тестирования других функций
    '''
    print()
    print("compiler tests:")
    #scaner_tests()
    #print()
    parser_tests()

def compile():
    '''
    Компилирует файл (собирает дерево и анализирует его, 
    используя модули scanner, parser, analyzer)
    В случае успешной компиляции возвращает собранное дерево
    В случае ошибки возвращает None
    '''
    print("compiling:")
    tokens = find_tokens()
    if tokens == None: 
        return None
    tree = build_tree(tokens)
    if tree == None:
        return None
    if analyse_all_errors(tree):
        return None
    print("compiled successfully")
    return tree

if __name__ == "__main__":
    print ("run first compiler\n")
    compile()
    tests()
else:
    print("added first compiler [script]")