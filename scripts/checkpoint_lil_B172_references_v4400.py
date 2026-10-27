"""Checkpoint B172 reference/gameplay approval; preserve pending counts and main."""
from copy import deepcopy
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B172_reference_checkpoint_text_v4400 import SUMMARY,NEXT
import gzip
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B172_reference_checkpoint_v4400')
INPUT = Path('translations/lil_B172_editorial_manuscript_v3.json')
DOC = Path('translations/lil_B172_editorial_manuscript_v4.json')
APPROVAL = Path('work/analysis/lil_B172_reference_approval_v4399/approval_receipt.json')
FAMILY = 'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27'



def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode()


if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    before_bytes = lp.read_bytes()
    assert sha(before_bytes) == read('work/analysis/promotion_v4392/promotion_receipt.json')['ledger_sha256']
    ledger = json.loads(before_bytes)
    approval, doc = map(read, [APPROVAL, DOC])
    assert approval['manuscripts'] == {str(DOC): sha(DOC.read_bytes())}
    assert approval['new_emulator_runs'] == 4 and len(approval['actual_sampled_display_IDs']) == 27 and not approval['offline_only_display_IDs']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5789, 5762, 27)
    assert len(fresh['pending_contextual_families']) == 1
    pending = fresh['pending_contextual_families'][0]
    assert pending['id'] == FAMILY and pending['manuscript'] == str(INPUT)
    paths = [APPROVAL, DOC, Path(__file__)]
    for key in ['reference_map', 'representative_proof', 'final_padding_proof', 'relocated_control_proof', 'termination_decode_proof', 'focused_repeat_proof']:
        p = Path(doc[key])
        assert sha(p.read_bytes()) == doc[key + '_sha256']
        paths.append(p)
    for p, digest in approval['evidence'].items():
        assert sha(Path(p).read_bytes()) == digest
        paths.append(Path(p))
    evidence = {str(p): sha(p.read_bytes()) for p in paths}
    pending.update(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), manuscripts=approval['manuscripts'], pending=NEXT,
        actual_sampled_display_IDs=approval['actual_sampled_display_IDs'], offline_only_display_IDs=[], new_emulator_runs=4,
        reference_approval=str(APPROVAL), reference_approval_sha256=sha(APPROVAL.read_bytes()))
    fresh.update(latest_contextual_manuscript=str(DOC), latest_pending_contextual_family=FAMILY,
        coverage_note='5789 rereads/5762 integrated/27 pending;B172 native/reference/representative approved. No additional review/completion credit;registered integration remains.')
    active = ledger['active_source_prose_drafts']
    assert active['route_record_subsets_pending'][str(INPUT)] == [r['id'] for r in doc['records']]
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(INPUT)] = []
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in doc['records']]
    active.update(status='3-reviewed-COMMON-incomplete;27-Lil-B172-reference-approved-pending-registered-release', note=fresh['coverage_note'])
    for unit in ledger['coverage_units']:
        if unit['id'] == FAMILY:
            unit.update(**pending, status=doc['status'], actual_new_cold_boot_runs=4, actual_complete_native_panels=27, registered_release_pending=True)
        elif unit['id'] == 'all-route-scenes':
            unit['next'] = NEXT
    oldscope = ledger['unfinished_editorial_scope_v4379']
    assert sha(Path(oldscope['path']).read_bytes()) == oldscope['sha256']
    inventory = deepcopy(read(oldscope['path']))
    inventory.update(next_focus=NEXT)
    inventory['B172_reference_and_actual_coverage_v4400'] = pending
    ROOT.mkdir(parents=True)
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v4400'] = {**oldscope, 'path': str(inv), 'sha256': sha(inv.read_bytes())}
    ledger['lil_B172_reference_reconciliation_v4400'] = dict(summary=SUMMARY, evidence=evidence, pending_family=pending,
        source_prose_reviews_added=0, completion_credit_added=0, actual_new_cold_boot_runs=4, full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    fixture = read('work/analysis/lil_B172_display_fixture_v4389/complete_effect_preserving_B22_fixtures.json')
    pinned = 0
    for row in fixture['fixtures'] + [read('work/analysis/lil_B172_research_v4384/research_image_receipt.json')]:
        rom = Path(row['research_ROM'])
        assert sha(rom.read_bytes()) == row['research_ROM_sha256']
        if not any(p['path'] == str(rom.resolve()) for p in pins):
            pins.append(dict(path=str(rom.resolve()), reason='V4400 B172 source-bound full-content evidence input. Preserve every ROM;no pruning. SHA-256 ' + sha(rom.read_bytes())))
            pinned += 1
    assert pinned == 3
    docs = [Path('docs') / n for n in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']]
    (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes, mtime=0))
    planned = {lp: encode_ledger(ledger), pins_path: encoded(pins)}
    section = '## V4400:27 B172 reviews reference/gameplay approved;registered integration pending\n\n' + SUMMARY + '\n\nApproval: ' + APPROVAL.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '.\n\nNext: ' + NEXT + '\n\n'
    for index, path in enumerate(docs):
        first, rest = path.read_text(encoding='utf-8').split('\n', 1)
        planned[path] = (('# Current editorial handoff - V4400' if index == 0 else first) + '\n\n' + section + rest).encode()
    staged = ROOT / 'staged'
    staged.mkdir()
    mutations = []
    for index, (path, data) in enumerate(planned.items()):
        out = staged / (str(index) + '.planned')
        out.write_bytes(data)
        mutations.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(out.resolve()), planned_sha256=sha(data)))
    save(ROOT / 'mutation_plan.json', mutations)
    stable = ['translations/release_stack.json', 'translations/promoted_build.json', 'scripts/build_integrated_release.py']
    stable_hashes = {p: sha(Path(p).read_bytes()) for p in stable}
    for row in mutations:
        assert sha(Path(row['target']).read_bytes()) == row['before_sha256']
        assert sha(Path(row['planned']).read_bytes()) == row['planned_sha256']
    for row in mutations:
        path, data = Path(row['target']), Path(row['planned']).read_bytes()
        with path.open('r+b') as stream:
            stream.write(data)
            if stream.seek(0, os.SEEK_END) != len(data):
                stream.truncate(len(data))
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(path.read_bytes()) == row['planned_sha256']
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in stable_hashes.items())
    save(ROOT / 'checkpoint_receipt.json', dict(checkpoint='V4400', evidence=evidence, ledger_sha256=sha(lp.read_bytes()),
        fresh_reread=5789, integrated=5762, pending=27, source_prose=5792,
        new_source_prose_reviews=0, new_completed_records=0, preserved_release_files=stable_hashes,
        updated_files={str(Path(row['target']).relative_to(Path.cwd())): row['planned_sha256'] for row in mutations},
        new_emulator_runs=4, actual_complete_native_panels=27, reviewed_sheets=5,
        ROMs_pinned=3, ROMs_deleted=0, all_jobs_terminal=True, full_goal_complete=False))
    print('V4400 checkpoint complete:27 reference-approved pending records;27 actual panels/four boots;3 ROMs pinned. MainV4353,registry,builder and all credit counts preserved.')
