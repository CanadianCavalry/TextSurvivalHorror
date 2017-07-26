import pyglet
import copy
import Enemies
import Parser
import StateControl
import time

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, color, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', color * 4)
        )

class DisplayWindow(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(0, 0, 0, 255), bold=True)
        )
        font = self.document.get_font()
        height = (font.ascent - font.descent) * 22 
        
        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=True, batch=batch)
        
        self.layout.x = x
        self.layout.y = y
        
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, [64, 64, 64, 255], batch)

class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), 
            dict(color=(0, 0, 0, 255), bold=True)
        )
        font = self.document.get_font()
        height = (font.ascent - font.descent)
        
        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, [200, 200, 220, 255], batch)

    def clearContents(self):
        self.document.delete_text(0, len(self.document.text))

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

class MenuButton(object):
    def __init__(self, buttonFunction, text, x, y, batch):
        self.buttonFunction = buttonFunction

        self.label = pyglet.text.Label(text, x=x, y=y, font_name='Times New Roman',font_size=22,
                                        color=(125,125,125,255), bold=True)
        self.label.anchor_x = 'center'
        self.pressed = False
        self.hover = False
        
        #load and position the sprites
        self.defaultImage = pyglet.image.load("Sprites/buttonNormal.png");
        self.defaultImage.anchor_x = self.defaultImage.width // 2
        self.defaultImage.anchor_y = self.defaultImage.height // 2
        self.hoverImage = pyglet.image.load("Sprites/buttonHighLight.png");
        self.hoverImage.anchor_x = self.hoverImage.width // 2
        self.hoverImage.anchor_y = self.hoverImage.height // 2
        self.pressedImage = pyglet.image.load("Sprites/buttonPressed.png");
        self.pressedImage.anchor_x = self.pressedImage.width // 2
        self.pressedImage.anchor_y = self.pressedImage.height // 2

        self.defaultSprite = pyglet.sprite.Sprite(self.defaultImage, x, y + 10, batch=batch)
        self.defaultSprite.scale = 0.6

    def hit_test(self, x, y):
        return (0 < x - (self.defaultSprite.x - (self.defaultSprite.width / 2)) < self.defaultSprite.width and
                0 < y - (self.defaultSprite.y - (self.defaultSprite.height / 2)) < self.defaultSprite.height)

    def delete(self):
        self.label.delete()
        
class StatsPanel(object):
    def __init__(self, batch):
        self.condition = 'Unhurt'
        self.spirit = 'Saint Like'
        self.intoxication = 'Sober'
        x = 640
        y = 325
        width = 140
        height = 200
        pad = 2
        self.border = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, [204, 0, 0, 255], batch)
        self.filler = Rectangle(x - pad + 5, y - pad + 5,
                                   x + width + pad -5, y + height + pad - 5, [0, 0, 0, 255], batch)
        
        self.labels = [
            pyglet.text.Label('Condition:\n' + self.condition, x=x+15, y=y+175, font_name='Times New Roman',font_size=16,
                                        batch=batch, color=(155,0,0,255), bold=True, multiline=True, width = width - 10),
            pyglet.text.Label('Spirit:\n' + self.spirit, x=x+15, y=y+100, font_name='Times New Roman',font_size=16,
                                        batch=batch, color=(155,0,0,255), bold=True, multiline=True, width = width - 10),
            pyglet.text.Label('Intoxication:\n' + self.intoxication, x=x+15, y=y+40, font_name='Times New Roman',font_size=16,
                                        batch=batch, color=(155,0,0,255), bold=True, multiline=True, width = width - 10)
        ]
        
    def updateStats(self, player):
        condition = player.getCondition()
        spirit = player.getSpirit()
        intoxication = player.getIntoxication()
        
        self.labels[0].text = 'Condition:\n' + condition
        self.labels[1].text = 'Spirit:\n' + spirit
        self.labels[2].text = 'Intoxication:\n' + intoxication

class EquipPanel(object):
    def __init__(self, batch):
        self.mainHand = "Empty"
        self.offHand = "Empty"
        self.armor = "None"
        x = 640
        y = 100
        width = 140
        height = 200
        pad = 2
        self.border = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, [204, 0, 0, 255], batch)
        self.filler = Rectangle(x - pad + 5, y - pad + 5,
                                   x + width + pad -5, y + height + pad - 5, [0, 0, 0, 255], batch)
        
        self.labels = [
            pyglet.text.Label('Main Hand:\n' + self.mainHand, x=x+15, y=y+165, font_name='Times New Roman',font_size=16,
                                        batch=batch, color=(155,0,0,255), bold=True, multiline=True, width = width - 10),
            pyglet.text.Label('Off Hand:\n' + self.offHand, x=x+15, y=y+105, font_name='Times New Roman',font_size=16,
                                        batch=batch, color=(155,0,0,255), bold=True, multiline=True, width = width - 10),
            pyglet.text.Label('Armor:\n' + self.armor, x=x+15, y=y+40, font_name='Times New Roman',font_size=16,
                                        batch=batch, color=(155,0,0,255), bold=True, multiline=True, width = width - 10)
        ]

    def updateEquip(self, player):
        mainHand = player.getMainHand()
        offHand = player.getOffHand()
        armor = player.getArmor()
        
        if mainHand:
            mainHand = mainHand.name
        else:
            mainHand = "Empty"
        if offHand:
            offHand = offHand.name
        else:
            offHand = "Empty"
        if armor:
            armor = armor.name
        else:
            armor = "None"
        
        self.labels[0].text = 'Main Hand:\n' + mainHand
        self.labels[1].text = 'Off Hand:\n' + offHand
        self.labels[2].text = 'Armor:\n' + armor

class Window(pyglet.window.Window):

    def __init__(self, player, *args, **kwargs):
        super(Window, self).__init__(1024, 768, caption='Text Game')

        self.newPlayer = player
        self.inMenu = False
        self.writingText = False
        self.textToWrite = ""
        
        self.startMainMenu()

    def startMainMenu(self):
        self.inMenu = True
        self.batch = pyglet.graphics.Batch()
        self.parser = Parser.Parser()
        self.player = copy.copy(self.newPlayer)
        self.state = None
        self.widgets = None
        self.focus = None
        self.buttonClick = pyglet.media.load('Sounds/UI/menuClick.mp3')
        soundtrack = pyglet.media.load('Music/Oblivion.mp3')
        self.menuSoundtrack = soundtrack.play()

        self.title = pyglet.text.Label('Welcome to Hell', x=(self.width / 2), y=(self.height - 100), anchor_x='center', anchor_y='center',
                                        font_name='Times New Roman',font_size=32, batch=self.batch, color=(155,0,0,255), bold=True)
        
        self.menuButtons = [
            MenuButton(StateControl.newGameState, 'New Game', (self.width / 2), (self.height - 225), self.batch),
            MenuButton(StateControl.loadState, 'Load Game', (self.width / 2), (self.height - 350), self.batch),
            MenuButton(StateControl.newSimulationState, 'Training', (self.width / 2), (self.height - 475), self.batch),
            MenuButton(StateControl.quit, 'Quit', (self.width / 2), (self.height - 600), self.batch)
        ]

    def startGameState(self, state):
        pyglet.clock.schedule_interval(self.updateText, 0.01)
        self.inMenu = False
        self.batch = pyglet.graphics.Batch()
        self.state = state
        self.parser.loadState(state)

        
        self.menuSoundtrack.pause()
        
        self.title = pyglet.text.Label('The Title', x=240, y=550, font_name='Times New Roman',font_size=28,
                                        batch=self.batch, color=(155,0,0,255), bold=True)

        self.disp = DisplayWindow(self.state.introText, 20, 100, self.width - 210, self.batch)
        
        self.widgets = [
            TextWidget('', 20, 30, self.width - 210, self.batch)
        ]
        
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.set_focus(self.widgets[0])
        
        self.statsDisplay = StatsPanel(self.batch)
        self.equipDisplay = EquipPanel(self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()
        #We have to manually draw all menu button labels because pyglet 
        #will randomly decide not to include them in the batch. Thanks, pyglet
        if (self.inMenu):
            for button in self.menuButtons:
                button.label.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.inMenu:
            for button in self.menuButtons:
                if button.hit_test(x, y):
                    button.defaultSprite.image = button.hoverImage
                    if not button.hover:
                        pyglet.media.load('Sounds/UI/menuHover.wav').play()
                        button.hover = True
                else:
                    button.defaultSprite.image = button.defaultImage
                    button.pressed = False
                    button.hover = False
            
        if self.widgets:
            for widget in self.widgets:
                if widget.hit_test(x, y):
                    self.set_mouse_cursor(self.text_cursor)
                    break
            else:
                self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.inMenu:
            for button in self.menuButtons:
                if button.hit_test(x, y):
                    button.defaultSprite.image = button.pressedImage
                    button.pressed = True

        if self.widgets:
            for widget in self.widgets:
                if widget.hit_test(x, y):
                    self.set_focus(widget)
                    break
            else:
                self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.inMenu:
            if self.menuButtons:    
                for button in self.menuButtons:
                    if button.hit_test(x, y) and button.pressed:
                        self.buttonClick.play()
                        state = button.buttonFunction(self.player)
                        self.startGameState(state)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            if self.state.player.health < 1:
                self.startMainMenu()
                return
            
            userInput = self.widgets[0].document.text
            self.parsePlayerInput(userInput)
            self.widgets[0].clearContents()
            
            self.statsDisplay.updateStats(self.state.player)
            self.equipDisplay.updateEquip(self.state.player)
        elif self.widgets and (not self.focus == self.widgets[0]):
            self.set_focus(self.widgets[0])


    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)
            
    def on_close(self):
        StateControl.quit()
            
    def parsePlayerInput(self, userInput):
        print "Tracking Enemies"
        actingEnemies = self.player.getActingEnemies()
        pursuingEnemies = self.player.getPursuingEnemies()
        
        enemyDestination = self.player.currentLocation
        
        print "Player taking action"
        turnResult = self.parser.parse(userInput)
        try:
            resultString,turnPassed = turnResult
        except ValueError:
            resultString = turnResult
            turnPassed = False
            
        gameOver = self.checkGameOver()
        if gameOver:
            resultString += gameOver
            self.updateTextBox(resultString)
            return
        
        if turnPassed:
            #Perform enemy actions
            if (self.parser.command == "go") and (actingEnemies):
                resultString = "You turn to run...\n" + Enemies.enemyAction(self.state.player, actingEnemies) + "\n" + resultString
            else:
                resultString += "\n\n" + Enemies.enemyAction(self.state.player, actingEnemies)
            self.state.player.beginTurn()
            
            gameOver = self.checkGameOver()
            if gameOver:
                resultString += gameOver
                self.updateTextBox(resultString)
                return
                
            if pursuingEnemies:
                resultString += Enemies.enemyMovement(pursuingEnemies, enemyDestination, self.player)
            
        self.updateTextBox(resultString)

    def updateTextBox(self, text):
        self.disp.document.delete_text(0, len(self.disp.document.text))
        self.writingText = True
        self.textToWrite = text

    def checkGameOver(self):
        if self.state.player.health < 1:
            return "\nYou have died...\nPress enter to return to the main menu."
        return False

    def updateText(self, dt):
        if self.writingText:
            if len(self.textToWrite) > 0:
                self.disp.document.text += self.textToWrite[:2]
                self.textToWrite = self.textToWrite[2:]
            else:
               self.writingText = False