"""Prepare whole-image/source-reference checks for one B201 resized block and typed menu."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B201_reference_tools_v5934')
PARENT=Path('out/all_routes_combined_v5891_candidate.nds')
ROM=Path('out/lil_B201_reference_v5934_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B201_relocation_v5931/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B196_reference_v5619.py','scripts/create_lil_B201_reference_v5934.py',{
        'B196':'B201','prepare_lil_B196_research_v5618':'prepare_lil_B201_reference_tools_v5934','research_v5619':'research_v5934',
        'stored_v5616':'stored_v5932b','verification_v5614':'verification_v5927','stored_choices_v5617':'stored_choices_v5933',
        'six_final_typed_objects_twelve_references':'one_final_typed_object_two_references','all_six_stored_objects_and_twelve_actual_offsets':'one_stored_object_and_two_actual_offsets',
        "menus['fresh_count_calls']==12 and menus['fresh_label_pointer_calls']==24":"menus['fresh_count_calls']==2 and menus['fresh_label_pointer_calls']==4",
        '==[196]':'==[201]','all6_stored_menus12_labels':'all1_stored_menu2_labels','V5580':'V5891',
        "old=pins.read_bytes();values=json.loads(old)":"old=pins.read_bytes();values=json.loads(old);(ROOT/'pins.before.json').write_bytes(old)"}))
    source=Path('scripts/verify_lil_B200_loader_v5854.py').read_text(encoding='utf-8');a=source.index('    prior_path=');b=source.index("    for label, path in [('research', ROM)]:",a)
    tools.append(derive('scripts/verify_lil_B200_loader_v5854.py','scripts/verify_lil_B201_loader_v5935.py',{
        source[a:b]:'',"for label, path in [('research', ROM)]:":"for label, path in [('current', PARENT),('research', ROM)]:",
        'B200':'B201','prepare_lil_B200_reference_tools_v5850':'prepare_lil_B201_reference_tools_v5934','loader_v5854':'loader_v5935','research_v5853':'research_v5934',
        "'fresh_research_whole_SC2_loads':336,'exact_parent_reused_whole_SC2_loads':336,'fresh_parent_modes':672,'exact_parent_reused_modes':672":"'fresh_current_and_research_whole_SC2_loads':672,'fresh_current_and_research_parent_modes':1344,'exact_parent_reused_whole_SC2_loads':0",
        'New B200 research:336 original loads/cache hits and672 modes pass;byte-identical V5816 parent proof reused exactly. Representative/release pending.':
        'Current V5891 and B201 research:672 original whole-block loads/cache hits and1344 parent modes freshly pass. No old whole-ROM-hash reuse;representative/release pending.'}))
    tools.append(derive('scripts/verify_lil_B200_references_v5855.py','scripts/verify_lil_B201_references_v5936.py',{
        'B200':'B201','prepare_lil_B200_reference_tools_v5850':'prepare_lil_B201_reference_tools_v5934','loader_v5854':'loader_v5935',
        'reference_census_v5855':'reference_census_v5936','in [200]':'in [201]',
        "len(r['mapped_commands'])for r in result)==31":"len(r['mapped_commands'])for r in result)==44",
        "r['typed_relative_span_count']for r in result)==0":"r['typed_relative_span_count']for r in result)==4",
        "r['target_native_skip_cases']for r in result)==0":"r['target_native_skip_cases']for r in result)==20",
        'all31_commands_no_relative_sites':'all44_commands_four_relative_sites','all31_clean_current_target_commands_and_no_relative_sites':'all44_clean_current_target_commands_and_four_relative_sites',
        'native_commands_each=31,relative_sites=0,target_native_skip_cases=0':'native_commands_each=44,relative_sites=4,target_native_skip_cases=20'}))
    tools.append(derive('scripts/prove_lil_B200_ends_v5856.py','scripts/prove_lil_B201_ends_v5937.py',{
        'B200':'B201','prepare_lil_B200_reference_tools_v5850':'prepare_lil_B201_reference_tools_v5934','ends_v5856':'ends_v5937',
        'n==200':'n==201','two_declared_tail_end_decodes_no_relative_sites':'two_declared_tail_end_decodes_four_relative_sites'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        exact_source24_speeches_one2100_four_relative_sites_one_shared_end_and_zero_tailzeros=True,
        changed_name_data_runtime_requires_fresh_parent_loader_pass_not_old_whole_ROM_reuse=True,
        no_new_ROM_or_editorial_credit_by_preparer=True,full_goal_complete=False))
    print('B201 reference-image,whole loader,census and complete-end tools prepared;all native numeric constants preserved.')
