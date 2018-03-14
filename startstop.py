import RPi.GPIO as GPIO
import subprocess
import time
import os
import sys

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(0, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while (1):
        time.sleep(2)
        GPIO.wait_for_edge(0, GPIO.RISING)
        print("hallo")
        p = subprocess.Popen("sudo python3 /home/pi/SoundMixerTrainer/App.py", shell=True, preexec_fn=os.setsid)
        time.sleep(1)
        sys.exit()
