"""Prepare source-locked relocation and native reference checks from verified V5980."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B202_reference_tools_v5982')
PARENT=Path('out/all_routes_combined_v5947_candidate.nds')
ROM=Path('out/lil_B202_reference_v5985_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B202_relocation_v5983/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v5981/verified_handoff.json')
    assert prior['B202_native_approved_uncredited_objects']==19 and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256'] and sha(PARENT.read_bytes())==prior['candidate_sha256']
    registry=read('translations/release_stack.json');profile=registry['profiles'][prior['profile']];assert profile['status']=='experimental' and profile['lil_B201_editorial']=='translations/lil_B201_editorial_release_v1.json' and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    tools=[derive('scripts/research_lil_B200_relocation_v5851.py','scripts/research_lil_B202_relocation_v5983.py',{
      'B200':'B202','relocation_v5851':'relocation_v5983','v5816_candidate':'v5947_candidate','number==200':'number==202',"end_maps[0]['source_offset']==926":"end_maps[0]['source_offset']==582",
      "sum(len(r['command_map']) for r in results)==31":"sum(len(r['command_map']) for r in results)==26",'[200]':'[202]','source_FE_system_objects=2':'source_FE_system_objects=0','31commands/19speech':'26commands/19speech','all932':'all588'})]
    tools.append(derive('scripts/prove_lil_B200_stored_v5852.py','scripts/prove_lil_B202_stored_v5984.py',{
      'B200':'B202','stored_v5852':'stored_v5984','relocation_v5851':'relocation_v5983','voices_v5827':'voices_v5960','lil_current_font_oracles_v4792':'lil_current_font_oracles_v5918',
      '[19,172,254]':'[2,18,147,157]',"sum(c['consumer']=='FE-paper' for c in cases)==2":"sum(c['consumer']=='FE-paper' for c in cases)==0",'progressive=17,FE=2':'progressive=19,FE=0'}))
    shared={'B200':'B202','prepare_lil_B200_reference_tools_v5850':'prepare_lil_B202_references_v5982'}
    tools.append(derive('scripts/create_lil_B200_reference_v5853.py','scripts/create_lil_B202_reference_v5985.py',{
      **shared,'V5816':'V5947','research_v5853':'research_v5985','stored_v5852':'stored_v5984','verification_v5842':'verification_v5981','==[200]':'==[202]',
      "assert pins.read_bytes()==old;pins.write_bytes(encoded)":"assert pins.read_bytes()==old\n    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush()"}))
    tools.append(derive('scripts/verify_lil_B200_loader_v5854.py','scripts/verify_lil_B202_loader_v5986.py',{
      **shared,'V5816':'V5947','loader_v5854':'loader_v5986','research_v5853':'research_v5985',
      'work/analysis/lil_B199_loader_v5801/whole_SC2_and_B199_initial_entry_proof.json':'work/analysis/lil_B201_loader_v5935/whole_SC2_and_B201_initial_entry_proof.json'}))
    tools.append(derive('scripts/verify_lil_B200_references_v5855.py','scripts/verify_lil_B202_references_v5987.py',{
      **shared,'reference_census_v5855':'reference_census_v5987','loader_v5854':'loader_v5986','[200]':'[202]','31-command':'26-command',
      "sum(len(r['mapped_commands'])for r in result)==31":"sum(len(r['mapped_commands'])for r in result)==26",'all31':'all26','native_commands_each=31':'native_commands_each=26'}))
    tools.append(derive('scripts/prove_lil_B200_ends_v5856.py','scripts/prove_lil_B202_ends_v5988.py',{
      **shared,'ends_v5856':'ends_v5988','n==200':'n==202'}))
    tools.append(derive('scripts/prove_lil_B200_relocated_controls_v5857.py','scripts/prove_lil_B202_relocated_controls_v5989.py',{
      **shared,'relocated_controls_v5857':'relocated_controls_v5989','blocks[200]':'blocks[202]',
      'all12_source_current_nonspeech_leaves':'all7_source_current_nonspeech_leaves','[0x4830,0x4735]':'[0x4835,0x4721]','word==0x4830':'word==0x4835',
      "sum(r['resolved_actor_ID'] is None for r in dispatches)==2":"sum(r['resolved_actor_ID'] is None for r in dispatches)==0",'len(leaves)==12':'len(leaves)==7',
      "assert len(cp['two_resource_words20_boundary_cases'])==20 and len(cp['source6003_ten_boundary_cases'])==10 and len(cp['source_six_structural_pairs'])==6":"assert len(cp['ten_distinct_632A_decoder_boundary_cases'])==10 and cp['original632A_word_two_exact_source_sites']==[162,182] and len(cp['source_two_A000_structural_pairs'])==2",
      'and12_exact_leaves':'and7_exact_leaves','all12_source_current_target_control_leaves':'all7_source_current_target_control_leaves',
      'original20_resource10_audio_boundary_cases_and_six_structural_pairs_reused_by_exact_bytes_and_current_snapshot':'original10_unique632A_boundary_cases_two_word_sites_and_two_structural_pairs_reused_by_exact_bytes_and_current_snapshot',
      'all17_progressive_and_two_distinct_null_actor_FE_objects_preserved':'all19_progressive_and_zero_FE_objects_preserved','Stranger_target_not_applied=True':'original_names_and_Sailor_catalogue_alias_preserved=True',
      '19 relocated dispatches,one picture/one47xx pair and12 exact leaves pass':'19 relocated dispatches,one picture/one47xx pair and7 exact leaves pass'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),source_commands=26,source_speeches=19,source_relative_sites=0,source_tailzeros=2,source_FE_panels=0,previous_goal_turn_classification='progress',full_goal_complete=False));print('B202 seven reference tools prepared;26 commands/19 progressive speeches/seven leaves/end582. Parent loader reused only by exact complete ROM hash.')
