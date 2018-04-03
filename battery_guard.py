#!/usr/bin/env python3
import subprocess
import time
import shelve
from datetime import datetime
try:
    # Open data storage file for value of count
    data = shelve.open("data.dat")
    print("Cycle No.: ", data['count'])
except KeyError:
    # In case of first run
    data['count'] = 0
    data['high_flag'] = False
    data['low_flag'] = False

while True:
    # Keep it running

    # deep_mode occurs on each 100 count
    deep_mode = False
    if data['count'] >= 100:
        deep_mode = True

    # Get current battery juice
    current = int(open("/sys/class/power_supply/BAT0/capacity").read().strip())

    # Get Charge/Discharge status
    status = open("/sys/class/power_supply/BAT0/status").read().strip()

    # If deep mode, let it discharge till 10% else let it go till 40%
    low_thresh = 10 if deep_mode else 40

    # if deep mode, let it charge till 100% else let it go till 80%
    high_thresh = 100 if deep_mode else 80

    # if current is lesser then low_threshold value and if it's discharging
    if current <= low_thresh and status == "Discharging":
        # tell it that I've been lowest
        if deep_mode:
            data['low_flag'] = True

        # Log with current low count with date and time
        data[str((data['count'], 'low_at'))] = datetime.now()

        # print the current cycle detail on console, works if run on terminal, settings in README
        # will make it divert to log.txt
        # detail will contain Sr. No. of last cycle and time it powered the machine
        print("Cycle ", data['count'], ":\t",
              data[str((data['count'], 'low_at'))]-data[str((data['count'], 'high_at'))])

        # status variable for looping while being discharged
        status = open("/sys/class/power_supply/BAT0/status").read().strip()
        while status == "Discharging":
            # play the sound every 10 secs until its plugged in
            subprocess.check_output(["aplay", '-q', 'low_1.wav'])
            time.sleep(10)
            # update the status value
            status = open("/sys/class/power_supply/BAT0/status").read().strip()

    # if current is higher than maximum charge threshold and it's charging
    elif current >= high_thresh and status == "Charging":
        # tell it that I've been highest
        if deep_mode:
            data['high_flag'] = True

        # Log with current low count with date and time
        data[str((data['count'], 'high_at'))] = datetime.now()

        # status variable for looping while being charged
        status = open("/sys/class/power_supply/BAT0/status").read().strip()
        while status == "Charging":
            # play the sound every 10 secs until its plugged out
            subprocess.check_output(['aplay', '-q', 'full_1.wav'])
            time.sleep(10)
            # update the status value
            status = open("/sys/class/power_supply/BAT0/status").read().strip()

    # If it's been highest and lowest
    if data['high_flag'] and data['low_flag']:
        # if it was in deep mode(count=100), set count to 0
        if deep_mode:
            data['count'] = 0

        # else increase the count by 1, and mark a cycle to be completed as such
        else:
            data['count'] += 1
            data['high_flag'] = False
            data['low_flag'] = False
            deep_mode = False
    else: # Let's keep it this way
        if deep_mode:
            # wait for 10 seconds before checking the values again
            time.sleep(10)
        else:
            # wait for 5 seconds before checking the values again
            time.sleep(5)