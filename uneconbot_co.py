# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:38:54 2016

@author: owner
"""

import sqlite3 as sq
import telebot, time
import logging

con = sq.connect('unecon_bot.db', check_same_thread=False)

token = 'XXXXXXXXX:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
bot = telebot.TeleBot(token)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

welcome_msg = '''Бот предназначен для помощи с расписанием пар студентам СПбГЭУ.'''

@bot.message_handler(commands=['start','help'])
def start_help(message):
    bot.send_message(message.chat.id, welcome_msg)
    
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
    bot.polling(none_stop=True)
    time.sleep(100)