#11.11 - 12.11 Plans:
#1) rooms positions change with canvas (too dificult, I made optimisation)
#2) Room class a child of the RelativeLayout  DONE
#3) rooms positions change correctly with various room sizes Done
#4) change current and next rooms Done 
#5) make room hash table Done
#RESULTS - working but slow
#14.11 Plans:
#1) Change room class - make set_room_params function better, make constructor(?)
#2) Change rooms loading method

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
    img = ObjectProperty(None)
    name = StringProperty(None)
    up_name = StringProperty(None)
    down_name = StringProperty(None)

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

    def set_room_params(self, img, up_name, down_name, **args):
        if img!= None:
            self.change_img(img)
        if up_name!= None:
            self.up_name = up_name
        if down_name!= None:
            self.down_name = down_name


class House(RelativeLayout):
    '''
    class that contains and manipulates all rooms as children
    functions:
        create_current_room(self, name, width = None, height = None, x = 0, y = 0)
        create_up_room(self, name, width = None, height = None, **args)
        create_down_room(self, name, width = None, height = None,  **args)
        move_vert(self, dy)
        move_rooms_up(self, dy)
        move_rooms_down(self, dy)
        load_rooms(self)
    '''

    def create_current_room(self, name, width = None, height = None, x = 0, y = 0):
        '''
        create current for the first time
        '''
        self.cur_room = Room()
        if width != None:
            self.cur_room.size_hint_x = None
            self.cur_room.width = width
        if height != None:
            self.cur_room.size_hint_y = None
            self.cur_room.height = height
        self.cur_room.pos = x, y     # here is current room pos
        params = get_room_params(name)
        self.cur_room.set_room_params(**params)
        self.add_widget(self.cur_room)
        self.load_rooms()

    def create_up_room(self, name, width = None, height = None, **args):
        self.cur_room.up_name = name
        self.up_room = Room()
        if width != None:
            self.up_room.size_hint_x = None
            self.up_room.width = width
        if height != None:
            self.up_room.size_hint_y = None
            self.up_room.height = height
        self.up_room.pos = 0, self.cur_room.top
        self.add_widget(self.up_room)

    def create_down_room(self, name, width = None, height = None,  **args):
        self.cur_room.down_name = name
        self.down_room = Room()
        if width != None:
            self.down_room.size_hint_x = None
            self.down_room.width = width
        if height != None:
            self.down_room.size_hint_y = None
            self.down_room.height = height
        self.down_room.pos = 0, self.cur_room.y - self.down_room.height
        self.add_widget(self.down_room)

    def move_vert(self, dy):
        self.cur_room.y = self.cur_room.y + dy
        if self.cur_room.up_name != None:
            self.up_room.y = self.up_room.y + dy
        if self.cur_room.down_name != None:
            self.down_room.y = self.down_room.y + dy

    def move_rooms_up(self, dy):
        '''
        move rooms up, scroll down
        '''
        #top of current room is below the container top or there is the room below the current room
        if (self.cur_room.y < 0) or (self.cur_room.down_name != None):
            if self.cur_room.x == 0:
                self.move_vert(dy)
            elif self.cur_room.x > 0:
                self.cur_room.x = self.cur_room.x - 1
            else:
                self.cur_room.x = self.cur_room.x + 1

    def move_rooms_down(self, dy):
        '''
        move rooms down, scroll up
        '''
        #bottom of current room is upper the container bottom or there is the room upper the current room
        if (self.cur_room.top >= self.height) or (self.cur_room.up_name != None): 
            if self.cur_room.x == 0:
                self.move_vert(dy)
            elif self.cur_room.x > 0:
                self.cur_room.x = self.cur_room.x - 1
            else:
                self.cur_room.x = self.cur_room.x + 1

    def update_rooms(self):
        '''
        moves current room when it leaves the house in wrong direction
        and changes the current room when player go to enother room
        '''
        if self.cur_room.up_name != None:
            if self.cur_room.top < 0:
                print("opened upper door")
                self.cur_room = self.up_room
                self.load_rooms()
        elif (self.cur_room.top < self.height) and (self.cur_room.top < self.height - 1):
            print(self.cur_room.y)
            self.move_vert(1)

        if self.cur_room.down_name != None:
            if self.cur_room.y > self.height:
                print("opened down door")
                self.cur_room = self.down_room
                self.load_rooms()
        elif (self.cur_room.y > 0) and (self.cur_room.y > 1):
            print(self.cur_room.y)
            self.move_vert(-1)

    def load_rooms(self):
        '''
        first it removes all rooms but current
        then it loads rooms around the current
        use hash table of rooms params
        BUG: it does not always remove all the doors them moving up.
            Bug can be connected with update_rooms function. 
            Maybe House has two instances of cur_room.
        BUG: It is working very slow. In can be connected with used method of room creation.
        '''
        for child in self.children:
            print(child)
            if child != self.cur_room:
                self.remove_widget(child)
        if self.cur_room.up_name != None:
            room_params = get_room_params(self.cur_room.up_name)
            self.create_up_room(self.cur_room.up_name, **room_params)
            self.up_room.set_room_params(**room_params)
        if self.cur_room.down_name != None:
            room_params = get_room_params(self.cur_room.down_name)
            self.create_down_room(self.cur_room.down_name, **room_params)
            self.down_room.set_room_params(**room_params)

# rooms dictionary stores rooms properties
rooms = {"cur": {"img": "Wall.jpg", 
                 "up_name": "up", 
                 "down_name": "down"},
         "up":  {"img": "Bubbles.jpg", 
                 "up_name": "down", 
                 "down_name": "cur"},
         "down":{ "img": "2438_Love_Hina.gif", 
                 "up_name": "cur", 
                 "down_name": "up"}, 
            }#"width": None, "height" : None,

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
        self.house.create_current_room("cur")

    def update(self, dt):
        self.house.update_rooms()

    def on_touch_move(self, touch):
        if move_enabled:
            if abs(touch.dx) > abs(touch.dy): #Horisontal
                if touch.dx > 0: #right
                    print("right")
                else: #Left
                    print("left")
            else: #Vertical
                if touch.dy > 0: #move up scroll down
                    self.house.move_rooms_up(touch.dy)
                    print("move up scroll down")
                else: #move down scroll up
                    self.house.move_rooms_down(touch.dy)
                    print("move down scroll up")


class ScrollerApp(App):
    def build(self):
        game = ScrollerGame()
        game.make_rooms()
        Clock.schedule_interval(game.update, 1.0 / 20.0)
        return game


if __name__ == '__main__':
    ScrollerApp().run()
