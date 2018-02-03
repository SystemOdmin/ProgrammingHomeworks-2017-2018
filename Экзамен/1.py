import urllib.request
import re
import html
import os
import sqlite3

def get_data(file):
    req = urllib.request.Request('http://web-corpora.net/Test2_2016/short_story.html', headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        source = html.unescape(response.read().decode('utf-8'))
        data = re.findall(' ((?:с|С)[абвгдеёжзийклмнопростуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]+?)[ <]', source)
    datafile = '\n'.join(data)
    print(datafile)
    with open (file, 'w', encoding='utf-8') as f:
        f.write(datafile)
    return

def verbs(file, output):
    get_data(file)
    os.system('mystem.exe ' + file + ' ' + output + ' -n -d -i --generate-all')
    with open (output, 'r', encoding='utf-8') as f:
        verbs = []
        for line in f.readlines():
            verb = ''.join(re.findall('.+?{(.+?)=V', line))
            if verb not in verbs:
                verbs.append(verb)     
        print('\n'.join(verbs))

verbs('data.txt', 'output.txt')

with open ('output.txt', 'r', encoding='utf-8') as f:
    id_number = 0
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE table1(id INTEGER PRIMARY KEY, лемма TEXT, словоформа TEXT, часть_речи TEXT)")
    for line in f.readlines():
        id_number += 1
        lemma = ''.join(re.findall('.+?{(.+?)=', line))
        slovoforma = ''.join(re.findall('(.+?){.+?=', line))
        chast_rechi = ''.join(re.findall('.+?{.+?=(.+?),', line))
        c.execute("INSERT INTO table1(id, лемма, словоформа, часть_речи) VALUES (?,?,?,?)", [id_number, lemma, slovoforma, chast_rechi])
    conn.commit()
    conn.close()
              
