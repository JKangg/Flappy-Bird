import random
from libdw import sm
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label, CoreLabel
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition


flydown = "flydown.png"
flyup = "flyup.png"


        
class Game(FloatLayout):
    def __init__(self):
        super().__init__()

        self.birdy = Bird()
        self.add_widget(self.birdy)
        self.birdy.size_hint = (50/Window.size[0], 50/Window.size[1])
        self.birdy.pos_hint = {'x': 0.5, 'y': 0.5}
        self.birdy_windowpos = [self.birdy.pos_hint['x']*Window.size[0], self.birdy.pos_hint['y']*Window.size[1]]
        
        self.resetbtn = ResetBtn()
        self.add_widget(self.resetbtn)
        self.resetbtn.size_hint = (0.15, 0.06)
        self.resetbtn.pos_hint = {'x': 0.8, 'y': 0.90}
    
        
        self.walls = []
        self.current_bottom_wall = None
        self.current_top_wall = None
        self.add_random_wall()
        
        self.score = 0
        self.score_label = CoreLabel(text = "Score:" + str(self.score), font_size = 30, color=(1,0.7,0,0.8))
        self.score_label.refresh()
        with self.canvas:
            self.score_instruction = Rectangle(texture=self.score_label.texture, pos= (20,Window.size[1]-50), size=self.score_label.texture.size)
            
        self.high_score = 0
        
        self.birdy_update = Clock.schedule_interval(self.birdy.update, 0.03)
        self.wall_update = Clock.schedule_interval(self.update, 0)
    
        
    def add_bottom_wall(self, pos, size):
        with self.canvas:
            self.rect = Rectangle(source='Bottom wall.png',pos=pos, size=size)

        self.walls.append(self.rect)
        self.current_bottom_wall = self.rect
        
    def add_top_wall(self, pos, size):
        with self.canvas:
            self.rect = Rectangle(source='Top wall.png', pos=pos, size=size)

        self.walls.append(self.rect)
        self.current_top_wall = self.rect
        
    # Add wall at random height
    def add_random_wall(self):
        height = random.uniform(100, Window.size[1]-300)
        self.add_bottom_wall((0.9*Window.size[0], 0), (50, height))
        self.add_top_wall((0.9*Window.size[0], height+200), (50, Window.size[1]-height-200))
        
    def game_speed(self):
        bds = 0
        if self.score%5==0:
            bds= bds+self.score/5
        else:
            bds = bds+self.score//5
        bs = bird_stateSM(bds)
        bs.start()
        return bs.step(self.score)
    
    
    # Run updates
    def update(self, dt):
        self.score_instruction.pos = (20,Window.size[1]-50)
        self.birdy_windowpos = [self.birdy.pos_hint['x']*Window.size[0], self.birdy.pos_hint['y']*Window.size[1]]
        
        self.k = self.game_speed() + App.userspeed*20
        # move the wall
        for wall in self.walls:
            wall.pos = (wall.pos[0]-self.k*dt, wall.pos[1])
            
        # Remove wall from the list after it leaves screen
        self.walls = [i for i in self.walls if i.pos[0] >= -50]

        #add new wall when wall pass 0.48 of the window
        if self.walls[-1].pos[0] <= 0.48*Window.size[0]:
            self.add_random_wall()
            self.score +=1
        self.new_score()
        
        self.gameover()

    def new_score(self):
        self.score_label.text = "Score: " + str(self.score)
        self.score_label.refresh()
        self.score_instruction.texture = self.score_label.texture
        self.score_instruction.size = self.score_label.texture.size
        
    def get_high_score(self):
        if self.high_score < self.score:
            self.high_score = self.score
        else:
            return self.high_score

    def gameover(self):
        #when bird within the width of wall
        if self.current_bottom_wall.pos[0] <=(self.birdy_windowpos[0]+25) and (self.birdy_windowpos[0] + 25)<= self.current_bottom_wall.pos[0] + 50:
            #i bird hit the bottom wall
            if (self.current_bottom_wall.pos[1] + self.current_bottom_wall.size[1]) > (self.birdy_windowpos[1]+8):
                self.get_high_score()
                self.label = Label(text = "Game Over\n"+'Score:'+str(self.score)+'\n'+'High Score:'+str(self.high_score), halign = 'center', valign = 'center', font_size = 60)
                self.add_widget(self.label)
                self.label.size_hint = (0.5, 0.2)
                self.label.pos_hint = {'x': 0.25, 'y': 0.5}
                self.canvas.remove(self.score_instruction)
                Clock.unschedule(self.birdy_update)
                Clock.unschedule(self.wall_update)
            # if bird hit top wall
            elif self.current_top_wall.pos[1] < (self.birdy_windowpos[1]+60):
                self.get_high_score()
                self.label = Label(text = "Game Over\n"+'Score:'+str(self.score)+'\n'+'High Score:'+str(self.high_score), halign = 'center', valign = 'center', font_size = 60)
                self.add_widget(self.label)
                self.label.size_hint = (0.5, 0.2)
                self.label.pos_hint = {'x': 0.25, 'y': 0.5}
                self.canvas.remove(self.score_instruction)
                Clock.unschedule(self.birdy_update)
                Clock.unschedule(self.wall_update)
        # if bird out of zone        
        elif self.birdy_windowpos[1]+10 <= 0: 
            self.get_high_score()
            self.label = Label(text = "Game Over\n"+'Score:'+str(self.score)+'\n'+'High Score:'+str(self.high_score), halign = 'center', valign = 'center', font_size = 60)
            self.add_widget(self.label)
            self.label.size_hint = (0.5, 0.2)
            self.label.pos_hint = {'x': 0.25, 'y': 0.5}
            self.canvas.remove(self.score_instruction)
            Clock.unschedule(self.birdy_update)
            Clock.unschedule(self.wall_update)
            
        elif self.birdy_windowpos[1]+50 >= Window.size[1]:
            self.get_high_score()
            self.label = Label(text = "Game Over\n"+'Score:'+str(self.score)+'\n'+'High Score:'+str(self.high_score), halign = 'center', valign = 'center', font_size = 60)
            self.add_widget(self.label)
            self.label.size_hint = (0.5, 0.2)
            self.label.pos_hint = {'x': 0.25, 'y': 0.5}
            self.canvas.remove(self.score_instruction)
            Clock.unschedule(self.birdy_update)
            Clock.unschedule(self.wall_update)

    def reset(self):
        self.clear_widgets()
        for wall in self.walls:
            del wall
        del self.current_bottom_wall
        del self.current_top_wall
        self.canvas.clear()
        Clock.unschedule(self.birdy_update)
        Clock.unschedule(self.wall_update)
        
        self.birdy = Bird()
        self.add_widget(self.birdy)
        self.birdy.size_hint = (50/Window.size[0], 50/Window.size[1])
        self.birdy.pos_hint = {'x': 0.5, 'y': 0.5}
        self.birdy_windowpos = [self.birdy.pos_hint['x']*Window.size[0], self.birdy.pos_hint['y']*Window.size[1]]
        
        self.resetbtn = ResetBtn()
        self.add_widget(self.resetbtn)
        self.resetbtn.size_hint = (0.15, 0.06)
        self.resetbtn.pos_hint = {'x': 0.8, 'y': 0.90}
        
        self.walls = []
        self.current_bottom_wall = None
        self.current_top_wall = None
        self.add_random_wall()
        
        self.score = 0
        self.score_label = CoreLabel(text = "Score:" + str(self.score), font_size = 30, color=(1,0.7,0,0.8))
        self.score_label.refresh()
        with self.canvas:
            self.score_instruction = Rectangle(texture=self.score_label.texture, pos= (20,Window.size[1]-50), size=self.score_label.texture.size)
        
        self.birdy_update = Clock.schedule_interval(self.birdy.update, 0.03)
        self.wall_update = Clock.schedule_interval(self.update, 0)

        
class Bird(Image):
    def __init__(self):
        super().__init__(source = flyup)
        self.fly = 0.5
        self.fall = 0

    def on_touch_down(self, touch):
        self.fly += 0.15
        self.source = flyup
        self.fall = 0

    def update(self, dt):
        self.fall += 1
        self.fly += -0.01

        self.pos_hint = {'x': 0.5, 'y': self.fly}
        if self.source != flydown and self.fall == 10:
            self.source = flydown

            
class ResetBtn(Button):
    def __init__(self):
        super().__init__(text = "Reset", halign = "center", valign = "center")

    def on_release(self):
        super().on_release()
        self.parent.reset()
        
    

class bird_stateSM(sm.SM):
    def __init__(self,current_state):
        self.start_state = current_state
    def get_next_values(self, state, inp):
        if state == 0:
            if inp <5:
                next_state = 0
                output = 140
            else:
                next_state = 1
                output = 180
            return next_state, output
        elif state == 1:
            if inp <10:
                next_state = 1
                output = 180
            else:
                next_state = 2
                output = 220
            return next_state, output
        elif state == 2:
            if inp <15:
                next_state = 2
                output = 220
            else:
                next_state = 3
                output = 280
            return next_state, output
        elif state == 3:
            if inp <20:
                next_state = 3
                output = 280
            else:
                next_state = 4
                output = 360
            return next_state, output
        elif state == 4:
            if inp <30:
                next_state = 4
                output = 360
            else:
                next_state = 5
                output = 460
            return next_state, output
        elif state == 5:
            if inp <50:
                next_state = 5
                output = 460
            else:
                next_state = 5
                output = 600
            return next_state, output
            

## Screens            
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Welcome", font_size=50))
        
        buttonlayout = BoxLayout(size_hint_y=0.5)

        # Create buttons with a custom text
        self.option = Button(text='Options')
        self.option.size_hint = (0.5, 0.5)
        self.option.bind(on_release=self.go_to_options)
        buttonlayout.add_widget(self.option)
        
        self.start = Button(text='Start')
        self.start.size_hint = (0.5, 0.5)
        self.start.bind(on_release=self.start_game)
        buttonlayout.add_widget(self.start)
        
        layout.add_widget(buttonlayout)
        # And add the layout to the Screen
        self.add_widget(layout)

    def go_to_options(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'option'
        
    def start_game(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'game'

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical')
        top_layout = BoxLayout(orientation='horizontal')
        middle_layout = BoxLayout(orientation='horizontal')
        back_layout = BoxLayout(orientation='horizontal',size_hint_y=0.3)
        
        self.speedcontrol = Slider(min=1, max =5)
   
        top_layout.add_widget(Label(text='Game Speed'))
        top_layout.add_widget(self.speedcontrol)

        middle_layout.add_widget(Label(text='Speed'))
        self.speedvalue = Label(text='1')
        middle_layout.add_widget(self.speedvalue)

        self.speedcontrol.bind(value=self.on_value)
        
        self.save = Button(text='Save')
        self.save.bind(on_release=self.switch_back)
        back_layout.add_widget(self.save)
        
        main_layout.add_widget(top_layout)
        main_layout.add_widget(middle_layout)
        main_layout.add_widget(back_layout)
        self.add_widget(main_layout)
        
    def on_value(self, instance, speed):
        self.speedvalue.text = "{}".format(int(speed))
        App.userspeed = int(self.speedvalue.text)
        
    def switch_back(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Welcome'
        
class GameScreen(Screen):
    def on_enter(self):
        g = Game()
        self.add_widget(g)


        
class BirdApp(App):
    def build(self):
        App.userspeed = 0
        screen_manager = ScreenManager()
        screen_manager.add_widget(WelcomeScreen(name = 'Welcome'))
        screen_manager.add_widget(OptionsScreen(name = 'option'))
        screen_manager.add_widget(GameScreen(name = 'game'))
        return screen_manager

if __name__ == "__main__":
    BirdApp().run()