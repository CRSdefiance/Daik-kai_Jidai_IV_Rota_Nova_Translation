"""Advance current research handoff while preserving every completed key and release."""
import gzip
import json
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B131_B150_checked_20261102')
CHECKPOINT = ROOT / 'formatting_checkpoint.json'
LEDGER = Path('translations/editorial_review_current_v1.json')


def main():
    backup = ROOT / 'handoff_mutation_v1'
    assert not backup.exists()
    checkpoint = load(CHECKPOINT)
    assert checkpoint['all_individual_five_gates_pass_in_research'] and checkpoint['new_credit'] == 0
    registry = Path('translations/release_stack.json')
    assert sha(registry.read_bytes()) == 'd3cf0000ad4d1a3e4f9df5c0880a001f7449744e5251ced6f613a05d438d076a'
    before = LEDGER.read_bytes()
    prior = json.loads(before)
    assert prior['records_editorially_completed'] == 8527 and not prior['full_goal_complete']
    final = load(checkpoint['final_review'])
    completed = {(r['file_path'], r['id']) for r in prior['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not completed & {(r['file_path'], r['id']) for r in final['records']}
    ledger = deepcopy(prior)
    key = 'Hodram_B131_B150_five_gate_research_20261102'
    assert key not in ledger
    ledger[key] = dict(**checkpoint, checkpoint=str(CHECKPOINT), checkpoint_sha256=sha(CHECKPOINT.read_bytes()))
    note = '''B131–B150 now has all329 individual five-gate research reviews:180 revisions/149 justified retentions. All23 layout findings are resolved;328 final speech pages andten captions are visually approved.20 scoped name decisions add three source-supported de corrections/17 retentions. The two physical fields have three reviewed owners (Geronimo36 also shares with Alonso49;Vasquez42 is exclusive),four bytes total.32 native name calls/32 directly viewed name planes and13 semantic rejection cases per name test pass. No biography orrank was added;all earlier name repairs remain.

All617 commands andthree label-free2000 controls are preserved across19 rebuilt blocks;640 original native relative cases,325 whole archive loads and38 fresh/612 exact reused handoff cases pass. Five declared initialized English cold boots/59005frames and19 directly viewed QA sheets cover the role7/personality4 panel,cargo instructions,both two-choice highlights/decline branch,Sera’s embedded headings/FI/naming/acquisition,Rafael0’s portrait/name/smile,three-line pause,pagination andport returns.83 complete captured body planes,two headers andtwo highlights match native pixels. Other conditional content remains offline-only;all three changed full-catalogue UIs remain unvisited.

The B133 fixture reaches an invalid instruction after the unchanged C600 monster-battle command. A separate5001-frame clean-Japanese control reaches the identical fault/address andfinal framebuffer. This is a source-controlled fixture-context limitation;do not claim a natural monster encounter orverified battle transition. Preserve both runs;do not replay orpatch around this control. The source line itself is observed andmatches the native plane.

Continue with registered cumulative integration:qualify the13 documented structural/dramatic layouts in a source-locked release successor (the prior v5 release module forbids all LB);append the four-byte complete-owner-group name stage after the unchanged existing runtime/Emilio/Fernando/Samwell/Follower/Diogo stages. Preserve ASCII right-bound correction. Build/qualify the registered candidate,make the exactly reconstructable clean-input patch,andrun candidate-own startup before once-only329 completion credit. Final manuscript explicitly records the narrow grammatical weak-ending waiver for B142R159. All current jobs are terminal;do not rerun completed source/prose/native/stored/visual/gameplay checks without a changed dependency orconcrete new risk.

Use work/analysis/Hodram_B131_B150_checked_20261102/formatting_checkpoint.json and translations/hodram_B131_B150_contextual_final_review_v1.json. Complete research reference7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04 is research-only,not a registered testing handoff. Registered candidate f2f0bf2f,main,accepted layers and8527 completed credits are unchanged. Full editorial scope remains active. No guide photos;preserve all ROMs/translations/evidence;graphics artwork andthe later older-record technical re-audit remain separate.
'''
    ledger['latest_checkpoint'] = 'B131–B150:329 five-gate research reviews,180 revisions/149 retentions,328 pages,23 layout fixes;20 names/three de corrections in four owned bytes;640 relative cases/325 archive loads;five English runs59005frames/19 sheets andsource-controlled B133 battle-fixture limit. Registered integration/clean patch/own startup/329 once-only credits pending.8527/current f2f0bf2f/main unchanged;full goal active;no guide photos.'
    allowed = {key, 'latest_checkpoint'}
    assert {k: v for k, v in ledger.items() if k not in allowed} == {k: v for k, v in prior.items() if k not in allowed}
    backup.mkdir()
    (backup / 'ledger.before.json.gz').write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    staged = encode_ledger(ledger)
    assert json.loads(staged) == ledger
    new_doc = Path('docs/editorial_hodram_B131_B150_checked_20261102.md')
    assert not new_doc.exists()
    updates = {new_doc: '# Hodram B131–B150: all five research gates pass\n\n' + note + '''
Exact artifacts:

- Final dialogue: `translations/hodram_B131_B150_contextual_final_review_v1.json`.
- Names: `translations/hodram_B131_B150_speaker_name_review_v1.json`;grouped fields: `translations/geronimo_vasquez_alonso_owned_name_review_v1.json`.
- Proposal: `work/analysis/Hodram_B131_B150_name_fields_20261102/owned_fields_proposal_v2.json`;new source-qualified grouped planner: `dk4tool/patch/owned_name_fields_v3.py`. Keep the older exclusive planner unchanged.
- Research reconstruction: `work/analysis/Hodram_B131_B150_rebuilt_20261102/reconstruction.json`;with names: `work/analysis/Hodram_B131_B150_name_research_20261102/research_reference.json`.
- Stored: `work/analysis/Hodram_B131_B150_stored_20261102/stored_native_verification.json`;loaders: `work/analysis/Hodram_B131_B150_loaders_20261102/verification.json`.
- Actual review: `work/analysis/Hodram_B131_B150_checked_20261102/actual_review.json`;pixels: `work/analysis/Hodram_B131_B150_actual_pixels_20261102/focused_actual_pixels.json`.
- Source control: `work/analysis/Hodram_B133_source_control_20261102/source_control_result.json`.

Current speech plan/native/visual proofs remain `Hodram_B131_B150_editorial_20261102/plans_v3`, `native_v3`,and`visual_review_progress_v7.json`. They are bound to manuscriptv2;the final review changes approval/reference metadata andadds the individual R159 waiver without changing words orcompiled layout. Preserve the exact binding chain rather than rerendering unchanged pages. Reuse the documented initialized-scene limitation;future necessary capture reruns can stop when the target returns instead of replaying the following port/sailing tutorial.
'''}
    handoff = Path('docs/editorial_handoff_current.md')
    old = handoff.read_text(encoding='utf-8')
    updates[handoff] = '# Current editorial handoff - 2026-11-02: B131–B150 five research gates pass\n\n' + note + '\nSee [exact current artifacts](editorial_hodram_B131_B150_checked_20261102.md). Earlier checkpoint sections below are historical.\n\n# Historical offline-display checkpoint\n' + old.split('\n', 1)[1]
    short = 'All329 B131–B150 five-gate research reviews pass (180 revisions/149 retentions);328 pages,23 wrap fixes,20 names/three de corrections in four owned bytes,640 relative cases andfive English runs59005frames/19 viewed sheets are checked. B133’s post-dialogue fixture battle fault is reproduced with clean Japanese;natural battle transition remains unvisited. Registered integration/exact clean patch/own startup andonce-only credits remain.8527 completed/current f2f0bf2f/main unchanged. Continue from [the checked checkpoint](editorial_hodram_B131_B150_checked_20261102.md). Full scope preserved;no guide photos.\n'
    for filename in ['editorial_efficiency_workflow.md', 'translation_progress.md', 'known_issues.md', 'todo.md']:
        path = Path('docs') / filename
        updates[path] = '## Current B131–B150 research checkpoint - 2026-11-02\n\n' + short + '\nEarlier entries below are historical.\n\n' + path.read_text(encoding='utf-8')
    plan = []
    for index, (path, text) in enumerate(updates.items()):
        old = path.read_bytes() if path.exists() else None
        if old is not None:
            (backup / f'{index}.before').write_bytes(old)
        plan.append(dict(path=str(path), before_sha256=sha(old) if old is not None else None, after_sha256=sha(text.encode('utf-8'))))
    save(backup / 'mutation_plan.json', dict(ledger_before_sha256=sha(before), ledger_after_sha256=sha(staged), docs=plan,
                                            completed_keys_unchanged=True, release_registry_unchanged=True))
    assert LEDGER.read_bytes() == before
    for entry, (path, text) in zip(plan, updates.items()):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(text, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    LEDGER.write_bytes(staged)
    assert sha(LEDGER.read_bytes()) == sha(staged)
    assert sha(registry.read_bytes()) == 'd3cf0000ad4d1a3e4f9df5c0880a001f7449744e5251ced6f613a05d438d076a'
    save(backup / 'verified_mutations.json', dict(ledger_sha256=sha(staged), complete_prior_ledger_except_two_progress_keys_preserved=True,
         new_credit=0, current_registered_candidate_andmain_unchanged=True, full_goal_complete=False))
    print('Current handoff/ledger updated:329 research gates pass;registered integration remains;8527 completions andall completed keys unchanged.')


if __name__ == '__main__':
    main()
