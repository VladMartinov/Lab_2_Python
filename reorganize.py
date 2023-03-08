#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Задание №6.
Напишите скрипт reorganize.py, который в директории --source создает
две директории: Archive и Small. В первую директорию помещаются
файлы с датой изменения, отличающейся от текущей даты на
количество дней более параметра --days (т.е. относительно старые
файлы). Во вторую – все файлы размером меньше параметра --size байт.
Каждая директория должна создаваться только в случае, если найден
хотя бы один файл, который должен быть в нее помещен. Пример
вызова:
"""

import time, sys, os
time_Unix = time.time()

def reorgaize(argv):
    if argv[1] == '--source' and argv[3] == '--days' and argv[5] == '--size':
        for _, _, files in os.walk(argv[2]):
            for name in files:

                path_to_file = argv[2] + f"\{name}"
                
                try:
                    if os.stat(path_to_file).st_size < int(argv[6]):
                        dir_name = argv[2] + "\Small"
                        try:
                            os.mkdir(dir_name)
                        except FileExistsError:
                            pass
                        os.replace(path_to_file, dir_name + f"\{name}")
                        continue

                    if os.path.getmtime(path_to_file) < (time_Unix - (float(argv[4])*86400)):
                        dir_name = argv[2] + "\Archive"
                        try:
                            os.mkdir(dir_name)
                        except FileExistsError:
                            pass
                        os.replace(path_to_file, dir_name + f"\{name}")
                except FileNotFoundError:
                    pass

                    
reorgaize(sys.argv)

