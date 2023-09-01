#
# race_meet_loop_batch_2.py
#
# run the race_meet_loop_2 javascript, 20 rows at a time
# e.g., node ./race_meet_loop_2.js 100 120;

import os

for x in range(0, 160, 20):
    os.system("node ./race_meet_loop_2.js " + str(x) + " " + str(x + 20))

os.system("node ./race_meet_loop_2.js 160 170")

exit(0)



