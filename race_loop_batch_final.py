#
# race_loop_batch_final.py
#
# Run the race_loop_final javascript, 10 rows at a time
# e.g., node ./race_loop_final.js 100 120;
#
# There are 1301 races to scrape.
#

import os

for x in range(20, 1300, 10):
    os.system("node ./race_loop_final.js " + str(x) + " " + str(x + 10))

os.system("node ./race_loop_final.js 1300 1301")

exit(0)
