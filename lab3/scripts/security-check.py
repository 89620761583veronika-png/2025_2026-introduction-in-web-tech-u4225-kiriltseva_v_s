#!/usr/bin/env python3
"""Bounded checks of the lab's localhost target; preserve exact paths with curl."""
import subprocess, json, datetime, html
from pathlib import Path
root=Path(__file__).resolve().parents[1]
paths=['/../../../etc/passwd','/..%2F..%2F..%2Fetc%2Fpasswd','/....//....//....//etc/passwd','/docs/../../etc/passwd','/files/..%2F..%2Fetc%2Fpasswd','/files/%252e%252e%252fetc%252fpasswd','/missing-lab3-control','/.env','/config.php','/backup.sql','/config.bak','/index.html.old','/config.backup','/admin','/wp-admin','/phpmyadmin','/.git/config','/files/','/']
results=[]
for i,path in enumerate(paths):
 cmd=['curl','--path-as-is','--max-time','5','-sS','-i','http://127.0.0.1:8083'+path]
 p=subprocess.run(cmd,capture_output=True,text=True,check=True)
 (root/'logs'/f'security-{i+1:02}.txt').write_text('$ '+' '.join(cmd)+'\n'+p.stdout)
 results.append({'path':path,'response':p.stdout,'status':int(p.stdout.split()[1])})
(root/'logs/security-results.json').write_text(json.dumps({'time':datetime.datetime.now().astimezone().isoformat(),'results':results},indent=2))
for group,rows in [('traversal',results[:6]),('files',results[6:13]),('admin-headers',results[13:])]:
 body=''.join('<section><h2>'+html.escape(r['path'])+' — HTTP '+str(r['status'])+'</h2><pre>'+html.escape(r['response'])+'</pre></section>' for r in rows)
 (root/'logs'/f'{group}.html').write_text('<!doctype html><meta charset="utf-8"><title>Lab3: '+group+'</title><style>body{font:16px system-ui;margin:32px;background:#f5f7fa}section{background:white;border:1px solid #cbd5e1;padding:16px;margin:16px 0}pre{white-space:pre-wrap;font:13px monospace}h2{font-size:18px}</style><h1>Lab 3 — реальные HTTP-ответы: '+group+'</h1><p>Локальный учебный стенд http://127.0.0.1:8083 · команды curl --path-as-is</p>'+body)
print('\n'.join(str(r['status'])+' '+r['path'] for r in results))
