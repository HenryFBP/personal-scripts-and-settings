import sqlite3
from pprint import pprint

from win32 import win32crypt  # see https://github.com/mhammond/pywin32

if __name__ == '__main__':
    default_sqlite_location = r'P:\GitHub\personal-scripts-and-settings\Python\chrome_info\HenryFBP\User Data\Default'

    conn = sqlite3.connect(default_sqlite_location)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM logins')

    names = [description[0] for description in cursor.description]  # list of names
    d = {v: k for k, v in list(enumerate(names))}  # dict of name:position for sqlite cursor

    pprint(names)
    pprint(d)

    for result in cursor.fetchall():
        pwhash = result[d['password_value']]

        pw = win32crypt.CryptUnprotectData(pwhash, None, None, None, 0)[1]

        pprint(pw)
