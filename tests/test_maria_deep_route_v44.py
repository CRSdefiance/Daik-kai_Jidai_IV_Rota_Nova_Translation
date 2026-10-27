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
BASE=Path('out/raphael_natural_v2_accepted_base.nds'); BATCH=Path('translations/maria_deep_route_v44.json')
def _load(p:Path)->dict[str,object]:
 v=json.loads(p.read_text(encoding='utf-8')); assert isinstance(v,dict); return v
def test_maria_v44_inventory_layout_and_allocations()->None:
 b=_load(BATCH); assert b['inventory']['identified_records']==66; assert b['inventory']['translated_records']==65; assert b['inventory']['excluded_records']==1
 source=NdsImage.open(BASE).read_file('/data/SC3.DK4'); profile=get_dialogue_profile(str(b['dialogue_profile'])); rows=materialize_translation_batch(b,source); failures=[]
 for r in rows:
  a=audit_fixed_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],profile); errors=[i for i in a['issues'] if i['severity']=='error']
  if errors: failures.append((r['id'],errors))
 assert not failures,failures
 rebuilt=rebuild_mesfile(source,rows); expected={(int(r['id'].split('_B',1)[1].split('_',1)[0]),int(r['id'].rsplit('R',1)[1])) for r in rows}; assert changed_segments(source,rebuilt)==expected
 old,new=IlnkContainer.parse(source),IlnkContainer.parse(rebuilt)
 for block,index in expected: assert len(new.blocks[block].split(b'\0')[index])==len(old.blocks[block].split(b'\0')[index])
def test_maria_v44_macros_states_exclusion_and_release()->None:
 b=_load(BATCH); by={r['id']:r for r in b['records']}; assert '{MACRO:FI}' in by['DK4_MES_B03_R0005']['english']; assert '{MACRO:FO}' in by['DK4_MES_B05_R0005']['english']; assert by['DK4_MES_B03_R0005']['english'].startswith('{SPEAKER:29}'); assert by['DK4_MES_B04_R0009']['english'].startswith('{SPEAKER:2B}'); assert by['DK4_MES_B05_R0015']['english'].startswith('{SPEAKER:B8}'); assert {x['id'] for x in b['excluded']}=={'DK4_MES_B00_R0002'}
 release=_load(Path('translations/release_stack.json')); assert release['profiles']['maria-deep-route-v44']['batches'][-1]==BATCH.as_posix()
