#
# race_loop_batch_redo.py
#
# Run the race_loop_redo javascript, 10 rows at a time
# e.g., node ./race_loop_final.js 10 20;
#
#

import os

#for x in range(0, 12, 3):
#    os.system("node ./race_loop_redo.js " + str(x) + " " + str(x + 3))

os.system("node ./race_loop_redo.js 0 1")

exit(0)
