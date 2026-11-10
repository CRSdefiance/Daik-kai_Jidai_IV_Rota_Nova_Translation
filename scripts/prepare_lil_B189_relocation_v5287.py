"""Prepare reversible full-scene relocation and final stored native targets."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B189_relocation_tools_v5287')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B188_relocation_v5246.py','scripts/research_lil_B189_relocation_v5287.py',{
        'B188':'B189','relocation_v5246':'relocation_v5287','combined_v5219':'combined_v5263','Relocate all11':'Relocate all17','preserve10 progressive':'preserve16 progressive',
        'len(source)==484 and old_end==482':'len(source)==772 and old_end==770',"len(spec['all_current_native_commands'])==14":"len(spec['all_current_native_commands'])==20",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==11":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==17",
        'number==188':'number==189','==[478]':'==[766]',"sum(len(r['text_records']) for r in results)==11":"sum(len(r['text_records']) for r in results)==17",
        "sum(len(r['command_map']) for r in results)==14":"sum(len(r['command_map']) for r in results)==20",'not in [188]':'not in [189]','all11speech':'all17speech',
        '14structural commands/11speech/10progressive':'20structural commands/17speech/16progressive'} )]
    rows.append(derive('scripts/prove_lil_B188_stored_v5247.py','scripts/prove_lil_B189_stored_v5288.py',{
        'B188':'B189','stored_v5247':'stored_v5288','relocation_v5246':'relocation_v5287','voices_v5233':'voices_v5274b','Verify all11':'Verify all17',
        '[130,150,254]':'[82,104,113,147,254]','len(cases)==11':'len(cases)==17','fresh+reused==44':'fresh+reused==68',
        'all11_final_stored_targets44_macro_cases':'all17_final_stored_targets68_macro_cases','current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=68',
        'all11_final_targets':'all17_final_targets','stored_targets=11,progressive=10':'stored_targets=17,progressive=16','macro_cases=44':'macro_cases=68'}))
    ROOT.mkdir(parents=True)
    font=Path('work/analysis/lil_B189_fonts_v5285/all17_progressive_FE_native_planes_and136_alignment_cases.json');f=read(font)
    save(ROOT/'viewed_layout_retention_reasons.json',dict(native_font_proof=str(font),native_font_proof_sha256=sha(font.read_bytes()),all17_panels_on_three_native_sheets_viewed_after_image_return=True,
        retained_layouts=[dict(id='DK4_MES_B189_R0006',reason='The forty-character recent-acquisition sentence uses two substantial native rows. The ordinary complete-word wrap after hold leaves its of-it/date completion clear on the next row;it adds neither punctuation nor a dramatic pause. Two balanced rows create no extra row or orphan;maximum first-row fill is not required.'),
            dict(id='DK4_MES_B189_R0016',reason='The courteous wish spans two substantial rows. The complete-word wrap between much and like remains continuous speech without a manual pause. Both rows are legible,all words fit,and no orphan or third row is introduced.'),
            dict(id='DK4_MES_B189_R0022',reason='The recent-craze complaint uses three substantial rows for the cause and availability result. Source-explicit meaning remains complete;no fourth row or isolated final word is produced.'),
            dict(id='DK4_MES_B189_R0046',reason='Three complete native rows preserve the commodity,recent sale and boast. The last full row is the complete You would not believe the price sentence,contracted naturally in the manuscript.'),
            dict(id='DK4_MES_B189_R0049',reason='Three native rows keep the pleased customer judgment,the speaking pair’s lack of cash and proposed approach. The final question continues naturally across two rows without adding a manual pause or a fourth row.')],
        no_new_contextual_review_credit=True,no_record_specific_exception_or_font_guard_width_change=True,full_goal_complete=False))
    save(ROOT/'prepared_linear_relocation_and_stored_checks.json',dict(tools=rows,source_stored_bytes=772,source_logical_end=770,source_alignment_tailzeros=2,
        source_commands=20,speeches=17,progressive=16,FE=1,relative_sites=0,predicates=0,A000=1,C200=1,source_end=766,expected_stored_alignment_cases=68,
        target_lengths_to_be_measured=True,exact_inverse_includes_original_tailzeros=True,no_ROM_registry_ledger_or_review_credit_change=True,full_goal_complete=False))
