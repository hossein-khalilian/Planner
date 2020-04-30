import os
import pause
from datetime import datetime, timedelta

python = "/usr/bin/python"
while True:
    os.system(python + ' ~/bin/DailyTime.py')
    pause.until(datetime.now() + timedelta(minutes=20))
    print()
