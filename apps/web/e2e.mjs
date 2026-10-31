import {chromium} from '@playwright/test';
import fs from 'node:fs';
const began=Date.now();const base=process.argv[2]||'http://127.0.0.1:8000';const full=process.argv.includes('--full');const record=process.argv.includes('--record');let finished=false;const auditEvidence=[];
const browser=await chromium.launch({headless:true});const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,...(record?{recordVideo:{dir:'.run/rehearsal-video',size:{width:390,height:844}}}:{})});
const page=await context.newPage();const video=page.video();const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(base,{waitUntil:'networkidle'});await page.getByRole('button',{name:'English',exact:true}).click();
 await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:/I agree/}).click();
 await page.getByRole('heading',{name:'Who are we looking after?',exact:true}).waitFor();await page.getByRole('checkbox').first().check();await page.getByRole('button',{name:'Continue',exact:true}).click();
 // Avoid speech spend during automated UI checks while preserving real backend interview controls.
 await page.route('**/speak',route=>route.fulfill({status:204}));
 const answers=['158','64','BP / hypertension','2019','Yes','No','Telma 40 mg','BP / hypertension','Once daily','None','None','No','No','No'];
 for(let i=0;i<answers.length;i++){
  if(full&&i===2&&process.env.PCC_E2E_AUDIO_B64){
   const out=await page.evaluate(async(encoded)=>{const bytes=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));const f=new FormData();f.append('audio',new Blob([bytes],{type:'audio/wav'}),'answer.wav');f.append('duration','6');const r=await fetch('/v1/journeys/'+localStorage.getItem('pc_jid')+'/voice',{method:'POST',headers:{Authorization:'Bearer '+localStorage.getItem('pc_token'),'Idempotency-Key':crypto.randomUUID()},body:f});return r.json();},process.env.PCC_E2E_AUDIO_B64);
   if(!out.accepted)throw new Error('Live speech slot was not preserved');
   await page.reload({waitUntil:'networkidle'});await page.getByRole('heading',{name:/Since when/}).waitFor();
  }else if(full&&i===6){
   const encoded=await page.evaluate(()=>{const c=document.createElement('canvas');c.width=1000;c.height=500;const ctx=c.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,1000,500);ctx.fillStyle='black';ctx.font='48px Arial';['TELMA 40','Telmisartan Tablets IP','Each tablet contains:','Telmisartan 40 mg'].forEach((line,n)=>ctx.fillText(line,40,80+n*85));return c.toDataURL('image/png').split(',')[1];});
   const response=page.waitForResponse(r=>r.url().endsWith('/photo')&&r.request().method()==='POST');
   await page.locator('input[type=file][accept="image/*"]').setInputFiles({name:'synthetic-printed-strip.png',mimeType:'image/png',buffer:Buffer.from(encoded,'base64')});
   const out=await(await response).json();if(out.status!=='agree')throw new Error('Synthetic printed strip readers did not agree');
   await page.getByRole('button',{name:/Telmisartan 40\s?mg/}).first().click();
   await page.getByRole('heading',{name:/What do you take this medicine for/}).waitFor();
  }else{
   const response=page.waitForResponse(r=>r.url().endsWith('/answer')&&r.request().method()==='POST');await page.getByRole('button',{name:answers[i],exact:true}).click();await response;await page.waitForTimeout(100);
  }
 }
 await page.getByRole('heading',{name:'Does this look right?',exact:true}).waitFor();
 for(let i=0;i<14;i++){await page.getByRole('button',{name:'Sahi hai — confirm this line',exact:true}).click();await page.waitForFunction(n=>document.querySelector('.review-progress')?.textContent?.trim().startsWith(String(n)+' /'),i+1);}
 await page.getByRole('button',{name:'Explore sample plan payouts',exact:true}).click();
 await page.getByRole('heading',{name:'See what the examples pay.',exact:true}).waitFor();
 const labels=await page.locator('.plan-label').allTextContents();if(labels.join(',')!=='Plan B,Plan C,Plan A')throw new Error('Ranking order incorrect');
 await page.locator('.big-payout').first().click();await page.locator('.modal .calculation-row button').first().click();await page.locator('blockquote').waitFor();await page.getByRole('button',{name:'Close',exact:true}).click();
 fs.mkdirSync('.run/screenshots',{recursive:true});await page.screenshot({path:'.run/screenshots/ranking-mobile.png',fullPage:true});
 await page.getByRole('button',{name:'Make my Promise Card',exact:true}).first().click();await page.locator('.promise-card').waitFor();
 await page.getByRole('heading',{name:'Your upcoming dates',exact:true}).waitFor();
 await page.locator('.promise-row').filter({hasText:'Declared hypertension'}).click();if(!(await page.locator('blockquote').textContent()).includes('31st day'))throw new Error('BP date did not cite Instant Cover clause');await page.getByRole('button',{name:'Close',exact:true}).click();
 const dates=await page.locator('.promise-row').allTextContents();if(!dates.some(x=>x.includes('30 November 2026')))throw new Error('Promise date missing');
 await page.screenshot({path:'.run/screenshots/promise-mobile.png',fullPage:true});
 if(full){
  await page.getByRole('button',{name:'Continue to ₹1 test payment',exact:true}).click();
  await page.getByLabel('Demo passphrase',{exact:true}).fill(process.env.DEMO_LOGIN_PASSPHRASE);
  await page.getByRole('button',{name:'Save and continue',exact:true}).click();
  await page.getByRole('button',{name:'Create test order',exact:true}).click();await page.locator('.order-status').waitFor();
  if(await page.getByRole('button',{name:'Complete simulated payment',exact:true}).count()){
   await page.getByRole('button',{name:'Complete simulated payment',exact:true}).click();await page.getByText('Simulation complete — no payment was made',{exact:true}).waitFor();
  }else throw new Error('Real-staging payment requires test instrument interaction; automated simulation test not applicable');
  await page.getByRole('button',{name:'Continue to policy check',exact:true}).click();
  for(const [variant,count] of [['m1_ped_addon_missing',2],['m2_declared_condition_missing',1],['m3_dob_wrong',1],['clean',0]]){
   await page.locator('.field-label select').selectOption(variant);const pending=page.waitForResponse(r=>r.url().endsWith('/audit')&&r.request().method()==='POST');await page.getByRole('button',{name:'Check this sample',exact:true}).click();const result=await(await pending).json();auditEvidence.push({variant,mode:result.extraction_mode,flags:result.flags.length,verifiedFields:result.verified_field_count});if(variant==='clean'?result.flags.length!==0:!result.flags.some(f=>f.status==='mismatch'))throw new Error('Audit result did not match fixture');await page.locator('.audit-results').waitFor();
   if(variant==='clean'){await page.getByText('No differences found in verified fields',{exact:true}).waitFor();}else if(await page.locator('.audit-flag').count()<1)throw new Error('Planted mismatch missed');
  }
  await page.screenshot({path:'.run/screenshots/audit-mobile.png',fullPage:true});
 }
 if(errors.length)throw new Error('Browser runtime errors: '+errors.join(';'));
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);if(overflow)throw new Error('Mobile horizontal overflow');
 const report={passed:true,base,full,ranking:labels,browserErrors:errors.length,audits:auditEvidence,durationSeconds:Math.round((Date.now()-began)/1000)};fs.mkdirSync('evals/results',{recursive:true});fs.writeFileSync('evals/results/browser-'+Date.now()+'.json',JSON.stringify(report,null,2));finished=true;console.log(JSON.stringify(report));
}finally{await context.close();if(finished&&record&&video){fs.copyFileSync(await video.path(),'.run/sunita-fallback.webm');}await browser.close();}
