"""Body-only prose/layout research; no speaker or FE consumer approval."""
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('translations/lil_london_editorial_manuscript_v1.json')
ROOT = Path('work/analysis/lil_London_body_probe_v1881b')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc=read(DOC)
    profile=get_dialogue_profile('lil-opening-editorial-native-v1')
    rows=[]
    for r in doc['records']:
        english=r['english'].split('}',1)[1].removesuffix('{PAD}')
        row=dict(id=r['id'],source_prefix=r['source_presentation_prefix_hex'],english=english)
        try:
            result=encode_relocatable_dialogue(bytes.fromhex(r['source_hex'])[1:],english,profile)
            row.update(encoded_body_hex=result.encoded.hex(),diagnostics=[dict(code=d.code,severity=d.severity,message=d.message) for d in result.diagnostics])
        except ValueError as e:
            row['error']=str(e)
        rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'body_only_prose_layout_research.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        rows=rows,scope='Body-only progressive formatting research,not source preamble/control proof. FE consumer is separate andnot approved bythis probe.',
        all_scene_native_fonts_full_controls_macro_catalog_and_actual_display_still_pending=True,
        no_ROM_orledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:
        problems=[d for d in r.get('diagnostics',[]) if d['code']!='line-break-count']
        if r.get('error') or problems:
            print(dict(id=r['id'],prefix=r['source_prefix'],error=r.get('error'),diagnostics=problems))
    print(dict(records=len(rows),encoding_errors=sum('error' in r for r in rows)))
