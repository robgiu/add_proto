import os
from time import sleep

os.system("echo \"23=0.1\" > /dev/pi-blaster")
#os.system("echo \"23=0\" > /dev/pi-blaster")
sleep(2)

os.system("echo \"23=0.2\" > /dev/pi-blaster")
#os.system("echo \"23=0\" > /dev/pi-blaster")
sleep(2)

os.system("echo \"23=0.1\" > /dev/pi-blaster")
#os.system("echo \"23=0\" > /dev/pi-blaster")
sleep(2)

os.system("echo \"23=0.2\" > /dev/pi-blaster")
sleep(1)
os.system("echo \"23=0\" > /dev/pi-blaster")
