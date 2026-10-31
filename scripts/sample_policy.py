#!/usr/bin/env python3
"""Explicit CLI export of a synthetic policy, never a real buyer upload."""
import argparse,sys
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from apps.api.app.sample_policy import make_policy,VARIANTS
from apps.api.app.engine.rules import plans
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--variant',choices=sorted(VARIANTS),default='clean');p.add_argument('--out',required=True);a=p.parse_args()
 Path(a.out).write_bytes(make_policy(plans()['care_supreme_ic'],{'age':52,'sex':'F'},['hypertension'],date(2026,10,31),a.variant));print('Synthetic sample policy exported')
