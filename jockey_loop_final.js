//
// jockey_loop.js
// -----------------
//
// loop through a list of jockeys and store the relevant
// page on racing.com
//
// we take 2 different pages, 1 for current data, 1 for historic
//
// e.g., for jockey Kerrin McEvoy, these would be:
// 
// * https://www.racing.com/jockeys/kerrin-mcevoy/form
// * https://www.racing.com/jockeys/kerrin-mcevoy/stats
//
// take 2 arguments for the start and stop lines
//

const arg = process.argv.slice(2);

arg[0] = Number(arg[0]);
arg[1] = Number(arg[1]);

console.log('Scraping from ' + arg[0] + ' to ' + arg[1]);

const { chromium } = require('playwright');
var fs = require('fs');

// Reads the CSV file and saves it
csv = '/Users/phillipmonk/research_paper/horse_code/data/jockeys.csv'
var jockeys = fs.readFileSync(csv)
    .toString()
    .split('\n')
    .map(e => e.trim())

page_root = 'https://racing.com/jockeys/';

function slurp_jockey(sub_page) {

    // Start of for loop, to loop through csv file
    for (let jockey_no = arg[0]; jockey_no < arg[1]; jockey_no++) {

	(async () => { 
	    const browser = await chromium.launch({headless: false, args:['--start-maximized']});
	    const context = await browser.newContext( { viewport: null } );
	    const page = await context.newPage();
	
	    var jockey_arr = jockeys[jockey_no].split(',');
	    jockey_stub = jockey_arr[0] + "/" + sub_page;
	    target_page = page_root + jockey_stub;
	    
	    // Navigate to a website
	    console.log('Read: ' + jockey_no + ' ' + target_page);
	    var jockey_stub_under = jockey_stub.replaceAll('/', '_');
	    console.log('target_page=>' + target_page);
	    await page.goto(target_page, {timeout: 0});
	
	    const html = await page.content();

	    fs.writeFile('/Users/phillipmonk/research_paper/html/jockeys_final/racing_com_jockeys_' + jockey_stub_under + '.html', html, err => {
		if (err) {
		    console.error(err);
		}
		// file written successfully
	    });

	    await browser.close();
    
	})();
    } // slurp_jockey
}

slurp_jockey("form")
slurp_jockey("stats")
