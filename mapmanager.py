# напиши здесь код создания и управления картой
import pickle
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
import os
import os.path
summa = 0
save_text = 'Save is:'
class Mapmanager():
    def __init__(self):
        self.save_obj = OnscreenText(text=save_text, pos=(1, 0.90), scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)
        self.model = 'blocks/grass_block.glb' # генерация
        #self.texture = 'block (1).png'
        self.skybox = 'skybox/skybox.egg'
        #self.colors = [(0.5, 0.3, 0.0, 1),(0.2, 0.2, 0.3, 1), (0.5, 0.5, 0.2, 1), (0.0, 0.6, 0.0, 1), (0.0, 0.7, 0.7, 0.8)]
        self.startNew()
        self.addBlock((0,10, 0))
    def startNew(self):
        self.land = render.attachNewNode("land") 
    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        #self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        #self.color = self.getColor(position[2])
        #self.block.setColor(self.color)
        self.block.setTag("block", str(position))
        self.block.reparentTo(self.land)
    #def getColor(self, z):
    #    if z < len(self.colors):
    #        return self.colors[z]
    #    else:
    #        return self.colors[len(self.colors) - 1]
    def clearLand(self):
        self.land.removeNode()
        self.startNew()
    def loadLand(self, filename):
        self.clearLand()
        with open(filename) as file:
            y = 0 
            for line in file:
                x= 0 
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
    def isEmpty(self, position):
        blocks = self.findBlocks(position)
        if blocks:
            return False
        else:
            return True
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
           z += 1
        return (x, y, z)

    def findBlocks(self, position):
        return self.land.findAllMatches("=block=" + str(position))
    
    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()
    def buildBlock(self, position):
        x, y, z = position
        new = self.findHighestEmpty(position)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        position = x, y, z - 1
        for block in self.findBlocks(position):
            block.removeNode()
        
    def saveMap(self):
        global summa

        blocks = self.land.getChildren()
        if summa < 5:
            summa += 1
            save_obj = 'my_map' + str(summa)  + '.dat' 
            with open(save_obj, 'wb') as s_m:
                pickle.dump(len(blocks), s_m)
                for block in blocks:
                    x, y, z = block.getPos()
                    pos = (int(x), int(y), int(z))
                    pickle.dump(pos, s_m)

    def loadMap(self, map):
        self.clearLand()
        with open(map, 'rb') as l_m:
            length = pickle.load(l_m)
            for _ in range(length):
                pos = pickle.load(l_m)
                self.addBlock(pos)
    #def loadModels(self):
    #    self.grass_block = loader.loadModel('blocks/grass_block.glb')
    #    self.glass_block = loader.loadModel('blocks/glass_block.glb')
    #    self.brick_block = loader.loadModel('blocks/brick_block.glb')
    #    self.error = loader.loadModel('blocks/error_block.glb')
    #    self.just_sphere = loader.loadModel('blocks/ball1.glb') # no hitbox
    def loadSaves(self, save):
        if save == 'save_1':
            if os.path.isfile('C:\Users\Семья\Desktop\Minecraft\my_map1.dat'):
                self.loadMap('my_map1.dat')
                self.setupSky()

            return True
        elif save == 'save_2':
            if os.path.isfile('C:\Users\Семья\Desktop\Minecraft\my_map2.dat'):
                self.loadMap('my_map2.dat')
                self.setupSky()

            return True
        elif save == 'save_3':
            if os.path.isfile('C:\Users\Семья\Desktop\Minecraft\my_map3.dat'):
                self.loadMap('my_map3.dat')
                self.setupSky()

            return True
        elif save == 'save_4':
            if os.path.isfile('C:\Users\Семья\Desktop\Minecraft\my_map4.dat'):
                self.loadMap('my_map4.dat')
                self.setupSky()

            return True
        elif save == 'save_5':
            if os.path.isfile('C:\Users\Семья\Desktop\Minecraft\my_map5.dat'):
                self.loadMap('my_map5.dat')
                self.setupSky()

            return True
        else:
            return False
    #def changeBlock(self, block):
    #    self.type_model = block
    def changeSaves(self, map):
        self.save = map
        if self.loadSaves(self.save):
            self.save_obj.setText('Save is: ' + self.save)
        else:
            self.save_obj.setText('Save_Error')
    def setupSky(self):
        skybox = loader.loadModel(self.skybox)
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(self.land)


