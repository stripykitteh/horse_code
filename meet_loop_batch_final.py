#
# meet_loop_batch_final.py
#
# Run the meets_loop_final javascript, 10 rows at a time
# e.g., node ./meets_loop_final.js 100 110;
#
# There are 137 meets to scrape.
#

import os

for x in range(0, 130, 10):
    os.system("node ./meets_loop_final.js " + str(x) + " " + str(x + 10))

os.system("node ./meets_loop_final.js 130 137")

exit(0)
