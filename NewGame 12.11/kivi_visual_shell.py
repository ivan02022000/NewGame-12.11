#11.11 - 12.11 Plans:
#1) rooms positions change with canvas (too dificult, I made optimisation)
#2) Room class a child of the RelativeLayout  DONE
#3) rooms positions change correctly with various room sizes Done
#4) change current and next rooms Done 
#5) make room hash table Done

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

log  = False

def print_log(line):
    if log:
        print(line)


class Img(Image):
    pass

class Item(Widget):
    pass

class Room(RelativeLayout):
    '''
    class for most content in scroller game
    poles:
        img = ObjectProperty(None)
        name = StringProperty(None)
        up_name = StringProperty(None)
        down_name = StringProperty(None)
    functions:
        change_img(self, source)
        add_item(self, x = 0, y = 0,  size = (10, 10), source = None)
        move_item(self, dx, dy)
        set_room_params(self, img, up_name, down_name, **args)
    '''
    name = StringProperty(None)
    width_ = NumericProperty(WIDTH)
    height_ = NumericProperty(HEIGHT)
    up_name = StringProperty(None)
    down_name = StringProperty(None)
    left_name = StringProperty(None)
    right_name =StringProperty(None)
    img = ObjectProperty(None)

    def change_img(self, source): 
        if source != None:
            if self.img != None:
                self.remove_widget(self.img)
            self.img = Img()
            self.img.pos = 0, 0
            self.img.source = source
            self.add_widget(self.img)
            self.img.reload()

    def add_item(self, x = 0, y = 0,  size = (10, 10), source = None):
        self.item = Item()
        self.item.size_hint = (None, None)
        self.item.size = (10, 10)
        self.item.pos = x, y
        self.item.source = source
        self.add_widget(self.item)

    def move_item(self, dx, dy):
        self.item.pos = self.item.x + dx, self.item.y + dy
        self.item.bind()

    def set_room_params(self, name, height = None, width = None, img = None, up = None, down = None, left = None, right = None):
        self.name = name
        if height != None:
            self.height_ = height
        if width != None:
            self.width_ = width
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
    class that contains and manipulates all rooms as children
    functions:
        create_current_room(self, name, widget)
        create_up_room(self, name)
        create_down_room(self, name)
        move_vert(self, dy)
        move_rooms_up(self, dy)
        move_rooms_down(self, dy)
    '''

    height_ = NumericProperty(HEIGHT)
    width_ = NumericProperty(WIDTH)
    def create_current_room(self, name = None, widget = None):
        '''
        create current room and all rooms connected to current
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
        self.up_room = rooms_collection[name]
        self.up_room.pos = 0, self.cur_room.top
        self.add_widget(self.up_room)

    def create_down_room(self, name):
        self.down_room = rooms_collection[name]
        self.down_room.pos = 0, self.cur_room.y - self.down_room.height
        self.add_widget(self.down_room)

    def create_left_room(self, name):
        self.left_room = rooms_collection[name]
        self.left_room.pos = self.cur_room.x - self.left_room.width, 0 
        self.add_widget(self.left_room)

    def create_right_room(self, name):
        self.right_room = rooms_collection[name]
        self.right_room.pos = self.cur_room.right, 0
        self.add_widget(self.right_room)

    def move_vert(self, dy):
        self.cur_room.y = self.cur_room.y + dy
        if self.cur_room.up_name != None:
            self.up_room.y = self.up_room.y + dy
        if self.cur_room.down_name != None:
            self.down_room.y = self.down_room.y + dy

    def move_horiz(self, dx):
        self.cur_room.x = self.cur_room.x + dx
        if self.cur_room.left_name != None:
            self.left_room.x = self.left_room.x + dx
        if self.cur_room.right_name != None:
            self.right_room.x = self.right_room.x + dx

    def move_rooms_up(self, dy):
        '''
        move rooms up, scroll down
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
        move rooms down, scroll up
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
        move rooms left, opening right
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
        move rooms right, opening left
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
        moves current room when it leaves the house in wrong direction
        and changes the current room when player go to enother room
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

# rooms dictionary stores rooms properties ------ before integration
rooms = {"cur": {   "img"       : "D:\\python_progs\\NewGame 12.11\\NewGame 12.11\\images\\Bubbles.jpg",
                    "up"        : "up", 
                    "down"      : "down"},
         "up":  {   "img"       : "D:\\python_progs\\NewGame 12.11\\NewGame 12.11\\images\\Wall.jpg",
                    "up"        : "down", 
                    "down"      : "cur"},
         "down":{   "img"       : "D:\\python_progs\\NewGame 12.11\\NewGame 12.11\\images\\Love.gif",
                    "up"        : "cur", 
                    "down"      : "up"}, 
            }

rooms_collection = {}

def create_rooms_collection_from_tree():# integration part
    for name_ in tree:
        params = get_room_params_from_tree(tree[name_])
        room = Room()
        room.set_room_params(**params, name = name_)
        rooms_collection[name_] = room
    print('collection created (integration)')

def get_room_params_from_tree(room):# integration part
    '''
    returns dictionary of rooms propertyes from room object
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

def create_rooms_collection():
    for name_ in rooms:
        params = get_room_params(name_)
        room = Room()
        room.set_room_params(**params, name = name_)
        rooms_collection[name_] = room
    print('collection created')

def get_room_params(name):
    '''
    returns dictionary of rooms propertyes by rooms name
    '''
    if name in rooms:
        print(rooms[name])
        return rooms[name]
    else:
        print("ERROR - room name dosen't exist: " + name)

move_enabled = BooleanProperty(True)

class ScrollerGame(Widget):
    house = ObjectProperty(None)

    def make_rooms(self):
        #create_rooms_collection() #------- before integration
        create_rooms_collection_from_tree()
        self.house.create_current_room(name = "cur")

    def update(self, dt):
        self.house.update_rooms()

    def on_touch_move(self, touch):
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

tree = None
from compiler import compile

class ScrollerApp(App):
    def build(self):
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