"""B74 body-only wrapping research; no full Gerhard/FE/choice approval."""
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

DOC=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/lil_Hamburg_body_probe_v1951')

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(DOC)
    profile=get_dialogue_profile('lil-opening-editorial-native-v1')
    rows=[]
    for source in doc['records']:
        english=source['english'].split('}',1)[1].removesuffix('{PAD}')
        row=dict(id=source['id'],source_prefix=source['source_presentation_prefix_hex'],english=english)
        try:
            result=encode_relocatable_dialogue(bytes.fromhex(source['source_hex'])[1:],english,profile)
            row.update(encoded_body_hex=result.encoded.hex(),diagnostics=[dict(code=d.code,severity=d.severity,message=d.message)for d in result.diagnostics])
        except ValueError as error:row['error']=str(error)
        rows.append(row)
    assert len(rows)==79
    ROOT.mkdir(parents=True)
    save(ROOT/'body_only_prose_layout_research.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        rows=rows,scope='Conservative progressive body-only wrapping research. Source complete controls,Gerhard16 source scope and separate FE modal geometry/fonts/pagination/choice checks remain pending.',
        FE_rows_not_approved_by_progressive_body_probe=True,no_ROM_orledger_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for row in rows:
        problems=[d for d in row.get('diagnostics',[])if d['code']!='line-break-count']
        if row.get('error')or problems:print(dict(id=row['id'],prefix=row['source_prefix'],english=row['english'],error=row.get('error'),diagnostics=problems))
    print(dict(records=len(rows),encoding_errors=sum('error'in r for r in rows),FE_actual_geometry_unapproved=True))
