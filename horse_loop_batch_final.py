#
# horse_loop_batch_final.py
#
# Run the horse_loop_final javascript, 10 rows at a time
# e.g., node ./horse_loop_final.js 100 120;
#
# There are 4348 races to scrape.
#

import os

for x in range(0, 4340, 10):
    os.system("node ./horse_loop_final.js " + str(x) + " " + str(x + 10))

os.system("node ./horse_loop_final.js 4340 4348")

exit(0)
