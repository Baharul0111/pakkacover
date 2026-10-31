#!/usr/bin/env python3
"""Commit a completed piece, then commit its resumable tracking entry."""
import argparse, subprocess, re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
p=argparse.ArgumentParser(); p.add_argument('--step',required=True); p.add_argument('--next',required=True); p.add_argument('--done',required=True); p.add_argument('--tests',default='not yet run'); p.add_argument('--problems',default='none'); p.add_argument('--paytm',default='simulated — keys not yet verified'); p.add_argument('--processes',default='None. Inspect `.run/` PID files; stop with `scripts/run_demo --stop` once implemented.'); p.add_argument('--run',default='`.venv/bin/python -m uvicorn apps.api.app.main:app --host 0.0.0.0 --port 8000` (once shell exists); final `scripts/run_demo`'); p.add_argument('--test-command',default='`.venv/bin/python -m pytest -q`'); a=p.parse_args()
def git(*args): return subprocess.check_output(['git',*args],text=True).strip()
subprocess.run(['git','add','-A'],check=True)
if git('diff','--cached','--name-only'):
 subprocess.run(['git','commit','-m',a.done[:100]],check=True)
sha=git('rev-parse','--short','HEAD'); now=datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST')
pth=Path('TRACKING.md'); txt=pth.read_text()
resume=f"## Resume here\n- Time: {now}. {a.step}.\n- Next action: {getattr(a,'next')}\n- Run app: {a.run}\n- Run tests: {a.test_command}\n- Background processes: {a.processes}\n- Done and verified / half-done: {a.done}; verification: {a.tests}. The next action above identifies unfinished work.\n- Open problems and decisions: {a.problems}\n- Paytm mode: {a.paytm}.\n\n"
txt=re.sub(r'## Resume here\n.*?(?=## Implementation log)',lambda _:resume,txt,flags=re.S)
entry=f'- {now} | {a.step} | {a.done} | Tests: {a.tests} | Commit: `{sha}`\n'
pos=txt.index('## Implementation log')+len('## Implementation log')
# Keep historical orientation below implementation entries.
marker='\n## Original orientation notes'
end=txt.find(marker,pos)
if end<0:end=txt.find('\nUpdated: 2026-10-31 (Asia/Kolkata)',pos)
if end<0: end=len(txt)
txt=txt[:end].rstrip()+'\n'+entry+'\n'+txt[end:].lstrip('\n')
pth.write_text(txt)
subprocess.run(['git','add','-A'],check=True); subprocess.run(['git','commit','-m','Update resumable build checkpoint'],check=True)
print(f'Checkpoint {now}; implementation {sha}')
