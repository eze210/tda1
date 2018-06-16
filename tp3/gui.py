from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooser, FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from game import *


class StartButton(Button):

    def __init__(self, **kwargs):
        super(StartButton, self).__init__(**kwargs)

    def on_press(self):
        self.parent.startGame()


class ShipButton(Button):

    def __init__(self, ship, game, **kwargs):
        super(ShipButton, self).__init__(**kwargs)
        self.ship = ship
        self.game = game

    def on_press(self):
        super(ShipButton, self).on_press()
        self.game.selectRow(self.ship.identifier)
        self.parent.update()


class LeftPannel(GridLayout):
    def __init__(self, **kwargs):
        super(LeftPannel, self).__init__(**kwargs)
        self.cols = 2

        self.textinput = TextInput(text='1', input_filter='int')
        self.add_widget(Label(text='Número de armas:'))
        self.add_widget(self.textinput)

        playerClassesNames = {
            'dyn': 'Dinámico',
            'gr1': 'Grido, variante 1',
            'gr2': 'Grido, variante 2',
            'gr3': 'Grido, variante 3'
        }

        for num, playerClass in enumerate(PlayerClasses):
            myCheckBox1 = CheckBox(size_hint_y=5);
            myCheckBox1.active = (num == 0)
            myCheckBox1.group = 'group'
            myCheckBox1.color = (1, 1, 1, 1)
            myCheckBox1.value = True
            self.add_widget(myCheckBox1)
            self.add_widget(Label(size_hint_y=5, text=playerClassesNames[playerClass]))

    def getNumberOfGuns(self):
        return int(self.textinput.text)

    def getPlayerClass(self):
        return DinamicoMissilePlayer


class ShipLabel(Label):

    def __init__(self, ship, game, **kwargs):
        super(ShipLabel, self).__init__(**kwargs)
        self.ship = ship
        self.game = game
        self.totalHealth = ship.health

    def updateHealth(self):
        self.text = "Vida restante:\n{} de {}".format(self.ship.health, self.totalHealth)


class GridView(GridLayout):

    def __init__(self, game, **kwargs):
        super(GridView, self).__init__(**kwargs)
        self.game = game
        self.buttons = {}
        self.labels = []
        ships = game.shipPlayer.getShips()
        self.rows = len(ships)
        for ship in ships:
            label = ShipLabel(ship, game, halign='center')
            label.updateHealth()
            self.add_widget(label)
            self.labels.append(label)
            for turn, d in enumerate(ship.damageList):
                if turn not in self.buttons:
                    self.buttons[turn] = []

                button = ShipButton(ship, game, text="{}".format(d))
                self.add_widget(button)
                self.buttons[turn].append(button)
        self.update()

    def update(self):
        currentTurn = self.game.getCurrentTurn()
        for turn, buttons in self.buttons.items():
            for button in buttons:
                if turn is currentTurn % len(self.buttons):
                    button.disabled = (button.ship.health == 0)
                else:
                    button.disabled = True

        for label in self.labels:
            label.updateHealth()


class MyFileChooser(FileChooserIconView):

    def __init__(self, **kwargs):
        super(MyFileChooser, self).__init__(**kwargs)
        self.bind(selection=self.selectFile)

    def selectFile(self, chooser, fileName):
        self.parent.loadFile(fileName[0])


class GameView(GridLayout):

    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)
        self.setSetupView()

    def setSetupView(self):
        self.cols = 2
        self.spacing = [30, 0]

        self.add_widget(Label(text='PARÁMETROS', bold=True))
        self.add_widget(Label(text='SELECCIONE UN ARCHIVO', bold=True))

        self.leftPannel = LeftPannel(size_hint_y=10)
        self.add_widget(self.leftPannel)

        self.chooser = MyFileChooser(path=".", size_hint_x=2)
        self.add_widget(self.chooser)

    def setGridView(self):
        self.gridView = GridView(self.game)
        self.add_widget(self.gridView)

    def loadFile(self, fileName):
        numberOfGuns = self.leftPannel.getNumberOfGuns()
        self.game = loadGame(fileName, numberOfGuns, PlayerClasses['dyn'])
        self.clear_widgets()
        self.setGridView()


class GameApp(App):

    def __init__(self):
        App.__init__(self)

    def build(self):
        return GameView()

if __name__ == '__main__':
    GameApp().run()
