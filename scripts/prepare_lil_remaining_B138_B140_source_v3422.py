"""Prepare a clean/current lead refresh excluding the now integrated B137 family."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/map_lil_remaining_B137_B140_source_v3380b.py');b=Path('scripts/map_lil_remaining_B138_B140_source_v3422.py');assert not b.exists()
    t=a.read_text(encoding='utf-8')
    changes=[('lil_remaining_B137_B140_source_v3380b','lil_remaining_B138_B140_source_v3422'),('editorial_handoff_verification_v3377b','editorial_handoff_verification_v3421'),('all-routes-unified-v3372','all-routes-unified-v3416'),('[137,138,139,140]','[138,139,140]'),('len(new)==159','len(new)==111'),('len(allphysical)-len(new)==374','len(allphysical)-len(new)==422'),('len(rows)==159','len(rows)==111'),("for b in packets)==374","for b in packets)==257"),('remaining_four_blocks','remaining_three_blocks'),('complete159_remaining','complete111_remaining'),("'total_editorial_objects':159","'total_editorial_objects':111"),("'speech_objects':159","'speech_objects':111"),("'ordinary_source_speeches':159","'ordinary_source_speeches':111"),('completed374_source_location_speeches_excluded\':374','completed422_source_location_speeches_excluded\':422'),('all_completed_B122_B136','all_completed_B122_B137'),("b['block'] in [137]","b['block'] in [138]"),('len(focus)==48','len(focus)==44'),("for b in selected)==117","for b in selected)==111"),('next48_B137','next44_B138'),("'total_editorial_objects':48","'total_editorial_objects':44"),("'speech_objects':48","'speech_objects':44"),("'ordinary_source_speeches':48","'ordinary_source_speeches':44"),('all48_complete_source_preambles','all44_complete_source_preambles')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    t=t[:t.rindex('    print(')]+"    print('Remaining111 physical speeches/three blocks/257 commands;422 completed source-location speeches excluded. Next B138:44 speech/111 commands/45 relative sites/10 predicates/one event query. Actor/entry/macro/context/prose/native/release binding pending;zero credit.')\n"
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_remaining_source_tools_v3422');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_earlier_sources_ROMs_and_translations_preserved=True,full_goal_complete=False))
