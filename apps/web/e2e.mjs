import {chromium} from '@playwright/test';
import fs from 'node:fs';
const base=process.argv[2]||'http://127.0.0.1:8000';const full=process.argv.includes('--full');
const browser=await chromium.launch({headless:true});const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(base,{waitUntil:'networkidle'});await page.getByRole('button',{name:'English',exact:true}).click();
 await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:/I agree/}).click();
 await page.getByRole('heading',{name:'Who are we looking after?',exact:true}).waitFor();await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:'Continue',exact:true}).click();
 // Avoid speech spend during automated UI checks while preserving real backend interview controls.
 await page.route('**/speak',route=>route.fulfill({status:204}));
 const answers=['158','64','BP / hypertension','2019','Yes','No','Telma 40 mg','BP / hypertension','Once daily','None','None','No','No','No'];
 for(const answer of answers){const response=page.waitForResponse(r=>r.url().endsWith('/answer')&&r.request().method()==='POST');await page.getByRole('button',{name:answer,exact:true}).click();await response;await page.waitForTimeout(80);}
 await page.getByRole('heading',{name:'Does this look right?',exact:true}).waitFor();
 for(let i=0;i<14;i++){await page.getByRole('button',{name:'Sahi hai — confirm this line',exact:true}).click();await page.waitForFunction(n=>document.querySelector('.review-progress')?.textContent?.trim().startsWith(String(n)+' /'),i+1);}
 await page.getByRole('button',{name:'Explore sample plan payouts',exact:true}).click();
 await page.getByRole('heading',{name:'See what the examples pay.',exact:true}).waitFor();
 const labels=await page.locator('.plan-label').allTextContents();if(labels.join(',')!=='Plan B,Plan C,Plan A')throw new Error('Ranking order incorrect');
 await page.locator('.big-payout').first().click();await page.locator('.modal .calculation-row button').first().click();await page.locator('blockquote').waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
 fs.mkdirSync('.run/screenshots',{recursive:true});await page.screenshot({path:'.run/screenshots/ranking-mobile.png',fullPage:true});
 await page.getByRole('button',{name:'Make my Promise Card',exact:true}).first().click();await page.locator('.promise-card').waitFor();
 await page.getByRole('heading',{name:'Your upcoming dates',exact:true}).waitFor();
 const dates=await page.locator('.promise-row').allTextContents();if(!dates.some(x=>x.includes('30 November 2026')))throw new Error('Promise date missing');
 await page.screenshot({path:'.run/screenshots/promise-mobile.png',fullPage:true});
 if(full){
  await page.getByRole('button',{name:'Continue to ₹1 test payment',exact:true}).click();
  await page.getByLabel('Demo passphrase',{exact:true}).fill(process.env.DEMO_LOGIN_PASSPHRASE);
  await page.getByRole('button',{name:'Save and continue',exact:true}).click();
  await page.getByRole('button',{name:'Create test order',exact:true}).click();
  if(await page.getByRole('button',{name:'Complete simulated payment',exact:true}).count()){
   await page.getByRole('button',{name:'Complete simulated payment',exact:true}).click();await page.getByText('Simulation complete — no payment was made',{exact:true}).waitFor();
  }else throw new Error('Real-staging payment requires test instrument interaction; automated simulation test not applicable');
  await page.getByRole('button',{name:'Continue to policy check',exact:true}).click();
  for(const [variant,count] of [['m1_ped_addon_missing',2],['m2_declared_condition_missing',1],['m3_dob_wrong',1],['clean',0]]){
   await page.locator('.field-label select').selectOption(variant);await page.getByRole('button',{name:'Check this sample',exact:true}).click();await page.locator('.audit-results').waitFor();
   if(variant==='clean'){await page.getByText('No differences found in verified fields',{exact:true}).waitFor();}else if(await page.locator('.audit-flag').count()<1)throw new Error('Planted mismatch missed');
  }
  await page.screenshot({path:'.run/screenshots/audit-mobile.png',fullPage:true});
 }
 if(errors.length)throw new Error('Browser runtime errors: '+errors.join(';'));
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);if(overflow)throw new Error('Mobile horizontal overflow');
 console.log(JSON.stringify({passed:true,base,full,ranking:labels,browserErrors:errors.length}));
}finally{await browser.close();}
