#!/usr/bin/env python3
"""Verify actual targets, datasource, and all four panel queries."""
import base64, json, subprocess, urllib.request, urllib.parse
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def get(url, auth=False):
 r=urllib.request.Request(url)
 if auth:r.add_header('Authorization','Basic '+base64.b64encode(b'admin:admin').decode())
 return json.load(urllib.request.urlopen(r,timeout=15))
def save(name,data):
 (root/'logs'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
targets=get('http://localhost:9090/api/v1/targets');save('prometheus-targets.json',targets)
active=targets['data']['activeTargets']
assert len(active)==2 and all(t['health']=='up' for t in active), active
health=get('http://localhost:3000/api/datasources/uid/prometheus/health',True);save('grafana-datasource-health.json',health)
assert health['status']=='OK',health
save('grafana-dashboard.json',get('http://localhost:3000/api/dashboards/uid/lab3-system',True))
dashboard=json.loads((root/'grafana/dashboards/system.json').read_text())
for i,panel in enumerate(dashboard['panels']):
 data=get('http://localhost:9090/api/v1/query?'+urllib.parse.urlencode({'query':panel['targets'][0]['expr']}));save(f'query-{i+1}.json',data)
 assert data['status']=='success' and data['data']['result'],panel['title']
 assert all(r['value'][1] not in ('NaN','+Inf','-Inf') for r in data['data']['result'])
 print(panel['title']+': '+str(len(data['data']['result']))+' series, OK')
for filename,args in [('containers.txt',['ps']),('promtool.txt',['exec','-T','prometheus','promtool','check','config','/etc/prometheus/prometheus.yml'])]:
 output=subprocess.check_output(['docker','compose','-f',str(root/'compose.yaml')]+args,text=True)
 (root/'logs'/filename).write_text(output)
print('Both targets UP; Grafana datasource OK; configuration valid.')
