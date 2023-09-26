//
// meets_loop.js
// -----------------
//
// loop through a list of meets and store the top level
// page from racenet.com
//
// take 2 arguments for the start and stop lines
//
// there are 137 meets to fetch
//
// once we have the meet data we know the URLs for the individual races
// and we can fetch the sectional data from there
//

const arg = process.argv.slice(2);

arg[0] = Number(arg[0]);
arg[1] = Number(arg[1]);

console.log('Scraping from ' + arg[0] + ' to ' + arg[1]);

const { chromium } = require('playwright');
var fs = require('fs');

// Reads the CSV file and saves it
csv = '/Users/phillipmonk/research_paper/horse_code/data/meets_final.csv'
var meets = fs.readFileSync(csv)
    .toString()
    .split('\n')
    .map(e => e.trim())

page_root = 'https://racing.com/form/';

page_root = 'https://www.racenet.com.au/form-guide/horse-racing/';

// rosehill-gardens-20230805/all-races

// Start of for loop, to loop through csv file
for (let meet_no = arg[0]; meet_no < arg[1]; meet_no++) {

    (async () => { 
	const browser = await chromium.launch({headless: false, args:['--start-maximized']});
	const context = await browser.newContext( { viewport: null } );
	const page = await context.newPage();
	
	var meet_arr = meets[meet_no].split(',');
	meet_stub = meet_arr[1] + '-' + meet_arr[0] + "/all-races";
	target_page = page_root + meet_stub;
	// Navigate to a website
	console.log('Read: ' + meet_no + ' ' + target_page);
	var meet_stub_under = meet_stub.replaceAll('/', '_');
	console.log('target_page=>' + target_page);
	await page.goto(target_page, {timeout: 0});
	
	const html = await page.content();

	fs.writeFile('/Users/phillipmonk/research_paper/html/meets/racenet_com_form_' + meet_stub_under + '.html', html, err => {
	    if (err) {
		console.error(err);
	    }
	    // file written successfully
	});

	await browser.close();
    
    })();
}
