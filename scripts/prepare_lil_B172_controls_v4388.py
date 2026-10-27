"""Prepare27 relocated speech dispatches and11 C200/A000/presentation/resource leaves."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_relocated_control_tools_v4388')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/prove_lil_B171_relocated_controls_v4339.py').read_text(encoding='utf-8')
    a=old.index("    assert [r['word'] for r in leaves]");b=old.index('    paths=',a)
    replacement='''    assert [r['word'] for r in leaves]==[0x6000,0x45FF,0x6329,0x4651,0x6340,0x4620,0x632A,0xC200,0xA000,0x6240,0]
    assert len(cp['three_resource_words30_boundary_cases'])==30
    assert len(cp['five_presentation_structural_cases'])==5 and len(cp['one_later_A000_structural_case'])==1
    assert cp['source_A000_hex']=='00a0ffff010cc960' and cp['source_A000_raw_hex_words']==['0C01','60C9']
    assert cp['source_C2001868_then_A0001870_then6240_1878_then_end1880_preserved']
    assert not spec['original2000_pause_and_resume_maps'] and not spec['relative_skip_fixups']
    assert [r['old_offset'] for r in leaves[-4:]]==[1868,1870,1878,1880]
    assert leaves[-3]['source_current_target_hex']=='00a0ffff010cc960'
'''
    tool=derive('scripts/prove_lil_B171_relocated_controls_v4339.py','scripts/prove_lil_B172_relocated_controls_v4388.py',{
        old[a:b]:replacement,'Bind all37 relocated dispatches, original C200 queue and all eight leaves.':'Bind all27 relocated dispatches,original C200 queue then A000 and all eleven leaves.',
        'prepare_lil_B171_research_v4334':'prepare_lil_B172_research_v4383','lil_B171_relocated_controls_v4339':'lil_B172_relocated_controls_v4388',
        'lil_B171_editorial_manuscript_v4':'lil_B172_editorial_manuscript_v3','[171]':'[172]','block=171':'block=172',
        "value[1:].replace(b'FI',b'Lil').hex()":"value[1:].hex()",'all8_source_current_nonrelative_nonspeech_leaves':'all11_source_current_nonrelative_nonspeech_leaves',
        '[0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100,0xA000,0x2000]':'[0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100,0x2000]',
        'len(dispatches)==37 and len(leaves)==8':'len(dispatches)==27 and len(leaves)==11',
        'all37_progressive_dispatches_C200_and8_leaves':'all27_progressive_dispatches_C200_then_A000_and11_leaves',
        'all8_source_current_target_nonrelative_nonspeech_leaves':'all11_source_current_target_nonrelative_nonspeech_leaves',
        'all37_progressive_consumers_FI1_FO0_exact':'all27_progressive_consumers_no_macros_exact',
        'source_resource10_boundary_cases_reused_only_by_exact_word_and_runtime':'source_resource30_boundary_cases_reused_only_by_exact_words_and_runtime',
        'source_four_presentation_structural_results_reused_only_by_exact_whole_commands_and_runtime':'source_five_presentation_and_one_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime',
        'presentation_resource_bodies_not_fully_executed_by_this_probe':'presentation_resource_later_A000_bodies_not_fully_executed_by_this_probe',
        'both_consecutive_endwords_and_no_source_pause_or_A000_preserved=True':'single_tail_end_and_no_source_pause_preserved=True,source_A000_hex=cp[\'source_A000_hex\'],source_A000_raw_hex_words=cp[\'source_A000_raw_hex_words\'],source_C200_then_A000_then6240_and_end_preserved=True',
        'actual_selected_B171_IDs':'actual_selected_B172_IDs',
        '37 relocated dispatches,8 exact leaves,C200 queue pair and both ends pass.':'27 relocated dispatches,11 exact leaves,C200 queue pair then A000/6240 and one tail end pass.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_macros=0,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
