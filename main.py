from User import User, menu
from random import randint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
from os.path import isfile


token = "dda4bbad0100bbce1899e2ab3a63e6ef4e54d3848eef2402566e3dd2efdbe3b613e2d2cca23efc945afb3"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def new_mess(user_id, mes_for_user):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': mes_for_user,
               'random_id': randint(0, 1000000000)})


print("Начали")
for event in longpoll.listen():

    # Если пришло новое сообщение и если оно для меня( то есть бота)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        # Полное имя пользователя
        user = vk.method("users.get", {"user_ids": event.user_id})
        fullname = user[0]['first_name'] + ' ' + user[0]['last_name']

        json_file_name = f'{event.user_id}.json'
        if isfile(json_file_name):
            with open(json_file_name, "r") as user_file:
                dict_user = json.load(user_file)

            all_features = 'money', 'bet', 'box', 'true_answer', 'condition'
            money, bet, box, true_answer, condition = [dict_user.get(features) for features in all_features]

            user = User(event.user_id, money, bet, box, true_answer, condition)

            response_mess = user.response(event.message)
            new_mess(event.user_id, response_mess)

        elif event.text == 'Начать':
            user = User(event.user_id)
            new_mess(event.user_id, menu)

        with open(f"{event.user_id}.json", "w") as file_user:
            user_dict = {
                'money': user.money,
                'bet': user.bet,
                'box': user.box,
                'true_answer': user.true_answer,
                'condition': user.condition,
            }
            json.dump(user_dict, file_user)