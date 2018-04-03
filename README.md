# battery_guard #

The application which helps you maximise your battery life. Keeping your battery levels between 80% and 40% (Recommended range). It will let it discharge and charge to 10% and 100% respectively after every 100th cycle.

### How do I get set up? ###
* Need to have python3 installed on your system.
* Tested on Ubuntu 17.04, should work with most Linux systems.
* For Ubuntu 17.04, Open `Startup Application Preferences` then click `Add`  
Type `battery_guard` in name,  
Enter `/bin/bash -c "sleep 15 && cd /full/path/to/battery_guard/; ./battery_guard.py >> /full/path/to/battery_guard/out.txt"`