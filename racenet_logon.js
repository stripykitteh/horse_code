//
// sectional_loop.js
// -----------------
//


const { chromium } = require('playwright');
var fs = require('fs');


(async () => { 
    const browser = await chromium.launch({headless: false, args:['--start-maximized']});
    const context = await browser.newContext( { viewport: null } );
    const page = await context.newPage();
    
    target_page = "https://myaccount.racenet.com.au/s/"
    // Navigate to a website
    console.log('Read: ' + target_page);
    console.log('target_page=>' + target_page);
    await page.goto(target_page, {timeout: 0});
    
    const html = await page.content();
    
    await browser.close();
    
})();

