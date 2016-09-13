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
        
def get_groups_by_f(f,y):
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("SELECT g_id,name FROM groups WHERE f_id=? AND year=?",(f,y))
        p = cur.fetchall()
        return p

def get_faculty_name(f_id):
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM faculty WHERE f_id=?",(f_id,))
        f = cur.fetchone()
        return f[0]
        
def get_sch_by_date(user,date):
    ts = []    
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("SELECT g_id FROM users WHERE u_id=?",user)
        u = cur.fetchone()
        cur.execute('SELECT * FROM classes WHERE c_date=? AND g_id=?',(date,u[0]))
        p = cur.fetchall()
        for row in p:
            msg = '{0}, {1} пара (неделя {2}):\n{3}\n{4}\n{5}\n'.format(row['c_date'], row['c_time'],row['week'],row['name'],row['prepod'],row['place'])
            ts.append(msg)
    return ts
    
def add_new_user(u_id,g_id):
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("INSERT INTO users VALUES(?,?)",(u_id,g_id))
    return True
    
def delete_user(u_id):
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE u_id=?",(u_id,))
    return True
    
def check_users():
    tc = []
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        p = cur.fetchall()
        for row in p:
            z = 'User ID: {0}\nGroup ID: {1}\n\n'.format(row['u_id'],row['g_id'])
            tc.append(z)
    return tc