#
# race_loop_batch.py
#
# run the race_loop javascript, 20 rows at a time
# e.g., node ./race_loop.js 100 120;

import os

for x in range(0, 12720, 20):
    os.system("node ./race_loop.js " + str(x) + " " + str(x + 20))

os.system("node ./race_loop.js 12720 12738")

exit(0)



