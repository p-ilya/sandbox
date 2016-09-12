# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 05:19:40 2016

@author: owner
"""

import sqlite3 as sq
import bot_config

con = sq.connect(bot_config.DATABASE, check_same_thread=False)

def get_faculty_names():
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM faculty")
        p = cur.fetchall()
        return p
        
def get_groups_by_f(f):
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("SELECT g_id,name FROM groups WHERE f_id=?",(f,))
        p = cur.fetchall()
        return p

def get_faculty_name(f_id):
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM faculty WHERE f_id=?",(f_id,))
        f = cur.fetchone()
        return f[0]
        
def get_sch_by_date(date):
    ts = []    
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM classes WHERE c_date=?',(date,))
        p = cur.fetchall()
        for row in p:
            msg = '{0}, {1} пара (неделя {2}):\n{3}\n{4}\n{5}\n'.format(row['c_date'], row['c_time'],row['week'],row['name'],row['prepod'],row['place'])
            ts.append(msg)
    return ts
            