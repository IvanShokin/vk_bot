from random import randint

menu = [('🎰 Начать игру', 'positive'),
        ('💰 Испытать удачу', 'secondary '),
        ('👛 Мой кошелек', 'primary '),
        ('⚠ Изменить ставку', 'negative '),
        ('📦 Изменить количество коробок', 'primary')]

regulations = "Дорогой друг,как мы видим ты новенький, поэтому вот тебе наши правила игры:\n" \
              "1.Начать играть - это начать играть в обычное Казино\n" \
              "2.Испытать удачу - это дополнительный режим где ты просто можешь испытать свою удачу шанс ,что ты выграешь и програешь = 50%\n" \
              "3.В твоем кошельке находяться твои монеты ,которыми ты можешь играть\n" \
              "4.Изменить ставку - это монеты на которые ты играешь\n" \
              "5.Изменить количество коробок - просто можешь поставить меньше коробок и повысить себе шанс угадать))\n" \
              "Приятной игры тебе!\n"

colors = ['primary', 'secondary', 'negative', 'positive']


class User:
    def __init__(self, id_user, money=100, bet=10, box=4, true_answer=None, condition='menu'):
        self.id_user = id_user
        self.money = money
        self.bet = bet
        self.box = box
        self.true_answer = true_answer
        self.condition = condition

    def menu(self, new_mess):
        command = {
            '🎰 Начать игру': self.game,
            '💰 Мой кошелек': str(self.money),
            '👛 Испытать удачу': self.luck,
            '⚠ Изменить ставку': self.new_bet,
            '📦 Изменить количество коробок': self.new_box_quantity
        }
        if isinstance(command.get(new_mess), tuple):
            return command.get(new_mess)
        else:
            return command.get(new_mess)()

    def game(self):
        self.condition = 'game'
        self.true_answer = randint(1, self.box)
        keyboard = []
        for box_i in range(self.box):
            button = f'{box_i+1} Box', 'primary'
            keyboard.append(button)
        return 'Выбери бокс!', keyboard

    def answer(self, user_answer):
        self.condition = 'menu'
        user_answer = int(user_answer.split()[0])

        if user_answer == self.true_answer:
            self.money += self.bet * self.box
            return f'Вы выиграли {self.bet * self.box} монет!', menu
        else:
            self.money -= self.bet
            return f'Вы проиграли {self.bet * self.box} монет(', menu

    def new_bet(self):
        self.condition = 'new_bet'
        return 'Напишите новую ставку!', []

    def new_box_quantity(self):
        self.condition = 'new_box_quantity'
        keyboard = []
        for box_i in range(2, 6):
            button = str(box_i), randint(colors(0, 3))
            keyboard.append(button)
        return 'Выбери количество коробок', keyboard

    def set_new_bet(self, new_bet):
        self.condition = 'menu'
        self.bet = int(new_bet)
        return 'Ставка изменилась ✅', menu

    def set_new_box_quantity(self, new_box_quantity):
        self.condition = 'menu'
        self.box = int(new_box_quantity)
        return 'Изменения внесены ✅', menu

    def luck(self):
        if randint(1, 2) == 1:
            self.money += self.bet
            return f'Вы выиграли ✅ {self.bet}!', menu
        else:
            self.money -= self.bet
            return f'Вы проиграли ❌ {self.bet}', menu

    def response(self, new_mess):
        all_condition = {
            'menu': self.menu,
            'game': self.answer,
            'new_bet': self.set_new_bet,
            'new_box_quantity': self.set_new_box_quantity,
        }

        return all_condition.get(self.condition)(new_mess)
