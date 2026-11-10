"""Publish concise verified release/next-source progress without changing completion credit."""
import gzip
import json
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B131_B150_release_verified_20261102')
LEDGER = Path('translations/editorial_review_current_v1.json')
NEXT = Path('work/analysis/Hodram_B151_B170_clean_20261102/clean_intake_checkpoint_v1.json')


def main():
    root = ROOT / 'handoff_mutation_v1'
    assert not root.exists()
    release_path = ROOT / 'registered_release_verification.json'
    completion_path = ROOT / 'completion_checkpoint.json'
    release, completion, next_intake = map(load, [release_path, completion_path, NEXT])
    assert completion['new_credit'] == 329 and completion['counts']['completed'] == 8856
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (660, 114, 23)
    assert release['candidate_sha256'] == '7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    assert next_intake['total_editorial_objects'] == 642 and next_intake['source_meanings_saved'] == 157
    before = LEDGER.read_bytes()
    prior = json.loads(before)
    assert prior['records_editorially_completed'] == 8856 and not prior['full_goal_complete']
    ledger = deepcopy(prior)
    key = 'Hodram_B151_B170_clean_next_20261102'
    assert key not in ledger
    ledger[key] = dict(**next_intake, checkpoint=str(NEXT), checkpoint_sha256=sha(NEXT.read_bytes()))
    ledger['latest_checkpoint'] = 'B131–B150 registered/patch/own-startup verified:329 once-only completions,8856 completed (5540 revisions/3316 retentions),660 entries/114 accepted layers/23 checks. Current experimental7fb6f6d7;main unchanged. Next642 clean B151–B170 objects:157 meanings saved,477 ordinary/eight caption meanings pending;no prior English ordrafts. B156 cinematic FE source geometry needs qualification. Full scope/allROMs/evidence/later audit preserved;no guide photos.'
    assert {k: v for k, v in ledger.items() if k not in [key, 'latest_checkpoint']} == {k: v for k, v in prior.items() if k != 'latest_checkpoint'}
    note = '''B131–B150 is registered and credited once:329 records,180 revisions/149 justified retentions,23 layout fixes andthree full-name de corrections in four bytes. All660 manifest entries,114 accepted layers and23 release checks pass;23 semantic/layout/ownership rejection cases pass too. The exact clean-input patch andcandidate-own4001-frame startup are verified. Build3816/qualification28129/startup87660 are terminal/exit0;the patch verifier andcompletion writer are terminal/exit0. Do not repeat completed checks.

Current experimental: `out/all_routes_combined_hodram_b131_b150_names_20261102_candidate.nds`,SHA256 `7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04`. Profile `all-routes-hodram-b131-b150-names-20261102`;use `build_integrated_release_with_grouped_fields.py` so all earlier runtime/name stages andthe ASCII right-bound repair remain. Changes fromregistered parent f2f0bf2f are SC1’s19 reviewed blocks andfour ARM9 name bytes. Main remains unchanged;no promotion.

Coverage:8856 completed,8859 source/prose anddrafts,5540 revisions/3316 retentions. Next clean intake B151–B170 has642 objects (634 ordinary speeches/eight captions in four menus;no styles),zero completed overlaps and14 label-free two-byte2000 controls.157 clean meanings are saved across complete B151–B157 exchanges;477 ordinary/eight caption meanings remain. Earlier English has not been consulted andno localized drafts exist. Finish the clean meanings andidentity/item/context bindings before localized drafts andprior-English comparison.

Preserve B156’s retirement/farewell emotional progression,explicit new supreme-command/princess facts andGerhard’s warm closing joke. Its cinematic FE bodies have leading blank rows,full-width staging spaces andSera/FI headings:qualify the actual consumer geometry/speaker continuity before applying ordinary FE formatting. In B157,Hodram offers to help Al;do not reverse that direction. Retain the later older-record technical re-audit andunresolved graphics artwork separately. Every storyline/shared-town/random/other prose family remains in scope.

B133’s initialized monster-battle fault is reproduced with clean Japanese at the same address andfinal framebuffer;natural battle activation/transition stays unvisited. All other unvisited conditional paths andfull-catalogue UIs retain the documented offline scope. No guide photo collection;all ROMs,earlier translations andevidence remain preserved. Full editorial goal active.
'''
    release_doc = Path('docs/editorial_hodram_B131_B150_release_20261102.md')
    assert not release_doc.exists()
    detail = '# Hodram B131–B150: registered cumulative release verified\n\n' + note + f'''
The canonical base is `out/raphael_natural_v2_accepted_base.nds`,SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. The prior registered parent is `out/all_routes_combined_hodram_b111_b130_names_20261102_candidate.nds`,SHA256 `f2f0bf2fd904ead5d539b25d516d53fa70a0175af145be27751e8d9f6f2ccde2`. This experimental successor preserves all accepted and earlier experimental layers. Its complete manifest is beside the candidate;main promotion requires the user’s acceptance after testing.

- Manifest SHA256: `{release['manifest_sha256']}`.
- Registry SHA256: `{release['registry_sha256']}`.
- Clean input `work/clean.nds` SHA256: `{release['clean_input_sha256']}`.
- Patch: `{release['patch']}`,SHA256 `{release['patch_sha256']}`. Applying it to that exact clean input reproduces the entire candidate byte-for-byte.
- Release proof: `work/analysis/Hodram_B131_B150_release_verified_20261102/registered_release_verification.json`.
- Own startup: `work/analysis/Hodram_B131_B150_release_verified_20261102/own_registered_startup_verification.json`. Ten exact RGB pairs reuse prior direct visual review. Native checks use this run’s explicitly recorded final frame4001 read-only snapshot;the first verifier’s request for an uncaptured frame4000 snapshot was corrected without rerunning the cold boot orusing old RAM.
- Completion/source/current references: `completion_checkpoint.json` and `integrated_record_bindings.json` in the same verified folder. Every prior completed key andthe older native relocation reference are preserved.
- Next source: `work/analysis/Hodram_B151_B170_clean_20261102/clean_intake_checkpoint_v1.json`;three hashed clean-meaning parts cover42+86+29 ordinary records before current English exposure.

Representative gameplay remains five initialized English runs/59005frames plus the separate5001-frame Japanese B133 control.83 captured body planes,two headers andboth complete two-choice highlights match native output;19 QA sheets were directly viewed. Native offline coverage includes all328 speech pages,ten captions/eight personality alternatives,640 relative cases and325 archive loads. The unchanged full-catalogue UIs for the three corrected de names remain unvisited. Suggested human testing is ordinary cold boot,Hodram’s opening,town UI andthe reviewed story scenes when reached naturally;the registered candidate is experimental rather than a claim of a full route playthrough.
'''
    updates = {release_doc: detail}
    handoff = Path('docs/editorial_handoff_current.md')
    old_handoff = handoff.read_text(encoding='utf-8')
    updates[handoff] = '# Current editorial handoff - 2026-11-02: B131–B150 release verified;next642 source objects\n\n' + note + '\nContinue from [the verified release andclean-source checkpoint](editorial_hodram_B131_B150_release_20261102.md). Earlier sections below are historical.\n\n# Historical research checkpoint\n' + old_handoff.split('\n', 1)[1]
    short = 'B131–B150 is registered/credited:329 records,180 revisions/149 retentions,23 layout fixes andthree de names in four bytes.660 entries/114 accepted layers/23 checks,exact clean patch andown startup pass. Current experimental7fb6f6d7;8856 completed;main unchanged. Next642 clean objects have157 meanings saved before prior English;477 ordinary/eight caption meanings remain. Qualify B156’s cinematic FE layout when formatting. Reuse completed checks;no guide photos. See [current exact checkpoint](editorial_hodram_B131_B150_release_20261102.md). Full scope/all prior work remain.\n'
    for name in ['editorial_efficiency_workflow.md', 'translation_progress.md', 'known_issues.md', 'todo.md']:
        path = Path('docs') / name
        updates[path] = '## Current verified checkpoint - 2026-11-02\n\n' + short + '\nEarlier entries below are historical.\n\n' + path.read_text(encoding='utf-8')
    root.mkdir()
    (root / 'ledger.before.json.gz').write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    staged = encode_ledger(ledger)
    mutations = []
    for i, (path, text) in enumerate(updates.items()):
        old = path.read_bytes() if path.exists() else None
        if old is not None:
            (root / f'{i}.before').write_bytes(old)
        mutations.append(dict(path=str(path), before_sha256=sha(old) if old is not None else None, after_sha256=sha(text.encode('utf-8'))))
    save(root / 'mutation_plan.json', dict(ledger_before_sha256=sha(before), ledger_after_sha256=sha(staged), documentation=mutations,
                                          no_completion_credit_added=True, all_completed_keys_preserved=True))
    assert LEDGER.read_bytes() == before
    for entry, (path, text) in zip(mutations, updates.items()):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(text, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    LEDGER.write_bytes(staged)
    assert sha(LEDGER.read_bytes()) == sha(staged)
    save(root / 'verified_mutations.json', dict(ledger_sha256=sha(staged), completed=8856, next_clean_objects=642,
        clean_meanings_saved=157, new_credit=0, all_prior_completed_scope_preserved=True, main_unchanged=True, full_goal_complete=False))
    print('Verified release handoff andnext642-source checkpoint saved;8856 completions preserved;full goal active.')


if __name__ == '__main__':
    main()
