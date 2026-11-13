"""Exclude the now-completed B131/B133 source keys and map the next35."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/map_lil_remaining_B131_B140_source_v3306b.py');new=Path('scripts/map_lil_remaining_B135_B140_source_v3345b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_remaining_B131_B140_source_v3306b':'lil_remaining_B135_B140_source_v3345b',
      'editorial_handoff_verification_v3305':'editorial_handoff_verification_v3343b',
      'BLOCKS=[131,133,135,136,137,138,139,140]':'BLOCKS=[135,136,137,138,139,140]',
      'all-routes-unified-v3300':'all-routes-unified-v3338',
      'len(new)==255':'len(new)==194','len(allphysical)-len(new)==278':'len(allphysical)-len(new)==339',
      'len(rows)==255 and len(choices)==2':'len(rows)==194 and len(choices)==0',
      'for b in packets)==547':'for b in packets)==435',
      "for r in rows)==18":"for r in rows)==0","for r in rows)==1":"for r in rows)==0",
      'all8_original_label_getters_clean_current_even_alignments_pass=True':'no2100_label_objects_in_remaining_six_blocks=True',
      'complete257_remaining_clean_current_context':'complete194_remaining_clean_current_context',
      "'total_editorial_objects':257,'speech_objects':255,'ordinary_source_speeches':254,'system_FE_panels':1,'typed_choice_objects':1,'typed_choice_labels':2":"'total_editorial_objects':194,'speech_objects':194,'ordinary_source_speeches':194,'system_FE_panels':0,'typed_choice_objects':0,'typed_choice_labels':0",
      "'completed278_source_location_speeches_excluded':278":"'completed339_source_location_speeches_excluded':339",
      'all_completed_B122_B127_B128_B130_B132_B134_and_prior_families_excluded':'all_completed_B122_B134_and_prior_families_excluded',
      "b['block'] in [131,133]":"b['block'] in [135,136]",'len(focus)==61':'len(focus)==35',
      'for b in selected)==112':'for b in selected)==61',
      'next63_B131_B133_clean_current_context':'next35_B135_B136_clean_current_context',
      "'total_editorial_objects':63,'speech_objects':61,'ordinary_source_speeches':60,'system_FE_panels':1,'typed_choice_objects':1,'typed_choice_labels':2":"'total_editorial_objects':35,'speech_objects':35,'ordinary_source_speeches':35,'system_FE_panels':0,'typed_choice_objects':0,'typed_choice_labels':0",
      'all18_source00_speeches_require_static_actor_macro_and_route_binding_not_empty_paragraphs':'all35_complete_source_preambles_require_current_actor_macro_and_entry_binding',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    t=t[:t.rindex('    print(')]+"    print('Remaining194 physical speeches/sixblocks/435commands;339completedsource-location speeches excluded. NextB135/B136:35speeches/61commands,no2100orFE. Source/context/entry/native review stillpending;zero credit.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B135_B140_source_tools_v3345');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
