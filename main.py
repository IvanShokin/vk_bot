from bot import User, menu
from random import randint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from json import load, dump
from os.path import isfile


with open('config.json', 'r') as file:
    config = load(file)

token = config.get('token')


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def new_mess(user_id, mes_for_user):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': mes_for_user,
               'random_id': randint(0, 1000000000)})


def save(file_save, user_save):
    with open(file_save, "w") as file_user:
        user_dict = {
            'money': user_save.money,
            'bet': user_save.bet,
            'box': user_save.box,
            'true_answer': user_save.true_answer,
            'condition': user_save.condition,
        }
        dump(user_dict, file_user)


with open('requests_response.json', 'r') as file:
    requests_response = load(file)


if __name__ == '__main__':
    print("Начали")
    for event in longpoll.listen():

        # Если пришло новое сообщение и если оно для меня( то есть бота)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            # Полное имя пользователя
            user = vk.method("users.get", {"user_ids": event.user_id})
            fullname = user[0]['first_name'] + ' ' + user[0]['last_name']

            json_file_name = f'{event.user_id}.json'

            response = requests_response.get(event.text)
            if response:
                new_mess(event.user_id, response)
            elif isfile(json_file_name):
                with open(json_file_name, "r") as user_file:
                    dict_user = load(user_file)

                all_features = 'money', 'bet', 'box', 'true_answer', 'condition'
                money, bet, box, true_answer, condition = [dict_user.get(features) for features in all_features]

                user = User(event.user_id, money, bet, box, true_answer, condition)

                response_mess = user.response(event.message)
                new_mess(event.user_id, response_mess)
                save(json_file_name, user)
            elif event.text == 'Начать':
                user = User(event.user_id)
                new_mess(event.user_id, menu)
                save(json_file_name, user)