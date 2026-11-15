"""Stage,audit,apply and verify the uncredited all11 reference/actual checkpoint losslessly."""
import argparse
import gzip
import json
import os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read, save
from scripts.lil_B194_checkpoint_text_v5527 import NEXT, SUMMARY
from scripts.seal_lil_B194_references_v5526 import INPUT, OUTPUT as DOC, MAP, PLAN, CENSUS, CONTROL, STORED, ENDS, VISUAL, BINDING

ROOT = Path('work/analysis/lil_B194_checkpoint_v5527')
VERIFY = Path('work/analysis/editorial_handoff_verification_v5528')
LEDGER = Path('translations/editorial_review_current_v1.json')
PRIOR = Path('work/analysis/editorial_handoff_verification_v5505/verified_handoff.json')
APPROVAL = Path('work/analysis/lil_B194_reference_approval_v5526/approval_receipt.json')
KEY, PREVIOUS, SCOPE = 'Lil_B194_reference_actual_v5527', 'previous_latest_checkpoint_before_Lil_B194_v5527', 'unfinished_editorial_scope_v5527'
COUNTERS = dict(records_editorially_completed=6124, records_with_source_and_prose_pass=6127,
                records_revised_and_integrated=3867, retained_wordings_editorially_completed=2257)


def inverse(value):
    result = deepcopy(value)
    result['latest_checkpoint'] = result.pop(PREVIOUS)
    result.pop(KEY)
    result.pop(SCOPE)
    return result


def gates():
    doc, earlier, approval = map(read, [DOC, INPUT, APPROVAL])
    assert approval['manuscripts'][str(DOC)] == sha(DOC.read_bytes())
    assert len(doc['records']) == 11 and (doc['revised'], doc['retained']) == (4, 7)
    assert doc['source_prose_or_completion_credit_added'] == 0 and doc['registered_integration_pending']
    assert Counter(r['editorial_decision'] for r in doc['records']) == {'revise': 4, 'retain-wording': 7}
    assert all(all(r['review'].values()) and r['actual_B22_display_fixture_observed'] for r in doc['records'])
    for a, b in zip(earlier['records'], doc['records'], strict=True):
        for key in ['english', 'compiled_hex', 'source_hex', 'current_hex', 'source_reference', 'current_reference', 'editorial_decision']:
            assert a[key] == b[key]
    plan, mapping, control, stored, visual = map(read, [PLAN, MAP, CONTROL, STORED, VISUAL])
    b = plan['blocks'][0]
    assert (b['source_bytes'], b['source_logical_end'], b['research_bytes'], b['research_logical_end']) == (540, 540, 516, 514)
    assert len(b['command_map']) == 21 and len(b['relative_skip_fixups']) == 4 and len(b['target_native_skip_cases']) == 20
    assert stored['current_final_stored_macro_alignment_cases'] == 44
    assert (stored['new_parity_macro_alignment_cases'], stored['exact_byte_identical_reused_macro_alignment_cases']) == (20, 24)
    assert control['changed_unaligned_operand_scratch_owned_and_restored']
    assert len(control['relocated_C200_prior_result_cases']) == len(control['relocated_resource42_prior_result_cases']) == 10
    assert visual['unique_actual_display_objects'] == 11 and visual['total_frames'] == 36004
    assert visual['actual_new_cold_boot_runs'] == 4 and visual['all_content_jobs_terminal_and_reaped']
    assert [v['complete_native_holds'] for v in visual['versions']] == [35, 44]
    assert [v['return_frames'] for v in visual['versions']] == [[5017, 5017], [5737, 5737]]
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert not visual['visual_review_pending'] and visual['no_open_translation_specific_display_or_control_finding']
    evidence = {str(p): sha(p.read_bytes()) for p in [DOC, INPUT, MAP, PLAN, CENSUS, CONTROL, STORED, ENDS, VISUAL, BINDING, APPROVAL, PRIOR,
        Path('scripts/lil_B194_checkpoint_text_v5527.py'), Path(__file__)]}
    for data in [doc, mapping, approval]:
        if 'evidence' in data:
            for p, h in data['evidence'].items():
                assert sha(Path(p).read_bytes()) == h
                evidence[p] = h
        for k, v in data.items():
            if k.endswith('_sha256') and isinstance(data.get(k[:-7]), str):
                p = Path(data[k[:-7]])
                if p.is_file():
                    assert sha(p.read_bytes()) == v
                    evidence[str(p)] = v
    for version in visual['versions']:
        for field in ['visual_analysis', 'actual_proof']:
            p = Path(version[field])
            assert sha(p.read_bytes()) == version[field + '_sha256']
            evidence[str(p)] = version[field + '_sha256']
        for sheet in version['viewed_sheets']:
            assert sheet['viewed_after_image_return'] and sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
            evidence[sheet['path']] = sheet['sha256']
    prior = read(PRIOR)
    assert sha(Path(prior['candidate']).read_bytes()) == prior['candidate_sha256'] == doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes()) == prior['patch_sha256']
    registry = read('translations/release_stack.json')
    assert len(registry['accepted_layers']) == 114 and registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4701'
    manifest = read(Path(prior['candidate']).with_suffix('.manifest.json'))
    assert len(manifest['batches']) == 577 and len(manifest['checks']) == 18 and all(manifest['checks'].values())
    for script in ['research_lil_B194_relocation_v5506.py', 'prepare_lil_B194_display_v5514.py',
                   'prepare_lil_B194_actual_audit_v5517.py', 'prepare_lil_B194_actual_audit_v5517b.py',
                   'audit_lil_B194_available_v5523.py', 'prepare_lil_B194_available_review_v5524.py']:
        p = Path('scripts') / script
        evidence[str(p)] = sha(p.read_bytes())
    return doc, evidence


def audit(plan, applied=False):
    for row in plan['files']:
        assert sha(Path(row['target']).read_bytes()) == row['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(row['planned']).read_bytes()) == row['planned_sha256']
    for p, h in plan['evidence'].items():
        assert sha(Path(p).read_bytes()) == h
    old = json.loads(gzip.decompress((ROOT / 'ledger.before.json.gz').read_bytes()))
    new = read(plan['files'][0]['planned'])
    assert inverse(new) == old and new['current_integrated_candidate'] == old['current_integrated_candidate']
    assert all(new[k] == old[k] == v for k, v in COUNTERS.items())
    assert new['goal_status'] == 'active' and not new['full_goal_complete']
    gates()
    return new


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['stage', 'audit', 'apply', 'verify'])
    phase = parser.parse_args().phase
    if phase == 'stage':
        assert not ROOT.exists()
        before = LEDGER.read_bytes()
        old = json.loads(before)
        assert sha(before) == read(PRIOR)['ledger_sha256']
        assert all(k not in old for k in [KEY, PREVIOUS, SCOPE])
        doc, evidence = gates()
        ROOT.mkdir(parents=True)
        (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before, mtime=0))
        scope_path = Path(old['unfinished_editorial_scope_v5504']['path'])
        assert sha(scope_path.read_bytes()) == old['unfinished_editorial_scope_v5504']['sha256']
        scope = deepcopy(read(scope_path))
        scope['next_focus'] = NEXT
        scope['historical_Lil_B194_native_only_before_v5527'] = scope.pop('next_Lil_B194_native_approved_uncredited_v5504')
        scope['next_Lil_B194_reference_actual_approved_uncredited_v5527'] = dict(manuscript=str(DOC), sha256=sha(DOC.read_bytes()),
            reference_map=str(MAP), reference_map_sha256=sha(MAP.read_bytes()), objects=11, revisions=4, retentions=7,
            unique_actual_display_objects=11, actual_cold_boots=4, disclosed_original_recruitment_setup=True,
            uncredited=True, atomic_compiler_registered_release_and_current_startup_pending=True)
        inventory_path = ROOT / 'unfinished_editorial_scope_inventory.json'
        save(inventory_path, scope)
        evidence[str(inventory_path)] = sha(inventory_path.read_bytes())
        plan_data = read(PLAN)
        targets_by_id = {r['id']: r for r in plan_data['blocks'][0]['text_records']}
        records = []
        fields = ['id', 'file_path', 'block', 'source_record_index', 'source_reference', 'source_hex', 'source_Japanese',
                  'current_record_index', 'current_reference', 'current_hex', 'english', 'compiled_hex', 'editorial_decision',
                  'localization_note', 'fresh_retained_wording_justification', 'review']
        for row in doc['records']:
            item = {k: row[k] for k in fields if k in row}
            target = targets_by_id[row['id']]
            item.update(research_target_reference=dict(block=194, offset=target['new_offset'], bytes=target['new_length'], record_index=target['new_record_index']),
                        research_stored_target_hex=target['target_hex'], parity_space_added=target['parity_space_added'],
                        actual_disclosed_B22_fixture_observed=True, integrated_reference_pending=True, source_prose_or_completion_credit_added=0)
            records.append(item)
        new = deepcopy(old)
        new[KEY] = dict(summary=SUMMARY, next=NEXT, manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), records=records,
            approved_uncredited_objects=11, revised=4, retained=7, reference_map=str(MAP), reference_map_sha256=sha(MAP.read_bytes()),
            source_native_references_and_representative_checks_complete=True,
            remaining_gates=['atomic-compiler-and-negatives', 'registered-cumulative-release', 'exact-clean-input-patch', 'fresh-current-startup'],
            unique_actual_display_objects=11, actual_new_cold_boots=4, actual_frames=36004,
            new_research_ROMs=5, all_new_and_earlier_ROMs_preserved=True,
            previous_goal_turn_classification='no progress;user clarification only', current_goal_turn_classification='progress',
            source_prose_or_completion_credit_added=0, evidence=evidence, full_goal_complete=False)
        new[SCOPE] = dict(path=str(inventory_path), sha256=sha(inventory_path.read_bytes()),
            Lil_B194_reference_actual_approved_uncredited_objects=11, all_broader_editorial_scope_preserved=True,
            graphics_and_later_older_record_technical_reaudit_separate=True, full_goal_complete=False)
        new[PREVIOUS], new['latest_checkpoint'] = old['latest_checkpoint'], SUMMARY
        assert inverse(new) == old
        targets = {LEDGER: encode_ledger(new)}
        assert len(targets[LEDGER]) < 100 * 1024 * 1024
        section = '## V5527: All eleven B194 reference and actual reviews approved;integration pending\n\n' + SUMMARY + '\n\n'
        for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']:
            target = Path('docs') / name
            text = target.read_text(encoding='utf-8')
            if name == 'editorial_handoff_current.md':
                after = '# Current editorial handoff - V5527\n\n' + section + NEXT + '\n\n' + text
            else:
                first, rest = text.split('\n', 1)
                after = first + '\n\n' + section + rest.lstrip('\n')
            targets[target] = after.replace('\n', '\r\n').encode('utf-8')
        files = []
        for index, (target, data) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(data)
            if target != LEDGER:
                (ROOT / f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()), before_sha256=sha(target.read_bytes()),
                              planned=str(planned.resolve()), planned_sha256=sha(data)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, no_shared_mutation_yet=True, full_goal_complete=False))
        print('Six targets staged;all11 source/reference/actual approvals remain uncredited.')
    elif phase == 'audit':
        assert not (ROOT / 'independent_preapplication_audit.json').exists()
        plan = read(ROOT / 'staged_checkpoint.json')
        audit(plan)
        save(ROOT / 'independent_preapplication_audit.json', dict(all_six_before_planned_and_evidence_hashes_exact=True,
            full_nested_inverse_recovers_every_historical_value=True, staged_plan_sha256=sha((ROOT / 'staged_checkpoint.json').read_bytes()), full_goal_complete=False))
        print('Six targets and complete historical inverse pass.')
    elif phase == 'apply':
        assert not (ROOT / 'application_receipt.json').exists()
        plan = read(ROOT / 'staged_checkpoint.json')
        assert read(ROOT / 'independent_preapplication_audit.json')['staged_plan_sha256'] == sha((ROOT / 'staged_checkpoint.json').read_bytes())
        audit(plan)
        workspace = Path.cwd().resolve()
        for row in plan['files']:
            assert Path(row['target']).is_relative_to(workspace) and Path(row['planned']).is_relative_to(ROOT.resolve())
        for row in plan['files']:
            with Path(row['target']).open('r+b') as stream:
                stream.write(Path(row['planned']).read_bytes())
                stream.truncate()
                stream.flush()
                os.fsync(stream.fileno())
            assert sha(Path(row['target']).read_bytes()) == row['planned_sha256']
        save(ROOT / 'application_receipt.json', dict(all6_targets_exact=True, all_before_hashes_checked_before_first_write=True, full_goal_complete=False))
        print('Six audited checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT / 'application_receipt.json')['all6_targets_exact']
        plan = read(ROOT / 'staged_checkpoint.json')
        new = audit(plan, True)
        prior = read(PRIOR)
        VERIFY.mkdir(parents=True)
        save(VERIFY / 'verified_handoff.json', dict(ledger_sha256=sha(LEDGER.read_bytes()), candidate=prior['candidate'],
            candidate_sha256=prior['candidate_sha256'], patch=prior['patch'], patch_sha256=prior['patch_sha256'],
            all_original_root_and_nested_history_preserved=True, all_coverage_counters_unchanged=True,
            completed=6124, source_prose=6127, revised=3867, retained=2257, SC2=4239, SC3=96, reviewed_routes=4525, completed_routes=4525,
            approved_uncredited_Lil_B194_objects=11, Lil_proposed_revisions=4, Lil_justified_retentions=7,
            all11_source_native_reference_and_representative_checks_complete=True,
            stored_alignment_cases=44, fresh_target_native_loads=336, fresh_target_parent_modes=672, target_skip_cases=20,
            actual_unique_objects=11, actual_panel_observations=20, complete_native_holds=79, paired_nontext_samples=230,
            viewed_full_screens=24, actual_cold_boots=4, actual_frames=36004, all_content_jobs_terminal_and_reaped=True,
            default_returns=[5017, 5017], conditional_returns=[5737, 5737], default_and_original_setup_outcomes_unforced=True,
            atomic_compiler_and_registered_integration_pending=True, main_V4701_preserved=True, new_editorial_credit=0,
            new_research_ROMs=5, full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5527 verified;V5478 remains current. Eleven reference/actual-approved objects uncredited;atomic compiler and registered release pending;full goal active.')
