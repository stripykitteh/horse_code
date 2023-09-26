#
# sectional_loop_batch_final.py
#
# Run the sectional_loop_final javascript, 10 rows at a time
# e.g., node ./meets_loop_final.js 100 110;
#
# There are 137 meets to scrape.
#

import os

for x in range(0, 1300, 10):
    os.system("node ./sectional_loop_final.js " + str(x) + " " + str(x + 10))

os.system("node ./sectional_loop_final.js 1300 1301")

exit(0)
