import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import *
from constants import *
from compiler import compile

# Если необходимо, чтобы программа описывала каждое действие, значение меняется на True
LOG = False
# Словарь содержащий комнтаты из скомпелированного файла, дающий к ним доступ по имени
tree = None
# Свойство отвечающее за возможность двигать комнаты
move_enabled = BooleanProperty(True)
# Словарь содержащий виджеты комнат, дающий к ним доступ по имени
rooms_collection = {}

def print_log(line):
    '''
    Печатает текст, описывающий действия программы, если LOG == True
    на вход передается текст
    '''
    if LOG:
        print(line)

class Img(Image):
    '''
    Виджет для изображения
    '''
    pass

class Item(Widget):
    '''
    Виджет для предмета
    '''
    pass

class Room(RelativeLayout):
    '''
    Класс для визуальных объектов: Комната
    '''
    # Назване комнаты
    name = StringProperty(None)
    # Название комнаты сверху
    up_name = StringProperty(None)
    # Название комнаты снизу
    down_name = StringProperty(None)
    # Название комнаты слева
    left_name = StringProperty(None)
    # Название комнаты справа
    right_name =StringProperty(None)
    # Название изображения
    img = ObjectProperty(None)

    def change_img(self, source):
        '''
        Меняет изображение по входящему названию
        '''
        if source != None:
            if self.img != None:
                self.remove_widget(self.img)
            self.img = Img()
            self.img.pos = 0, 0
            self.img.source = source
            self.add_widget(self.img)
            self.img.reload()

    def add_item(self, x = 0, y = 0,  size = (10, 10), source = None):
        '''
        Добавляет пердмет в комнату
        Параметры описывают характеристики предмета
        '''
        self.item = Item()
        self.item.size_hint = (None, None)
        self.item.size = (10, 10)
        self.item.pos = x, y
        self.item.source = source
        self.add_widget(self.item)

    def move_item(self, dx, dy):
        '''
        Двигает предмет
        Параметры описывают движение предмета
        '''
        self.item.pos = self.item.x + dx, self.item.y + dy
        self.item.bind()

    def set_room_params(self, name, height, width, img = None, up = None, down = None, left = None, right = None):
        '''
        Изменяет поля комнаты
        Параметры описывают комнату
        '''
        self.name = name
        self.height = height
        self.width = width
        if img != None:
            self.change_img(img)
        if up != None:
            self.up_name = up
        if down != None:
            self.down_name = down
        if left != None:
            self.left_name = left
        if right != None:
            self.right_name = right


class House(RelativeLayout):
    '''
    Класс для визуального объекта, который содержит в себе все комнаты,
    и управляет движением всех комнат
    '''

    height = NumericProperty(HEIGHT)
    width = NumericProperty(WIDTH)
    def create_current_room(self, name = None, widget = None):
        '''
        Создает current_room и все прилегающие к ней комнаты
        На вход передается или виджет комнаты или название комнаты
        '''
        if widget != None:
            name = widget.name
            x = widget.x
            y = widget.y
        else:
            x = 0
            y = 0
        self.clear_widgets()
        self.cur_room = rooms_collection[name]
        self.cur_room.size_hint = (None, None)
        self.cur_room.pos = x, y
        self.add_widget(self.cur_room)
        if self.cur_room.up_name != None:
            self.create_up_room(self.cur_room.up_name)
        if self.cur_room.down_name != None:
            self.create_down_room(self.cur_room.down_name)
        if self.cur_room.left_name != None:
            self.create_left_room(self.cur_room.left_name)
        if self.cur_room.right_name != None:
            self.create_right_room(self.cur_room.right_name)

    def create_up_room(self, name):
        '''
        Создает up_room
        На вход передается название комнаты
        '''
        self.up_room = rooms_collection[name]
        self.up_room.size_hint = (None, None)
        self.up_room.center_x = self.width/2
        self.up_room.y = self.cur_room.top
        self.add_widget(self.up_room)

    def create_down_room(self, name):
        '''
        Создает down_room
        На вход передается название комнаты
        '''
        self.down_room = rooms_collection[name]
        self.down_room.size_hint = (None, None)
        self.down_room.center_x  = self.width/2
        self.down_room.y = self.cur_room.y - self.down_room.height
        self.add_widget(self.down_room)

    def create_left_room(self, name):
        '''
        Создает left_room
        На вход передается название комнаты
        '''
        self.left_room = rooms_collection[name]
        self.left_room.size_hint = (None, None)
        self.left_room.x = self.cur_room.x - self.left_room.width
        self.left_room.center_y = self.height/2
        self.add_widget(self.left_room)

    def create_right_room(self, name):
        '''
        Создает right_room
        На вход передается название комнаты
        '''
        self.right_room = rooms_collection[name]
        self.right_room.size_hint = (None, None)
        self.right_room.x = self.cur_room.right
        self.right_room.center_y = self.height/2
        self.add_widget(self.right_room)

    def move_vert(self, dy):
        '''
        Двигает комнаты по вертикали
        На вход передается изменение координаты y
        '''
        self.cur_room.y = self.cur_room.y + dy
        if self.cur_room.up_name != None:
            self.up_room.y = self.up_room.y + dy
        if self.cur_room.down_name != None:
            self.down_room.y = self.down_room.y + dy

    def move_horiz(self, dx):
        '''
        Двигает комнаты по горизонтали
        На вход передается изменение координаты x
        '''
        self.cur_room.x = self.cur_room.x + dx
        if self.cur_room.left_name != None:
            self.left_room.x = self.left_room.x + dx
        if self.cur_room.right_name != None:
            self.right_room.x = self.right_room.x + dx

    def move_rooms_up(self, dy):
        '''
        Двигает комнаты вверх при перелистывании вниз
        На вход передается изменение координаты y
        '''
        #top of current room is below the container top or there is the room below the current room
        if (self.cur_room.y < 0) or (self.cur_room.down_name != None):
            if (self.cur_room.x <= 1) and (self.cur_room.right + 1 >= self.width):
                self.move_vert(dy)
            elif self.cur_room.x > 0:
                self.move_horiz(-1)
            else:
                self.move_horiz(1)

    def move_rooms_down(self, dy):
        '''
        Двигает комнаты вниз при перелистывании вверх
        На вход передается изменение координаты y
        '''
        #bottom of current room is above the container bottom or there is the room above the current room
        if (self.cur_room.top >= self.height) or (self.cur_room.up_name != None): 
            if (self.cur_room.x <= 1) and (self.cur_room.right + 1 >= self.width):
                self.move_vert(dy)
            elif self.cur_room.x > 0:
                self.move_horiz(-1)
            else:
                self.move_horiz(1)

    def move_rooms_left(self, dx):
        '''
        Двигает комнаты влево при перелистывании вправо
        На вход передается изменение координаты x
        '''
        if (self.cur_room.right >= self.width) or (self.cur_room.right_name != None): 
            if (self.cur_room.y <= 1) and (self.cur_room.top + 1 >= self.height):
                self.move_horiz(dx)
            elif self.cur_room.y > 0:
                self.move_vert(-1)
            else:
                self.move_vert(1)

    def move_rooms_right(self, dx):
        '''
        Двигает комнаты вправо при перелистывании влево
        На вход передается изменение координаты x
        '''
        if (self.cur_room.x <= 0) or (self.cur_room.left_name != None): 
            if (self.cur_room.y <= 1) and (self.cur_room.top + 1 >= self.height):
                self.move_horiz(dx)
            elif self.cur_room.y > 0:
                self.move_vert(-1)
            else:
                self.move_vert(1)

    def update_rooms(self):
        '''
        Двигает current_room, когда она покидает house в неправильном направлении
        Меняет current_room когда игрок переходит в другую комнату
        '''
        if self.cur_room.up_name != None:
            if self.cur_room.top < 0:
                print_log("opened above door")
                self.create_current_room(widget = self.up_room)
        elif (self.cur_room.top < self.height ):
            print_log("y = " + str(self.cur_room.y))
            self.move_vert(1)

        if self.cur_room.down_name != None:
            if self.cur_room.y > self.height:
                print_log("opened down door")
                self.create_current_room(widget = self.down_room)
        elif (self.cur_room.y > 0):
            print_log("y = " + str(self.cur_room.y))
            self.move_vert(-1)

        if self.cur_room.left_name != None:
            if self.cur_room.x > self.width:
                print_log("opened left door")
                self.create_current_room(widget = self.left_room)
        elif (self.cur_room.x > 0):
            print_log("x = " + str(self.cur_room.x))
            self.move_horiz(-1)

        if self.cur_room.right_name != None:
            if self.cur_room.right < 0:
                print_log("opened right door")
                self.create_current_room(widget = self.right_room)
        elif (self.cur_room.right < self.width):
            print_log("x = " + str(self.cur_room.x))
            self.move_horiz(1)

# integration part
def create_rooms_collection_from_tree():
    '''
    Создает коллекцию комнат из дерева
    '''
    for name_ in tree:
        params = get_room_params_from_tree(tree[name_])
        room = Room()
        room.set_room_params(**params, name = name_)
        rooms_collection[name_] = room
    print('collection created (integration)')

# integration part
def get_room_params_from_tree(room):
    '''
    Возвращает словарь из свойств комнаты
    Принимает объект Room
    '''
    params = {}
    if room.height != None:
        params["height"] = room.height.value
    if room.width != None:
        params["width"] = room.width.value
    if room.left != None:
        params["left"] = room.left.value
    if room.right != None:
        params["right"] = room.right.value
    if room.up != None:
        params["up"] = room.up.value
    if room.down != None:
        params["down"] = room.down.value
    if room.img != None:
        params["img"] = IMG_DIR + room.img.value
    return params


class ScrollerGame(Widget):
    '''
    Виджет игры 
    '''
    # Объект House
    house = ObjectProperty(None)

    def make_rooms(self):
        '''
        Подготавливает игру: создает комнаты
        '''
        create_rooms_collection_from_tree()
        self.house.create_current_room(name = "cur")

    def update(self, dt):
        '''
        Обновляет игру
        '''
        self.house.update_rooms()

    def on_touch_move(self, touch):
        '''
        Обрабатывает движения игрока
        '''
        if move_enabled:
            if abs(touch.dx) > abs(touch.dy): #Horisontal
                if touch.dx > 0: #right
                    self.house.move_rooms_right(touch.dx)
                    print_log("right")
                else: #Left
                    self.house.move_rooms_left(touch.dx)
                    print_log("left")
            else: #Vertical
                if touch.dy > 0: #move up scroll down
                    self.house.move_rooms_up(touch.dy)
                    print_log("move up scroll down")
                else: #move down scroll up
                    self.house.move_rooms_down(touch.dy)
                    print_log("move down scroll up")


class ScrollerApp(App):
    '''
    Приложение Scroller
    '''
    def build(self):
        '''
        Создание приложения
        '''
        global tree
        tree = compile()
        if tree == None:
            return None
        game = ScrollerGame()
        game.make_rooms()
        Clock.schedule_interval(game.update, 1.0 / 20.0)
        return game


if __name__ == '__main__':
    ScrollerApp().run()