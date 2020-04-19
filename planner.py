#!/home/hse/henv/bin/python
import os
import pause
from datetime import datetime, timedelta

python = "/home/hse/henv/bin/python"
while True:
    os.system(python + ' ~/bin/DailyTime.py')
    pause.until(datetime.now() + timedelta(minutes=20))
    print()
