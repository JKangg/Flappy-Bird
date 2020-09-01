# Birdy Game
## How to Play
* When the game is started, you will be brought to the welcome screen. 
* Press the _Option button_ to select the game speed. To start playing, press the start button.
* Control the bird such that it will be flying between the bottom and top wall. By default, the bird will be flying downwards. When the mouse is clicked, the bird will fly up before flying down again almost immediately.
* The game will start with a slower speed and it will increases as time pass by.
* The game is over once the bird hits the wall or if it flys out of the zone. The player's score and high score will be displayed.


## About the code
1. **Imports**
    * import random
    * from kivy.app import App
    * from kivy.core.window import Window
    * from kivy.uix.widget import Widget
    * from kivy.uix.label import Label, CoreLabel
    * from kivy.uix.button import Button
    * from kivy.uix.slider import Slider
    * from kivy.uix.floatlayout import FloatLayout
    * from kivy.uix.boxlayout import BoxLayout
    * from kivy.uix.image import Image
    * from kivy.clock import Clock
    * from kivy.graphics import Rectangle, Color
    * from kivy.uix.screenmanager import ScreenManager, Screen
    * from kivy.uix.screenmanager import SlideTransition
    * from libdw import sm


2. **Screens**
    * WelcomeScreen
        * This screen will be shown when the game is first launched.
    * OptionsScreen
        * This screen will allow the player to choose the game speed.
    * GameScreen
        * Upon entering this screen, the game will start.


3. **Main Game** - _Game, Bird, ResetBtn, bird_stateSM class_
    * The **Game class** is a FloatLayout. Inside, there are methods to add the wall, adjust the game speed and to update scores and positions. The _gameover method_ will be called once the bird collide with the wall or when it flies out of the screen and the game will end. The _reset method_ allows the player to reset and start a new game. 
    
        The walls are made using canvas and Rectangle. The _add_random_wall method_ will add a new wall at random position once the previous wall is at 48% of the window's width. This is when the wall passes the bird. In this game, the wall will be moving from the right to the left. A Clock.schedule_interval will call the _update method_ to update the position of the wall. If the bird collides with the wall,the game stops and will unschedule all scheduled intervals.
            
        Everytime the bird passes the wall successfully, the score will increase by 1.
        
        The _game_speed method_ will adjust the speed according to the states from bird_stateSM class, which will be explained below.

    
    * **Bird class** inherits from Image class. A Clock.schedule_interval will call the _update method_ of the bird class to update the position of the bird. Also, when the mouse is clicked, it will change to an image of the bird flying up, before changing back to the image of the bird flying down.
    
        The _on_touch_down method_ sets the height of the bird to be higher for the instance when the mouse is clicked.

    * **ResetBtn class** is a button which has a _on_release method_ to reset the game.

    * **bird_stateSM class** inherits from the SM class. It takes in the state of the bird and based on its state, it ouputs the speed of the game. The state starts from 0 and will increase to 5 as the game progress and the player score increase.