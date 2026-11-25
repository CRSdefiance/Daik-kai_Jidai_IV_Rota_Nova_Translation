"""Record requested retrospective name localization without changing historical reviews."""
import argparse
import gzip
import json
import os
import struct
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/names_scope_v5708')
VERIFY = Path('work/analysis/editorial_handoff_verification_v5709')
LEDGER = Path('translations/editorial_review_current_v1.json')
PRIOR = Path('work/analysis/editorial_handoff_verification_v5698/verified_handoff.json')
CATALOG = Path('work/analysis/lil_B198_voices_v5703/current207_catalog_eight_voices_and_two_source_selectors.json')
KEY = 'speaker_names_and_role_labels_localization_scope_v5708'
SCOPE = 'unfinished_editorial_scope_v5708'
PREVIOUS = 'previous_latest_checkpoint_before_names_scope_v5708'
COUNTERS = dict(records_editorially_completed=6215, records_with_source_and_prose_pass=6218,
                records_revised_and_integrated=3905, retained_wordings_editorially_completed=2310)
SUMMARY = (
    'The user expands the full editorial goal to include retrospective localization of '
    'proper names and generic speaker-role labels. Review natural American English, clean '
    'Japanese meaning, identification function, cultural context and consistency across '
    'nameplates, catalogs, dialogue references and other player-facing consumers. Preserve '
    'approved Rafael, Hodram, Joakim, Maria and Camille. Do not infer age, marriage, kinship, '
    'rank or biography from a portrait, unused metadata or a literal label. Existing native '
    'name proofs establish behavior, not a fresh contextual editorial approval. '
    'Clean actors164/165 are カップル男/カップル女; V5692 catalog labels are Man in a Couple/'
    'Woman in a Couple. The relationship qualifier is supported, but these English labels '
    'sound like descriptions of records. Reopen both as a paired editorial finding; final '
    'wording awaits the complete shared exchange and all name consumers. Do not substitute '
    'Husband/Wife or restore Young Man/Young Woman without source support. Preserve the '
    'earlier manuscript and its rationale as history. Queue all207 current catalog entries '
    'for source-bound review and add other name/alias consumers as discovered. '
    'Lil B198 has17 uncredited clean-first speech glosses and source/current mapping, fresh '
    '207-name/eight-voice binding,34 speech dispatches, an entry getter,80 relative-skip '
    'cases and four original name consumers. Actors12/15 resolve to Yukihisa Shiraki/'
    'Angelo Puccini in progressive names; full catalog Yukihisa Genjo Shiraki/Angelo Puccini. '
    'The FE text is an unattributed speaking voice. Controls, predicate semantics, complete '
    'scene behavior, contextual English, display and release integration remain pending. '
    'No new ROM, emulator run or editorial credit is added by this scope checkpoint. '
    'All counters, V5692 experimental candidate/patch and promoted main V4701 stay unchanged. '
    'The full four-storyline, earlier-dialogue, shared town/shop, random, Help and remaining '
    'prose goal, including retrospective early wrapping, stays active. Unresolved graphics/'
    'all18 plaques and later older-record technical re-audit remain separate and open.'
)
POLICY = '''## Speaker names and role labels: retrospective localization review

Include proper names and generic speaker-role labels in the full editorial pass,
including labels in earlier reviewed translations. Use natural American English
that preserves the clean Japanese identity and the label's function in the complete
exchange. Review a recurring pair or group together. Preserve the approved names
Rafael, Hodram, Joakim, Maria and Camille; record any other naming decision with its
exact source and current references, context, revision or justified retention.

Check consistency across progressive nameplates, full-name catalogs, dialogue,
runtime substitutions, menus and other relevant consumers. A runtime rendering
proof alone does not establish a natural localization. Keep literal labels and
unused name-table metadata as evidence, without inventing age, marriage, family,
rank, nationality or biography. Do not mechanically expand an internal identifier
into a player-facing label or replace all labels through a global substitution.

The screenshot's “Woman in a Couple” and paired “Man in a Couple” are source-bound
leads (actors165/164: カップル女/カップル男). Their relationship qualifier is supported;
their English phrasing needs review in the complete shared exchange. Neither
“Wife/Husband” nor “Young Woman/Young Man” follows from these labels alone.
Final replacement wording and integration remain pending; preserve the earlier
approved manuscript and rationale as historical evidence.

For each proposed change, bind all relevant native consumers and verify complete
leading/trailing characters, width, bounds, truncation, substitutions and any
pagination. Use representative gameplay and focused tests for distinct behavior
or concrete risks. Keep actual observations separate from offline checks. Integrate
validated revisions through the registered cumulative release and clean-input patch
workflow. Retain good labels with individual reasons; do not add duplicate dialogue
credit or relabel an old technical proof as a new editorial review.

'''


def inverse(value):
    result = deepcopy(value)
    result['latest_checkpoint'] = result.pop(PREVIOUS)
    result.pop(KEY)
    result.pop(SCOPE)
    return result


def check(plan, applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes()) == item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes()) == item['planned_sha256']
        assert sha(gzip.decompress(Path(item['before']).read_bytes())) == item['before_sha256']
    for path, digest in plan['evidence'].items():
        assert sha(Path(path).read_bytes()) == digest
    old = json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()))
    new = read(plan['files'][0]['planned'])
    assert inverse(new) == old
    assert new['current_integrated_candidate'] == old['current_integrated_candidate']
    assert all(new[k] == old[k] == v for k, v in COUNTERS.items())
    assert new['goal_status'] == 'active' and not new['full_goal_complete']
    assert read(PRIOR)['ledger_sha256'] == plan['files'][0]['before_sha256']
    for key in ['candidate', 'patch']:
        prior = read(PRIOR)
        assert sha(Path(prior[key]).read_bytes()) == prior[key + '_sha256']
    return new


def stage():
    assert not ROOT.exists()
    before = LEDGER.read_bytes()
    old = json.loads(before)
    assert sha(before) == read(PRIOR)['ledger_sha256']
    assert all(k not in old for k in [KEY, SCOPE, PREVIOUS])
    cat = read(CATALOG)
    assert cat['candidate_sha256'] == read(PRIOR)['candidate_sha256']
    rows = cat['catalog']['rows']
    assert len(rows) == 207 and len({r['actor_ID'] for r in rows}) == 207
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    historical = Path('translations/ordinary_name_fidelity_manuscript_v1.json')
    earlier = read(historical)
    leads = []
    for ident, expected, current in [(164, 'カップル男', 'Man in a Couple'), (165, 'カップル女', 'Woman in a Couple')]:
        field = 0x122000 + (ident - 164) * 32
        parts = []
        for delta in [0, 4]:
            pointer = struct.unpack_from('<I', clean, field + delta)[0]
            at = pointer - 0x02000000
            raw = clean[at:clean.index(0, at) + 1]
            parts.append(dict(pointer_field=field + delta, source_pointer=pointer,
                              storage_offset=at, terminated_hex=raw.hex(), Japanese=raw[:-1].decode('cp932')))
        assert parts[0]['Japanese'] == expected and parts[1]['Japanese'] == 'ヨーロッパ'
        row = next(r for r in rows if r['actor_ID'] == ident)
        previous = next(r for r in earlier['records'] if r['index'] == ident)
        assert row['current_catalog_name'] == previous['english'] == current
        assert previous['japanese'] == expected and previous['table_field'] == field
        leads.append(dict(actor_ID=ident, source_file='/__arm9__.bin', source_fields=parts,
                          source_third_field_null=struct.unpack_from('<I', clean, field + 8)[0] == 0,
                          current_catalog=row, current_reference=f'{CATALOG}#/catalog/rows/{rows.index(row)}',
                          historical_manuscript=str(historical), historical_record_id=previous['id'],
                          finding='Source-supported couple role expressed as an awkward catalog-like English label.',
                          earlier_rationale_preserved=True, final_replacement=None,
                          status='reopened; complete shared exchange and consumer review pending',
                          no_marriage_or_age_inferred=True, new_editorial_credit=0))
    ROOT.mkdir(parents=True)
    review = ROOT / 'speaker_names_and_role_labels_review_scope.json'
    save(review, dict(user_requested_retrospective_scope=True, approved_names=['Rafael','Hodram','Joakim','Maria','Camille'],
        full_catalog_queue=[dict(actor_ID=r['actor_ID'], current_name=r['current_catalog_name'],
            current_reference=f'{CATALOG}#/catalog/rows/{i}', status='fresh contextual name-localization review pending')
            for i,r in enumerate(rows)], source_bound_initial_findings=leads,
        catalog_queue_not_exhaustive_of_all_name_alias_consumers=True,
        previous_name_native_proofs_not_new_editorial_credit=True,
        existing_Samwell_catalogue_middle_field_and_other_alias_leads_preserved=True,
        new_editorial_credit=0, new_ROMs=0, new_emulator_runs=0, full_goal_complete=False))
    old_scope = Path(old['unfinished_editorial_scope_v5697']['path'])
    assert sha(old_scope.read_bytes()) == old['unfinished_editorial_scope_v5697']['sha256']
    scope = deepcopy(read(old_scope))
    scope['speaker_names_and_role_labels_localization_review_v5708'] = dict(path=str(review), sha256=sha(review.read_bytes()),
        all207_current_catalog_entries_queued=True, includes_previous_translations=True, initial_paired_actor_leads=[164,165],
        no_editorial_completion_or_final_replacement_claimed=True)
    scope['next_Lil_B198_clean_review_pending']['fresh_source_native_evidence_v5700_to_v5707'] = dict(
        source_objects=17, all_uncredited=True, source_current_dispatches=34, relative_skip_cases=80,
        original_name_consumers=4, no_actual_B198_gameplay=True,
        source_predicate_meanings_and_scene_controls_and_contextual_English_and_release_pending=True)
    scopepath = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(scopepath, scope)
    evidence_paths = [PRIOR,CATALOG,historical,old_scope,review,scopepath,Path(__file__),
        Path('work/analysis/lil_B198_clean_context_v5701/all17_clean_exchange_fresh_glosses_and_Namahage_scope.json'),
        Path('work/analysis/lil_B198_source_v5702/all17_clean_current_complete_context.json'),
        Path('work/analysis/lil_B198_dispatches_v5704/all17_source_current_dispatches_no_macros_and12_control_leaves.json'),
        Path('work/analysis/lil_B198_entry_v5705/source_EV2_B198_action_dependency_and_native_getter_binding.json'),
        Path('work/analysis/lil_B198_branches_v5706/original_relative_skip_operand_proof.json'),
        Path('work/analysis/lil_B198_names_v5707/four_original_progressive_and_catalogue_name_consumers.json')]
    evidence = {str(p):sha(p.read_bytes()) for p in evidence_paths}
    new = deepcopy(old)
    new[KEY] = dict(summary=SUMMARY, scope=str(review), scope_sha256=sha(review.read_bytes()), evidence=evidence,
                    requested_by_user=True, new_editorial_credit=0, full_goal_complete=False)
    new[SCOPE] = dict(path=str(scopepath), sha256=sha(scopepath.read_bytes()),
                      speaker_name_localization_review_open=True, Lil_B198_uncredited_objects=17, full_goal_complete=False)
    new[PREVIOUS] = old['latest_checkpoint']
    new['latest_checkpoint'] = SUMMARY
    assert inverse(new) == old
    targets = {LEDGER: encode_ledger(new)}
    assert len(targets[LEDGER]) < 100*1024*1024
    section = ('## V5708: Add retrospective speaker-name and role-label localization\n\n' + SUMMARY + '\n\n')
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path = Path('docs') / name
        prefix = ('# Current editorial handoff - V5708\n\n' if name == 'editorial_handoff_current.md' else '') + section
        targets[path] = prefix.replace('\n','\r\n').encode('utf-8') + path.read_bytes()
    for name in ['editorial_localization_and_layout_standard.md','natural_dialogue_workflow.md']:
        path = Path('docs') / name
        content = path.read_bytes()
        end = content.index(b'\n') + 1
        targets[path] = content[:end] + ('\n'+POLICY).replace('\n','\r\n').encode('utf-8') + content[end:]
    files = []
    for i,(target,data) in enumerate(targets.items()):
        planned = ROOT / f'{i:02d}.after'
        backup = ROOT / f'{i:02d}.before.gz'
        planned.write_bytes(data)
        backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),
                          planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True))
    print('Eight targets staged; two exact clean-source findings and207 pending catalog entries. No credit or ROM change.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['stage','audit','apply','verify'])
    phase = parser.parse_args().phase
    if phase == 'stage':
        stage()
    else:
        planpath = ROOT/'staged_checkpoint.json'
        plan = read(planpath)
        if phase == 'audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists()
            check(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(planpath.read_bytes()),
                all_before_planned_evidence_hashes_exact=True, full_nested_historical_inverse_exact=True))
            print('Eight-file preapplication audit and full historical inverse pass.')
        elif phase == 'apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'independent_preapplication_audit.json')['plan_sha256'] == sha(planpath.read_bytes())
            check(plan)
            for item in plan['files']:
                assert Path(item['target']).is_relative_to(Path.cwd().resolve())
                assert Path(item['planned']).is_relative_to(ROOT.resolve())
            for item in plan['files']:
                with Path(item['target']).open('r+b') as stream:
                    stream.write(Path(item['planned']).read_bytes())
                    stream.truncate()
                    stream.flush()
                    os.fsync(stream.fileno())
                assert sha(Path(item['target']).read_bytes()) == item['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all8_targets_exact=True, all_before_hashes_checked_before_first_write=True))
            print('Eight audited targets applied; every historical ledger value preserved.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all8_targets_exact']
            check(plan,True)
            prior = read(PRIOR)
            VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),
                candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
                patch=prior['patch'],patch_sha256=prior['patch_sha256'],
                all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
                **COUNTERS, names_and_role_labels_retrospective_scope_recorded=True,
                catalog_entries_queued=207,source_bound_initial_findings=2, final_name_replacements=0,
                Lil_B198_uncredited_objects=17,no_new_ROM_or_emulator_run=True,main_V4701_preserved=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5709 verified: name-localization scope active; V5692/counters/main unchanged. Full goal active.')
