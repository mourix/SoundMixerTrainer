#import RPi.GPIO as GPIO
import subprocess
import time
import os

if __name__ == "__main__":
  #  GPIO.setmode(GPIO.BCM)

   # GPIO.setup(0, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    p = subprocess.Popen("C:/Users/M/Documents/GitHub/SoundMixerTrainer/App.py", shell=True)
    state = 1
    time.sleep(10)
    while(1):
    #    GPIO.wait_for_edge(0, GPIO.RISING)
        if state == 1:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            state == 0
            time.sleep(1)
        else:
            p = subprocess.Popen("C:/Users/M/Documents/GitHub/SoundMixerTrainer/App.py", shell=True, preexec_fn=os.setsid)
            state == 1
            time.sleep(1)
