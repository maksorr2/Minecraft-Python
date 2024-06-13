from mapmanager import *
from panda3d.core import TransparencyAttrib
from pandac.PandaModules import WindowProperties
from direct.gui.OnscreenImage import OnscreenImage

# управление
change_view = 'v' # смена лица 
forward = 'w' # шаг вперёд
left = 'a' # шаг влево
right = 'd' # шаг вправо
back = 's' # шаг назад
turn_right = 'h' # поворот вправо
turn_left = 'g' # поворот налево
up = 'e' # вверх
down = 'r' # вниз 
buildBlock = 'b' # построить блок
destroyBlock = 'z' # уничтожить блок
saveMap = 'c' # сохранить карту (бинарный тип)
loadMap = 'l' # загрузить карту (бинарный тип)
listMap = 'm' # список сохранений 
listBlocks = 'm'
save_1 = '1' # трава ( по умолчанию )
save_2 = '2' # стекло 
save_3 = '3' # кирпичи
save_4 = '4' # ошибка жизни
save_5 = '5' # сфера



class Hero():
    def __init__(self, position, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(position)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.captureMouse()
        self.get_events()
        self.cross = OnscreenImage(image='crosshairs.png', pos=(0, 0, 0), scale=0.05)
        self.cross.setTransparency(TransparencyAttrib.MAlpha)
        self.mode = False

        taskMgr.add(self.update, 'update')
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        position = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-position[0], -position[1], -position[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def get_events(self):
        base.accept(change_view, self.changeView)
        base.accept(back, self.back)
        base.accept(left, self.left)
        base.accept(right, self.right)
        base.accept(forward, self.forward)
        base.accept(up, self.up)
        base.accept(up +'-repeat', self.up)
        base.accept(down, self.down)
        base.accept(down +'-repeat', self.down)
        base.accept(saveMap, self.land.saveMap)
        base.accept(loadMap, self.land.loadMap)
        base.accept(turn_right, self.turn_right)
        base.accept(turn_right +'-repeat', self.turn_right)
        base.accept(turn_left, self.turn_left)
        base.accept(turn_left +'-repeat', self.turn_left)
        base.accept(buildBlock, self.build)
        base.accept(destroyBlock, self.destroy)

        base.accept(save_1, self.land.changeSaves, ['save_1'])
        base.accept(save_2, self.land.changeSaves, ['save_2'])
        base.accept(save_3, self.land.changeSaves, ['save_3'])
        base.accept(save_4, self.land.changeSaves, ['save_4'])
        base.accept(save_5, self.land.changeSaves, ['save_5'])

        #base.accept(listBlocks, self.land.changeSaves)
        
    def update(self, task):

        dt = globalClock.getDt()


        x_movement = 0
        y_movement = 0
        z_movement = 0

        camera.setPos(
            camera.getX() + x_movement,
            camera.getY() + y_movement,
            camera.getZ() + z_movement,
        )
        md = base.win.getPointer(0)
        mouseX = md.getX()
        mouseY = md.getY()

        mouseChangeX = mouseX - self.lastMouseX
        mouseChangeY = mouseY - self.lastMouseY

        self.cameraSwingFactor = 10

        currentH = base.camera.getH()
        currentP = base.camera.getP()

        base.camera.setHpr(
            currentH - mouseChangeX * dt * self.cameraSwingFactor,
            min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
            0
        )

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY

        return task.cont
    
    def captureMouse(self):

        md = base.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(properties)

    def changeView(self):
        if self.cameraOn is True:
            self.cameraUp()
            self.changeMode()
        else:
            self.cameraBind()
            self.changeMode()

    def changeMode(self):
       if self.mode:
           self.mode = False
       else:
           self.mode = True

    def just_move(self, angle):
        position = self.look_at(angle)
        self.hero.setPos(position)
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            # перед нами свободно. Возможно, надо упасть вниз:
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            # перед нами занято. Если получится, заберёмся на этот блок:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    

    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        return from_x + dx, from_y + dy, from_z
    
    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
           return (0, -1)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def back(self):
        angle = (self.hero.getH() + 180 % 360)
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90 % 360)
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270 % 360)
        self.move_to(angle)

    def forward(self):
        angle = (self.hero.getH() % 360)
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)
        

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)


    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)


    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)



