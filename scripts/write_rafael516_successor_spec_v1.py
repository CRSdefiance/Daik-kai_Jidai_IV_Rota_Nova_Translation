"""Declare the existing verified prefix and exact research dependencies for one cumulative build."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

OUT = Path('translations/rafael516_registered_successor_spec_v1.json')
ROOT = Path('work/analysis/Rafael516_combined_research_v1_20261105')
BASE = Path('work/analysis/Rafael255_reconstruction_inputs_v1_20261105')
CHECKED = Path('work/analysis/Rafael255_checked_v2_20261105')

if __name__ == '__main__':
    assert not OUT.exists()
    original = load('translations/rafael261_registered_successor_spec_v2.json')
    registry = Path('translations/release_stack.json')
    assert sha(registry.read_bytes()) == '11021a16ab4b1157d9e34fc71f214fdb2b9eeb565325122444e59e261d0bcec0'
    rebased = load(ROOT/'reconstruction.json')
    spec = {k:original[k] for k in ['parent_release','previous_profile']}
    spec.update(expected_registry_sha256=sha(registry.read_bytes()),
        profile='all-routes-rafael516-20261105', extension_id='rafael-b101-b120',
        module='dk4tool.patch.rafael_story_b101_b120_release_v1',
        config='translations/rafael_B101_B120_editorial_release_v1.json',
        qualified_prefix_preparation='work/analysis/Rafael261_registered_preparation_v2_20261105/registered_preparation.json',
        qualified_prefix_qualification='work/analysis/Rafael261_release_qualification_20261105/qualification.json',
        new_extension_parent='work/analysis/Rafael261_registered_preparation_v1_20261105/stage_0_RESEARCH_REFERENCE.nds',
        verified_parent_ROM_sha256='cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448',
        verified_parent_archive_sha256='d71706e4c6a08459a8803f64b30c2d11fb18a43e71d8aa9784a714e21da12c67',
        stage_configs=[p.replace('Rafael261','Rafael516') for p in original['stage_configs']],
        counts=dict(record_count=255,speech_count=243,typed_choice_count=12,menu_count=4,scoped_name_count=18,
            native_pages=248,relative_cases=180,FE_count=22,actual_frames=29362,actual_runs=2,
            actual_speeches=75,actual_body_pages=77,offline_speeches=168),
        evidence=dict(manuscript=rebased['manuscript'],plan=rebased['plan'],reconstruction=str(ROOT/'reconstruction.json'),
            compiled_native=str(BASE/'native.json'), stored_native='work/analysis/Rafael255_stored_native_v3_20261105/stored_native_verification.json',
            stored_lookup='work/analysis/Rafael255_stored_catalogue_v1_20261105/all_stored_effective_body_bindings.json',
            loaders='work/analysis/Rafael255_loaders_v1_20261105/verification.json',visual_review=str(CHECKED/'complete_visual_approval.json'),
            actual=str(CHECKED/'actual_review.json'),scoped_names='translations/rafael_B101_B120_scoped_names_final_v1.json',
            typed_menu=str(BASE/'menu.json'),native_styles=str(BASE/'styles.json'),
            focused_pixels='work/analysis/Rafael255_Julio_actual_pixels_v1_20261105/focused_actual_pixels.json',
            menu_body_pixels='work/analysis/Rafael255_dynamic_actual_pixels_v1_20261105/focused_actual_pixels.json',
            menu_pixels='work/analysis/Rafael255_menu_actual_pixels_v1_20261105/menu_actual_pixels.json',
            dependency_qualification=str(ROOT/'dependency_reuse.json'),
            research_reconstruction='work/analysis/Rafael255_rebuilt678_v2_20261105/reconstruction.json'),
        note='Experimental cumulative261+255 Rafael reviews afterverified678:516 objects,246 revisions/270 retentions. Retainall114 accepted layers/eight final stages andfull editorial scope. Failed679 remains preserved,not a registered predecessor. No promotion,guidephotos ornew credit beforecomplete verification.')
    spec['dependencies'] = sorted(set(original['dependencies'] + [
        'dk4tool/patch/rafael_story_b85_b100_release_v1.py',
        'translations/rafael_B85_B100_editorial_release_v1.json',
        'dk4tool/dialogue/reviewed_actor_style_object_v1.py',
        'scripts/prepare_plain_SC0_registered_successor_v1.py',
        'scripts/prepare_rafael516_registered_successor_v1.py',str(Path(__file__)),
        'scripts/rebase_rafael255_over261_v1.py',str(CHECKED/'research_completion.json'),
        'scripts/finalize_rafael255_research_v1.py','scripts/finalize_rafael255_research_v2.py',
        str(BASE/'visual_andinventory_approval.json'),
        'work/analysis/Rafael241_scoped_name_planes_v1_20261105/native_name_planes.json',
        'work/analysis/Rafael255_Julio_compact_sheets_v1_20261105/receipt.json',
        'work/analysis/Rafael255_dynamic_compact_sheets_v1_20261105/receipt.json',
        'translations/rafael_B101_B120_contextual_final_review_v1.json',
    ]))
    assert all(Path(p).is_file() for p in [*spec['dependencies'],*spec['evidence'].values()])
    save(OUT,spec)
    print('Declared516 successor ofverified678 withtwo immutable ordered adapters;all dependencies present. No registry mutation yet.')
