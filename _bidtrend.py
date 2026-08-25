import subprocess, json, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
snap = {}
for c in subprocess.run(['git','log','--format=%H','--','naver_kw_bidest_data.js'], capture_output=True).stdout.decode().split():
    raw = subprocess.run(['git','show',c+':naver_kw_bidest_data.js'], capture_output=True).stdout.decode('utf-8','replace')
    try: d = json.loads(raw[raw.index('=')+1:].rstrip().rstrip(';\n '))
    except Exception: continue
    if d['day'] in snap: continue
    snap[d['day']] = {r['kw']: r.get('bid',0) for r in d['rows'] if r['device']=='MO'}
print('TOP50 모바일 입찰가 추이')
print('%-12s %6s %9s   %s' % ('대상일','대상수','평균입찰가','최빈값'))
for day in sorted(snap):
    b = [v for v in snap[day].values() if v]
    if not b: continue
    c = Counter(b).most_common(3)
    print('%-12s %6d %9s   %s' % (day, len(b), format(round(sum(b)/len(b)),','),
          ' · '.join('%s원×%d' % (format(k,','), n) for k,n in c)))
