"""Prepare reversible B183 relocation and both final stored FE consumers."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B183_relocation_tools_v4947')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B181_relocation_v4846.py','scripts/research_lil_B183_relocation_v4947.py',{
        'B181':'B183','relocation_v4846':'relocation_v4947','combined_v4821':'combined_v4914',
        'editorial_manuscript_v3':'editorial_manuscript_v7',
        'len(source)==old_end==396':'len(source)==old_end==956',
        "len(spec['all_current_native_commands'])==13":"len(spec['all_current_native_commands'])==28",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==10":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==25",
        'number==181':'number==183','==[392]':'==[952]',
        "sum(len(r['text_records']) for r in results)==10":"sum(len(r['text_records']) for r in results)==25",
        "sum(len(r['command_map']) for r in results)==13":"sum(len(r['command_map']) for r in results)==28",
        'not in [181]':'not in [183]','all10speech':'all25speech','source_FE_system_objects=1':'source_FE_system_objects=2',
        'Relocate all10':'Relocate all25','preserve9 progressive,one impersonal FE':'preserve23 progressive,two impersonal FE',
        '13structural commands/10speech/9progressive/1FE':'28structural commands/25speech/23progressive/2FE'}),
        derive('scripts/prove_lil_B181_stored_v4847.py','scripts/prove_lil_B183_stored_v4948.py',{
            'B181':'B183','stored_v4847':'stored_v4948','relocation_v4846':'relocation_v4947','voices_v4833':'voices_v4926',
            'editorial_manuscript_v3':'editorial_manuscript_v7','in [166,167,168,254]':'in [85,110,132,148,153,254]',
            'len(cases)==10':'len(cases)==25','fresh+reused==40':'fresh+reused==100',
            "sum(c['consumer']=='FE-paper' for c in cases)==1":"sum(c['consumer']=='FE-paper' for c in cases)==2",
            'all10_final_stored_targets40':'all25_final_stored_targets100','current_final_stored_macro_alignment_cases=40':'current_final_stored_macro_alignment_cases=100',
            'all10_final_targets':'all25_final_targets','Verify all10':'Verify all25',
            'stored_targets=10,progressive=9,FE=1,macro_cases=40':'stored_targets=25,progressive=23,FE=2,macro_cases=100'})]
    ROOT.mkdir(parents=True);save(ROOT/'prepared_relocation.json',dict(tools=tools,source_bytes=956,source_commands=28,
        speeches=25,progressive=23,FE=2,relative_sites=0,predicates=0,A000=1,C200=1,end952=True,
        final_stored_alignment_cases=100,new_ROM_or_emulator_or_credit_change=False,full_goal_complete=False))
    print('Prepared B183 linear relocation/inverse and100 final stored alignment cases,including both FE objects.')
