"""Prepare exact-parent reference gates for the measured716-byte B187 target."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_research_tools_v5204')
PARENT=Path('out/all_routes_combined_v5177_candidate.nds')
ROM=Path('out/lil_B187_reference_v5205_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B187_relocation_v5202/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/create_lil_B185_reference_v5108.py','scripts/create_lil_B187_reference_v5205.py',{
        'B185':'B187','prepare_lil_B185_research_v5107':'prepare_lil_B187_research_v5204','research_v5108':'research_v5205',
        'stored_v5106':'stored_v5203','all8_final_stored_targets32':'all16_final_stored_targets64','all8_final_targets':'all16_final_targets',
        'editorial_handoff_verification_v5082':'editorial_handoff_verification_v5183',
        "stored['current_final_stored_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==64",
        'current_final_stored_macro_alignment_cases=32':'current_final_stored_macro_alignment_cases=64','==[185]':'==[187]','V5076':'V5177',
    })]
    rows.append(derive('scripts/verify_lil_B186_loader_v5162.py','scripts/verify_lil_B187_loader_v5206.py',{
        'B186':'B187','prepare_lil_B186_research_v5160':'prepare_lil_B187_research_v5204',
        'loader_v5162':'loader_v5206','research_v5161':'research_v5205',
        'work/analysis/lil_B185_loader_v5109/whole_SC2_and_B185_initial_entry_proof.json':'work/analysis/lil_B186_loader_v5162/whole_SC2_and_B186_initial_entry_proof.json',
        'V5122':'V5177',
    }))
    rows.append(derive('scripts/verify_lil_B185_references_v5110.py','scripts/verify_lil_B187_references_v5207.py',{
        'B185':'B187','prepare_lil_B185_research_v5107':'prepare_lil_B187_research_v5204',
        'reference_census_v5110':'reference_census_v5207','loader_v5109':'loader_v5206','[185]':'[187]',
        '11-command/no-relative-site':'19-command/no-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==11":"sum(len(r['mapped_commands'])for r in result)==19",
        'all11':'all19','native_commands_each=11':'native_commands_each=19',
    }))
    rows.append(derive('scripts/prove_lil_B185_ends_v5111.py','scripts/prove_lil_B187_ends_v5208.py',{
        'B185':'B187','prepare_lil_B185_research_v5107':'prepare_lil_B187_research_v5204',
        'ends_v5111':'ends_v5208','n==185':'n==187',
    }))
    rows.append(derive('scripts/prove_lil_B185_relocated_controls_v5112.py','scripts/prove_lil_B187_relocated_controls_v5209.py',{
        'B185':'B187','prepare_lil_B185_research_v5107':'prepare_lil_B187_research_v5204',
        'relocated_controls_v5112':'relocated_controls_v5209','editorial_manuscript_v4':'editorial_manuscript_v3',
        'blocks[185]':'blocks[187]','block=185':'block=187','00a0ffff013807a1':'00a0ffff014e2fa1','len(dispatches)==8':'len(dispatches)==16',
        '[(0xA000,8,8),(0xC200,382,370),(0,384,372)]':'[(0xA000,8,8),(0xC200,672,708),(0,674,710)]',
        "len(spec['command_map'])==11":"len(spec['command_map'])==19",
        'all8_progressive_FE':'all16_progressive_FE','all7_progressive_static_actors1':'all15_progressive_static_actors1',
        'Bind 8 relocated dispatches':'Bind16 relocated dispatches',
        '8 relocated dispatches,7 progressive/one impersonal FE':'16 relocated dispatches,15 progressive/one impersonal FE',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[680,678],target_stored_logical=[716,714],source_and_target_two_tailzeros=True,
        commands=19,speeches=16,progressive=15,FE=1,relative_sites=0,predicates=0,
        A000_source8_target8=True,C200_source672_target708=True,end_source674_target710=True,
        parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B187 one-block reference and complete loader/census/end/linear-control gates;only exact V5177 parent proof can be reused.')
