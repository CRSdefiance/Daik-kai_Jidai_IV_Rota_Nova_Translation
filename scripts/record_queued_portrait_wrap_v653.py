"""Archive the shared formatter repair without closing any graphics audit scope."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')
DOC = Path('docs/queued_portrait_wrap_v653_checkpoint.md')
KEY = 'shared_original_queued_portrait_parents19_voices19_actual_states_and_complete_native_planes_v653'
LATEST = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V653 Shared portrait wrapping')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V653 Recruitment and crew')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    path = ROOT / 'release_proof.json'
    proof, pre = read(path), read(ROOT / 'preflight.json')
    assert proof['script_sha256'] == sha(Path('scripts/verify_queued_portrait_wrap_v653.py').read_bytes())
    assert proof['all_three_observed_word_splits_repaired'] and not proof['full_goal_complete']
    assert len(proof['actual_complete_portrait_planes']) == 19
    assert sum(r['actual_native_view'] is not None for r in proof['actual_complete_portrait_planes']) == 7
    for suffix, digest in (('.nds', proof['candidate_sha256']), ('.xdelta', proof['patch_sha256']),
                           ('.manifest.json', proof['manifest_sha256'])):
        assert sha(Path(proof['candidate']).with_suffix(suffix).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, LATEST, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    scripts = ['dk4tool/patch/queued_portrait_wrap.py',
               'scripts/prepare_queued_portrait_wrap_v653.py', 'scripts/probe_queued_portrait_wrap_v653.py',
               'scripts/probe_queued_callers_v653.py', 'scripts/prepare_queued_runs_v653.py',
               'scripts/prepare_queued_export_controls_v653.py', 'scripts/run_queued_portrait_v653.py',
               'scripts/native_full_fleet_proximity_v653.py', 'scripts/verify_queued_portrait_wrap_v653.py',
               'scripts/record_queued_portrait_wrap_v653.py', 'scripts/build_integrated_release.py']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    # Clearly labeled actual comparisons; never count these composites as guide captures.
    for case, frame in (('staffing', 5200), ('staffing', 12800), ('battle', 15200)):
        row = next(r for r in proof['actual_complete_portrait_planes'] if r['case'] == case and r['frame'] == frame)
        sheet = Image.new('RGB', (2 * 228 * 3 + 30, 80 * 3 + 36), (35, 42, 48))
        draw = ImageDraw.Draw(sheet)
        for index, key, label in ((0, 'source_PNG', 'V651 original'), (1, 'candidate_PNG', 'V653 repaired')):
            draw.text((10 + index * (228 * 3 + 10), 8), label, fill='white')
            crop = Image.open(row[key]['path']).convert('RGB').crop((16, 296, 244, 376))
            sheet.paste(crop.resize((228 * 3, 80 * 3), Image.Resampling.NEAREST), (10 + index * (228 * 3 + 10), 28))
        sheet.save(ROOT / f'{case}_{frame:06d}_ACTUAL_COMPARISON.png')
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.txt'), *ROOT.glob('*.log'),
                   *map(Path, scripts), Path('translations/queued_portrait_wrap_v1.json')]:
        copy(source, ARCHIVE / source.name)
    initial = read(ROOT / 'initial_newgame_report.json')
    export = read(ROOT / 'independent_export_control_proof.json')
    controls = [r for r in export['cases'] if r['label'] == 'control']
    receipts = [*proof['reports'], {'case': 'newgame_initial', **initial},
                {'case': 'newgame_control', 'path': controls[0]['current'],
                 'sha256': controls[0]['current_report_sha256']}]
    assert len(receipts) == 5
    guides = []
    for receipt in receipts:
        rp = Path(receipt['path'])
        assert sha(rp.read_bytes()) == receipt['sha256']
        report = read(rp)
        assert report['frames'] in (19600, 23600, 24100)
        copy(rp, ARCHIVE / (receipt['case'] + '_capture_report.json'))
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            copy(shot['path'], ARCHIVE / receipt['case'] / Path(shot['path']).name)
            if receipt['case'] == 'staffing' and shot['frame'] in (5200, 12800):
                target = GUIDE / Path(shot['path']).name
                copy(shot['path'], target)
                guides.append({'path': str(target), 'sha256': shot['PNG_sha256'],
                    'report': str(rp), 'frame': shot['frame'],
                    'ordinary_input_no_gameplay_fixture_unmodified_capture': True})
    assert len(guides) == 2
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
         'screenshots': guides, 'publication_approved': False})
    entry = {'documentation': str(DOC), 'proof': str(path), 'proof_sha256': sha(path.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'profile': proof['profile'], 'patch_sha256': proof['patch_sha256'],
        'status': 'experimental_shared_queued_portrait_wrap_native_and_actual_verified',
        'same_original_actor_factory_two_exact_parents_no_per_table_admission': True,
        'all19_voices114_native_layouts_and22008_unrelated_dispatch_executions_pass': True,
        'all19_actual_changed_states_complete_ink_shadow_blank_cells_and_word_checks': True,
        'all191_other_sampled_two_screen_frames_exact': True,
        'seven_complete10944_cell_captured_native_views_pass': True,
        'five_terminal_cold_boots_and178_independent_whole_screen_export_controls': True,
        'only16_existing_ARM9_dispatcher_bytes_changed_prose_and_graphics_unchanged': True,
        'all470_batches114_layers921_views57_embedded_extents_and_exact_patch_retained': True,
        'all18_original_plaques_incomplete_22_historical_scopes_exact': True,
        'helper_fifth_row_and_oversized_word_fallbacks_not_arbitrary_pagination_clearance': True,
        'archive': str(ARCHIVE), 'guide_archive': str(GUIDE),
        'canonical_promoted': False, 'full_goal_complete': False}
    for name in frozen:
        target = Path('translations') / name
        data = read(target)
        data[KEY] = entry
        latest = data.get(LATEST, {}).copy()
        latest.update({'candidate': proof['candidate'], 'sha256': proof['candidate_sha256'],
                       'profile': proof['profile'], 'shared_queued_portrait_wrap_actual_verified': True,
                       'broader_graphics_gates_remain_open': True})
        data[LATEST], data['current_goal_turn_classification'] = latest, 'progress'
        save(target, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, LATEST, 'current_goal_turn_classification'))
    heading = '## V653: shared queued portrait formatter and complete actual text planes'
    addition = ('The original question/notice role parents share one actor-backed widget. '
        'V653 changes only16 dispatcher bytes to admit both parents independently of voice table, '
        'preserving all prose and graphics. All19 affected voices pass114 native layouts; '
        '22008 unrelated numeric dispatch executions remain exact. Five terminal cold boots '
        'verify19 changed message states,191 unchanged whole screens and seven complete10944-cell '
        'native views. Recruitment coins,unassigned that and retreat Retreat are no longer split. '
        'Two coordinate-only battle fixtures are disclosed;fleet outcomes remain exact and '
        'victory/rewards are not reached. Two independent export controls match178 whole frames. '
        'All470 batches/114 layers/921 views/57 embedded extents and exact clean patch remain. '
        'Latest compiled experimental pointer advances to V653;canonical/V610 verified pointers '
        'stay unchanged. All18 plaques remain incomplete and22 scopes exact;full goal active. '
        'Evidence and two ordinary guide candidates on E. See '
        '[V653 checkpoint](queued_portrait_wrap_v653_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'all_five_runs_terminal_and_no_savestates': True,
        'only_battle_uses_two_position_fixtures_no_earned_victory_claim': True,
        'ROM_patch_manifest_RAM_native_exports_retained_at_original_E_paths': True,
        'final_support_scripts': {p: sha(Path(p).read_bytes()) for p in scripts},
        'runner_optional_export_control_support_added_only_after_initial_three_runs_terminal': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V653 evidence archived; all three audits and four progress documents updated; full18/22 scope remains open.')


if __name__ == '__main__':
    main()
