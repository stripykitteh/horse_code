#
# race_meet_loop_batch.py
#
# run the race_meet_loop javascript, 20 rows at a time
# e.g., node ./race_meet_loop.js 100 120;

import os

for x in range(0, 1940, 20):
    os.system("node ./race_meet_loop.js " + str(x) + " " + str(x + 20))

exit(0)



