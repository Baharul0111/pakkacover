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
   await page.getByRole('heading',{name:'Who is this cover for?',exact:true}).waitFor();
   if((await page.locator('.form-row strong').allTextContents()).some(v=>v&&v!=='—'))throw new Error('Reset form is not empty');
   if(await page.evaluate(()=>localStorage.getItem('pc_jid'))===oldJourney)throw new Error('Reset did not replace journey');
   await page.getByRole('button',{name:'Notifications',exact:true}).click();await page.getByText('No notifications yet',{exact:true}).waitFor();await page.getByRole('button',{name:'Notifications',exact:true}).click();
  }
  if(run===1){await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:/I agree/}).click();}
  await page.getByRole('heading',{name:'Who is this cover for?',exact:true}).waitFor();
  if(run===1){await shot('talk');await desktopShot('talk');await page.getByRole('button',{name:/Your form/}).click();await page.locator('.live-form.drawer-open').waitFor();await shot('form-drawer');await page.getByRole('button',{name:/Your form/}).click();}
  const answers=['Mother','I agree','Sunita','52','Female','5 foot 2','68 kilo','BP / hypertension','2019','Yes','No','Yes','Telma 40 mg','1 tablet','Once daily','BP / hypertension','None','None','No','No','No'];
  const groups=[1,1,2,3,4,5,6,7,7,7,7,7,8,8,8,8,9,10,11,11,12];
  for(let i=0;i<answers.length;i++){
   if((await page.locator('.question-count').textContent()).trim()!==groups[i]+' / 12')throw new Error('Question counter incorrect at '+i);
   if(full&&i===7&&process.env.PCC_E2E_AUDIO_B64){
    const out=await page.evaluate(async(encoded)=>{const f=new FormData();f.append('audio',new Blob([Uint8Array.from(atob(encoded),c=>c.charCodeAt(0))],{type:'audio/wav'}),'answer.wav');f.append('duration','6');const r=await fetch('/api/journeys/'+localStorage.getItem('pc_jid')+'/voice',{method:'POST',headers:{Authorization:'Bearer '+localStorage.getItem('pc_token'),'Idempotency-Key':crypto.randomUUID()},body:f});return r.json();},process.env.PCC_E2E_AUDIO_B64);
    voice={attempted:true,accepted:!!out.accepted,fallbackUsed:!out.accepted,source:out.source||'speech_or_media_fallback'};
    if(!out.accepted){if(!out.fallback)throw new Error('Speech failed without a fallback');await postResponse('/answer',()=>page.getByRole('button',{name:'BP / hypertension',exact:true}).click());}
    await page.reload({waitUntil:'networkidle'});await page.getByRole('heading',{name:/Since when/}).waitFor();
   }else if(full&&i===12){
    const encoded=await page.evaluate(()=>{const c=document.createElement('canvas');c.width=1000;c.height=500;const ctx=c.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,1000,500);ctx.fillStyle='black';ctx.font='48px Arial';['TELMA 40','Telmisartan Tablets IP','Each tablet contains:','Telmisartan 40 mg'].forEach((line,n)=>ctx.fillText(line,40,80+n*85));return c.toDataURL('image/png').split(',')[1];});
    const out=await postResponse('/photo',()=>page.locator('input[type=file][accept="image/*"]').setInputFiles({name:'synthetic-printed-strip.png',mimeType:'image/png',buffer:Buffer.from(encoded,'base64')}));
    if(out.status!=='agree')throw new Error('Synthetic printed strip readers did not agree');
    await page.getByRole('button',{name:/Telmisartan 40\s?mg/}).first().click();
    await page.getByRole('heading',{name:'What dose do you take each time?',exact:true}).waitFor();
   }else{
    const chip=page.getByRole('button',{name:answers[i],exact:true});
    if(await chip.count())await postResponse('/answer',()=>chip.click());
    else{
     if(!await page.locator('#answer-input').count())await page.getByRole('button',{name:'Type instead',exact:false}).click();
     await page.locator('#answer-input').fill(answers[i]);await postResponse('/answer',()=>page.getByRole('button',{name:'Send answer',exact:true}).click());
    }
    await page.waitForTimeout(120);
   }
   const fieldChecks={0:['relation','mother'],2:['name','Sunita'],3:['age','52'],4:['sex','F'],5:['height','157 cm'],6:['weight','68 kg'],7:['conditions','BP / hypertension'],8:['since','2019'],12:['medicine',full?'Telmisartan':'Telma'],16:['hospital','None'],17:['tests','None'],18:['tobacco','No'],19:['tobacco','No'],20:['family_history','No']};
   if(fieldChecks[i]){const [field,value]=fieldChecks[i];if(!(await page.locator('.form-row[data-field="'+field+'"] strong').textContent()).includes(value))throw new Error('Live form missing '+field);}
   if((await page.locator('.form-row strong').allTextContents()).some(v=>v.includes('Not sure')))throw new Error('Unexpected unknown value');
   await noOverflow('interview '+i);
  }
  await page.getByRole('heading',{name:'Does this look right?',exact:true}).waitFor();
  if(run===1)await shot('review');
  for(let i=0;i<20;i++){
   await page.getByRole('button',{name:'Sahi hai',exact:true}).click();
   await page.waitForFunction(n=>document.querySelector('.review-progress')?.textContent?.trim().startsWith(String(n)+' /'),i+1);
  }
  await page.getByRole('button',{name:'Compare sample plans',exact:true}).click();
  await page.getByRole('heading',{name:'What would each plan pay?',exact:true}).waitFor();
  const labels=await page.locator('.plan-label').allTextContents();if(labels.join(',')!=='Plan B,Plan C,Plan A')throw new Error('Ranking incorrect');
  if(await page.locator('.mini-timeline').count()!==3)throw new Error('Comparison timelines missing');
  const percents=await page.locator('.timeline-wait').evaluateAll(nodes=>nodes.map(n=>parseFloat(n.style.width)));
  if(!(percents[0]>0&&percents[0]<5&&percents[1]>60&&percents[1]<70&&percents[2]===100))throw new Error('Shared timeline positions incorrect');
  if((await page.locator('.for-you-row').count())!==10)throw new Error('For you summaries missing');
  await page.locator('.plan-card .text-button').first().click();if(!(await page.locator('.modal blockquote').textContent()).includes('31st day'))throw new Error('Comparison BP clause wrong');await page.getByRole('button',{name:'Close',exact:true}).click();
  await page.locator('.big-payout').first().click();await page.locator('.modal .calculation-row button').first().click();await page.locator('.modal blockquote').waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
  if(run===1){await shot('ranking');await desktopShot('ranking');}
  if(run===1){
   // While Compare is visible, emulate a corrected line arriving from another
   // request. Selection must return to that exact Check card, without an error.
   const changed=await page.evaluate(async()=>{const root='/api/journeys/'+localStorage.getItem('pc_jid'),h={Authorization:'Bearer '+localStorage.getItem('pc_token'),'Content-Type':'application/json'};const j=await(await fetch(root,{headers:h})).json();const line=j.lines.find(l=>l.key==='weight');await fetch('/api/lines/'+line.id+'/reopen',{method:'POST',headers:h});await fetch(root+'/answer',{method:'POST',headers:h,body:JSON.stringify({text:'68 kilo'})});return line.id;});
   await page.getByRole('button',{name:'Make my Promise Card',exact:true}).first().click();await page.getByRole('heading',{name:'Does this look right?',exact:true}).waitFor();
   if(!(await page.locator('.review-card').textContent()).includes('68'))throw new Error('Did not focus corrected line');
   if(await page.locator('.message.error').count())throw new Error('Confirmation redirect showed an error');
   await page.getByRole('button',{name:'Sahi hai',exact:true}).click();await page.getByRole('button',{name:'Compare sample plans',exact:true}).waitFor();await page.getByRole('button',{name:'Compare sample plans',exact:true}).click();await page.locator('.plans-grid').waitFor();
   for(const [label,id] of [['Plan C','tata_premier'],['Plan A','optima_secure'],['Plan B','care_supreme_ic']]){
    const article=page.locator('.plan-card').filter({has:page.locator('.plan-label',{hasText:label})});
    const selected=await postResponse('/select',()=>article.getByRole('button',{name:'Make my Promise Card',exact:true}).click());
    if(selected.plan_id!==id)throw new Error('Wrong Promise Card plan');await page.locator('.promise-card').waitFor();
    if(label!=='Plan B'){await page.getByRole('button',{name:'Back to plans',exact:true}).click();await page.locator('.plans-grid').waitFor();}
   }
  }else{await page.getByRole('button',{name:'Make my Promise Card',exact:true}).first().click();await page.locator('.promise-card').waitFor();}
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
