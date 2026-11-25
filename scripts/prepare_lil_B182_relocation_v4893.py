"""Prepare reversible B182 relocation, preserving all conditional command fields."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B182_relocation_tools_v4893')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B180_relocation_v4798.py','scripts/research_lil_B182_relocation_v4893.py',{
        'B180':'B182','relocation_v4798':'relocation_v4893','combined_v4766':'combined_v4867',
        'all11':'all8','len(source)==old_end==576':'len(source)==old_end==636',
        "len(spec['all_current_native_commands'])==28":"len(spec['all_current_native_commands'])==25",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==11":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==8",
        'number==180':'number==182','==[572]':'==[632]',
        "sum(len(r['text_records']) for r in results)==11":"sum(len(r['text_records']) for r in results)==8",
        "sum(len(r['command_map']) for r in results)==28":"sum(len(r['command_map']) for r in results)==25",
        'not in [180]':'not in [182]','28structural commands/11speech':'25structural commands/8speech'}),
        derive('scripts/prove_lil_B180_stored_v4799.py','scripts/prove_lil_B182_stored_v4894.py',{
            'B180':'B182','stored_v4799':'stored_v4894','relocation_v4798':'relocation_v4893','voices_v4775':'voices_v4879',
            'len(cases)==11':'len(cases)==8','fresh+reused==44':'fresh+reused==32',
            'all11_final_stored_targets44_macro_cases':'all8_final_stored_targets32_macro_cases',
            'current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=32',
            'all11_final_targets':'all8_final_targets','Verify all11':'Verify all8',
            'stored_targets=11,progressive=10':'stored_targets=8,progressive=7','macro_cases=44':'macro_cases=32'})]
    ROOT.mkdir(parents=True);save(ROOT/'prepared_relocation.json',dict(tools=tools,source_bytes=636,source_commands=25,
        speeches=8,progressive=7,FE=1,relative_sites=10,predicates=2,alternative_A000=3,C200=1,single_end=632,
        final_stored_alignment_cases=32,no_ROM_registry_ledger_or_credit_change=True,full_goal_complete=False))
    print('Prepared conditional B182 relocation/inverse and32 final stored alignment cases.')
