"""Prepare complete linear relocation and measured stored native alignment."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B193_relocation_tools_v5461')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B192_relocation_v5420.py','scripts/research_lil_B193_relocation_v5461.py',{
        'B192':'B193','relocation_v5420':'relocation_v5461','combined_v5396':'combined_v5437','all8':'all15','preserve7 progressive':'preserve14 progressive',
        'len(source)==404 and old_end==402':'len(source)==668 and old_end==666',"len(spec['all_current_native_commands'])==11":"len(spec['all_current_native_commands'])==18",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==8":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==15",
        'number==192':'number==193','==[398]':'==[662]',"sum(len(r['text_records']) for r in results)==8":"sum(len(r['text_records']) for r in results)==15",
        "sum(len(r['command_map']) for r in results)==11":"sum(len(r['command_map']) for r in results)==18",'not in [192]':'not in [193]',
        '11structural commands/8speech/7progressive':'18structural commands/15speech/14progressive'} )]
    rows.append(derive('scripts/prove_lil_B192_stored_v5421.py','scripts/prove_lil_B193_stored_v5462.py',{
        'B192':'B193','stored_v5421':'stored_v5462','relocation_v5420':'relocation_v5461','voices_v5407':'voices_v5448','[115,153,254]':'[166,167,168,254]',
        'len(cases)==8':'len(cases)==15','fresh+reused==32':'fresh+reused==60','all8':'all15','targets32_macro':'targets60_macro','current_final_stored_macro_alignment_cases=32':'current_final_stored_macro_alignment_cases=60',
        'stored_targets=8,progressive=7':'stored_targets=15,progressive=14','macro_cases=32':'macro_cases=60'}))
    ROOT.mkdir(parents=True);font=Path('work/analysis/lil_B193_fonts_v5459/all15_progressive_FE_native_planes_and120_alignment_cases.json')
    save(ROOT/'viewed_layout_retention_reasons.json',dict(native_font_proof=str(font),native_font_proof_sha256=sha(font.read_bytes()),
        all15_panels_on_two_native_sheets_viewed_after_image_return=True,
        retained_layouts=[dict(id='DK4_MES_B193_R0006',reason='Two substantial rows preserve the satisfied reaction and full first-person meal praise,without an isolated trailing word or added page.'),
            dict(id='DK4_MES_B193_R0025',reason='The complete explanation has109 ASCII characters including spaces;three guarded rows provide at most106 cells,so four rows are necessary without shortening the prose. The first two complete sentences each fit a row and the final compatibility clause occupies two substantial rows. All reportedness and ingredients remain;one page is complete.'),
            dict(id='DK4_MES_B193_R0037',reason='Two substantial rows keep relief,tentative first-person cooking intention and tonight complete. No artificial paragraph break or extra page.'),
            dict(id='DK4_MES_B193_R0044',reason='Two substantial rows retain the friendly question,explicit cooking instruction and now;the offer stays a single complete paragraph.')],
        no_record_specific_boundary_exception_or_font_metric_guard_width_change=True,no_credit=True,full_goal_complete=False))
    save(ROOT/'prepared_linear_relocation_and_stored_checks.json',dict(tools=rows,source_stored=668,source_logical=666,source_tailzeros=2,source_commands=18,speeches=15,
        expected_stored_cases=60,all_target_extents_to_be_measured=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
