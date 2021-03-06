# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 02:31:04 2016

@author: owner
"""

import sqlite3 as sq

con = sq.connect('unecon_bot.db')
#g_list = (('ИС-1301',4),('ИБ-1301',4),('ПМ-1301',4),('ПИ-1301',4))
'''f_list = (
    'Ф-т экономики и финансов',
    'Гуманитарный ф-т',
    'Юридический ф-т',
    'ФИПМ',
    'Ф-т управления',
    'Ф-т торгового и таможенного дела',
    'Ф-т туризма и гостеприимства',
    'Ф-т сервиса',
    'Очно-заочное/заочное')'''
#t_list = ('9:00 - 10:35','10:50 - 12:25','12:40 - 14:15','14:30 - 16:00','16:10 - 17:40','17:50 - 19:20')
c_list = (
    ("2016-09-05",1,'Инструментальные средства информационных систем','доц. Емельянов А.А.',1,1,'Г-2070'),
    ("2016-09-05",1,'Инструментальные средства информационных систем','доц. Емельянов А.А.',1,2,'Г-2070'),
    ("2016-09-05",2,'Инструментальные средства информационных систем','доц. Емельянов А.А.',1,1,'Г-2070'),
    ("2016-09-05",2,'Инструментальные средства информационных систем','доц. Емельянов А.А.',1,2,'Г-2070'),
    ("2016-09-05",3,'Инструментальные средства информационных систем','доц. Емельянов А.А.',1,1,'Г-2070'),
    ("2016-09-06",1,'Стандартизация, сертификация, управление качеством программного обеспечения','доц. Головкин Ю.Б.',1,1,'Г-2062'),
    ("2016-09-06",1,'Стандартизация, сертификация, управление качеством программного обеспечения','доц. Головкин Ю.Б.',1,2,'Г-2062'),
    ("2016-09-06",2,'Стандартизация, сертификация, управление качеством программного обеспечения','доц. Головкин Ю.Б.',1,1,'Г-2062'),
    ("2016-09-06",2,'Надежность информационных систем','проф. Богатырев В.А.',1,2,'Г-2008'),
    ("2016-09-06",3,'Надежность информационных систем','проф. Богатырев В.А.',1,1,'Г-2005'),
    ("2016-09-06",3,'Надежность информационных систем','проф. Богатырев В.А.',1,2,'Г-2005'),
    ("2016-09-07",1,'Автоматизированные системы управления производством','проф. Колбанев М.О.',1,1,'Г-2006'),
    ("2016-09-07",1,'Автоматизированные системы управления производством','проф. Колбанев М.О.',1,2,'Г-2006'),
    ("2016-09-07",2,'Автоматизированные системы управления производством','проф. Колбанев М.О.',1,1,'Г-2006'),
    ("2016-09-07",2,'Автоматизированные системы управления производством','проф. Колбанев М.О.',1,2,'Г-2006'),
    ("2016-09-08",1,'Моделирование систем','проф. Колбанев М.О.',1,1,'Г-2004'),
    ("2016-09-08",2,'Моделирование систем','проф. Колбанев М.О.',1,1,'Г-2004'),
    ("2016-09-08",2,'Моделирование систем','проф. Колбанев М.О.',1,2,'Г-2004'),
    ("2016-09-08",3,'Моделирование систем','проф. Колбанев М.О.',1,1,'Г-2060'),
    ("2016-09-08",3,'Моделирование систем','проф. Колбанев М.О.',1,2,'Г-2060'),
    ("2016-09-08",4,'Стандартизация, сертификация, управление качеством программного обеспечения','доц. Головкин Ю.Б.',1,1,'Г-2060'),
    ("2016-09-08",4,'Стандартизация, сертификация, управление качеством программного обеспечения','доц. Головкин Ю.Б.',1,2,'Г-2060'),
    ("2016-09-09",1,'Методы и средства проектирования информационных систем и технологий','доц. Емельянов А.А.',1,1,'Г-2052'),
    ("2016-09-09",1,'Методы и средства проектирования информационных систем и технологий','доц. Емельянов А.А.',1,2,'Г-2052'),
    ("2016-09-09",2,'Методы и средства проектирования информационных систем и технологий','доц. Емельянов А.А.',1,1,'Г-2052'),
    ("2016-09-09",2,'Методы и средства проектирования информационных систем и технологий','доц. Емельянов А.А.',1,2,'Г-2052'),
    ("2016-09-09",3,'Методы и средства проектирования информационных систем и технологий','доц. Емельянов А.А.',1,1,'Г-2052'))

with con:
    con.row_factory = sq.Row
    cur = con.cursor()
    
    #cur.execute('DROP TABLE IF EXISTS classes')
    # table creation
    '''cur.execute('CREATE TABLE classes (c_id INTEGER PRIMARY KEY NOT NULL,c_date DATE,c_time INT,
    name VARCHAR(200),prepod VARCHAR(40),g_id INT,week INT,
    FOREIGN KEY (c_time) REFERENCES time(t_id),FOREIGN KEY (g_id) REFERENCES groups(g_id))')'''
    #cur.execute('CREATE TABLE groups (g_id INTEGER PRIMARY KEY NOT NULL,name VARCHAR(10),year INT,f_id INT, FOREIGN KEY (f_id) REFERENCES faculty(f_id))')
    
    # test print
    data = "2016-09-07"
    cur.execute('SELECT * FROM classes WHERE c_date=?',(data,))
    p = cur.fetchall()
    for row in p: 
        print('{0}, {1} пара (неделя {2}):\n{3}\n{4}\n{5}\n'.format(row['c_date'], row['c_time'],row['week'],row['name'],row['prepod'],row['place']))
    
    # data insert
    #for i in c_list:
        #cur.execute('INSERT INTO classes(c_date,c_time,name,prepod,g_id,week,place) VALUES(?,?,?,?,?,?,?)',(i))
    
    #alter table
    #cur.executescript('''ALTER TABLE classes ADD COLUMN place VARCHAR(10)''')