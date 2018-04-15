Example usage of chrome scripts:

``python dump_chrome_info.py --users_dir=C:\Users --output_dir=chrome_info --users=timbillybob``

will dump the SQLITE3 db file, and

``python dump_chrome_sqlite.py --input="chrome_info\timbillybob\User Data\Default"``

will decrypt the binary BLOB columns in the SQLITE3 database.

