from utils import *
from Map import *
from InputHandler import getch


if __name__ == '__main__':
    map = Map("test")
    map.display()
    while (1):
        input = getch()
        print(input)
        map.refresh()
