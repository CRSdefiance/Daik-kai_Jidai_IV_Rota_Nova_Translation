"""Prepare source-locked B184 reference,load,census,end and relocated paths."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B184_research_tools_v5061')
PARENT=Path('out/all_routes_combined_v5030_candidate.nds')
ROM=Path('out/lil_B184_reference_v5062_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B184_relocation_v5059/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B183_reference_v4950.py','scripts/create_lil_B184_reference_v5062.py',{
        'B183':'B184','prepare_lil_B183_research_v4949':'prepare_lil_B184_research_v5061',
        'research_v4950':'research_v5062','stored_v4948':'stored_v5060',
        'all25_final_stored_targets100':'all9_final_stored_targets36','all25_final_targets':'all9_final_targets',
        'editorial_handoff_verification_v4921':'editorial_handoff_verification_v5058',
        "stored['current_final_stored_macro_alignment_cases']==100":"stored['current_final_stored_macro_alignment_cases']==36",
        'current_final_stored_macro_alignment_cases=100':'current_final_stored_macro_alignment_cases=36','==[183]':'==[184]','V4914':'V5030'}))
    loader=Path('scripts/verify_lil_B183_loader_v4951.py').read_text(encoding='utf-8')
    start=loader.index('    prior_path=');end=loader.index("    for label, path in [('research', ROM)]:",start)
    tools.append(derive('scripts/verify_lil_B183_loader_v4951.py','scripts/verify_lil_B184_loader_v5063.py',{
        loader[start:end]:'',"for label, path in [('research', ROM)]":"for label, path in [('current', PARENT),('research', ROM)]",
        'B183':'B184','prepare_lil_B183_research_v4949':'prepare_lil_B184_research_v5061','loader_v4951':'loader_v5063','research_v4950':'research_v5062',
        "'fresh_research_whole_SC2_loads':336,'exact_parent_reused_whole_SC2_loads':336,'fresh_parent_modes':672,'exact_parent_reused_modes':672":
        "'fresh_research_whole_SC2_loads':336,'fresh_current_whole_SC2_loads':336,'fresh_parent_modes':1344,'exact_parent_reused_modes':0",
        'New B183 research:336 original loads/cache hits and672 modes pass;byte-identical V4914 parent proof reused exactly. Representative/release pending.':
        'Both current V5030 and B184 research freshly pass672 total original loads/cache hits and1344 modes. Representative/release pending.'}))
    tools.append(derive('scripts/verify_lil_B183_references_v4952.py','scripts/verify_lil_B184_references_v5064.py',{
        'B183':'B184','prepare_lil_B183_research_v4949':'prepare_lil_B184_research_v5061','reference_census_v4952':'reference_census_v5064',
        'loader_v4951':'loader_v5063','[183]':'[184]','28-command/no-relative-site':'12-command/no-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==28":"sum(len(r['mapped_commands'])for r in result)==12",
        'all28':'all12','native_commands_each=28':'native_commands_each=12'}))
    tools.append(derive('scripts/prove_lil_B183_ends_v4953.py','scripts/prove_lil_B184_ends_v5065.py',{
        'B183':'B184','prepare_lil_B183_research_v4949':'prepare_lil_B184_research_v5061','ends_v4953':'ends_v5065','n==183':'n==184'}))
    tools.append(derive('scripts/prove_lil_B183_relocated_controls_v4954.py','scripts/prove_lil_B184_relocated_controls_v5066.py',{
        'B183':'B184','prepare_lil_B183_research_v4949':'prepare_lil_B184_research_v5061','relocated_controls_v4954':'relocated_controls_v5066',
        'editorial_manuscript_v7':'editorial_manuscript_v4','blocks[183]':'blocks[184]','block=183':'block=184',
        '00a0ffff013926a1':'00a0ffff011f22a1','len(dispatches)==25':'len(dispatches)==9',
        "sum(r['resolved_actor_ID'] is None for r in dispatches)==2":"sum(r['resolved_actor_ID'] is None for r in dispatches)==1",
        '[(0xA000,8,8),(0xC200,950,1048),(0,952,1050)]':'[(0xA000,8,8),(0xC200,426,410),(0,428,412)]',
        "len(spec['command_map'])==28":"len(spec['command_map'])==12",'all25':'all9',
        'all23_progressive_static_actors2_impersonal_null_actor_FE':'all8_progressive_static_actors1_impersonal_null_actor_FE',
        '25 relocated dispatches':'9 relocated dispatches','23 progressive/two impersonal FE':'8 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_bytes=432,target_bytes=416,target_logical_end=416,source_commands=12,speeches=9,progressive=8,FE=1,
        source_C200426_maps410_source_end428_maps412=True,both_current_and_target_whole_loaders_fresh=True,
        previous_goal_turn_classification='progress:V5057 native checkpoint and R14 visual wrapping correction verified',
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
