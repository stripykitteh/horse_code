//
// race_meet_loop_2.js
// -------------------
//
// loop through a list of race meets and store the relevant
// page on racing.com
//
// take 2 arguments for the start and stop lines
//
// this is for the meetings that weren't loaded for various reasons on 13
// August
//

const arg = process.argv.slice(2);

arg[0] = Number(arg[0]);
arg[1] = Number(arg[1]);

console.log('Scraping from ' + arg[0] + ' to ' + arg[1]);

const { chromium } = require('playwright');
var fs = require('fs');

// Reads the CSV file and saves it
csv = '/Users/phillipmonk/research_paper/data/meeting_diffs_no_trials.csv'
var tracks = fs.readFileSync(csv)
    .toString()
    .split('\n')
    .map(e => e.trim())

page_root = 'https://racing.com/form/';

// Start of for loop, to loop through csv file
for (let meet_no = arg[0]; meet_no < arg[1]; meet_no++) {

    (async () => { 
	const browser = await chromium.launch({headless: true}) //false, args:['--start-maximized']});
	const context = await browser.newContext( { viewport: null } );
	const page = await context.newPage();
	
	var track_arr = tracks[meet_no].split(',');
	meet_stub = track_arr[0] + '/' + track_arr[1];
	target_page = page_root + meet_stub + '/';
	// Navigate to a website
	console.log('Read: ' + meet_no + ' ' + target_page);
	var meet_stub_under = meet_stub.replaceAll('/', '_');
	console.log('target_page=>' + target_page);
	await page.goto(target_page, {timeout: 0});
//	await page.screenshot({ path: '/Users/phillipmonk/research_paper/screenshots/racing_com_form_' + meet_stub_under + '.png' });
	
	const html = await page.content();

	fs.writeFile('/Users/phillipmonk/research_paper/html/meets_2/racing_com_form_' + meet_stub_under + '.html', html, err => {
	    if (err) {
		console.error(err);
	    }
	    // file written successfully
	});

	await browser.close();
    
    })();
}
