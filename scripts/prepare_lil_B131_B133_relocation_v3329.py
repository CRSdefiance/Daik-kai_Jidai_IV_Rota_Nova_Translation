"""Relocate complete source00-aware speech andone two-option menu."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/research_lil_B122_B127_relocation_v3288b.py');new=Path('scripts/research_lil_B131_B133_relocation_v3329b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B122_B127_relocation_v3288b':'lil_B131_B133_relocation_v3329b',
      'lil_B122_B127_editorial_manuscript_v5.json':'lil_B131_B133_editorial_manuscript_v4.json',
      'lil_B122_B127_choice_manuscript_v4.json':'lil_B131_B133_choice_manuscript_v5.json',
      'all_routes_combined_v3251_candidate.nds':'all_routes_combined_v3300_candidate.nds',
      "b'\\0' not in value and value[:1]==old[:1]":"b'\\0' not in value[1:] and (b'\\0' not in value or value[0]==old[0]==0) and value[:1]==old[:1]",
      'len(results)==6':'len(results)==2',"sum(len(r['text_records']) for r in results)==155":"sum(len(r['text_records']) for r in results)==61",
      "sum(len(r['choice_commands']) for r in results)==2":"sum(len(r['choice_commands']) for r in results)==1",
      "sum(len(r['relative_skip_fixups']) for r in results)==64":"sum(len(r['relative_skip_fixups']) for r in results)==24",
      "sum(len(r['target_native_skip_cases']) for r in results)==320":"sum(len(r['target_native_skip_cases']) for r in results)==120",
      "sum(len(r['command_map']) for r in results)==312":"sum(len(r['command_map']) for r in results)==112",
      "sum(len(r['original2000_pause_and_resume_maps']) for r in results)==2":"sum(len(r['original2000_pause_and_resume_maps']) for r in results)==0",
      'range(122,128)':'[131,133]',
      'two_original2100_menus_four_labels=True':'one_original2100_menu_two_labels=True',
      'all155speech_four_choice_labels_and64_relative_operands_preserved':'all61speech_two_choice_labels_and24_relative_operands_preserved',
      'all320_relocated_native_skip_cases_match_original_target_mapping':'all120_relocated_native_skip_cases_match_original_target_mapping',
      'all330_other_SC2_blocks_exact':'all334_other_SC2_blocks_exact',
      "both_original2000_pause_words_and_mapped_resume_boundaries_exact=True,original2000_wait_proof=doc['original2000_wait_proof'],original2000_wait_proof_sha256=doc['original2000_wait_proof_sha256'],":"no_source2000_commands=True,whole_typed_speech_proof=doc['whole_typed_speech_proof'],whole_typed_speech_proof_sha256=doc['whole_typed_speech_proof_sha256'],all18_source00_prefixes_preserved_without_body_NUL=True,"}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    t=t[:t.rindex("    print('")]+"    print('112 physical commands/61speeches/one two-option menu/24spanfixups/120skipcases;all18leading source00 controls,body terminators,inversebytes and334otherblocks exact. Research only.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B131_B133_relocation_tools_v3329');root.mkdir(parents=True);save(root/'source00_relocation_successor_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),strict_source00_prefix_only_NUL_rule_preserved=True,no_previous_producer_orROM_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
