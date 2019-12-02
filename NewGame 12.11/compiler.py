from scaner import find_tokens
from scaner import print_tokens
from scaner import tests as scaner_tests
from parser_ import build_tree
from parser_ import print_tree
from parser_ import tests as parser_tests
from analyzer import analyse_all_errors
from constants import *

def tests():
    print()
    print("compiler tests:")
    #scaner_tests()
    #print()
    parser_tests()

def compile():
    print("compiling:")
    tokens = find_tokens()
    if tokens == None: 
        #print_tokens()
        return None
    tree = build_tree(tokens)
    if tree == None:
        #print_tree()
        return None
    if analyse_all_errors(tree):
        #print_tree()
        return None
    print("compiled successfully")
    return tree

if __name__ == "__main__":
    print ("run first compiler\n")
    compile()
    #tests()
else:
    print("added first compiler [script]")