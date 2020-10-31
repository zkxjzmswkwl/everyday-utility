# Hacky script to automatically organize the Downloads folder on my laptop

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
import time



class FileHandler(FileSystemEventHandler):

    def on_modified(self, event):
        watch_dir = '/home/carter/Downloads'
        __FILE_TYPE_MUSIC = ('.mp3', '.flac', '.wav')
        __FILE_TYPE_IMAGE = ('.jpeg', '.jpg', '.png', '.gif', '.svg')
        __FILE_TYPE_INSTALLER = ('.msi', '.deb')
        __EXCLUDE = ['clean', 'music', 'images', 'installers']
                
        for file_path in os.listdir(watch_dir):
            move_dest = f'{watch_dir}/clean/{file_path}'
            
            if file_path.endswith(__FILE_TYPE_MUSIC):
                move_dest = f'{watch_dir}/music/{file_path}'
            
            if file_path.endswith(__FILE_TYPE_IMAGE):
                move_dest = f'{watch_dir}/images/{file_path}'
            
            if file_path.endswith(__FILE_TYPE_INSTALLER):
                move_dest = f'{watch_dir}/installers/{file_path}'

            if file_path not in __EXCLUDE:
                os.rename(f'/home/carter/Downloads/{file_path}', move_dest)

Organize = FileHandler()
observer = Observer()
observer.schedule(Organize, '/home/carter/Downloads', recursive=True)
observer.start()

try:
    while True:
        time.sleep(15)
except KeyboardInterrupt:
    observer.stop()
observer.join()