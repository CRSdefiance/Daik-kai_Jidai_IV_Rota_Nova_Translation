"""Prepare B172 relocation and108 final stored processor/alignment cases."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_relocation_tools_v4381')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B171_relocation_v4332.py','scripts/research_lil_B172_relocation_v4381.py',{
        'Relocate all37 B171 speeches;preserve eight leaves,C200 and both consecutive ends.':'Relocate all27 B172 speeches;preserve eleven leaves,C200 then later A000 and one tail end.',
        'lil_B171_relocation_v4332':'lil_B172_relocation_v4381',
        'lil_B171_editorial_manuscript_v4':'lil_B172_editorial_manuscript_v3','all_routes_combined_v4303':'all_routes_combined_v4353',
        'assert number==171 and len(end_maps)==2':'assert number==172 and len(end_maps)==1',
        '[2112,2116] # both consecutive source ends preserved':'[1880] # one complete source tail end preserved',
        'for r in results)==37':'for r in results)==27',"for r in results)==45":"for r in results)==38",
        '[171]':'[172]','all37speech_and8_nonrelative_leaves_preserved':'all27speech_and11_nonrelative_leaves_preserved',
        'two_consecutive_declared_endwords_exact':'single_declared_tail_endword_exact',
        '45commands/37speech/noFE/no_relative_sites,no pause andtwo consecutive ends':'38commands/27speech/noFE/no_relative_sites,no pause,C200 then later A000 andone tail end',
    })]
    tools.append(derive('scripts/prove_lil_B171_stored_v4333.py','scripts/prove_lil_B172_stored_v4382.py',{
        'all37':'all27','lil_B171_stored_v4333':'lil_B172_stored_v4382',
        'lil_B171_editorial_manuscript_v4':'lil_B172_editorial_manuscript_v3',
        'lil_B171_relocation_v4332':'lil_B172_relocation_v4381','lil_B171_voices_v4312':'lil_B172_voices_v4365',
        '[2,25,81]':'[2,26,201]','len(cases)==37':'len(cases)==27','fresh+reused==148':'fresh+reused==108',
        'stored_targets148':'stored_targets108','current_final_stored_macro_alignment_cases=148':'current_final_stored_macro_alignment_cases=108',
        'stored_targets=37,progressive=37,FE=0':'stored_targets=27,progressive=27,FE=0','macro_cases=148':'macro_cases=108',
        'four previously verified original macro cases':'four previously verified original processor/alignment cases;source macros0',
        'Fresh original four-alignment macro calls':'Fresh original four-alignment processor calls;source macros0',
        'actual_selected_scenes_and_presentation_resource_bodies_unexecuted':'actual_selected_scenes_and_presentation_resource_later_A000_bodies_unexecuted',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=172,speeches=27,commands=38,
        nonrelative_leaves=11,relative_sites=0,predicates=0,pause=0,A000=1,A000_hex='00a0ffff010cc960',C200=1,
        resources=[0x6329,0x6340,0x632A],source_end_offsets=[1880],presentations=[0x6000,0x45FF,0x4651,0x4620,0x6240],
        source_macros=0,final_stored_processor_alignment_cases=108),no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B172 relocation and108 stored alignment-case producers;eleven leaves,C200-before-A000 and one tail end retained.')
