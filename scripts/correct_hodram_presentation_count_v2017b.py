"""Count all source prefixes explicitly; there are six FE objects,not seven."""
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_source_v2017b')
SOURCE=Path('work/analysis/hodram_opening_source_v2017/all73_clean_current_opening_and_Lil_encounter_source.json')

if __name__=='__main__':
    assert not ROOT.exists();doc=read(SOURCE)
    counts=Counter(r['source_reference']['leading_byte_hex']for p in doc['packets']for r in p['records'])
    assert counts=={'01':26,'fe':6,'12':9,'10':10,'17':8,'02':9,'09':5}
    doc['remaining_control_gate']=doc['remaining_control_gate'].replace('seven separate FE panels','six separate FE panels')
    doc['presentation_counts']=dict(counts);doc['supersedes']=str(SOURCE);doc['superseded_packet_sha256']=sha(SOURCE.read_bytes())
    ROOT.mkdir(parents=True);target=ROOT/SOURCE.name;save(target,doc)
    handoff=Path('docs/editorial_handoff_current.md');before=handoff.read_bytes();(ROOT/'handoff_before.md').write_bytes(before)
    text=before.decode().replace('source_v2017/all73_clean_current_opening_and_Lil_encounter_source.json','source_v2017b/all73_clean_current_opening_and_Lil_encounter_source.json',1)
    assert text.count('andsevenFE objects')==1
    text=text.replace('andsevenFE objects','andsixFE objects',1).replace('# Current editorial handoff - V2017','# Current editorial handoff - V2017b',1)
    handoff.write_text(text,encoding='utf-8')
    save(ROOT/'presentation_count_correction.json',dict(presentation_counts=dict(counts),source_packet=str(target),source_packet_sha256=sha(target.read_bytes()),
        source_only_no_ROM_registry_or_coverage_counter_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(speeches=73,progressive=67,separate_FE=6,source_only=True))
