from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch
from dk4tool.script.mesfile import rebuild_mesfile
from scripts.build_integrated_release import changed_segments
BASE=Path('out/raphael_natural_v2_accepted_base.nds');BATCH=Path('translations/maria_deep_route_v49.json')
def _load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def test_maria_v49_inventory_and_allocations():
 b=_load(BATCH);assert b['inventory']['identified_records']==27;assert b['inventory']['translated_records']==27;source=NdsImage.open(BASE).read_file('/data/SC3.DK4');profile=get_dialogue_profile(b['dialogue_profile']);rows=materialize_translation_batch(b,source);fail=[]
 for r in rows:
  errors=[i for i in audit_fixed_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],profile)['issues'] if i['severity']=='error']
  if errors:fail.append((r['id'],errors))
 assert not fail,fail;rebuilt=rebuild_mesfile(source,rows);expected={(int(r['id'].split('_B',1)[1].split('_',1)[0]),int(r['id'].rsplit('R',1)[1])) for r in rows};assert changed_segments(source,rebuilt)==expected
def test_maria_v49_states_and_macros():
 b=_load(BATCH);by={r['id']:r for r in b['records']};assert by['DK4_MES_B31_R0063']['english'].startswith('{SPEAKER:28}');assert by['DK4_MES_B31_R0067']['english'].startswith('{SPEAKER:9B}');assert '{MACRO:FO}' in by['DK4_MES_B31_R0008']['english'];assert '{MACRO:FI}' in by['DK4_MES_B31_R0042']['english']
