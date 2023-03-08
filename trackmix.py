#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path
import subprocess
import re
import shutil
import time as times
import sys

def trackmix(argv):
    cmd_commands = ['--source', '--destination', '--count', '--frame']
    
    sorted_argum = [f'{str(os.getcwd())}', 'mix', 0, 10, False, False]
    
    for i in range(1, len(argv)):
        for j in range(len(cmd_commands)):
            if argv[i] == cmd_commands[j]:
                sorted_argum[j] = (type(sorted_argum[j]))(argv[i+1])
                break
                
    source = sorted_argum[0]
    destination = sorted_argum[1]
    count = sorted_argum[2]
    frame = sorted_argum[3]
    
    
    if '--log' in argv:
        log = True
    if '--extended' in argv:
        extended = True
    
    with open(str(Path(source)) + '\\log.txt', 'w') as out:
        files = list(Path(source).glob("*.mp3")) #Собираем список файлов
    
        if count == 0: #Если кол-во файлов не указано
            count = len(files) #Используем все файлы

        #Создание фрагментов отдельных файлов
        if not(Path(source+r"\tmp").exists()): #Все фрагменты будем заносить в папку tmp
            os.mkdir(source + r"\tmp")
            
        for index in range(count):
            command = 'ffprobe.exe -i "'+str(files[index])+'" -hide_banner' # Задаем команду на получение длитеьлности файла
            
            text = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Читаем вывод
            text = text.stdout.read().decode('cp866') #Декодируем вывод
            
            duration = re.compile('\d\d:\d\d:\d\d.\d\d').search(text).group() # Получаем строку Duration: 'время'
            minutes = int(duration.split(':')[1]) # Получаем количество полных минут длительности
            seconds = round(float(duration.split(':')[2])) # Получаем количество секунд длительности
            
            time = minutes*60+seconds # Длительность в секундах
            time = round(time/100*15) # С 15% начнется музыка
            if extended == True:
                # Добавляем fade in/out
                command = 'ffmpeg.exe -ss '+str(time)+' -t '+str(frame)+' -i "' +                          str(files[index])+'" -filter:a "afade=in:st=0:d=2, afade=out:st='+str(frame-2) +                          ':d=2" -y "' + str(Path(source)) + '\\tmp\mix'+str(index)+'.mp3"' 
            else:
                # Без добавление fade in/out 
                command = 'ffmpeg.exe -ss ' + str(time) + ' -t ' + str(frame) + ' -i "' +                           str(files[index]) + '" -y "' + str(Path(source)) + '\\tmp\mix' +                          str(index) + '.mp3"'
            if log==True: #Если log - True выводим логи
                print('-- processing file '+str(index)+': '+str(os.path.split(files[index])[-1]))
            p = subprocess.Popen(command, stdout=out, stderr=out) # Выполняем команду, в папке tmp появится файл mix{index}.mp3
            while True: # Завершился ли процесс Popen ? (проверка)
                if p.poll() == 0:
                    break
                times.sleep(0.2)
                
                
        os.chdir(source+os.sep+r'\tmp')# Переход в папку с миксами
        files = os.listdir(os.getcwd()) # Получаем список миксов
        
        # Запись списка музыки в файл
        with open("musicMix_List.txt", "w") as f:
            for it in files:
                f.write(f"file '{it}'\n")
            f.close()

        # Выполнение конкатенации
        command = 'ffmpeg -f concat -i musicMix_List.txt -c copy ' + destination + '.mp3' #Формируем команду для объединения файлов
        subprocess.Popen(command, stdout=out, stderr=out) #Выполняем команду
       
        # Завершился ли subprocess?
        while True:
            if p.poll() == 0:
                break
            times.sleep(0.2)
            
        if log==True:
            print("-- done!")
            
        out.close()

# test - ['trackmix.py', '--source', "C:\\Lab2Mus", '--count', '0', '--frame', '15', '--log', '--extended']
trackmix(sys.argv)


# In[ ]:





# In[ ]:




