"""Explicit research-only allowlist, private-path/link checks and byte manifest."""
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES=['.gitignore','.gitattributes','README.md','VERSION','project.yaml',
       'PIPELINE_STATE.md','CHANGELOG.md','RELEASE_NOTES.md','CONTRIBUTORS.md','THIRD_PARTY_NOTICES.md',
       'docs/DISTILLATION_PLAN.md','docs/MAINTENANCE.md',
       'research/BOOK_OVERVIEW.md','research/chapter-01.md','research/chapters-02-03.md',
       'research/chapters-04-05.md','research/chapters-06-appendix.md',
       'research/tasks.json','research/SOURCE_MANIFEST.json','research/SOURCE_CORRECTIONS.md',
       'evaluation/REPORT.md','logs/RUN.md',
       'scripts/inventory_source.py','scripts/build_research_index.py','scripts/freeze_public.py']

def freeze():
    selected=FILES+(['publication/RECEIPT.md'] if (ROOT/'publication/RECEIPT.md').exists() else [])
    rows=[]
    for rel in sorted(selected):
        p=ROOT/rel; data=p.read_bytes(); s=data.decode('utf-8')
        if re.search(r'[A-Za-z]:[\\/]',s):
            raise ValueError('Absolute Windows path in '+rel)
        if p.suffix=='.json': json.loads(s)
        if p.suffix=='.md':
            for dest in re.findall(r'\]\(([^)]+)\)',s):
                if re.match(r'^[a-z]+://',dest): continue
                target=dest.split('#')[0]
                if target and not (p.parent/target).resolve().exists():
                    raise ValueError(f'Broken link {rel}: {target}')
        rows.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                         git_blob_sha1=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()))
    report=dict(version='0.1.0',scope='stage-0 research only; no active skill',
                exclusions=['private/','OCR','PDF','scans','personal paths','render_source.py','ocr_windows.ps1'],
                hash_recursion='manifest and SHA256SUMS exclude themselves; both included in remote tree checks',
                git_object_format='sha1; compare against observed remote object ids before accepting',
                checks=dict(utf8=True,json_parse=True,relative_links=True,no_absolute_windows_paths=True),files=rows)
    out=ROOT/'publication'; out.mkdir(exist_ok=True)
    (out/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in rows),encoding='utf-8')
    print(json.dumps(dict(files=len(rows),bytes=sum(x['bytes'] for x in rows),checks=report['checks'])))
    return selected+['publication/manifest.json','SHA256SUMS']
if __name__=='__main__': freeze()
