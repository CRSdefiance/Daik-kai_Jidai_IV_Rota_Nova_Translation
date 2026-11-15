"""Prepare source-locked B190 predicate ownership and complete conditional gates."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B190_research_tools_v5331')
PARENT=Path('out/all_routes_combined_v5304_candidate.nds')
ROM=Path('out/lil_B190_reference_v5332_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B190_relocation_v5328/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/prove_lil_B186_predicate700_v5159.py','scripts/prove_lil_B190_predicate500_v5330.py',{
        'B186':'B190','700':'500','699':'499','701':'501','5159':'5330','source_v5132':'source_v5314','all12_clean_current':'all17_clean_current',
        'voices_v5133':'voices_v5315','relocation_v5157':'relocation_v5328','blocks[186]':'blocks[190]',
        '0080ffffbc020000':'0080fffff4010000','[540]':'[8]',
        "if r['offset']==at and r['supplied_CPU_only_seed_fixture']==fixture":"if r['version'] in ['clean','current'] and r['offset']==at and r['supplied_CPU_only_seed_fixture']==fixture",
        "not pair[0]['operand_pointer_unaligned'] and pair[1]['operand_pointer_unaligned']":"not pair[0]['operand_pointer_unaligned'] and not pair[1]['operand_pointer_unaligned']",
        'all12_aligned_and_unaligned_original':'all12_aligned_original',
    })]
    rows.append(derive('scripts/create_lil_B186_reference_v5161.py','scripts/create_lil_B190_reference_v5332.py',{
        'B186':'B190','prepare_lil_B186_research_v5160':'prepare_lil_B190_research_v5331','research_v5161':'research_v5332',
        'stored_v5158':'stored_v5329','all12_final':'all17_final','targets48_macro':'targets68_macro',
        'editorial_handoff_verification_v5128':'editorial_handoff_verification_v5310',
        "stored['current_final_stored_macro_alignment_cases']==48":"stored['current_final_stored_macro_alignment_cases']==68",
        'current_final_stored_macro_alignment_cases=48':'current_final_stored_macro_alignment_cases=68','==[186]':'==[190]','V5122':'V5304',
    }))
    rows.append(derive('scripts/verify_lil_B189_loader_v5291.py','scripts/verify_lil_B190_loader_v5333.py',{
        'B189':'B190','prepare_lil_B189_research_v5289':'prepare_lil_B190_research_v5331',
        'loader_v5291':'loader_v5333','research_v5290':'research_v5332',
        'work/analysis/lil_B188_loader_v5250/whole_SC2_and_B188_initial_entry_proof.json':'work/analysis/lil_B189_loader_v5291/whole_SC2_and_B189_initial_entry_proof.json','V5263':'V5304',
    }))
    rows.append(derive('scripts/verify_lil_B186_references_v5163.py','scripts/verify_lil_B190_references_v5334.py',{
        'B186':'B190','prepare_lil_B186_research_v5160':'prepare_lil_B190_research_v5331','reference_census_v5163':'reference_census_v5334','loader_v5162':'loader_v5333',
        '[186]':'[190]','24-command':'29-command',"sum(len(r['mapped_commands'])for r in result)==24":"sum(len(r['mapped_commands'])for r in result)==29",
        'all24_commands':'all29_commands','all24_clean_current':'all29_clean_current','native_commands_each=24':'native_commands_each=29',
        'relative_sites=10,target_native_skip_cases=50':'relative_sites=6,target_native_skip_cases=30',
    }))
    rows.append(derive('scripts/prove_lil_B186_ends_v5164.py','scripts/prove_lil_B190_ends_v5335.py',{
        'B186':'B190','prepare_lil_B186_research_v5160':'prepare_lil_B190_research_v5331','ends_v5164':'ends_v5335','n==186':'n==190',
    }))
    rows.append(derive('scripts/prove_lil_B186_relocated_controls_v5165.py','scripts/prove_lil_B190_relocated_controls_v5336.py',{
        'B186':'B190','relocated_controls_v5165':'relocated_controls_v5336','prepare_lil_B186_research_v5160':'prepare_lil_B190_research_v5331',
        'predicate700_v5159':'predicate500_v5330','probe700':'probe500','C200_v5138':'C200_v5318','editorial_manuscript_v5':'editorial_manuscript_v3',
        'blocks[186]':'blocks[190]','len(dispatches)==12':'len(dispatches)==17','a%4==0 and b%4==2':'a%4==0 and b%4==0',
        '[540]':'[8]',"after['C200_offsets']==[644] and after['source_end_offset']==646":"after['C200_offsets']==[600] and after['source_end_offset']==602",
        '{560,572,584}':'{28,40,52}','all12_dispatches':'all17_dispatches','whole_exchange_all12_speeches':'whole_exchange_all17_speeches',
        'B186 relocation:12 dispatches':'B190 relocation:17 dispatches',
    }))
    plan=read(PLAN);b=plan['blocks'][0]
    assert [c['new_offset'] for c in b['command_map'] if c['word']==0x8000]==[8]
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_source_locked_conditional_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        speeches=17,commands=29,relative_sites=6,target_skip_cases=30,threshold=500,predicate_source_target_offset=8,
        aligned_actual_predicate_operands=True,source_stored=608,target_stored=704,source_end=602,target_end=698,
        no_actual_emulator_seed_forcing=True,no_completion_credit=True,full_goal_complete=False))
    print('Prepared source-locked B190 ownership/reference/loader/census/end/control gates.')
