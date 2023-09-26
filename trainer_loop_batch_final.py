#
# trainer_loop_batch_final.py
#
# Run the trainer_loop_final javascript, 5 rows at a time
# e.g., node ./trainer_loop_final.js 100 105;
#
# There are 545 trainers to scrape.
#

import os

for x in range(0, 545, 5):
    os.system("node ./trainer_loop_final.js " + str(x) + " " + str(x + 5))

# os.system("node ./trainer_loop_final.js 250 253")

exit(0)
