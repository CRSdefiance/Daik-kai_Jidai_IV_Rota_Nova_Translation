"""Prepare B198 whole-image, loading, entry and single-end research checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B198_research_tools_v5732')
PARENT=Path('out/all_routes_combined_v5692_candidate.nds')
ROM=Path('out/lil_B198_reference_v5733_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B198_relocation_v5725/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/create_lil_B197_reference_v5677.py').read_text(encoding='utf-8')
    menu=source[source.index('    menus=read('):source.index('    parent,image=')]
    receipt=source[source.index("        stored_menu_proof="):source.index('registered_candidate=False')]
    shared={'B197':'B198','prepare_lil_B197_research_v5676':'prepare_lil_B198_research_v5732'}
    rows=[derive('scripts/create_lil_B197_reference_v5677.py','scripts/create_lil_B198_reference_v5733.py',{
        **shared,'V5637':'V5692','research_v5677':'research_v5733','stored_v5672':'stored_v5726',
        'all21':'all17','targets84':'targets68','verification_v5675':'verification_v5731',
        "stored['current_final_stored_macro_alignment_cases']==84":"stored['current_final_stored_macro_alignment_cases']==68",
        'current_final_stored_macro_alignment_cases=84':'current_final_stored_macro_alignment_cases=68','==[197]':'==[198]',
        menu:"    assert not any(b['choice_commands'] or b['actor_style_commands'] for b in plan['blocks'])\n",
        receipt:'        no_source_choice_or_actor_style_objects=True,'})]
    rows.append(derive('scripts/verify_lil_B197_loader_v5678.py','scripts/verify_lil_B198_loader_v5734.py',{
        **shared,'V5637':'V5692','loader_v5678':'loader_v5734','research_v5677':'research_v5733',
        'work/analysis/lil_B196_loader_v5620/whole_SC2_and_B196_initial_entry_proof.json':
        'work/analysis/lil_B197_loader_v5678/whole_SC2_and_B197_initial_entry_proof.json'}))
    rows.append(derive('scripts/verify_lil_B197_references_v5679.py','scripts/verify_lil_B198_references_v5735.py',{
        **shared,'39-command/6-span':'37-command/8-span','reference_census_v5679':'reference_census_v5735','loader_v5678':'loader_v5734',
        '[197]':'[198]',"sum(len(r['mapped_commands'])for r in result)==39":"sum(len(r['mapped_commands'])for r in result)==37",
        "sum(r['typed_relative_span_count']for r in result)==6":"sum(r['typed_relative_span_count']for r in result)==8",
        "sum(r['target_native_skip_cases']for r in result)==30":"sum(r['target_native_skip_cases']for r in result)==40",
        'all39_commands6_relative_sites':'all37_commands8_relative_sites',
        'all39_clean_current_target_commands_and6_relative_sites':'all37_clean_current_target_commands_and8_relative_sites',
        'native_commands_each=39,relative_sites=6,target_native_skip_cases=30':'native_commands_each=37,relative_sites=8,target_native_skip_cases=40'}))
    rows.append(derive('scripts/prove_lil_B197_ends_v5680.py','scripts/prove_lil_B198_ends_v5736.py',{
        **shared,'ends_v5680':'ends_v5736','all6_in_block_relative_destinations':'all8_in_block_relative_destinations'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[544,544],target_stored_logical=[644,644],source_tailzeros=0,target_tailzeros=0,
        commands=37,speeches=17,progressive=11,FE=6,relative_sites=8,predicates=2,ends=1,
        source_choices_and_actor_style_objects=0,parent_loader_reuse_requires_exact_whole_ROM_hash=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B198 one-block reference,whole loader,37-command/eight-span entry census and guarded single-end proofs.')
