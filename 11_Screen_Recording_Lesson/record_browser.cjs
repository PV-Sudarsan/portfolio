// From this folder: npm install playwright
// Then: npx playwright install chromium
// Then: node record_browser.cjs
// Produces a real browser recording, not a simulated storyboard.
const {chromium}=require('playwright');
const {pathToFileURL}=require('url');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1280,height:720},recordVideo:{dir:path.join(__dirname,'temporary_recording'),size:{width:1280,height:720}}});
 const page=await context.newPage();
 await page.goto(pathToFileURL(path.join(__dirname,'lesson_to_record.html')).href);
 await page.waitForTimeout(3000);await page.click('#next');
 await page.waitForTimeout(3000);await page.click('#next');
 await page.check('input[value="svg"]');await page.click('#quiz button');
 await page.waitForTimeout(3000);const video=page.video();
 await context.close();await video.saveAs(path.join(__dirname,'raw_recording.webm'));
 await browser.close();console.log('Saved raw_recording.webm. Run python edit_recording.py to export the edited MP4.');
})().catch(e=>{console.error(e);process.exitCode=1});
