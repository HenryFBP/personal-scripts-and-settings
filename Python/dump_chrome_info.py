import os
import shutil
import sys

import click

data_location = r'AppData\Local\Google\Chrome\User Data\Default\Login Data'


def walk_through_files(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def remove_first_slash(thing: str):
    if thing[0] is '\\' or thing[0] is '/':
        thing = thing[1:]
    return thing


@click.command()
@click.option('--users_dir', default=r'C:\Users', type=str)
@click.option('--output_dir', default=r'chrome_info', type=str)
@click.option('--users', default='Public', type=str)
@click.option('--overwrite', default=False, type=bool)
def dump(users_dir: str, output_dir: str, users: str, overwrite: bool):
    """Given a windows directory, dump all chrome user-related data."""

    if not os.path.isabs(output_dir):  # if output_dir not absolute, make it relative to our location!
        output_dir = os.path.join(os.path.dirname(sys.argv[0]), output_dir)

    print(f"'{users_dir}' ==[dump]=> '{output_dir}':")

    users = users.split(',')  # split by comma

    if len(users) > 0:
        for user in users:
            src = os.path.join(users_dir, user, data_location)
            dest = os.path.join(output_dir, user, r'User Data\Default')

            print(src + " => " + dest + "...", end='')

            if os.path.exists(dest):  # if dest path exists, possibly overwrite
                if overwrite is True:
                    shutil.rmtree(dest)
                else:
                    print(" Failed! ")
                    print("Not dumping into destination as `overwrite` isn't True and a directory exists there.")
            else:
                copy_chrome_user_data(src, dest, overwrite)
                print(' Done! ')


def copy_chrome_user_data(src: str, dest: str, overwrite: bool = False):
    if os.path.isfile(src):
        copy_file(src, dest)
    elif os.path.isdir(src):
        copy_tree(src, dest, overwrite)


def copy_file(src, dest, overwrite=False):
    if not os.path.exists(os.path.dirname(dest)):  # if path DNE, make it
        os.makedirs(os.path.dirname(dest))

    if overwrite and os.path.exists(dest):  # if we want to overwrite
        os.remove(dest)

    shutil.copyfile(src, dest)


def copy_tree(src, dest, overwrite=False):
    for filepath in walk_through_files(src):
        relpath = filepath.replace(src, '')

        relpath = remove_first_slash(relpath)

        destpath = os.path.join(dest, relpath)

        print(filepath + ' -> ' + destpath + ' ... ', end='')

        try:
            copy_file(filepath, destpath, overwrite)
            print('[OK]')
        except Exception as e:
            print(f'[{e.__class__.__name__}]')


if __name__ == '__main__':
    dump()
