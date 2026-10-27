"""Exclude completed B135/B136 andrefresh the remaining159 source locations."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/map_lil_remaining_B135_B140_source_v3345b.py');new=Path('scripts/map_lil_remaining_B137_B140_source_v3380b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_remaining_B135_B140_source_v3345b':'lil_remaining_B137_B140_source_v3380b',
      'editorial_handoff_verification_v3343b':'editorial_handoff_verification_v3377b',
      'BLOCKS=[135,136,137,138,139,140]':'BLOCKS=[137,138,139,140]',
      'all-routes-unified-v3338':'all-routes-unified-v3372',
      'len(new)==194':'len(new)==159','len(allphysical)-len(new)==339':'len(allphysical)-len(new)==374',
      'len(rows)==194':'len(rows)==159','for b in packets)==435':'for b in packets)==374',
      'remaining_six_blocks':'remaining_four_blocks',
      'complete194_remaining_clean_current_context':'complete159_remaining_clean_current_context',
      "'total_editorial_objects':194,'speech_objects':194,'ordinary_source_speeches':194":"'total_editorial_objects':159,'speech_objects':159,'ordinary_source_speeches':159",
      "'completed339_source_location_speeches_excluded':339":"'completed374_source_location_speeches_excluded':374",
      'all_completed_B122_B134_and_prior_families_excluded':'all_completed_B122_B136_and_prior_families_excluded',
      "b['block'] in [135,136]":"b['block'] in [137]",'len(focus)==35':'len(focus)==48','for b in selected)==61':'for b in selected)==117',
      'next35_B135_B136_clean_current_context':'next48_B137_clean_current_context',
      "'total_editorial_objects':35,'speech_objects':35,'ordinary_source_speeches':35":"'total_editorial_objects':48,'speech_objects':48,'ordinary_source_speeches':48",
      'all35_complete_source_preambles_require_current_actor_macro_and_entry_binding':'all48_complete_source_preambles_require_current_actor_macro_and_entry_binding',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    t=t[:t.rindex('    print(')]+"    print('Remaining159 physicalspeeches/fourblocks/374commands;374completedsource-location speeches excluded. NextB137:48speech/117commands. Actor/entry/macro/context/prose/native/release binding pending;zero newcredit.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B137_B140_source_tools_v3380');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
