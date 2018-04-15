import os
import sqlite3
import sys

import click
from win32 import win32crypt  # see https://github.com/mhammond/pywin32

default_sqlite_location = r'chrome_info\Default\User Data\Default'


@click.command()
@click.option('--input', default=default_sqlite_location, type=str)
@click.option('--output', default=os.path.join(default_sqlite_location, 'passwords.txt'), type=str)
@click.option('--overwrite', default=False, type=bool)
def cli(input: str, output: str, overwrite: bool):

    if not os.path.isabs(input):
        input = os.path.join(os.path.dirname(sys.argv[0]), input)

    if not os.path.isabs(output):
        output = os.path.join(os.path.dirname(sys.argv[0]), output)

    if os.path.exists(input):
        users = dump_passwords(input)
        print(str(len(users)) + " users dumped!")

        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))

        if os.path.isfile(output) and not overwrite: #file exists and we DON'T want to overwrite
            print(f'File exists at {output} and `overwrite` = false!')
            print("Failed!")
            exit(1)

        print(input + " -> " + output)

        f = open(output, 'w', encoding='utf-16')

        for user in users:
            f.write(str(user))

        f.close()

        print("Done!")

    else:
        print(f'File at \'{input}\' doesn\'t exist!')


class User:
    def __init__(self, name, site, pw):
        self.name = name
        self.site = site
        self.pw = pw

    def __str__(self):
        return f'{self.name}@{self.site}:{self.pw}'


def dump_passwords(path: str):
    users = []

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logins')

    names = [description[0] for description in cursor.description]  # list of names
    d = {v: k for k, v in list(enumerate(names))}  # dict of name:position for sqlite cursor

    for result in cursor.fetchall():
        pwhash = result[d['password_value']]
        pw = win32crypt.CryptUnprotectData(pwhash, None, None, None, 0)[1]

        site = result[d['origin_url']]
        name = result[d['username_value']]

        user = User(name, site, pw.decode('ascii'))
        users.append(user)

    return users


if __name__ == '__main__':
    cli()
