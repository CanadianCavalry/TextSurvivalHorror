import pyglet
import copy
import Enemies
import Parser
import StateControl

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
                                        batch=batch, color=(155,0,0,255), bold=True)
        self.label.anchor_x = 'center'
        
        height = 30
        width = self.label.content_width
        pad = 3
        rectX = x - (width / 2)

        self.rectangle = Rectangle(rectX - pad, y - pad, 
                                   rectX + width + pad, y + height + pad, [96, 96, 96, 255], batch)
        
    def hit_test(self, x, y):
        return (0 < x - (self.label.x - (self.label.content_width / 2)) < self.label.content_width and
                0 < y - self.label.y < self.label.content_height)
        
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
        super(Window, self).__init__(800, 600, caption='Text Game')
        
        self.newPlayer = player
        
        self.startMainMenu()

    def startMainMenu(self):
        self.batch = pyglet.graphics.Batch()
        self.parser = Parser.Parser()
        self.player = copy.copy(self.newPlayer)
        self.state = None
        self.widgets = None
        self.focus = None
        soundtrack = pyglet.media.load('Music/Oblivion.mp3')
        self.menuSoundtrack = soundtrack.play()
        
        self.menuButtons = [
            MenuButton(StateControl.newGameState, 'New Game', (self.width / 2), 450, self.batch),
            MenuButton(StateControl.loadState, 'Load Game', (self.width / 2), 350, self.batch),
            MenuButton(StateControl.newSimulationState, 'Combat Simulator', (self.width / 2), 250, self.batch),
            MenuButton(StateControl.quit, 'Quit', (self.width / 2), 150, self.batch)
        ]

    def startGameState(self, state):
        self.batch = pyglet.graphics.Batch()
        self.state = state
        self.parser.loadState(state)
        #intro = "September 3rd, 2015. You wake up around 10 a.m. as usual, and have already ate and freshened up for the day. You recall that the new Director of the Rehab House - Father Malachi - is going to be giving a talk outlining why he and his associates have implemented new policies in House management, and will be taking questions afterwards. The architect of many new regulations you find draconian and invasive, this will be the first time the director has made an appearance to you and the other residents. You plan to attend the talk to get a better idea of the nature of the man who will control much of your life in the forseeable future. The talk is taking place in fifteen minutes, and is located in the auditorium of the old church wing. You recall that the easiest way to get there is to simply head north through the residents wing, past the courtyard, until you reach the auditorium.<paragraph break> You are currently located in your quarters in the resident wing of the house. Like virtually every other service offered by the house, they spared no expense in providing the residents with a fine place to live. Your quarters are large, fully furnished, and even come with a personal computer and a large plasma TV. Right now, you are craving some alcohol. This is surprising as the new medication, 'Rejuvinax', that father Malachi has been providing you with has been practically miraculous in controlling your cravings, to the point of you hardly being aware of them.It's an exquisite longing that is more pronounced than anything you've felt since your time here. Odd. Why would you b experiencing symptoms like this now, completely out of nowhere?"
        
        self.menuSoundtrack.pause()
        
        self.title = pyglet.text.Label('Effluvium', x=240, y=550, font_name='Times New Roman',font_size=28,
                                        batch=self.batch, color=(155,0,0,255), bold=True)

        self.disp = DisplayWindow('Intro goes here', 20, 100, self.width - 210, self.batch)
        
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

    def on_mouse_motion(self, x, y, dx, dy):
        if self.widgets:
            for widget in self.widgets:
                if widget.hit_test(x, y):
                    self.set_mouse_cursor(self.text_cursor)
                    break
            else:
                self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.widgets:
            for widget in self.widgets:
                if widget.hit_test(x, y):
                    self.set_focus(widget)
                    break
            else:
                self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)
        
        if self.menuButtons:    
            for button in self.menuButtons:
                if button.hit_test(x, y):
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
        actingEnemies = self.player.getActingEnemies()
        
        enemyDestination = self.player.currentLocation
        pursuingEnemies = self.player.getPursuingEnemies()
        
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
                Enemies.enemyMovement(pursuingEnemies, enemyDestination)
            
        self.updateTextBox(resultString)

    def updateTextBox(self, text):
        self.disp.document.text = text

    def checkGameOver(self):
        if self.state.player.health < 1:
            return "\nYou have died...\nPress enter to return to the main menu."
        return False
        