//
// trainer_loop.js
// -----------------
//
// loop through a list of trainers and store the relevant
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
csv = '/Users/phillipmonk/research_paper/horse_code/data/trainers.csv'
var trainers = fs.readFileSync(csv)
    .toString()
    .split('\n')
    .map(e => e.trim())

page_root = 'https://racing.com/trainers/';

// Start of for loop, to loop through csv file
for (let trainer_no = arg[0]; trainer_no < arg[1]; trainer_no++) {

    (async () => { 
	const browser = await chromium.launch({headless: false, args:['--start-maximized']});
	const context = await browser.newContext( { viewport: null } );
	const page = await context.newPage();
	
	var trainer_arr = trainers[trainer_no].split(',');
	trainer_stub = trainer_arr[0];
	target_page = page_root + trainer_stub;
	// Navigate to a website
	console.log('Read: ' + trainer_no + ' ' + target_page);
	var trainer_stub_under = trainer_stub.replaceAll('/', '_');
	console.log('target_page=>' + target_page);
	await page.goto(target_page, {timeout: 0});
	
	const html = await page.content();

	fs.writeFile('/Users/phillipmonk/research_paper/html/trainers/racing_com_trainers_' + trainer_stub_under + '.html', html, err => {
	    if (err) {
		console.error(err);
	    }
	    // file written successfully
	});

	await browser.close();
    
    })();
}
