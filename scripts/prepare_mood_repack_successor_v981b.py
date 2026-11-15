"""Preserve retained selections and their entire opaque copy spans unchanged."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/mood_comments_v981')

def main():
    pairs=[('dk4tool/patch/mood_comments_editorial.py','dk4tool/patch/mood_comments_editorial_v981b.py'),
           ('scripts/audit_mood_comments_native_v981.py','scripts/audit_mood_comments_native_v981b.py')]
    prepared=[]
    for source,target in pairs:
        s,t=Path(source),Path(target);raw=s.read_bytes();text=raw.decode('utf-8')
        assert not t.exists()
        if source.startswith('dk4tool'):
            needle='    pack=FunctionType(repack.__code__'
            assert text.count(needle)==1
            text=text.replace(needle,"    # Reviewed retained strings need no replacement. Keep their complete original\n    # copy spans, including nontext bytes after the owned NUL.\n    authored={n:payload for n,payload in authored.items() if payload!=before[n].text}\n"+needle)
        else:
            needle='from dk4tool.patch import mood_comments_editorial as owned'
            assert text.count(needle)==1
            text=text.replace(needle,'from dk4tool.patch import mood_comments_editorial_v981b as owned')
        ast.parse(text);prepared.append((s,t,raw,text))
    records=[]
    for s,t,raw,text in prepared:
        with t.open('x',encoding='utf-8') as f:f.write(text)
        assert s.read_bytes()==raw
        records.append({'source':str(s),'source_sha256':sha(raw),'source_after_sha256':sha(s.read_bytes()),
                        'successor':str(t),'successor_sha256':sha(t.read_bytes()),'historical_source_unchanged':True})
    save(ROOT/'repack_successor_provenance_v981b.json',{'files':records,
        'reason':'The generic repacker rejects any authored entry with an opaque tail, even if its compiled text is byte-identical. IDs1854/1865 are retained verbatim; omit byte-identical strings from replacement input so all complete opaque spans remain exact. All39 source/compiled/font gates still apply; no repacker or source guard weakened.',
        'initial_native_audit_failed_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Successors prepared; historical module, audit and generic repacker unchanged.')

if __name__=='__main__':main()
