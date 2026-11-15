"""Prepare the full English scene and exact paired clean-source capture audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_English_tools_v6042')
if __name__=='__main__':
    assert not ROOT.exists();plan=read('work/analysis/lil_B203_relocation_v6035/nested_source_relocation_research.json');b=plan['blocks'][0]
    assert b['block']==203 and b['source_bytes']==816 and b['source_logical_end']==814
    tools=[derive('scripts/research_lil_B202_English_fixture_v5990.py','scripts/research_lil_B203_English_fixture_v6042.py',{
        'B202':'B203','prepare_lil_B202_references_v5982':'prepare_lil_B203_references_v6034',
        'English_fixture_v5990':'English_fixture_v6042','English_v5990':'English_v6042','source_fixture_v5967':'source_fixture_v6018',
        'bank[202]':'bank[203]','source_block=202':'source_block=203',
        'len(native)==26 and len(commands)==35 and len(speeches)==19':'len(native)==31 and len(commands)==40 and len(speeches)==22',
        'all35':'all40','all26':'all31','event202_activation':'event203_activation',
        'source_fixture_v5968':'source_fixture_v6019','English_fixture_v5991':'English_fixture_v6043',
        'source_run_v5968':'source_run_v6019','source_v5968':'source_v6019','English_run_v5991':'English_run_v6043','English_v5991':'English_v6043',
        '26 original+9 initializer commands,19 speech objects':'31 original+9 initializer commands,22 speech objects',
    })]
    tools.append(derive('scripts/audit_lil_B202_actual_v5992.py','scripts/audit_lil_B203_actual_v6044.py',{
        'B202':'B203','actual_v5992':'actual_v6044','source_fixture_v5967':'source_fixture_v6018','English_fixture_v5990':'English_fixture_v6042',
        'source_run_v5968':'source_run_v6019','English_run_v5991':'English_run_v6043',
        'fonts_v5978':'fonts_v6030','all19_progressive_native_planes_and152_alignment_cases':'all22_progressive_FE_native_planes_and176_alignment_cases',
        '[5,9,13,16,20,23,27,31,35,39,43,47,51,55,58,61,65,68,72]':'[5,9,13,17,21,24,28,31,35,38,42,46,50,54,57,60,63,67,70,74,77,80]',
        "pairs[-1]['source_offset']==582":"pairs[-1]['source_offset']==810",'len(pairs)==35':'len(pairs)==40',
        'len(actual)==19':'len(actual)==22',"sum(r['prefix']==254 for r in actual)==0":"sum(r['prefix']==254 for r in actual)==1",
        'all26_source_commands':'all31_source_commands','end582':'end810','event202_activation':'event203_activation',
        'nineteen_actual_panels':'twenty_two_actual_panels','actual_unique_speech_panels=19':'actual_unique_speech_panels=22','panels=19':'panels=22',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_English_fixture_and_audit_tools.json',dict(tools=tools,source_bytes=816,source_logical_end=814,target_bytes=b['research_bytes'],target_logical_end=b['research_logical_end'],all31_source_commands_and9_initializers_preserved=True,new_review_credit=0,full_goal_complete=False))
    print('Complete B203 English fixture/run and22-panel progressive/FE paired audit prepared;exact extents bound to relocation proof.')
