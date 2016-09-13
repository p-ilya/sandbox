# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:38:54 2016

@author: owner
"""

import telebot
import logging
import db_utils

bot = telebot.TeleBot(db_utils.bot_config.TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

welcome_msg = '''Бот предназначен для помощи с расписанием пар студентам СПбГЭУ.\n
Пока что напрочь недоделан, поэтому оставь попытки взаимодействия всяк сюда входящий :)'''

@bot.message_handler(commands=['start','help'])
def start_help(message):
    bot.send_message(message.chat.id, welcome_msg)

users_to_register = {}
  
@bot.message_handler(commands=['new'])
def register(message):
    user_id = message.from_user.id
    users_to_register[user_id] = [0,0,0] #fak,god,group
    f_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for row in db_utils.get_faculty_names(): 
        button = '{1} {0}'.format(row['name'], row['f_id'])     
        f_markup.add(button)            
    msg = bot.send_message(message.chat.id,'Я запомнил ваш id.\nВыберите ваш факультет, пожалуйста.',reply_markup=f_markup)
    bot.register_next_step_handler(msg,send_year_list)

def send_year_list(message):
    answer = message.text.split(' ',1)
    flty = int(answer[0])
    users_to_register[message.from_user.id][0]=flty
    y_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(1,7): 
        y_markup.add('{} год обучения'.format(i))
    msg = bot.send_message(message.chat.id,'Выберите курс:',reply_markup=y_markup)
    bot.register_next_step_handler(msg,send_group_list)

def send_group_list(message):
    answer = message.text.split(' ',1)
    year = int(answer[0])
    users_to_register[message.from_user.id][1]=year
    flty = users_to_register[message.from_user.id][0]
    g_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for row in db_utils.get_groups_by_f(flty,year): 
        button = '{1} {0}'.format(row['name'],row['g_id'])        
        g_markup.add(button)
    chosen_f = db_utils.get_faculty_name(flty)
    msg = bot.send_message(message.from_user.id,'Вы выбрали {}.\nВыберите вашу группу:'.format(chosen_f),reply_markup=g_markup)
    bot.register_next_step_handler(msg,confirm_changes)
    
def confirm_changes(message):
    answer = message.text.split(' ',1)
    group = int(answer[0])
    users_to_register[message.from_user.id][2]=group
    r = db_utils.add_new_user(message.chat.id,users_to_register[message.chat.id][2])
    if not r: 
        bot.send_message(message.chat.id,"Что-то сломалось. Попробуйте настроить снова.")
    else:
        bot.send_message(message.chat.id,"Я вас запомнил, приятно познакомиться!")
    
#@bot.callback_query_handler(func=lambda call: True)
'''def send_group_list(call):
    answer = call.data.split(' ')
    flty = int(answer[1])
    g_markup = telebot.types.InlineKeyboardMarkup()
    for row in db_utils.get_groups_by_f(flty): 
        button = telebot.types.InlineKeyboardButton(text=row['name'], callback_data='g_id {}'.format(row['g_id']))        
        g_markup.add(button)
    chosen_f = db_utils.get_faculty_name(flty)
    bot.send_message(call.from_user.id,'Вы выбрали {}.\nВыберите вашу группу:'.format(chosen_f),reply_markup=g_markup)      
'''
@bot.message_handler(commands=['deleteme'])
def delete_me(message):
    r = db_utils.delete_user(message.chat.id) 
    if r:
        bot.send_message(message.chat.id,'Всего доброго, {}'.format(message.from_user.first_name))
    
@bot.message_handler(commands=['расп'])
def test(message):
    user_id = message.from_user.id
    date = message.text[6:]      
    ts = db_utils.get_sch_by_date(user_id,date)
    if not ts:
        bot.send_message(message.chat.id,'Я не могу найти ваше расписание на {}.'.format(date))
    for m in ts:            
        bot.send_message(message.chat.id,m)

if __name__=='__main__':
    bot.polling()
    print(db_utils.check_users())