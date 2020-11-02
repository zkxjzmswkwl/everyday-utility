import os
from time import sleep

def get_devices():
    to_return = []
    unfiltered_devices = os.popen('arp -a')
    
    for device in unfiltered_devices:
        to_return.append({
            'name': device.split('(')[0],
            'addy': device.split('(')[1].split(')')[0],
            'mac': device.split('at ')[1].split(' [')[0]})
    
    return to_return


def renderUi(devices):
    os.system('clear')

    print('***********************************')
    
    for device in devices:
        print(f'* {device["name"]}')
        print(f'** {device["addy"]}')
        print(f'*** {device["mac"]}\n')
    
    print('***********************************')
    
    sleep(5)
    os.system('clear')

while True:
    renderUi(get_devices())
