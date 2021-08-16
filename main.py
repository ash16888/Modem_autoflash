from time import sleep
import subprocess
import serial.tools.list_ports
import colorama
from colorama import Fore, Back, Style

def main():
    rndis_port()
    sleep(13)
    flash('Firmware_Filename')
    sleep(20)
    send_godload()
    sleep(10)
    flash('WebUi_Filename')

def send_godload():
    colorama.init()
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
            if 'PC UI Interface' in p.description:
                print(Fore.GREEN + 'Порт найден начинаем прошивку модема')
                # Connection to port
                ser = serial.Serial(p.device)
                ser.write('AT^GODLOAD\r'.encode())
                ser.close() 

def rndis_port():
    reply = subprocess.run("ping 192.168.8.1 -n 1", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if reply.returncode == 0:
        code = subprocess.run("curl.exe -X POST -d @sw_project_mode.xml http://192.168.8.1/CGI", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)
        send_godload()

    elif reply.returncode == 1:
            ports = list(serial.tools.list_ports.comports())
            if not ports:
                print('Модем не найден')
            else:
                for p in ports:
                    if 'PC UI Interface' in p.description:
                        send_godload()

def flash(filename):
    subprocess.run(['balongflash.exe', filename])
    

if __name__ == '__main__':
    main()
