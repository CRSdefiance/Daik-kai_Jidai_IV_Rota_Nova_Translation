"""Record bounded source classification without closing missing screen contexts."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.research_relocated_sources_v695 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V695 Relocated UI sources')
DOC = Path('docs/relocated_sources_v695_checkpoint.md')
KEY = 'actual_relocated42_source_planes177_native_selections_two_original_ARM9_UI_atlases_v695'
SOURCES = ('scripts/research_relocated_sources_v695.py', 'scripts/verify_relocated_sources_v695.py',
           'scripts/record_relocated_sources_v695.py', 'scripts/verify_relocated_sources_archive_v695.py',
           'scripts/research_equipment_cursor_v663.py', 'scripts/research_town_scene_v644.py',
           'scripts/scan_graphic_template_aliases_v602.py', 'scripts/verify_graphic_paints_v669.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_relocated_sources_v695.py').read_bytes())
    assert len(proof['complete_actual_native_source_planes']) == 42
    assert len(proof['two_original_ARM9_embedded_UI_atlases']) == 6
    assert proof['no_missing_parent_no_global_unused_or_current_gameplay_claim']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'source_sheet_opened': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'original_button_backdrops_and_Latin_controller_glyphs_have_no_Japanese_text': True,
        'whole_planes_and_selected_native_use_not_all_palette_glyph_variants_or_new_gameplay': True,
        'source_art_retained_current_V692_has_no_new_art_change': True,
        'six_actual_control_contexts_remain_open': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'all42_complete_relocated_planes_and177_original_native_selections_verified': True,
        'two_whole_ARM9_UI_atlases_clean_V653_current_exact_retain_Latin_symbols_and_backdrops': True,
        'all660_current_PXL_files_exact_V653_and_all_executed_current_code_exact': True,
        'three_whole_native_lower_outputs_exact_retained_off_phase_not_new_same_frame_GPU_proof': True,
        'only_known_Frame_sources_contain_miniature_templates_no_selected_intersection': True,
        'no_new_missing_control_parent_or_global_nonuse_claim': True,
        'all18_plaques_incomplete22_historical_scopes_and_broader_goal_open_or_exact': True,
        'ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V695: relocated source planes and two original embedded UI atlases'
    addition = (
        'Three isolated original lower paints use retained V653 Sailor Info states;no new '
        'gameplay run. All660 current PXL files and every executed current instruction match. '
        'All42 whole source planes and177 actual primitive selections are retained,including '
        'relocated RAM/VRAM/DTCM palettes and pixels. Whole pixels/selected palettes bind '
        'Frame,Marker,Person Info and chip files. Two original ARM9 UI atlases at21279AC/'
        '211B688 match clean/V653/current completely:button backdrops and Latin controller '
        'icons,visually reviewed and retained. Seven current plus seven original complete '
        'templates find miniature captions only in known Frame sources;none of177 selected '
        'rectangles touches them. Matcher stride/non-anchor controls pass. Three complete '
        '98304-byte outputs equal retained explicit off-phase outputs;RGB capture differences '
        'are retained,not new same-frame GPU credit. Initial decoder/width/preflight mistakes '
        'are documented;no game bytes change. This narrows these sources without locating '
        'six missing control contexts or claiming global nonuse. All18 plaques incomplete '
        'and22 historical scopes exact;broader goal and V694 suffix gap remain open. V692/'
        'patch/registry/pointers unchanged;evidence on E,no guide promotion,commit or push. '
        'Full goal active. See [V695 checkpoint](relocated_sources_v695_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': proof['external_retained_capture_sources'],
        'no_new_ROM_gameplay_or_guide_promotion': True, 'full_goal_complete': False})
    print('V695 complete relocated-source and embedded-art classification recorded; missing contexts remain open.', flush=True)


if __name__ == '__main__':
    main()
