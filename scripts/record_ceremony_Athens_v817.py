"""Record Athens partial evidence and failed state gate without completion credit."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_Athens_v816')
ACCESS = Path('work/analysis/ceremony_access_v810')
DOC = Path('docs/ceremony_Athens_v816_checkpoint.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ROM = Path('out/all_routes_combined_v809_candidate.nds')
SUMMARY = ('V816-V817 reaches Athens through original docking with declared coordinate/date/access inputs and creates new normally saved test donors. '
    'The alternate Temple chant passes7 complete holds,19 whole-screen controls and23 state pairs,including its48-tick return. '
    'Site dance/fast/climb/decline add26 complete glyph holds and22 screen controls, but the unchanged full state gate FAILS after climb frame18600: '
    '123 actor bytes and87 town bytes differ;calendar,funds,models and tasks match. PRNG matches at18200 then reaches states860 versus870 original-generator calls later;exact source remains unmapped. '
    'All assertions remain in place;glyph-only evidence does not approve world outcomes. Source-confirmed open findings cover COMMON335/336 split stat words and SC1 B158 R0039 dark/gloomy wording. '
    'Combined actual glyph coverage is59 holds across37 distinct IDs;other protagonist reactions and final whole-family verification remain. '
    'V809 ROM/patch/dependencies stay exact;550 completed/605 COMMON source-prose/55 pending unchanged;editorial goal active and graphics audit separate.')


def main():
    assert sha(ROM.read_bytes()) == '4b85eae04e1f1654022433c2a9a2aafd8b719daf10cc5f2120a32f9781728ae2'
    cfg = read('translations/ceremony_editorial_release_v1.json')
    for path, expected in cfg['dependencies'].items():
        assert sha(Path(path).read_bytes()) == expected, path
    temple_path = ROOT/'Athens_Temple_chant_gameplay_verification_v816.json'
    glyph_path = ROOT/'Athens_site_glyph_stage_only_v817.json'
    failure_path = ROOT/'Athens_site_full_gate_failure_v817.json'
    temple, glyph, failure = [read(p) for p in (temple_path, glyph_path, failure_path)]
    assert temple['producer_sha256'] == sha(Path('scripts/verify_ceremony_Athens_gameplay_v816.py').read_bytes())
    assert glyph['producer_sha256'] == failure['producer_sha256'] == sha(Path('scripts/audit_ceremony_Athens_failure_v817.py').read_bytes())
    assert not failure['full_gate_passed'] and failure['no_assertions_removed_or_failures_waived']
    assert '18600' in failure['assertion'] and 'persistent_objects' in failure['assertion']
    assert len(temple['complete_scene_holds']) == 7 and len(glyph['complete_scene_holds']) == 26
    assert len(temple['full_screen_controls']) == 19 and len(glyph['full_screen_controls']) == 22
    historical = [read(ACCESS/'prayer_gameplay_verification_v814.json'),
        *(read(ACCESS/(n+'_gameplay_verification_v815.json')) for n in ('site_chant', 'temple_preparations', 'church_prayer'))]
    holds = [h for p in (*historical, temple, glyph) for h in p['complete_scene_holds']]
    ids = sorted({h['message_id'] for h in holds}); assert len(holds) == 59 and len(ids) == 37
    donor_directory = Path('E:/Rota Nova translations/Saves/Test fixtures')
    for name in ('V816 Athens day21 Temple ready', 'V816 Athens day21 site ready'):
        manifest = read(donor_directory/(name+'.fixture.json'))
        assert sha((donor_directory/(name+'.dsv')).read_bytes()) == manifest['sha256']
    guide = Path('E:/Rota Nova translations/Guide screenshots/Editorial V809/Athens Temple chant')
    guide.mkdir(parents=True, exist_ok=True); images = []
    for h in temple['complete_scene_holds']:
        source = Path(h['capture']['path']); target = guide/f"COMMON{h['message_id']}_frame_{h['frame']:06d}.png"
        if target.exists():
            assert sha(target.read_bytes()) == sha(source.read_bytes())
        else:
            shutil.copyfile(source, target)
        images.append(dict(path=str(target), sha256=sha(target.read_bytes()), frame=h['frame'], message_ID=h['message_id']))
    save(guide/'provenance.json', dict(ROM_sha256=sha(ROM.read_bytes()), verification=str(temple_path),
        verification_sha256=sha(temple_path.read_bytes()), targeted_actual_emulator_test=True,
        isolated_access_not_earned_campaign=True, site_world_outcome_gate_failed_separately=True, images=images))
    ledger = read(LEDGER)
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert ledger['records_editorially_completed'] == 550 and ledger['records_with_source_and_prose_pass'] == 605
    backup = ROOT/'editorial_ledger_before_v817_checkpoint.json'
    if not backup.exists():
        shutil.copyfile(LEDGER, backup)
    detail = dict(documentation=str(DOC), whole_Temple_proof=str(temple_path),
        site_glyph_only_proof=str(glyph_path), retained_failed_state_gate=str(failure_path),
        new_glyph_holds=33, cumulative_glyph_holds=59, cumulative_distinct_actual_IDs=ids,
        whole_family_approved=False, completion_credit=0,
        remaining='Trace post-climb random/time-update divergence and resolve state gate;verify14 distinct reactions under real Rafael/Lil/Maria identities,then final family review.',
        full_goal_complete=False)
    frame_probe = ROOT/'read_only_frame_probe_v817.json'
    if frame_probe.exists():
        probe = read(frame_probe)
        assert len(probe['read_only_probe_controls']) == 8
        assert probe['first_random_state_difference'] == 18203
        assert probe['first_persistent_object_difference'] == 18220
        assert probe['original_full_state_gate_still_failed']
        detail['read_only_frame_probe'] = str(frame_probe)
        detail['first_random_state_difference_frame'] = 18203
        detail['first_actor_town_difference_frame'] = 18220
        detail['probe_exports_do_not_change_8_selected_entire4MiB_controls'] = True
    ledger['actual_ceremony_Athens_v817'] = detail
    ledger['pending_registered_ceremony_candidate'].update(
        status='partial-actual-fonts-verified;post-climb-state-gate-failed;whole-family-pending',
        latest_actual_checkpoint=detail)
    ledger['next_ceremony_source_packet'].update(actual_partial_gameplay_latest=detail,
        status='37-distinct-IDs-glyph-verified;post-climb-state-gate-failed-and-other-protagonists-pending',
        next=detail['remaining'])
    ledger['active_source_prose_drafts']['note'] = ('51 production paragraphs have201 native layouts/fonts.59 actual glyph holds cover37 distinct IDs;'
        'Temple families pass;post-climb world state comparison fails. Other protagonist reactions and whole52 approval remain.3 older750-752 contexts remain.')
    findings = [dict(id='COMMON335-336-compound-stat-word-splitting', native_message_ids=[335,336],
        status='source-confirmed-open-native-compound-consumer-repair-required',
        proof=str(ACCESS/'levelup_formatting_leads_v816.json'),
        detail='Actual combined level-up notices split Agility/Luck across lines and lack separation. Original screen equality does not approve this formatting.'),
        dict(id='SC1-B158-R0039-dark-gloomy-English', file='/data/SC1.DK4', row_id='DK4_MES_B158_R0039',
        status='source-confirmed-open-naturalness-and-context-revision-required',
        proof=str(ACCESS/'Angelo_route_prose_leads_v816.json'),
        detail='暗いおっさん is a gloomy older man in the Angelo/Hodram/Gerhard exchange; current dark old man is opaque. Full natural-dialogue-v2 review pending.')]
    for finding in findings:
        if not any(row['id'] == finding['id'] for row in ledger['findings']):
            ledger['findings'].append({**finding, 'no_completion_credit':True})
    ledger['formatting_watchlist']['open_actual_levelup_word_split'] = findings[0]
    key = 'V817-Athens-actual-glyphs-and-retained-failed-world-state-gate'
    if not any(r['id'] == key for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(dict(id=key, documentation=str(DOC), new_ROM=False,
            new_editorially_completed=0, new_source_prose_reviewed=0, new_actual_glyph_holds=33,
            full_state_gate_passed=False, full_goal_complete=False))
    ledger['latest_checkpoint'] = SUMMARY
    if frame_probe.exists():
        ledger['latest_checkpoint'] += (' Read-only fine probes reproduce8 whole4MiB controls exactly;'
            'first random-state separation18203 and first persistent-object separation18220 are pinned. Caller/interleaving cause remains unmapped;state gate stays failed.')
    assert ledger['next_integrated_profile_for_goal_continuation'] == 'all-routes-unified-v809'
    save(LEDGER, ledger)
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md'):
        path = Path('docs')/name; text = path.read_text(encoding='utf-8')
        heading = '## V817: Athens glyphs verified; climb world-state gate remains failed'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [Athens evidence](ceremony_Athens_v816_checkpoint.md).\n', encoding='utf-8')
    archive = Path('E:/Rota Nova translations/Editorial review/V817 Athens partial verification')
    sources = [DOC, LEDGER, Path(__file__), *ROOT.glob('*.json'), *ROOT.glob('*.py'),
        *(p for p in ACCESS.glob('*v816*') if p.is_file()),
        *(Path('scripts')/name for name in ('native_ceremony_location_fixture_v816.py',
          'native_ceremony_athens_fixture_v816.py', 'run_ceremony_capture_v816.py',
          'verify_ceremony_Athens_gameplay_v816.py', 'audit_ceremony_Athens_failure_v817.py'))]
    artifacts = []
    for source in sources:
        folder = archive/('scripts' if source.parent.name == 'scripts' else 'access' if source.parent == ACCESS else 'verification' if source.parent == ROOT else 'checkpoint')
        folder.mkdir(parents=True, exist_ok=True); target = folder/source.name
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        artifacts.append(dict(source=str(source), archived=str(target), sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json', dict(artifacts=artifacts, new_verified_Temple_guide_images=7,
        unapproved_site_captures_remain_test_evidence=True, no_ROM_or_patch_changes=True,
        state_gate_failed=True, completion_credit=0, full_goal_complete=False))
    print(f'Recorded33 glyph holds/37 cumulative IDs;Temple approved,site state gate FAILED. Archived{len(artifacts)} artifacts and7 Temple guide images;550 completed,goal active.', flush=True)


if __name__ == '__main__':
    main()
