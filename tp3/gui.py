from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooser, FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

import game

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
        self.parent.parent.update()


class PlayerCheckBox(CheckBox):

    def __init__(self, playerClass, **kwargs):
        super(PlayerCheckBox, self).__init__(**kwargs)
        self.playerClass = playerClass
    
    def on_active(self, selfAgain, isActive):
        super(PlayerCheckBox, self).on_active(selfAgain, isActive)

        if isActive:
            self.parent.playerClass = self.playerClass


class LeftPannel(GridLayout):
    def __init__(self, **kwargs):
        super(LeftPannel, self).__init__(**kwargs)
        self.cols = 2

        self.textinput = TextInput(text='1', input_filter='int')
        self.add_widget(Label(text='Número de armas:', size_hint_x=4))
        self.add_widget(self.textinput)

        playerClassesNames = {
            'dyn': 'Dinámico',
            'gr1': 'Grido, variante 1',
            'gr2': 'Grido, variante 2',
            'gr3': 'Grido, variante 3'
        }

        for num, playerClass in enumerate(game.players.PlayerClasses):
            checkBox = PlayerCheckBox(playerClass, size_hint_y=5)
            checkBox.group = 'group'
            checkBox.color = (1, 1, 1, 1)
            checkBox.value = True
            self.add_widget(checkBox)
            self.add_widget(Label(size_hint_y=5, text=playerClassesNames[playerClass]))
            if num == 0:
                checkBox.active = True
                self.playerClass = playerClass
            else:
                checkBox.active = False

    def getNumberOfGuns(self):
        return int(self.textinput.text)

    def getPlayerClass(self):
        return self.playerClass


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
        nextShot = self.game.calculateNextShot()
        for column, buttons in self.buttons.items():
            for button in buttons:
                if column is currentTurn % len(self.buttons):
                    button.disabled = (button.ship.health == 0)
                    if button.ship.identifier is nextShot:
                        button.color = [0, 1, 0.2, 1]
                else:
                    button.disabled = True

        for label in self.labels:
            label.updateHealth()


class StatusView(GridLayout):

    def __init__(self, game, **kwargs):
        super(StatusView, self).__init__(**kwargs)
        self.game = game
        self.rows = 2
        self.add_widget(Label(text='PUNTOS ACUMULADOS', halign='center'))
        self.add_widget(Label(text='TURNO ACTUAL', halign='center'))
        self.add_widget(Label(text='LANZADERAS USADAS\nEN ESTE TURNO', halign='center'))
        self.pointsLabel = Label()
        self.turnLabel = Label()
        self.gunsLabel = Label()
        self.add_widget(self.pointsLabel)
        self.add_widget(self.turnLabel)
        self.add_widget(self.gunsLabel)
        self.update()

    def update(self):
        self.turnLabel.text = '{}'.format(self.game.getCurrentTurn())
        self.pointsLabel.text = '{}'.format(self.game.shipPlayer.points)
        self.gunsLabel.text = '{}'.format(self.game.gunsUsedInTheCurrentTurn)


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
        self.cols = 1

        self.statusView = StatusView(self.game)
        self.add_widget(self.statusView)

        self.gridView = GridView(self.game, size_hint_y=2)
        self.add_widget(self.gridView)

    def loadFile(self, fileName):
        numberOfGuns = self.leftPannel.getNumberOfGuns()
        self.game = game.loadGame(fileName, numberOfGuns, game.players.PlayerClasses[self.leftPannel.getPlayerClass()])
        self.clear_widgets()
        self.setGridView()

    def update(self):
        self.gridView.update()
        self.statusView.update()
        if self.game.shipPlayer.countActiveShips() == 0:
            self.remove_widget(self.gridView)
            self.add_widget(Label(text='JUEGO TERMINADO', size_hint_y=2))


class GameApp(App):

    def __init__(self):
        App.__init__(self)

    def build(self):
        return GameView()

if __name__ == '__main__':
    GameApp().run()
