from random import randint
import json

menu = "Меню\n" \
       "1 - Начать игру\n" \
       "2 - Мой кошелек\n" \
       "3 - Изменить ставку\n" \
       "4 - Изменить количество коробок\n"


class User:
    def __init__(self, id_user, money=100, bet=10, box=4, true_answer=None, condition='menu', new_user=False):
        self.id_user = id_user
        self.money = money
        self.bet = bet
        self.box = box
        self.true_answer = true_answer
        self.condition = condition

        if new_user:
            with open(f"{id_user}.json", "w") as file_user:
                user_dict = {
                    'money': money,
                    'bet': bet,
                    'box': box,
                    'true_answer': true_answer,
                    'condition': condition,
                }
                json.dump(user_dict, file_user)

    def menu(self, new_mess):
        command = {
            'Начать игру': self.game,
            'Мой кошелек': str(self.money),
            'Изменить ставку': self.new_bet,
            'Изменить количество коробок': self.new_box_quantity
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
            mess += f'{box_i} Box\n'
        return mess

    def answer(self, user_answer):
        self.condition = 'menu'
        if user_answer == self.true_answer:
            self.money += self.bet * self.box
            return f'Вы выиграли {self.bet * self.box} монет!'
        else:
            self.money -= self.bet * self.box
            return 'Вы проиграли ('

    def new_bet(self):
        self.condition = 'new_bet'
        return 'Напишите новую ставку'

    def new_box_quantity(self):
        self.condition = 'new_box_quantity'
        return 'Напишите число от 2 до 10'

    def set_new_bet(self, new_bet):
        self.condition = 'menu'
        self.bet = int(new_bet)
        return 'Меню'

    def set_new_box_quantity(self, new_box_quantity):
        self.condition = 'menu'
        self.box = int(new_box_quantity)
        return 'Меню'

    def response(self, new_mess):
        all_condition = {
            'menu': self.menu,
            'game': self.answer,
            'new_bet': self.set_new_bet,
            'new_box_quantity': self.set_new_box_quantity,
        }

        return all_condition.get(self.condition)(new_mess)

