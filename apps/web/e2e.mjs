import {chromium} from '@playwright/test';
import fs from 'node:fs';
const began=Date.now(),base=process.argv[2]||'http://127.0.0.1:8000';
const full=process.argv.includes('--full'),record=process.argv.includes('--record');
const runsArg=process.argv.find(x=>x.startsWith('--runs='));const runs=runsArg?Number(runsArg.split('=')[1]):1;
const browser=await chromium.launch({headless:true});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,...(record?{recordVideo:{dir:'.run/rehearsal-video',size:{width:390,height:844}}}:{})});
const page=await context.newPage(),video=page.video(),errors=[],reports=[];
page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(25000);
fs.mkdirSync('.run/screenshots',{recursive:true});
let finished=false;
async function noOverflow(where){if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw new Error('Horizontal overflow: '+where);}
async function shot(where){await noOverflow(where);await page.screenshot({path:'.run/screenshots/'+where+'-mobile.png',fullPage:true});}
async function desktopShot(where){await page.setViewportSize({width:1440,height:1000});await noOverflow(where+' desktop');await page.screenshot({path:'.run/screenshots/'+where+'-desktop.png',fullPage:true});await page.setViewportSize({width:390,height:844});}
async function postResponse(suffix,click){const pending=page.waitForResponse(r=>r.url().endsWith(suffix)&&r.request().method()==='POST');await click();const r=await pending;if(!r.ok())throw new Error('API failed: '+suffix+' '+r.status());return r.json();}
try{
 // Avoid repeated TTS spend in the UI rehearsal; --live-voice separately uses real STT/extraction.
 await page.route('**/speak',route=>route.fulfill({status:204}));
 await page.goto(base,{waitUntil:'networkidle'});
 if(await page.getByRole('button',{name:'English',exact:true}).count())await page.getByRole('button',{name:'English',exact:true}).click();
 for(let run=1;run<=runs;run++){
  const started=Date.now(),audits=[];let voice={attempted:false,accepted:false,fallbackUsed:false};
  if(run>1){
   const oldJourney=await page.evaluate(()=>localStorage.getItem('pc_jid'));
   await page.getByRole('button',{name:'Menu',exact:true}).click();
   await postResponse('/reset',()=>page.getByRole('button',{name:'Reset demo',exact:true}).click());
   await page.getByRole('heading',{name:'Health cover, made clear.',exact:true}).waitFor();
   if(await page.evaluate(()=>localStorage.getItem('pc_jid'))===oldJourney)throw new Error('Reset did not replace journey');
   await page.getByRole('button',{name:'Notifications',exact:true}).click();await page.getByText('No notifications yet',{exact:true}).waitFor();await page.getByRole('button',{name:'Notifications',exact:true}).click();
  }
  await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:/I agree/}).click();
  await page.getByRole('heading',{name:'Who are we looking after?',exact:true}).waitFor();
  await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:'Continue',exact:true}).click();
  await page.getByRole('heading',{name:'Your height, in centimetres?',exact:true}).waitFor();
  if(run===1){await shot('talk');await desktopShot('talk');await page.getByRole('button',{name:/Your form/}).click();await page.locator('.live-form.drawer-open').waitFor();await shot('form-drawer');await page.getByRole('button',{name:/Your form/}).click();}
  const answers=['158','64','BP / hypertension','2019','Yes','No','Telma 40 mg','BP / hypertension','Once daily','None','None','No','No','No'];
  for(let i=0;i<answers.length;i++){
   if(full&&i===2&&process.env.PCC_E2E_AUDIO_B64){
    const out=await page.evaluate(async(encoded)=>{const f=new FormData();f.append('audio',new Blob([Uint8Array.from(atob(encoded),c=>c.charCodeAt(0))],{type:'audio/wav'}),'answer.wav');f.append('duration','6');const r=await fetch('/api/journeys/'+localStorage.getItem('pc_jid')+'/voice',{method:'POST',headers:{Authorization:'Bearer '+localStorage.getItem('pc_token'),'Idempotency-Key':crypto.randomUUID()},body:f});return r.json();},process.env.PCC_E2E_AUDIO_B64);
    voice={attempted:true,accepted:!!out.accepted,fallbackUsed:!out.accepted,source:out.source||'speech_or_media_fallback'};
    if(!out.accepted){if(!out.fallback)throw new Error('Speech failed without a fallback');await postResponse('/answer',()=>page.getByRole('button',{name:'BP / hypertension',exact:true}).click());}
    await page.reload({waitUntil:'networkidle'});await page.getByRole('heading',{name:/Since when/}).waitFor();
   }else if(full&&i===6){
    const encoded=await page.evaluate(()=>{const c=document.createElement('canvas');c.width=1000;c.height=500;const ctx=c.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,1000,500);ctx.fillStyle='black';ctx.font='48px Arial';['TELMA 40','Telmisartan Tablets IP','Each tablet contains:','Telmisartan 40 mg'].forEach((line,n)=>ctx.fillText(line,40,80+n*85));return c.toDataURL('image/png').split(',')[1];});
    const out=await postResponse('/photo',()=>page.locator('input[type=file][accept="image/*"]').setInputFiles({name:'synthetic-printed-strip.png',mimeType:'image/png',buffer:Buffer.from(encoded,'base64')}));
    if(out.status!=='agree')throw new Error('Synthetic printed strip readers did not agree');
    await page.getByRole('button',{name:/Telmisartan 40\s?mg/}).first().click();
    await page.getByRole('heading',{name:/What do you take this medicine for/}).waitFor();
   }else{
    await postResponse('/answer',()=>page.getByRole('button',{name:answers[i],exact:true}).click());
    await page.waitForTimeout(120);
   }
   await noOverflow('interview '+i);
  }
  await page.getByRole('heading',{name:'Does this look right?',exact:true}).waitFor();
  if(run===1)await shot('review');
  for(let i=0;i<15;i++){
   await page.getByRole('button',{name:'Sahi hai',exact:true}).click();
   await page.waitForFunction(n=>document.querySelector('.review-progress')?.textContent?.trim().startsWith(String(n)+' /'),i+1);
  }
  await page.getByRole('button',{name:'Compare sample plans',exact:true}).click();
  await page.getByRole('heading',{name:'What would each plan pay?',exact:true}).waitFor();
  const labels=await page.locator('.plan-label').allTextContents();if(labels.join(',')!=='Plan B,Plan C,Plan A')throw new Error('Ranking incorrect');
  if(await page.locator('.mini-timeline').count()!==3)throw new Error('Comparison timelines missing');
  await page.locator('.plan-card .text-button').first().click();if(!(await page.locator('.modal blockquote').textContent()).includes('31st day'))throw new Error('Comparison BP clause wrong');await page.getByRole('button',{name:'Close',exact:true}).click();
  await page.locator('.big-payout').first().click();await page.locator('.modal .calculation-row button').first().click();await page.locator('.modal blockquote').waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
  if(run===1){await shot('ranking');await desktopShot('ranking');}
  await page.getByRole('button',{name:'Make my Promise Card',exact:true}).first().click();await page.locator('.promise-card').waitFor();
  await page.getByRole('heading',{name:'Your upcoming dates',exact:true}).waitFor();
  await page.locator('.promise-row').filter({hasText:'Declared hypertension'}).click();if(!(await page.locator('.modal blockquote').textContent()).includes('31st day'))throw new Error('Promise BP clause wrong');await page.getByRole('button',{name:'Close',exact:true}).click();
  if(!(await page.locator('.promise-row').allTextContents()).some(x=>x.includes('30 November 2026')))throw new Error('Promise date missing');
  const download=page.waitForEvent('download');await page.getByRole('button',{name:'Add calendar',exact:true}).click();if((await download).suggestedFilename()!=='pakkacover-dates.ics')throw new Error('Calendar not downloaded');
  if(run===1){await shot('promise');await desktopShot('promise');}
  if(full){
   await page.getByRole('button',{name:'Pay ₹1 with Paytm',exact:true}).click();await page.getByLabel('Demo passphrase',{exact:true}).fill(process.env.DEMO_LOGIN_PASSPHRASE);
   await page.getByRole('button',{name:'Save and continue',exact:true}).click();await page.getByRole('heading',{name:'Pay for your health cover',exact:true}).waitFor();
   if(run===1)await shot('payment-sheet');
   const method=['UPI','Wallet','Card'][(run-1)%3];await page.getByRole('button',{name:method,exact:true}).click();
   await page.getByRole('button',{name:'Continue · ₹1',exact:true}).click();await page.getByRole('button',{name:'Pay ₹1',exact:true}).waitFor();
   await page.getByRole('button',{name:'Pay ₹1',exact:true}).click();await page.getByRole('heading',{name:'Payment successful via Paytm',exact:true}).waitFor();await page.locator('.phone-notification').waitFor();
   if(!(await page.locator('.payment-success .demo-chip').textContent()).includes('Demo'))throw new Error('Demo label missing');
   await page.getByRole('button',{name:'Notifications',exact:true}).click();await page.locator('.notification-list article').waitFor();if(await page.locator('.notification-list article').count()!==1)throw new Error('Duplicate notifications');await page.getByRole('button',{name:'Notifications',exact:true}).click();
   if(run===1)await shot('payment');
   await page.getByRole('button',{name:'Continue to policy check',exact:true}).click();
   for(const [variant,count] of [['m1_ped_addon_missing',1],['m2_declared_condition_missing',1],['m3_dob_wrong',1],['clean',0]]){
    await page.locator('.sample-picker select').selectOption(variant);
    const result=await postResponse('/audit',()=>page.getByRole('button',{name:'Check this sample',exact:true}).click());
    audits.push({variant,mode:result.extraction_mode,flags:result.flags.length,verifiedFields:result.verified_field_count});
    if(result.flags.length!==count)throw new Error('Audit fixture flag count: '+variant);
    await page.locator('.audit-results').waitFor();
    if(variant==='clean')await page.getByText('No differences found in verified fields',{exact:true}).waitFor();
    else{
     await page.locator('.audit-flag').first().waitFor();
     if(run===1&&variant==='m1_ped_addon_missing'){
      await shot('audit-mismatch');await desktopShot('audit-mismatch');
      await page.getByRole('button',{name:'Ask insurer to fix',exact:true}).first().click();await page.getByRole('heading',{name:'Ask insurer to fix',exact:true}).waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
      await page.getByRole('button',{name:/Cancel free by/}).first().click();await page.getByRole('heading',{name:'Free-look cancellation',exact:true}).waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
     }
    }
    await noOverflow('audit '+variant);
   }
   await page.getByRole('button',{name:'Advisor',exact:false}).last().click();await page.getByRole('heading',{name:'Callback request recorded',exact:true}).waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
   if(run===1)await shot('audit-clean');
  }
  if(errors.length)throw new Error('Browser errors: '+errors.join(';'));
  const report={run,passed:true,base,full,ranking:labels,browserErrors:errors.length,audits,voice,paymentMethod:full?['UPI','Wallet','Card'][(run-1)%3]:null,durationSeconds:Math.round((Date.now()-started)/1000)};
  reports.push(report);console.log(JSON.stringify(report));
 }
 const report={passed:true,runs:reports,totalSeconds:Math.round((Date.now()-began)/1000)};fs.mkdirSync('evals/results',{recursive:true});fs.writeFileSync('evals/results/browser-'+Date.now()+'.json',JSON.stringify(report,null,2));finished=true;
}finally{await context.close();if(finished&&record&&video)fs.copyFileSync(await video.path(),'.run/sunita-fallback.webm');await browser.close();}
