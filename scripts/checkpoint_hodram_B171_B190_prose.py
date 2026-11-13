"""Persist uncredited whole-exchange progress with an exact prior-ledger backup."""
import gzip
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
LEDGER = Path('translations/editorial_review_current_v1.json')
MANUSCRIPT = Path('translations/hodram_B171_B190_contextual_editorial_manuscript_v1.json')
NAMES = Path('translations/hodram_B171_B190_scoped_names_andterms_v1.json')
DOC = Path('docs/editorial_hodram_B171_B190_prose_20261104.md')
SUMMARY = ('B171–B190 has 435 complete contextual comparisons: 195 proposed revisions and 240 justified retentions, '
    'with all four prose gates passed. Also saved: 49 scoped name/term retentions for 32 actors, six story terms and 11 forecast cities. '
    'Fresh logical prose checks and 433 initial speech plans/440 pages pass; native FE row-membership testing found a real wrap defect and remains open. '
    'No completion credit or ROM added; 9498 complete, experimental 7774721f and main unchanged. Full scope and all evidence preserved; no guide photos.')


if __name__ == '__main__':
    mutation = ROOT / 'prose_checkpoint_mutation_20261104_v1'
    assert not mutation.exists() and not DOC.exists()
    doc, names, audit = map(load, [MANUSCRIPT, NAMES, ROOT / 'complete435_prose_consistency_v1.json'])
    assert doc['complete_four_gate_comparisons'] == 435 and (doc['proposed_revisions'], doc['wording_retentions']) == (195, 240)
    assert len(names['records']) == 49 and audit['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False) for r in doc['records'])
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 9498 and not prior['full_goal_complete']
    ledger = dict(prior)
    key = 'Hodram_B171_B190_clean_next_20261102'
    batch = dict(prior[key])
    batch.update(localized_drafts=435, current_English_comparisons=435, remaining_current_English_comparisons=0,
        proposed_revisions=195, justified_retentions=240, complete_four_prose_gate_reviews=435,
        ordinary_actor_bindings=32, current_name_consumer_bindings=64, scoped_name_andterm_retentions=49,
        native_identity_andterms_still_pending=False, no_current_ROM_English_extraction=False,
        initial_speech_plans=433, initial_planned_pages=440, new_credit=0,
        source_meanings_and435_drafts_sealed_before_current_ROM_English_extraction=True,
        no_blanket_before_any_prior_English_claim=True,
        formatting_visual_stored_gameplay_andregistered_release_pending=True,
        native_initial_job=dict(session=56647, terminal=True, exit_code=1,
            completed_block=171, completed_records=27, completed_pages=31,
            failure='B172 FE native row membership: planned rows and actual glyph rows differ; retain partial proofs and investigate only the new display risk.'),
        manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        scoped_names=str(NAMES), scoped_names_sha256=sha(NAMES.read_bytes()),
        consistency_proof=str(ROOT / 'complete435_prose_consistency_v1.json'),
        full_goal_complete=False, guide_photos=False)
    ledger[key] = batch
    ledger['latest_checkpoint'] = SUMMARY
    assert all(ledger[k] == v for k, v in prior.items() if k not in [key, 'latest_checkpoint'])
    registry = Path('translations/release_stack.json')
    assert sha(registry.read_bytes()) == '7e7288fe7920fb601ab96a6bde937793c2c9873dd6a9573be796853d7924d143'
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == '7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    prose = '''# Hodram B171–B190: complete contextual prose pass

All 435 objects across 20 complete exchanges have clean Japanese meanings, source-first English drafts and an individual comparison against the exact current ROM: 195 proposed revisions and 240 justified retentions. The four prose gates pass on every record; the display gate remains false. The two menu captions are included: Listen. replaces Hear; No thanks is retained as a natural refusal.

The pass corrects six lines that were still Japanese, unnatural self-reference, literal idioms, omitted qualifications, an invented fleet-admiral rank, confusing apprentice relationships and inconsistent names. It preserves the original order of the Sanghyeon name reveal. The perfume exchange keeps the source speaker's unspecified gender; the painting forecast concerns collecting paintings. The home-baked bread opening and the existing tea-shopping request work in context and are retained with specific reasons. Retention is an editorial decision, not a failed attempt to rewrite.

Thirty-two actors have 64 exact native name-consumer bindings: 14 actors freshly checked and 18 reused through matching dependencies. Individual localization decisions retain all 32 names/role labels, six typed story terms and 11 forecast cities. Man/Woman do not become Husband/Wife; Lady does not acquire a noble rank. The unnamed B179 FE-panel woman is not assigned another actor's identity. The distinct progressive Sailor/catalogue Retainer consumers remain intact. These are scoped decisions, not completion of the wider 207-name audit. The broader Proofs terminology question remains open.

All 435 logical paragraphs pass fresh CP932/ASCII, macro-count, no-authored-break/padding and scoped-spelling checks. Initial automatic formatting produces 440 pages for 433 speeches (405 progressive and 28 FE); two captions use their own consumer. Zero base-QA errors or warnings are present. Native testing completed B171's 27 speeches/31 pages, then detected actual FE glyph-row drift in B172. Session 56647 is terminal, exit 1. No full native, visual, stored, gameplay, release or fifth-gate pass is claimed. Preserve the partial native proof and investigate the actual failed row behavior before continuing; do not repeat B171 unchanged.

Authoritative artifacts:

- `translations/hodram_B171_B190_contextual_editorial_manuscript_v1.json`: all 435 decisions, exact source/current references and five individual gates.
- `translations/hodram_B171_B190_scoped_names_andterms_v1.json`: 49 individual name/term retentions and exact native binding references.
- `work/analysis/Hodram_B171_B190_clean_20261102/`: sealed meanings/drafts, four comparison parts, two-caption comparison, identity/term proofs and `complete435_prose_consistency_v1.json`.
- `work/analysis/Hodram_B171_B190_formatting_20261102/initial/automatic_plans.json`: fresh initial plans and diagnostics.
- `work/analysis/Hodram_B171_B190_native_20261102/initial/`: partial native results and readable QA sheets; no completed batch report exists yet.

All 435 clean meanings and drafts were sealed before extraction of the current ROM's English. The earlier user tea screenshot exposure remains disclosed; there is no blanket claim of no prior English exposure. Linked B89 crown context uses previously completed records without duplicate credit.

Registered release and counts remain unchanged: 9498 completed (5809 revisions/3689 retentions), historical source/prose/draft counters 9501. Experimental candidate SHA256 is `7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399`; main is `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Preserve the registered ASCII right-bound and all earlier name/runtime/static layers. No new ROM, completion credit, main promotion, commit/push, pruning or guide photos. All storylines, shared town/shop dialogue, random scenes and remaining player-facing prose remain in scope; graphics artwork and the later older-record technical re-audit remain separate.
'''
    updates = {DOC: prose}
    for name in ['editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md', 'known_issues.md', 'todo.md']:
        path = Path('docs') / name
        updates[path] = ('# Current editorial checkpoint - 2026-11-04\n\n' + SUMMARY +
            '\n\nContinue from [the complete prose checkpoint](editorial_hodram_B171_B190_prose_20261104.md). '
            'Reuse the completed source/prose work and B171 native proof. Correct the observed FE row behavior, then continue fresh formatting/native/visual checks. '
            'Earlier entries below are historical.\n\n' + path.read_text(encoding='utf-8'))
    encoded = encode_ledger(ledger)
    mutation.mkdir()
    (mutation / 'ledger.before.json.gz').write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    plan = []
    for index, (path, content) in enumerate(updates.items()):
        old = path.read_bytes() if path.exists() else None
        if old is not None:
            (mutation / f'{index}.before').write_bytes(old)
        plan.append(dict(path=str(path), before_sha256=sha(old) if old is not None else None,
            after_sha256=sha(content.encode('utf-8'))))
    save(mutation / 'mutation_plan.json', dict(documentation=plan, ledger_before_sha256=sha(before),
        ledger_after_sha256=sha(encoded), all_other_keys_preserved=True, new_credit=0))
    assert LEDGER.read_bytes() == before
    for entry, (path, content) in zip(plan, updates.items(), strict=True):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(content, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    staged = LEDGER.with_name('editorial_review_current_v1.pending_B171_B190_prose.json')
    assert not staged.exists()
    staged.write_bytes(encoded)
    os.replace(staged, LEDGER)
    save(mutation / 'verified_mutations.json', dict(ledger_sha256=sha(encoded), prose_comparisons=435,
        revisions=195, retentions=240, scoped_names_andterms=49, completed=9498,
        all_other_keys_preserved=True, native_display_failure_still_open=True, new_credit=0, full_goal_complete=False))
    print('Saved 435-comparison checkpoint; exact ledger backup and all prior credit/releases preserved.')
