#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import zipfile
import shutil
import socket
import threading

DIR = '/Users/panshao/Public/web/gaore/c.gaore.com'
IGNORE = ['include', 'lock', 'download', '.git', 'vendor', '.idea']


def doUnzip(g):
    """

    :param game:
    :return:
    """
    try:
        path = os.path.join(DIR, g)
        print(path)
        temp_dirs = [t for t in os.listdir(path) if os.path.isdir(os.path.join(path, t)) and t.startswith('game')]

        # remove old path
        for tt in temp_dirs:
            shutil.rmtree(os.path.join(path, tt))

        # unzip
        temp_files = [t for t in os.listdir(path) if os.path.isfile(os.path.join(path, t)) and t.endswith('.zip')]
        for ff in temp_files:
            zippath = os.path.join(path, ff)
            tmppath = os.path.join(path, 'temp')
            shutil.rmtree(tmppath)

            zip_ref = zipfile.ZipFile(zippath, 'r')
            zip_ref.extractall(tmppath)
            zip_ref.close()
            new_folder_name = os.path.splitext(zippath)[0]
            shutil.move(os.path.join(tmppath, 'game'), new_folder_name)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('127.0.0.1', 18222))

    s.listen()

    if len(sys.argv) > 1:
        specify_games = sys.argv[1].split(',')

    else:
        specify_games = []

    dirs = [d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d)) and d not in IGNORE]
    dirs = set(dirs) & set(specify_games) if specify_games else set(dirs)

    tasks = []
    print(dirs)

    for game in dirs:
        t = threading.Thread(target=doUnzip, args=[game])
        t.setDaemon(True)
        t.start()
        tasks.append(t)

    for t in tasks:
        t.join()

    s.close()