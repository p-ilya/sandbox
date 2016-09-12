# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:38:54 2016

@author: owner
"""

import sqlite3 as sq
import telebot, time
import logging
import bot_config

con = sq.connect(bot_config.DATABASE, check_same_thread=False)

bot = telebot.TeleBot(bot_config.TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

welcome_msg = '''Бот предназначен для помощи с расписанием пар студентам СПбГЭУ.'''

@bot.message_handler(commands=['start','help'])
def start_help(message):
    bot.send_message(message.chat.id, welcome_msg)
  
@bot.message_handler(commands=['new'])
def register(message):
    user_id = message.from_user.id
    f_markup = telebot.types.InlineKeyboardMarkup()
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM faculty")
        p = cur.fetchall()
        for row in p: 
            button = telebot.types.InlineKeyboardButton(text=row['name'], callback_data='f_id {}'.format(row['f_id']))        
            f_markup.add(button)            
    bot.send_message(message.chat.id,'Я запомнил ваш id.\nВыберите ваш факультет, пожалуйста.',reply_markup=f_markup)
    
    
@bot.message_handler(commands=['test'])
def test(message):
    ts = []
    data = message.text[6:]      
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        
        cur.execute('SELECT * FROM classes WHERE c_date=?',(data,))
        p = cur.fetchall()
        for row in p:
            msg = '{0}, {1} пара (неделя {2}):\n{3}\n{4}\n{5}\n'.format(row['c_date'], row['c_time'],row['week'],row['name'],row['prepod'],row['place'])
            ts.append(msg)           
    for m in ts:            
        bot.send_message(message.chat.id,m)

if __name__=='__main__':
    bot.polling()
    time.sleep(100)