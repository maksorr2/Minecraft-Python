# напиши здесь код основного окна игры
from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
#from pandac.PandaModules import WindowProperties
from hero import Hero

 
class Game(ShowBase):
    text = "Minecraft Beta v0.1"
    Object = OnscreenText(text=text, pos=(-1.5, 0.90), scale=0.07,
                          fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                          mayChange=0)
    def __init__(self):
        ShowBase.__init__(self)
        #props = WindowProperties()
        #props.setCursorHidden(True)
        self.land = Mapmanager()
        self.camLens.setFov(90)
        self.land.loadLand("land_empty.txt")
        self.land.setupSky()
        self.hero = Hero((0, 3, 1), self.land)
game = Game()
game.run()