"""Inventory the two registered snapshots; no raw OCR or image enters public report."""
from pathlib import Path
import argparse, hashlib, json
import pymupdf

def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    a=argparse.ArgumentParser()
    a.add_argument('primary',type=Path)
    a.add_argument('--alternate',type=Path)
    a.add_argument('--out',type=Path,default=Path('research/SOURCE_MANIFEST.json'))
    args=a.parse_args()
    sources=[]; docs=[]
    for role,p in [('primary',args.primary),('supplement',args.alternate)]:
        if p is None: continue
        d=pymupdf.open(p); docs.append(d)
        sources.append(dict(role=role,filename=p.name,bytes=p.stat().st_size,
                            sha256=sha(p.read_bytes()),pdf_pages=len(d)))
    expected=['cb8dd00db1c33abcea800df5933962c5a1bafa1975e18839ee0a58818ba2fdc9',
              '2bf9a09bc7dfe9107cb6e3d1f644804913464255b02a4a1ec2b7adc851734c6f']
    if [s['sha256'] for s in sources] != expected:
        raise ValueError('This ledger requires both registered snapshots; new sources need separate visual review.')
    pages=[]
    for i,p in enumerate(docs[0]):
        row=dict(pdf_page=i+1,printed_page_inferred=i-6 if i>=7 else None,
                 printed_mapping='inferred +7; chapter boundaries and selected folios visually checked',
                 image_objects=len(p.get_images()),content_streams=len(p.get_contents()))
        o=Path(f'private/extracted/page-{i+1:03}.json')
        if o.exists():
            j=json.loads(o.read_text(encoding='utf-8-sig'))
            row['ocr_nonspace_chars']=len(''.join(j['lines']).replace(' ',''))
            row['ocr_sha256']=sha(o.read_bytes())
        row['status']='image_present_unverified' if row['image_objects'] else 'empty_page'
        if i+1 in [80,99,116,117,118]: row['status']='missing_substantive_page'
        if i+1==401: row['status']='trailing_blank'
        if len(docs)>1:
            q=docs[1][i]
            if p.get_images() and q.get_images():
                row['same_render_as_alternate']=sha(p.get_pixmap().samples)==sha(q.get_pixmap().samples)
            if not p.get_images() and q.get_images():
                row['supplement_available']=True
                row['status']='supplement_visually_accepted_2026-11-06'
        pages.append(row)
    report=dict(schema_version=1,title='伪随机序列及其应用',
                authors=['肖国镇','梁传甲','王育民'],publication='国防工业出版社，1985-03第一版第一次印刷',
                source_status='source_hold',public_distribution=False,sources=sources,
                missing_primary_pdf_pages=[80,99,116,117,118],
                remaining_missing_pdf_pages=[80,99],
                notes=['OCR is a retrieval derivative, not a formula authority.',
                       'Hashing and image presence do not certify semantic reading or printed pagination.',
                       'Supplement 116–118 visually accepted in chapters-02-03.md; primary bytes remain unchanged.'],pages=pages)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(pages=len(pages),render_matches=sum(x.get('same_render_as_alternate',False) for x in pages),
                          missing=report['remaining_missing_pdf_pages']),ensure_ascii=False))
if __name__=='__main__': main()
