#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import zipfile
import shutil
import socket

DIR = '/data/www/c.gaore.com'
DIR = '/Users/panshao/Public/web/gaore/c.gaore.com'
IGNORE = ['include', 'lock', 'download', '.git', 'vendor', '.idea']

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('127.0.0.1', 18222))

    s.listen()

    if len(sys.argv) > 1:
        specify_games = sys.argv[1].split(',')
        dirs = [d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d)) and d not in IGNORE and d in specify_games]
    else:
        specify_games = []
        dirs = [d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d)) and d not in IGNORE]

    print(specify_games)

    for game in dirs:

        try:
            path = os.path.join(DIR, game)
            print(path)
            temp_dirs = [t for t in os.listdir(path) if os.path.isdir(os.path.join(path, t)) and t.startswith('game')]

            # remove old path
            for tt in temp_dirs:
                shutil.rmtree(os.path.join(path, tt))

            # unzip
            os.chdir(path)
            temp_files = [t for t in os.listdir(path) if os.path.isfile(os.path.join(path, t)) and t.endswith('.zip')]
            for ff in temp_files:
                zip_ref = zipfile.ZipFile(ff, 'r')
                zip_ref.extractall('temp')
                zip_ref.close()
                new_folder_name = os.path.splitext(ff)[0]
                shutil.move('temp/game', new_folder_name)

        except Exception as e:
            print(e)
            continue

    s.close()