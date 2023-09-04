//
// sectional_loop.js
// -----------------
//
// loop through a list of sectionals and store the relevant
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
csv = '/Users/phillipmonk/research_paper/data/races_sorted.csv'
var sectionals = fs.readFileSync(csv)
    .toString()
    .split('\n')
    .map(e => e.trim())

page_root = 'https://racing.com/form/';

// Start of for loop, to loop through csv file
for (let sectional_no = arg[0]; sectional_no < arg[1]; sectional_no++) {

    (async () => { 
	const browser = await chromium.launch({headless: false, args:['--start-maximized']});
	const context = await browser.newContext( { viewport: null } );
	const page = await context.newPage();
	
	var sectional_arr = sectionals[sectional_no].split(',');
	sectional_stub = sectional_arr[0] + '/' + sectional_arr[1] + '/race/' + sectional_arr[2] + "#/sectionals";
	target_page = page_root + sectional_stub;
	// Navigate to a website
	console.log('Read: ' + sectional_no + ' ' + target_page);
	var sectional_stub_under = sectional_stub.replaceAll('/', '_');
	console.log('target_page=>' + target_page);
	await page.goto(target_page, {timeout: 0});
	
	const html = await page.content();

	fs.writeFile('/Users/phillipmonk/research_paper/html/sectionals/racing_com_form_' + sectional_stub_under + '.html', html, err => {
	    if (err) {
		console.error(err);
	    }
	    // file written successfully
	});

	await browser.close();
    
    })();
}
