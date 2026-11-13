"""Correct the B198 test reference to the executed story caller's style11;change no ROM bytes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_story_style_tools_v5741')
PROOF='work/analysis/lil_B198_ellipsis_context_v5740c/original_caller_style11_two_CP932_pauses_and_ASCII_control.json'
OLD="    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)\n    raster.__kwdefaults__=original_raster.__kwdefaults__"
NEW="""    story_style=read(STORY_STYLE)
    assert story_style['candidate_sha256']==doc['current_ROM_sha256']
    assert story_style['source_context_style_field']==0x30 and story_style['source_explicit_style']==11
    assert all(r['exact_actual_ink'] and r['exact_actual_gray'] for r in story_style['cases'])
    raster_env={**original_raster.__globals__,'NdsImage':FontROM}
    exec(compile(story_style['source_owned_raster_adapter'],__file__+'::original_story_style11','exec'),raster_env)
    raster=raster_env['raster']"""
if __name__=='__main__':
    assert not ROOT.exists()
    proof=read(PROOF);assert len(proof['cases'])==3 and all(r['exact_actual_ink'] and r['exact_actual_gray'] for r in proof['cases'])
    rows=[derive('scripts/verify_lil_B198_fonts_v5723.py','scripts/verify_lil_B198_fonts_v5741.py',{
        'fonts_v5723':'fonts_v5741',OLD:NEW,
        "FORMATTER=Path('dk4tool/dialogue/lil_B198_layout_v2.py')":"FORMATTER=Path('dk4tool/dialogue/lil_B198_layout_v2.py')\nSTORY_STYLE=Path("+repr(PROOF)+')',
        'colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}':'colors={0:(239,232,201),1:(0,8,0),11:(0,8,0),15:(98,97,98)}',
        'FE_historical_calibration=calibration,':'source_original_progressive_caller_style=11,source_original_progressive_style_proof=str(STORY_STYLE),source_original_progressive_style_proof_sha256=sha(STORY_STYLE.read_bytes()),FE_historical_calibration=calibration,'})]
    rows.append(derive('scripts/prove_lil_B198_stored_v5726.py','scripts/prove_lil_B198_stored_v5742.py',{
        'stored_v5726':'stored_v5742','lil_B198_editorial_manuscript_v4.json':'lil_B198_editorial_manuscript_v5.json',
        OLD:NEW,
        "PLAN=Path('work/analysis/lil_B198_relocation_v5725/nested_source_relocation_research.json')":"PLAN=Path('work/analysis/lil_B198_relocation_v5725/nested_source_relocation_research.json')\nSTORY_STYLE=Path("+repr(PROOF)+')',
        "plan['manuscript_sha256']==sha(DOC.read_bytes())":"plan['manuscript_sha256']==doc['prior_native_approval_manuscript_sha256']",
        "FE_calibration=calibration,":"source_original_progressive_caller_style=11,source_original_progressive_style_proof=str(STORY_STYLE),source_original_progressive_style_proof_sha256=sha(STORY_STYLE.read_bytes()),FE_calibration=calibration,"}))
    rows.append(derive('scripts/audit_lil_B198_actual_v5740.py','scripts/audit_lil_B198_actual_v5743.py',{
        'actual_v5740':'actual_v5743',
        'fonts_v5723':'fonts_v5741'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_story_style11_native_successors.json',dict(tools=rows,original_story_style_proof=PROOF,
        preserved_generic_catalogue_style1_proof_does_not_model_this_CP932_story_shadow=True,
        preliminary_height_interpretation_v5740b_superseded_by_executed_style_argument11=True,
        no_ROM_runtime_prose_controls_wrapping_native_font_metrics_or_captured_pixel_change=True,
        all17_final_native_planes_and68_stored_alignment_cases_and15_actual_panels_required=True,
        initial_actual_audit_failure_and_all_probe_outputs_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared source-caller style11 native/stored/actual references. Runtime,prose,wrapping and captures remain unchanged.')
