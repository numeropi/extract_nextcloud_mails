#!/usr/bin/python3

import MySQLdb
from collections import defaultdict
from pprint import pprint 
from datetime import datetime, timedelta

DB_HOST = "localhost"
DB_USERNAME = "nextcloud"
DB_PASSWORD = "db_password"
DB_NAME = "db_name"

languages_groupby = ['en','es','ca']
last_login_filter_time = timedelta(days=30) #leave as None if you don't want to filter by last_login
groups_filter = ['premium'] #groupnames are case-sensitive, leave as empty list if no filter by groups

#you can have a .config file to load the db config outside of this file
from config import * 

# Open database connection

db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)

cursor = db.cursor()

cursor.execute("SELECT * FROM oc_accounts")

myresult = cursor.fetchall()
users = {}


for username, data in myresult:
#  print(data)
    data = data.replace('null','""')
    data = eval(data)
    users[username] = {}
    users[username]["email"] = data["email"]["value"]
    users[username]["groups"] = []


cursor.execute("SELECT * FROM oc_group_user")
myresult = cursor.fetchall()

for groupname, username in myresult:
    users[username]["groups"].append(groupname)


cursor.execute("SELECT * FROM oc_preferences")
myresult = cursor.fetchall()

for userid, appid, configkey, configvalue in myresult:
    if appid == 'files' and configkey == 'quota':
        users[userid]["quota"] = configvalue
    if appid == 'core' and configkey == 'lang':
        users[userid]["lang"] = configvalue
    if appid == 'login' and configkey == 'lastLogin':
        users[userid]["lastLogin"] = configvalue
    if appid == 'settings' and configkey == 'email':
        users[userid]["email"] = configvalue


new_filtered = []
if groups_filter:
    print('Filtering by groups', groups_filter)
    for u,u_data in users.items():
        u_data = users[u]
        if 'groups' in u_data:
            if list(set(groups_filter) & set(u_data["groups"])): #If groups intersect each other
                new_filtered.append(u)

    filtered_users = new_filtered

new_filtered = []
if last_login_filter_time:
    print('Filtering by last login time', last_login_filter_time)
    for u in filtered_users:
        u_data = users[u]
        if 'lastLogin' in u_data:
            lastLogin = int(u_data["lastLogin"])
            lastLogin = datetime.utcfromtimestamp(lastLogin)
            if datetime.now() - lastLogin > last_login_filter_time:
                #print(u, lastLogin.strftime("%Y-%m-%d %H:%M:%S"))
                new_filtered.append(u)

    filtered_users = new_filtered


if languages_groupby:
    print('Grouping by language', languages_groupby)
    users_by_langs = defaultdict(list)
    for u in filtered_users:
        u_data = users[u]
        if 'lang' in u_data :
            lang = u_data["lang"][:2]
            if lang in ['eu', 'gl']: #For the moment Euskara and Galician will be moved to Spanish lang
                lang = 'es'
            if lang not in languages_groupby: #English when no matched language
                lang = 'en'
        else:
            lang = 'en' #English if language is not mentioned in preferences
        users_by_langs[lang].append(u) 

    for lang,lang_users in users_by_langs.items():
        print('-'*20,'\nLang', lang)
        for u in lang_users:
            print("{} <{}>".format(u, users[u]["email"]))

else:
    print('All languages')
    for u in filtered_users:
        print("{} <{}>".format(u, users[u]["email"]))

# disconnect from server
db.close()


