import csv
import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 20261108
random.seed(SEED)

p = Path('/Volumes/1tbinside/NOVA/external_data/real_events/independent_events_comparison_expanded/jma_gpm_daily_jst_aligned_v2.csv')
g = defaultdict(list)
with p.open() as f:
    for r in csv.DictReader(f):
        g[r['event']].append(float(r['nearest_difference_mm']))
events = sorted(g)
vals = []
for _ in range(2000):
    sample = [random.choice(events) for _ in events]
    vals.append(sum(sum(g[e]) for e in sample) / sum(len(g[e]) for e in sample))
vals.sort()
out = p.with_name('jma_gpm_daily_v2_event_bootstrap.json')
out.write_text(json.dumps({
    'status': 'EXPLORATORY_ONLY',
    'replicates': 2000,
    'events': len(events),
    'seed': SEED,
    'ci95_mm': [vals[50], vals[1949]],
    'formal_pass': False,
}, ensure_ascii=False, indent=2) + '\n')
print(out)
