#
# jockey_loop_batch_final.py
#
# Run the jockey_loop_final javascript, 10 rows at a time
# e.g., node ./jockey_loop_final.js 100 105;
#
# There are 253 jockeys to scrape.
#

import os

for x in range(0, 250, 5):
    os.system("node ./jockey_loop_final.js " + str(x) + " " + str(x + 5))

os.system("node ./jockey_loop_final.js 250 253")

exit(0)
