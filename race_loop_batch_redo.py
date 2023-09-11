#
# race_loop_batch_redo.py
#
# Run the race_loop_redo javascript, 10 rows at a time
# e.g., node ./race_loop_final.js 10 20;
#
#

import os

for x in range(0, 10, 10):
    os.system("node ./race_loop_redo.js " + str(x) + " " + str(x + 10))

os.system("node ./race_loop_redo.js 10 13")

exit(0)
