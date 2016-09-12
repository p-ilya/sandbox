# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:38:54 2016

@author: owner
"""

import telebot
#import time
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
  
@bot.message_handler(commands=['new'])
def register(message):
    #user_id = message.from_user.id
    f_markup = telebot.types.InlineKeyboardMarkup()
    for row in db_utils.get_faculty_names(): 
        button = telebot.types.InlineKeyboardButton(text=row['name'], callback_data='f_id {}'.format(row['f_id']))        
        f_markup.add(button)            
    bot.send_message(message.chat.id,'Я запомнил ваш id.\nВыберите ваш факультет, пожалуйста.',reply_markup=f_markup)

@bot.callback_query_handler(func=lambda call: True)
def send_group_list(call):
    answer = call.data.split(' ')
    flty = int(answer[1])
    g_markup = telebot.types.InlineKeyboardMarkup()
    for row in db_utils.get_groups_by_f(flty): 
        button = telebot.types.InlineKeyboardButton(text=row['name'], callback_data='g_id {}'.format(row['g_id']))        
        g_markup.add(button)
    chosen_f = db_utils.get_faculty_name(flty)
    bot.send_message(call.from_user.id,'Вы выбрали {}.\nВыберите вашу группу:'.format(chosen_f),reply_markup=g_markup)      

@bot.message_handler(commands=['test'])
def test(message):
    date = message.text[6:]      
    ts = db_utils.get_sch_by_date(date)
    for m in ts:            
        bot.send_message(message.chat.id,m)

if __name__=='__main__':
    bot.polling()
    #time.sleep(100)