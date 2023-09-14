//
// race_loop_redo.js
// -----------------
//
// loop through a list of races and store the relevant
// page on racing.com
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
csv = '/Users/phillipmonk/research_paper/horse_code/data/races_redo.csv'
var races = fs.readFileSync(csv)
    .toString()
    .split('\n')
    .map(e => e.trim())

page_root = 'https://racing.com/form/';

// Start of for loop, to loop through csv file
for (let race_no = arg[0]; race_no < arg[1]; race_no++) {

    (async () => { 
	const browser = await chromium.launch({headless: false, args:['--start-maximized']});
	const context = await browser.newContext( { viewport: null } );
	const page = await context.newPage();
	
	var race_arr = races[race_no].split(',');
	race_stub = race_arr[0] + '/' + race_arr[1] + '/race/' + race_arr[2];
	target_page = page_root + race_stub;
	// Navigate to a website
	console.log('Read: ' + race_no + ' ' + target_page);
	var race_stub_under = race_stub.replaceAll('/', '_');
	console.log('target_page=>' + target_page);
	await page.goto(target_page, {timeout: 0});
	
	const html = await page.content();

	fs.writeFile('/Users/phillipmonk/research_paper/html/races_final/racing_com_form_' + race_stub_under + '.html', html, err => {
	    if (err) {
		console.error(err);
	    }
	    // file written successfully
	});

	await browser.close();
    
    })();
}
