"""Approve six complete native captions,keeping actual controller coverage pending."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

DOC = Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
PLAN = Path('work/analysis/Rafael261_sparse_row_refinement_v4_20261105/full_plan/automatic_plans.json')
ROOT = Path('work/analysis/Rafael261_choices_20261105')

if __name__ == '__main__':
    out = ROOT/'complete_native_visual_approval_v1.json'
    assert not out.exists()
    inputs = load(ROOT/'source_bound_inputs.json')
    assert inputs['manuscript_sha256'] == sha(DOC.read_bytes())
    menus, sheets, runtime = [], [], None
    for row, directory in zip(inputs['menus'], ['B85_native_v1', 'B88_native_v2', 'B91_native_v1'], strict=True):
        path = ROOT/directory/'menu_provider_and_planes.json'
        proof = load(path)
        assert proof['manuscript_sha256'] == sha(Path(row['manuscript']).read_bytes())
        assert proof['native_choice_object_hex'] == row['compiled_object_hex']
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert proof['source_index_andcount_preserved'] and proof['compiler_owned_zero_alignment_only_no_speech_encoder']
        assert proof['native_provider_alignments'] == 6 and proof['bridged_modal_returns'] == 18
        assert proof['complete_English_caption_style_planes'] == 8
        assert len(proof['compiler_negatives_rejected']) == 7
        if runtime is None:
            runtime = proof['runtime']
        assert proof['runtime'] == runtime
        sheet = proof['review_sheet']
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append(sheet)
        menus.append(dict(block=row['block'], source_command_offset=row['source_command_offset'], target_object_hex=proof['native_choice_object_hex'],
            native_proof=str(path), native_proof_sha256=sha(path.read_bytes())))
    save(out, dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), runtime=runtime,
        menus=menus, typed_labels=6, offline_visual_approved=True, direct_view_pending=False,
        all_three_native_caption_sheets_directly_viewed=True, sheets=sheets,
        complete24_current_andreviewed_style_planes_checked=True, actual_controller_gameplay_pending=True,
        clean_B88_label_host_read_truncation_corrected_without_ROM_orinstruction_change=True,
        failure_receipt=str(ROOT/'B88_provider_failure_v1.json'), new_credit=0))
    styles = ROOT/'no_style_objects_v1.json'
    assert not styles.exists()
    save(styles, dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), plan=str(PLAN), plan_sha256=sha(PLAN.read_bytes()),
        runtime=runtime, objects=[], no_source_style_alternatives_in_this_scope=True, new_credit=0))
    print('Six captions/three native menus approved offline. Actual controller coverage remains pending.')
