#!/usr/bin/env python3
"""Run browser QA with secrets only in the child environment, never stdout or argv."""
import os,subprocess,sys
from pathlib import Path
from dotenv import dotenv_values
ROOT=Path(__file__).resolve().parents[1]
env={**os.environ,**{k:v for k,v in dotenv_values(ROOT/'.env').items() if v is not None}}
raise SystemExit(subprocess.call(['node',str(ROOT/'apps/web/e2e.mjs'),*sys.argv[1:]],cwd=ROOT,env=env))
