from random import randint

menu = "Меню:\n" \
       "1 - 🎰 Начать игру\n" \
       "2 - 💰 Испытать удачу\n" \
       "3 - 👛 Мой кошелек\n" \
       "4 - ⚠ Изменить ставку\n" \
       "5 - 📦 Изменить количество коробок\n"


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
            '1': self.game,
            '2': self.luck,
            '3': str(self.money),
            '4': self.new_bet,
            '5': self.new_box_quantity
        }
        if isinstance(command.get(new_mess), str):
            return command.get(new_mess)
        else:
            return command.get(new_mess)()

    def game(self):
        self.condition = 'game'
        self.true_answer = randint(1, self.box)
        mess = ''
        for box_i in range(self.box):
            mess += f'{box_i + 1} Коробка\n'
        return mess

    def answer(self, user_answer):
        self.condition = 'menu'
        if int(user_answer) == self.true_answer:
            self.money += self.bet * self.box
            return f'Вы выиграли ✅ {self.bet * self.box} монет \n{menu}'
        else:
            self.money -= self.bet
            return f'Вы проиграли ❌ \n{menu}'

    def new_bet(self):
        self.condition = 'new_bet'
        return 'Напишите новую ставку'

    def new_box_quantity(self):
        self.condition = 'new_box_quantity'
        return 'Напишите число от 2 до 10'

    def set_new_bet(self, new_bet):
        self.condition = 'menu'
        self.bet = int(new_bet)
        return "Успешно✅\n" \
               "Меню:\n" \
               "1 - 🎰 Начать игру\n" \
               "2 - 💰 Испытать удачу\n" \
               "3 - 👛 Мой кошелек\n" \
               "4 - ⚠ Изменить ставку\n" \
               "5 - 📦 Изменить количество коробок\n"

    def set_new_box_quantity(self, new_box_quantity):
        self.condition = 'menu'
        self.box = int(new_box_quantity)
        return "Успешно✅\n" \
               "Меню:\n" \
               "1 - 🎰 Начать игру\n" \
               "2 - 💰 Испытать удачу\n" \
               "3 - 👛 Мой кошелек\n" \
               "4 - ⚠ Изменить ставку\n" \
               "5 - 📦 Изменить количество коробок\n"

    def luck(self):
        if randint(1, 2) == 1:
            self.money += self.bet
            return f'Вы выиграли ✅ {self.bet}!'
        else:
            self.money -= self.bet
            return f'Вы проиграли ❌ {self.bet}'

    def response(self, new_mess):
        all_condition = {
            'menu': self.menu,
            'game': self.answer,
            'new_bet': self.set_new_bet,
            'new_box_quantity': self.set_new_box_quantity,
        }

        return all_condition.get(self.condition)(new_mess)
