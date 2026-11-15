"""Archive route movie evidence, preserving original requirements/releases."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/route_opening_movies_v647')
DOC = Path('docs/route_opening_movies_v647_checkpoint.md')
KEY = 'ordinary_three_route_openings36_source_views94_RGB_frames5_complete_captions_v647'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V647 Route opening movies')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V640 Route opening movies')


def main():
    pp = ROOT / 'route_opening_movie_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['all94_active_movie_compositions_exact'] and not proof['full_goal_complete']
    assert proof['all5_English_captions_complete8559_ink_shadow_texels_and10_visible_boundary_controls']
    assert proof['post_movie_boundary_timing_and_independent_bitmap_paint_proof_remain_open']
    for p, digest in proof['scripts'].items():
        assert sha(Path(p).read_bytes()) == digest
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        current = read(Path('translations') / name)
        assert all(current[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.py'),
                   *ROOT.glob('*.log'), *[Path(p) for p in proof['scripts']]]:
        checked_copy(source, ARCHIVE / source.name)
    captures, guides = [], []
    for label, reports in proof['reports'].items():
        for kind, info in reports.items():
            assert sha(Path(info['path']).read_bytes()) == info['sha256']
            checked_copy(info['path'], ARCHIVE / f'capture_report_{label}_{kind}.json')
        report = read(reports['baseline']['path'])
        shots = {s['frame']: s for s in report['frames_captured']}
        target_dir = ARCHIVE / 'Unmodified ordinary captures' / label
        target_dir.mkdir(parents=True, exist_ok=True)
        for shot in shots.values():
            target = target_dir / Path(shot['path']).name
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            checked_copy(shot['path'], target)
            captures.append({'route': label, 'frame': shot['frame'], 'path': str(target), 'sha256': shot['PNG_sha256']})
        for tid, check in proof['routes'][label]['complete_caption_checks'].items():
            shot = shots[check['display_frame']]
            target = GUIDE / f'V640_{label.upper()}_CARD{tid}_frame{shot["frame"]:06d}_UNMODIFIED.png'
            checked_copy(shot['path'], target)
            guides.append({'route': label, 'card': tid, 'path': str(target), 'sha256': shot['PNG_sha256']})
    save(GUIDE / 'provenance_v647.json', {'candidate_sha256': proof['candidate_sha256'],
        'reports': proof['reports'], 'captures': guides, 'ordinary_no_save_cheat_or_export': True,
        'guide_candidates_only_no_publication_approval': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'captures': captures, 'guides': guides, 'native_exports_remain_on_E_at_report_paths': True,
        'derived_sheets_distinct_from_unmodified_captures': True,
        'all3_post_movie_boundaries_remain_open': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate_sha256': proof['candidate_sha256'], '94_complete_source_frames_36_native_views': True,
        '5_complete_captions_8559_ink_shadow_texels_10_boundary_controls': True,
        '185_complete_two_screen_baselines_exact': True, 'old_V299_Lil42_pixel_clip_reproduced': True,
        'all97_samples_accounted3_post_movie_boundaries_open': True,
        'all18_plaques_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_release_pointers_canonical_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidates': str(GUIDE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        current = read(path)
        current[KEY], current['current_goal_turn_classification'] = entry, 'progress'
        save(path, current)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V647: ordinary route openings and complete five-caption boundaries'
    addition = ('Current V640 ordinary New Game M20/M22/M24 playback binds all36 native source views. '
        '94 complete upper RGB compositions4620288 pixels and all5 caption planes8559 ink/shadow '
        'texels pass,with10 visible boundary controls. The old V299 Lil42-pixel clipping mechanism '
        'is reproduced. Three independent no-export baselines match185 whole two-screen frames '
        '18186240 pixels. All97 planned samples accounted;three post-movie bitmap paint/timing '
        'checks explicitly remain open. Captures/proof/five ordinary guide candidates on E. '
        'No ROM/patch/registry/pointer change. All18 plaques incomplete,all22 scopes exact;full '
        'goal active. See [V647 checkpoint](route_opening_movies_v647_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    print('V647 recorded;94 source frames,5 captions,185 baselines;3 boundaries open;18 plaques/22 scopes exact.')


if __name__ == '__main__':
    main()
