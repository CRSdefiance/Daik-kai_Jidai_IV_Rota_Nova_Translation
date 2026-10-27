"""Save metadata replay provenance without advancing unfinished editorial totals."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.register_shared_metadata_v783 import ROOT, CONFIG, MANUSCRIPT
from scripts.verify_shared_metadata_v783 import ROM
from scripts.verify_village_wrap_v608 import read, save


def main():
    proof = read(ROOT/'verification.json')
    assert proof['whole_ROM_identical_to_V782'] and proof['registered_speaker_context_replay_complete']
    assert proof['byte_exact_clean_input_reconstruction'] and not proof['new_editorial_completion_credit']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 367 and ledger['records_with_source_and_prose_pass'] == 420
    backup = ROOT/'editorial_ledger_before_metadata_replay.json'
    if not backup.exists():
        save(backup, ledger)
    doc = Path('docs/shared_dialogue_v783_metadata_replay.md')
    pending = ledger['pending_integrated_candidate']
    pending.update({'path': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                    'manifest': str(ROM.with_suffix('.manifest.json')), 'patch_sha256': proof['patch_sha256'],
                    'details': str(doc), 'registered_metadata_replay': str(ROOT/'verification.json'),
                    'remaining_gates': pending['remaining_actual_families'],
                    'gameplay_inherited_by_exact_whole_ROM_identity_from': 'out/all_routes_combined_v782_candidate.nds'})
    ledger['active_source_prose_drafts']['status'] = '750-752-context-unmapped;1020-1069-native-reviewed-integrated;five-actual-families-verified;metadata-replay-registered;fleet-private-pending'
    ledger['active_source_prose_drafts']['note'] = 'V783 registers corrected V3 role1 First Mate speaker context with native fallback. Every ROM byte is identical to V782;all50 remain drafts until fleet/private actual samples pass.'
    ledger['coverage_units'][0]['next'] = 'Complete fleet1030-1034 and private-barmaid1049-1069 actual samples;then close50-entry batch in V783. Continue COMMON1070 onward,resolve750-752,review all routes and remaining prose,and preserve graphics/older-record follow-up.'
    summary = ('V783 registers corrected First Mate speech-provider context for1035-1048 and rebuilds through the full470-batch/114-layer profile. '
               'Every ROM byte equals V782;the clean-input patch reconstructs exactly,so existing glyph/gameplay/startup evidence inherits by complete identity. '
               'All frozen V782 dependencies,prior profiles,canonical and original saves remain exact. '
               'Fleet/private actual samples remain;367 complete,420 source/prose,53 drafts. Full editorial goal and graphics audit stay unfinished.')
    ledger['latest_checkpoint'] = summary
    record = {'id': 'V783-registered-speaker-context-metadata-replay', 'documentation': str(doc),
              'candidate_sha256': proof['candidate_sha256'], 'new_editorially_completed': 0,
              'registered_metadata_replay_complete': True, 'whole_ROM_identical_to_V782': True,
              'remaining_gates': pending['remaining_actual_families'], 'full_goal_complete': False}
    if not any(p['id'] == record['id'] for p in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(record)
    save(ledger_path, ledger)
    latest = read('out/editorial_review_latest.json')
    latest.update({'pending_integrated_candidate': pending, 'latest_research_checkpoint': str(doc)})
    save('out/editorial_review_latest.json', latest)
    doc.write_text('''# V783: registered speaker-context correction

The First Mate metadata erratum is now integrated through an explicit new release
configuration and the registered all-routes-unified-v783 profile. Frozen V782
configuration/manuscript inputs and every previous registry profile are preserved.
V3 corrects only the speaker/context/localization notes for1035-1048. All50 compiled
paragraphs remain identical. The original role1 speech provider uses the assigned
First Mate or the game's native officer fallback; it is not the Barkeep.

The full registered builder preserves470 batches,114 accepted layers, canonical
baseline, changed-record inventory and all graphics contracts. Every byte of the
new ROM equals V782, SHA256:
9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d.
The identical clean-input xdelta reconstructs the entire V783 ROM exactly. Its
SHA256 is9a23ef0e69dea7a460e48c35e9278936344778d20b93cb1161441f2c56014b7f.
Files are out/all_routes_combined_v783_candidate.nds, its neighboring manifest
and .xdelta under E:/Rota Nova translations/Generated/out.

Existing V782 native-layout/copy, startup and actual-scene evidence applies by
whole-ROM identity. This is no claim of additional scene activations or wider
testing. Twelve actual holds across1020/1022/1028/1029/1035/1042 remain verified;
289 strict whole-screen controls, two original whole-screen phase controls and285
paired state/model/object/task snapshots remain the current actual scope.

Fleet rumors1030-1034 and private barmaid topics1049-1069 still need actual samples.
No new entries are credited complete:367 completed,420 source/prose reviewed,
53 drafts. V780 remains the last fully verified editorial batch; V783 is the
pending experimental integrated candidate. The entire editorial goal, remaining
routes/prose, separate graphics audit and older-record follow-up remain unfinished.
The historical V3 equivalence report's registration-pending flag is superseded by
work/analysis/shared_metadata_v783/verification.json; frozen evidence is not edited.
No canonical promotion, commit or GitHub push is made.
''', encoding='utf-8')
    for file in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        path = Path(file)
        text = path.read_text(encoding='utf-8')
        heading = '## V783: registered First Mate speaker-context replay'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V783 metadata replay](shared_dialogue_v783_metadata_replay.md).\n', encoding='utf-8')
    archive = Path('E:/Rota Nova translations/Editorial review/V783 Shared metadata replay')
    sources = [CONFIG, MANUSCRIPT, doc, ledger_path, ROM.with_suffix('.manifest.json')]
    sources += [ROOT/p for p in ('registration.json', 'verification.json', 'release_stack_before_v783.json')]
    sources += [Path('scripts')/p for p in ('register_shared_metadata_v783.py', 'verify_shared_metadata_v783.py', 'record_shared_metadata_v783.py')]
    for source in sources:
        target = archive/source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    save(ROOT/'archive_receipt.json', {'archive': str(archive), 'every_copy_SHA256_verified': True,
                                      'registered_replay_complete': True, 'editorial_batch_complete': False})
    print('V783 metadata replay recorded and archived;fleet/private actual samples remain. Full goal active.', flush=True)


if __name__ == '__main__':
    main()
