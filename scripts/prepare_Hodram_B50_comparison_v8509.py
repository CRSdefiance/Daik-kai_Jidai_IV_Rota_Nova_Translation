"""Source-lock B50 paired scene/resource/return/state comparisons with all differences retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_comparison_tools_v8509');assert not root.exists()
    proof=derive('scripts/compare_Hodram_B49_actual_v8410.py','scripts/compare_Hodram_B50_actual_v8509.py',{
        'Hodram_B49_comparison_v8410':'Hodram_B50_comparison_v8509',
        'Hodram_B49_actual_v8409':'Hodram_B50_actual_v8507',
        'for number in [49]':'for number in [50]',
        "len(old['unvisited_conditional_text_IDs'])==8":"len(old['unvisited_conditional_text_IDs'])==0",
        "len(old['speeches'])==len(new['speeches'])==6":"len(old['speeches'])==len(new['speeches'])==3\n        for g in [old,new]:\n            assert len(g['command_pairs'])==20 and [c['fixture_offset'] for c in g['command_pairs']]==[c['offset'] for c in g['fixture']['all_fixture_commands']]\n            assert len({s['id'] for s in g['speeches']})==3 and sum(s['source_selector']==254 for s in g['speeches'])==1\n            FE=next(s for s in g['speeches'] if s['source_selector']==254);clear=next(c for c in g['command_pairs'] if c['word']==0x6302)\n            assert FE['returned']<=clear['start'] and all(h['original_FE_absent_nameplate_preserved'] for h in FE['complete_holds'])",
        'if number==49:':'if number==50:',
        "c['word']==0x4820":"c['word']==0x4800",
        "command['whole_command_hex']=='204894a8' and command['canonical_clean_offset']==32":"command['whole_command_hex']=='004894a8' and command['canonical_clean_offset']==214",
        "min(c['start'] for c in hide)-4":"min(c['returned'] for c in hide)-4",
        'original_4820_calls':'original_4800_calls',
        'layout=[2,0,0]':'layout=[0,0,0]',
        'original_Ullr_Bow_item148_source_4820_layout2':'original_Ullr_Bow_item148_source_4800_layout0',
        'original4820_4700_actual':'original4800_4700_actual',
        'current_registered_V8377_andmainV4701_unchanged':'current_registered_V8475_andmainV4701_unchanged',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=proof,all_native_high_integer_constants_andmultiplicity_preserved=True,whole_original_command_order_FE_before6302_andall_three_speeches_enforced=True,no_unchanged_capture_replay=True,new_credit=0,full_goal_complete=False))
