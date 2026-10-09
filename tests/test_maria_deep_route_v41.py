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
BASE=Path('out/raphael_natural_v2_accepted_base.nds'); BATCH=Path('translations/maria_deep_route_v41.json')
def _load(p:Path)->dict[str,object]:
 v=json.loads(p.read_text(encoding='utf-8')); assert isinstance(v,dict); return v
def test_maria_v41_inventory_layout_and_allocations()->None:
 b=_load(BATCH); assert b['inventory']=={'identified_records':46,'translated_records':44,'excluded_records':2,'blocks':{'264':31,'265':1,'266':12}}
 source=NdsImage.open(BASE).read_file('/data/SC3.DK4'); profile=get_dialogue_profile(str(b['dialogue_profile'])); rows=materialize_translation_batch(b,source); failures=[]
 for r in rows:
  a=audit_fixed_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],profile); errors=[i for i in a['issues'] if i['severity']=='error']
  if errors: failures.append((r['id'],errors))
 assert not failures,failures
 rebuilt=rebuild_mesfile(source,rows); expected={(int(r['id'].split('_B',1)[1].split('_',1)[0]),int(r['id'].rsplit('R',1)[1])) for r in rows}; assert changed_segments(source,rebuilt)==expected
 old,new=IlnkContainer.parse(source),IlnkContainer.parse(rebuilt)
 for block,index in expected: assert len(new.blocks[block].split(b'\0')[index])==len(old.blocks[block].split(b'\0')[index])
def test_maria_v41_choice_macro_text_lead_exclusions_and_release()->None:
 b=_load(BATCH); by={r['id']:r for r in b['records']}
 assert by['DK4_MES_B264_R0104']['english']=='Push on{PAD}'
 assert by['DK4_MES_B264_R0106']['english']=='Search{PAD}'
 assert not by['DK4_MES_B264_R0104']['english'].startswith('{SPEAKER:')
 assert '{MACRO:FI}' in by['DK4_MES_B264_R0149']['english']
 assert by['DK4_MES_B265_R0005']['english'].startswith('{SPEAKER:5F}')
 assert {x['id'] for x in b['excluded']}=={'DK4_MES_B264_R0028','DK4_MES_B264_R0092'}
 release=_load(Path('translations/release_stack.json')); assert release['profiles']['maria-deep-route-v41']['batches'][-1]==BATCH.as_posix()
