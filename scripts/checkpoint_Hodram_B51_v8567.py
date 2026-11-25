"""Audited zero-credit B51 contextual/native/stored checkpoint; full goal intact."""
import argparse
import gzip
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_checkpoint_v8567')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8568')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8554/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B51_contextual_native_stored_pending_actual_policy_registered_v8567'
SCOPE = 'unfinished_editorial_scope_v8567'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7224, 7227, 7227, 4483, 2741]
PROOFS = {
    'clean': 'work/analysis/Hodram_B51_clean_v8548/complete_clean_SC1_B51_EV1_andcoverage_before_current_English.json',
    'gloss': 'work/analysis/Hodram_B51_clean_gloss_v8549/five_first_clean_glosses_warning_andconditional_reactions.json',
    'source_controls': 'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json',
    'source_display': 'work/analysis/Hodram_B51_source_display_v8556/source_display.json',
    'source_view': 'work/analysis/Hodram_B51_source_view_v8557/source_view.json',
    'result_flow': 'work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    'current': 'work/analysis/Hodram_B51_current_v8559/current_effective.json',
    'prose': 'work/analysis/Hodram_B51_prose_v8560/contextual_review.json',
    'manuscript': 'translations/hodram_B51_editorial_manuscript_v2.json',
    'names': 'translations/hodram_B51_speaker_name_review_v1.json',
    'logical': 'work/analysis/Hodram_B51_logical_v8561/logical_paragraphs.json',
    'plan': 'work/analysis/Hodram_B51_layout_v8562/automatic_plans.json',
    'pages': 'work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json',
    'native_view': 'work/analysis/Hodram_B51_native_review_v8564/native_body_review.json',
    'relocation': 'work/analysis/Hodram_B51_relocation_v8565/reconstruction.json',
    'stored': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
    'own_input': 'work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json',
    'release': 'work/analysis/Hodram_B50_release_v8544/registered_release_verification.json',
}

SUMMARY = '''Current registered experimental cumulative V8543 remains unchanged and verified. Counts remain7,224 completed/7,227 credited source-prose and drafts/4,483 integrated revisions/2,741 justified retentions. B50's three decisions remain integrated and credited once. The four-storyline and wider editorial objective is active; route subtotal5,624 is not the full-goal denominator. MainV4701 and the canonical baseline remain unchanged. Preserve every ROM, translation, draft, executed producer, proof and failure. No separate requested package, promotion, pruning, commit or push.

B51 now has a complete clean-first contextual comparison and five individually documented decisions: four proposed revisions and one justified retention. Restore the explicit southern Mediterranean setting using the established reviewed term. Restore Hodram's complete What do you mean? question. Replace the unsupported A monster rules here with an unnamed person described naturally as bad news and well-meant self-preservation advice to head for another sea. Echo bad news as Charles's hesitant question without adding gender. Retain Gerhard's (Could it be?) because the parenthesized question naturally conveys a sudden, private, unresolved possibility; do not turn it into confirmed recognition or name the person. Add no rulership, rank, gender, crime, supernatural identity, relationship, biography or guaranteed safety. All clean/current references, old raw English and individual reasons remain in manuscriptv2 and its predecessors.

Native source selectors71/01/12/10 resolve Port Worker/Hodram/Charles/Gerhard with original voices0/1/0/1. Four scoped name retentions bind exact clean/current fields, two original getters per actor and complete style11 nameplanes through identical entire current code/COMMON/font and whole actual captain1 actors. Gerhard uses the registered Adernkatz correction, with historical Ardelknatts kept as history. Approved Hodram/Joakim and Charles Jean Rochefort remain. Port Worker is a natural occupational label here; the familiar source brother form does not establish kinship, and unused Europe metadata is not a spoken surname or nationality. No name asset or full207-name credit is added; wider Port Worker contexts remain open.

All20 source commands/five complete six-byte preambles/eight relative sites/two queries/four opaque controls/full four-byte end are mapped. Forty native branch-extent cases and fifty fresh original-caller fragment cases prove that result-kind2 forwards the second result word and kind3 preserves it. Ten composed structural cases keep event30 and the raw predicate distinct: event30 complete skips later reactions; otherwise the raw value1 includes Charles before Gerhard, while other tested values omit Charles. These are native structural rules, not naturally reached conversation paths or outer eligibility. Ordinary snapshot queries both returned zero without forcing flags or actors. Preserve all six return words and query scratch restoration. Two stopped fragment producers remain; source-locked successors corrected an end sentinel equal to the entry PC and supplied the original caller's frame-pointer precondition, without changing native code, addresses or guards.

Five complete Japanese pages/four qualified reused nameplanes and five complete English pages were directly viewed. Twenty logical and twenty compiled guarded alignments pass. Automatic full216px wrapping preserves every word, first/internal/final glyph, bounds and complete consumption; all five English bodies fit single pages. Two original line-count infos remain, with zero warnings or waivers. Ordinary complete-word southern/Mediterranean and telling/you boundaries were read in context. No manual prose break, padding, shortening, narrowed viewport, font/global metric change or QA weakening is used. All five formatting gates remain false pending remaining required checks.

Research reconstruction is400 stored/logical bytes with zero separate tail, compared with340 before. All eight relative targets relocate to exact command boundaries and pass forty native skip cases. One compiler parity tail receives four fresh alignments and unchanged native ink; four byte-identical bodies explicitly reuse sixteen alignments. Five fresh stored dispatches, two fresh unforced queries, four disclosed opaque structural decodes and twenty-five complete normal value-carry ends pass. Exact source/current/final references and complete block/archive/whole-in-memory-ROM inverses pass. Every324 unowned SC1 block, all other files/components, names/font/123264-byte deployed payload remain exact. Only research block/archive files were written; no new ROM, emulator capture, registered layer or completion credit exists for B51.

Preserve all B50/B49/Gerhard/Rafael/Hodram/B48 gameplay limitations, timing/RNG/component/calendar/RGB findings and disclosed fixture-entry scopes. Native fragments and linear decoders do not establish complete effects, natural activation, original location, legitimately earned inventory, custom names, full routes, hardware, every-frame causality or future simulation equivalence. Full practical town/random capture, representative gameplay and focused concrete-risk tests remain required; exhaustive natural playthroughs and individually visiting every conditional line are not required. All four storylines, earlier translated dialogue, shared town/shop/random, Help/remaining prose, all207 names/roles/aliases/custom names and retrospective premature breaks remain open as recorded in the complete inverse-preserved scope inventory. Keep graphics/all18plaques and the later older-record technical re-audit separate. Roughly20,000 remaining candidates remains a planning estimate, not an audited prose denominator.'''

NEXT = '''Continue from verifiedV8568/current registeredV8543. B51 manuscriptv2/namesv1 and source8555-8557/result-flow8558c/current8559/prose8560/logical8561/plan8562/pages8563/native-view8564/relocation8565/stored8566 are complete within their stated offline scope. Reuse them without unchanged replay. Counts7224/7227/4483/2741 remain unchanged; four revisions/one retention are uncredited until integration. Keep every prior artifact and full objective intact.

Next bind independent command/source/current/final references, loader/cache paths and shipped callers, then compare representative complete clean-Japanese/revised B51 playback and normal transitions with original controls and identical ordinary inputs. Use own registeredV8543 Hodram captain1 context scripts/Hodram_B50_registered_route_context_v8546.py and current input8546; never overlay historical RAM or borrow captain2. An initialized entry fixture must be explicitly disclosed. Preserve original event30 query, separate raw predicate, nested Charles scope, private Gerhard thought, opaque effects, terminal and result channel. Do not force event flags, actor presence, role, inventory, RNG, outcomes or controller timing to make the pair match. Distinct concrete risks include four-row source-qualified English, initial selector71 Port Worker header, speaker/voice changes, relocated conditional targets and complete normal return. Record actual observed paths separately from structural possibilities and unvisited conditional content; do not require exhaustive natural activation or an individual gameplay visit for every line.

Then freeze source-qualified natural-dialogue-v2 profile/compiler/native/actual evidence with all required guards and individual gates. Use meaningful actual-changing semantic precommit challenges and one complete NDS-object commit. Integrate through the sole registered cumulative builder, preserving every accepted layer and frozen dependency, exact clean-input patch reconstruction and own startup. Current stages are outcomesv6, B49v3 and B50v1 before percent safety with builder guardv6. Inspect supported registered extension facilities before adding a stage; preserve the complete original builder inverse and exact priorV8543 compatibility. Credit the five source decisions once only after necessary checks pass. Do not promote, prune, package separately, commit or push.

The complete copied scope inventory preserves every earlier lead and history, including contraction/question-tag, unscanned558plans, weak-before-row, COMMON750-752/preLF6435, wider actors104/105/113/147, JanusPasar/Pasha, ceramics17wrap, Cristina/Christina, HansRetzel/Letzel, Samwellmiddle, SourceItem/LocalProduct, Alexandria, AksumGoldSeal, Armadillo/SteelHide, HerophilusMedicine, イギリス, AlShin/AlFeridShin, Sailor151-159 versus Retainer, older normal-end carry/nineteenth-cell/B47/B48/B50 metadata and all practical capture/technical scope limits. Graphics and later older-record re-audit remain separate.'''

def parent_at(value, path):
    for key in path[:-1]:
        value = value[key]
    return value, path[-1]

def restore(value):
    result = deepcopy(value)
    for op in reversed(value[KEY]['inverse_operations']):
        parent, key = parent_at(result, op['path'])
        if op['existed']:
            parent[key] = deepcopy(op['before'])
        else:
            parent.pop(key)
    return result

def gates():
    prior = read(PRIOR)
    data = {k: read(p) for k, p in PROOFS.items()}
    assert [prior[k] for k in ['completed', 'source_prose', 'revised', 'retained']] == [7224, 7227, 4483, 2741]
    assert prior['candidate_sha256'] == data['release']['candidate_sha256'] == data['own_input']['current_ROM_sha256']
    assert sha(Path(prior['candidate']).read_bytes()) == prior['candidate_sha256']
    doc = data['manuscript']
    assert len(doc['records']) == 5 and doc['revised'] == 4 and doc['retained'] == 1
    assert all(all(r['review'][k] for k in ['source', 'context', 'localization', 'naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert data['gloss']['all5_clean_utterances_glossed_before_current_English']
    assert data['current']['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert data['result_flow']['original_parser_r3_receives_carried_value_word'] and len(data['result_flow']['caller_fragment_cases']) == 50
    assert len(data['names']['records']) == 4 and data['names']['no_new_name_asset_orall207_name_review_credit']
    assert data['native_view']['manuscript_sha256'] == data['relocation']['manuscript_sha256'] == data['stored']['manuscript_sha256'] == sha(Path(PROOFS['manuscript']).read_bytes())
    assert not data['plan']['failures'] and len(data['pages']['records']) == 5 and len(data['native_view']['original_infos']) == 2
    assert not any(i['severity'] in ['warning', 'error'] for row in data['plan']['records'] for i in row['base_QA']['issues'])
    for sheet in [data['source_view']['directly_viewed_sheet'], data['native_view']['directly_viewed_sheet']]:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    stored = data['stored']
    assert stored['whole_current_inmemory_ROM_inverse_byte_exact'] and stored['all324_other_blocks_andall_other_files_components_exact']
    assert stored['whole_ROM_not_written_orregistered'] and stored['fresh_native_alignment_cases'] == 4 and stored['exact_reused_native_alignment_cases'] == 16
    assert len(stored['stored_dispatches']) == 5 and len(stored['stored_queries']) == 2 and len(stored['normal_seeded_ends']) == 25
    assert data['relocation']['source_relative_sites'] == 8 and data['relocation']['relocated_native_skip_cases'] == 40
    return prior, data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['stage', 'audit', 'apply', 'verify'])
    mode = parser.parse_args().phase
    prior, data = gates()
    if mode == 'stage':
        assert not ROOT.exists()
        before = LEDGER.read_bytes()
        old = json.loads(before)
        assert sha(before) == prior['ledger_sha256'] and [old[k] for k in COUNTERS] == COUNTS and old['goal_status'] == 'active'
        new, ops = deepcopy(old), []
        def put(path, value):
            parent, key = parent_at(new, path)
            ops.append(dict(path=path, existed=key in parent, before=deepcopy(parent.get(key))))
            parent[key] = deepcopy(value)
        pending = dict(status='five-contextual-decisions-native-fullwidth-stored-controls-refs-pass-pending-actual-policy-atomic-registered-integration',
            file_path='/data/SC1.DK4', blocks=[51], records=5, proposed_revisions=4, justified_retentions=1,
            scoped_name_retentions=4, source_commands=20, source_relative_sites=8, source_query_sites=2, source_FE_panels=0,
            source_selector_values=[113, 1, 113, 18, 16], manuscript=PROOFS['manuscript'], names=PROOFS['names'], proofs=PROOFS,
            records_with_exact_source_current_andresearch_final_references=deepcopy(data['stored']['records']),
            all_four_prose_gates_true=True, all_five_formatting_gates_false=True, current_English_dialogue_bodies_reviewed=True,
            automatic_fullwidth_pages=5, available_width_px=216, line_count_infos=2, warnings=0, waivers=0,
            logical_alignment_cases=20, compiled_alignment_cases=20, fresh_stored_parity_alignments=4, exact_stored_alignment_reuse=16,
            stored_block_bytes=400, stored_logical_end=400, stored_zero_tail_bytes=0, normal_stored_value_carry_cases=25,
            original_caller_result_channel_cases=50, structural_path_cases=10, actual_B51_emulator_runs=0,
            all324_unowned_blocks_andwhole_source_current_inverses_pass=True, independent_loaders_callers_actual_policy_atomic_registered_pending=True,
            new_source_prose_counter_credit=0, new_credit=0, full_goal_complete=False)
        oldpending = prior['pending_source_batch']
        marker = dict(checkpoint=KEY, prior_unread_andpending_flags_historical_not_deleted=True, new_credit=0)
        put([oldpending, 'superseded_by_contextual_native_stored_checkpoint'], marker)
        put(['latest_checkpoint'], SUMMARY + '\n\n' + NEXT)
        descriptor = old[prior['unfinished_scope']]
        assert sha(Path(descriptor['path']).read_bytes()) == descriptor['sha256']
        inventory = deepcopy(read(descriptor['path']))
        inventory[KEY] = deepcopy(pending)
        inventory['next_focus'] = NEXT
        if oldpending in inventory:
            inventory[oldpending]['superseded_by_contextual_native_stored_checkpoint'] = marker
        ROOT.mkdir(parents=True)
        scope = ROOT / 'unfinished_editorial_scope_inventory.json'
        save(scope, inventory)
        put([SCOPE], dict(path=str(scope), sha256=sha(scope.read_bytes()),
            all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            five_uncredited_contextual_decisions=5, graphics_andlater_older_record_technical_reaudit_separate=True, full_goal_complete=False))
        evidence = {str(p): sha(Path(p).read_bytes()) for p in [PRIOR, scope, Path(__file__), *map(Path, PROOFS.values())]}
        put([KEY], dict(**pending, summary=SUMMARY, next=NEXT, evidence=evidence, goal_turn_classification='progress', all_new_native_jobs_terminal_andreaped=True))
        new[KEY]['inverse_operations'] = deepcopy(ops)
        assert restore(new) == old and [new[k] for k in COUNTERS] == COUNTS
        assert new['completed_editorial_families'] == old['completed_editorial_families'] and new['current_integrated_candidate'] == old['current_integrated_candidate']
        (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before, mtime=0))
        targets = {LEDGER: encode_ledger(new)}
        for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']:
            path = Path('docs') / name
            prefix = ('# Current editorial handoff - V8567; V8543 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8567: B51 five contextual decisions/native/stored pass; actual and registered integration next\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8567 staged: six targets, five uncredited contextual/native/stored decisions. Exact inverse audit next.')
    else:
        plan = read(ROOT / 'staged_checkpoint.json')
        old = json.loads(gzip.decompress((ROOT / 'ledger.before.json.gz').read_bytes()))
        new = read(plan['files'][0]['planned'])
        assert restore(new) == old and [new[k] for k in COUNTERS] == COUNTS and new['completed_editorial_families'] == old['completed_editorial_families']
        assert new['current_integrated_candidate'] == old['current_integrated_candidate'] and new['goal_status'] == 'active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes()) == row['planned_sha256']
            assert sha(Path(row['target']).read_bytes()) == row['planned_sha256' if mode == 'verify' else 'before_sha256']
        for path, digest in plan['evidence'].items():
            assert sha(Path(path).read_bytes()) == digest
        if mode == 'audit':
            assert not (ROOT / 'preapplication_audit.json').exists()
            for index, row in enumerate(plan['files'][1:], start=1):
                original = gzip.decompress((ROOT / f'{index:02d}.before.gz').read_bytes())
                assert sha(original) == row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT / 'preapplication_audit.json', dict(staged_plan_sha256=sha((ROOT / 'staged_checkpoint.json').read_bytes()),
                every_prior_value_counter_candidate_andfamily_recovers_exactly=True, every_prior_document_preserved_byte_exact=True, new_credit=0))
            print('V8567 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
        elif mode == 'apply':
            assert not (ROOT / 'application_receipt.json').exists()
            assert read(ROOT / 'preapplication_audit.json')['staged_plan_sha256'] == sha((ROOT / 'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target, planned = Path(row['target']), Path(row['planned'])
                assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:
                    stream.write(planned.read_bytes())
                    stream.truncate()
                    stream.flush()
                    os.fsync(stream.fileno())
                assert sha(target.read_bytes()) == row['planned_sha256']
            save(ROOT / 'application_receipt.json', dict(all_six_targets_hash_exact=True, no_ROM_registry_orcompletion_counter_change=True, new_credit=0, full_goal_complete=False))
            print('V8567 applied; V8543 and all completion counters unchanged. Full goal active.')
        else:
            assert read(ROOT / 'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified = deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()), previous_verified_handoff=str(PRIOR), previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT, unfinished_scope=SCOPE, pending_source_batch=KEY, next_clean_exchange_not_selected=False,
                Hodram_B51_contextual_native_stored_checkpoint=deepcopy(new[KEY]), new_uncredited_source_positions=5,
                physical_speeches_pending=5, typed_choice_labels_pending=0, new_credit=0, new_emulator_runs=0, new_actual_frames=0, new_research_ROMs=0,
                all_new_native_jobs_terminal_andreaped=True, all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True)
            save(VERIFY / 'verified_handoff.json', verified)
            print('Verified V8568/current V8543: 7224 completed; B51 four revisions/one retention at native/stored checkpoint, actual/policy/registered integration pending. Full objective active.')
