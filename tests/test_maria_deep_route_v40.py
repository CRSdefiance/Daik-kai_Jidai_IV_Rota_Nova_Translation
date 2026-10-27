from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
BASE=Path("out/raphael_natural_v2_accepted_base.nds"); BATCH=Path("translations/maria_deep_route_v40.json")
def _load(p:Path)->dict[str,object]:
    v=json.loads(p.read_text(encoding='utf-8')); assert isinstance(v,dict); return v
def test_maria_v40_inventory_layout_and_allocations()->None:
    b=_load(BATCH); assert b['inventory']=={'identified_records':42,'translated_records':41,'excluded_records':1,'blocks':{'260':10,'261':10,'262':11,'263':10}}
    source=NdsImage.open(BASE).read_file('/data/SC3.DK4'); profile=get_dialogue_profile(str(b['dialogue_profile'])); rows=materialize_translation_batch(b,source); failures=[]
    for r in rows:
        a=audit_fixed_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],profile); errors=[i for i in a['issues'] if i['severity']=='error']
        if errors: failures.append((r['id'],errors))
    assert not failures,failures
    rebuilt=rebuild_mesfile(source,rows); expected={(int(r['id'].split('_B',1)[1].split('_',1)[0]),int(r['id'].rsplit('R',1)[1])) for r in rows}; assert changed_segments(source,rebuilt)==expected
    old,new=IlnkContainer.parse(source),IlnkContainer.parse(rebuilt)
    for block,index in expected: assert len(new.blocks[block].split(b'\0')[index])==len(old.blocks[block].split(b'\0')[index])
def test_maria_v40_branches_states_exclusion_and_release()->None:
    b=_load(BATCH); by={r['id']:r for r in b['records']}
    assert '{MACRO:FI}' in by['DK4_MES_B260_R0004']['english']
    assert by['DK4_MES_B261_R0018']['english']=='{SPEAKER:FE}Received 50,000 coins.{PAD}'
    assert by['DK4_MES_B262_R0024']['english']=='{SPEAKER:FE}Received 30,000 coins.{PAD}'
    assert by['DK4_MES_B263_R0013']['english'].startswith('{SPEAKER:D6}')
    assert by['DK4_MES_B263_R0026']['english'].startswith('{SPEAKER:9C}')
    for i in range(14,20): assert not by[f'DK4_MES_B263_R{i:04d}']['english'].startswith('{SPEAKER:')
    assert b['excluded']==[{'id':'DK4_MES_B263_R0002','reason':'Four-byte scene-entry payload 20469480; not independently rendered dialogue.'}]
    release=_load(Path('translations/release_stack.json')); assert release['profiles']['maria-deep-route-v40']['batches'][-1]==BATCH.as_posix()
