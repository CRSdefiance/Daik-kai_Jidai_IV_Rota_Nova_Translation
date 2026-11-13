"""Persist the verified release and next source-only batch with exact ledger backups."""
import gzip
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B171_B190_release_verified_20261104')
LEDGER = Path('translations/editorial_review_current_v1.json')
NEXT = Path('work/analysis/Hodram_B191_B210_clean_20261104/complete_clean_meanings_checkpoint_v1.json')


if __name__ == '__main__':
    mutation = ROOT / 'handoff_mutation_v1'
    document = Path('docs/editorial_hodram_B171_B190_release_20261104.md')
    assert not mutation.exists() and not document.exists()
    release, completion, intake = map(load, [ROOT / 'registered_release_verification.json', ROOT / 'completion_checkpoint.json', NEXT])
    assert completion['new_credit'] == 435 and completion['counts']['completed'] == 9933
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['candidate_sha256'] == 'd14c24ba6aefd312099970423b8e1a9611a5913bc85f87feeb70fae00b0fe19a'
    assert intake['total_editorial_objects'] == intake['source_meanings_saved'] == 373
    protected = {release['candidate']: release['candidate_sha256'], release['parent']: release['parent_sha256'],
        release['patch']: release['patch_sha256'], 'translations/release_stack.json': release['registry_sha256'],
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in protected.items())
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 9933 and not prior['full_goal_complete']
    key = 'Hodram_B191_B210_clean_next_20261104'
    assert key not in prior
    ledger = dict(prior)
    ledger[key] = dict(**intake, checkpoint=str(NEXT), checkpoint_sha256=sha(NEXT.read_bytes()))
    summary = ('B171–B190 registered and credited once: 435 reviews, 195 revisions and 240 justified retentions; '
        '439 pages and 15 layout corrections. All 663 manifest entries, 114 accepted layers and six final runtime/name/static stages pass. '
        'Exact clean-input patch and candidate-own startup pass. 9933 completed; experimental d14c24ba, main unchanged. '
        'Next B191–B210: all 373 clean source meanings saved, zero completed overlaps; native identities/terms and localized drafts remain. '
        'All scope, ROMs and evidence preserved. No live jobs or guide photos.')
    ledger['latest_checkpoint'] = summary
    assert all(ledger[k] == v for k, v in prior.items() if k != 'latest_checkpoint')
    text = f'''# Hodram B171–B190: registered cumulative release verified

435 complete-exchange reviews are integrated and credited once: 195 revisions and 240 individually justified retentions. The 49 scoped name/term retentions add no dialogue credit. All 433 speeches, 439 final pages, two captions and 31 distinct name strings pass their native and visual checks. Fifteen layout corrections preserve the prose: four FE row-membership fixes and eleven phrase/page refinements. Julio's “First” uses the normal F in the native and actual captured dialogue. Reuse the completed research checks; see [the research checkpoint](editorial_hodram_B171_B190_checked_20261104.md).

The experimental candidate is `{release['candidate']}`, SHA256 `{release['candidate_sha256']}`. Profile: `{release['profile']}`. The registered `scripts/build_integrated_release_with_static_text.py` driver completed successfully through all original guards. All {release['complete_stack_entries']} manifest entries, {release['accepted_layers']} accepted layers and {release['passing_release_checks']} release checks pass. The ASCII right-bound correction and the five later name/static stages are preserved. Main is unchanged; promotion still requires user testing and explicit acceptance.

The canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. The previous registered parent is `{release['parent']}`, SHA256 `{release['parent_sha256']}`. Only twenty `/data/SC1.DK4` blocks differ from that parent. ARM9, COMMON, fonts, graphics, all other files/components and earlier runtime/name/static corrections are byte-identical to the parent. This batch adds no new name/static-data mutation.

- Manifest SHA256: `{release['manifest_sha256']}`.
- Registry SHA256: `{release['registry_sha256']}`.
- Clean input `work/clean.nds` SHA256: `{release['clean_input_sha256']}`.
- Patch: `{release['patch']}`, SHA256 `{release['patch_sha256']}`. Applying it to the clean input reconstructs the entire candidate byte for byte.
- Release, own-startup, once-only completion and all 435 exact source/current/registered bindings: `work/analysis/Hodram_B171_B190_release_verified_20261104/`.
- Final reviews: `translations/hodram_B171_B190_contextual_final_review_v1.json` and `translations/hodram_B171_B190_scoped_names_final_v1.json`.

Offline verification covers all stored speeches/captions, 439 viewed pages, 390 relative cases and 325 complete archive loads. There are 232 fresh parity-dependent pages and 207 exact compiled-page reuses; 40 fresh and 610 exact reused loader handoffs. The B179 terminal alignment-space case has zero visible ink beyond the panel and identical complete glyph planes; its narrow qualification does not waive other FE bounds checks. Six new invalid production cases were rejected. Unchanged technical proofs and earlier final-stage negative cases were reused.

Actual QA consists of five disclosed initialized English content coldboots totaling 85005 frames. It observes 413 complete body capture planes, 188 record/page observations, 27 name headers and both complete menu highlights/responses; eight final QA sheets were approved through direct viewing or exact image reuse. The B171 tests cover the normal F, a complete one-page question and three refined two-page transitions. B179 keeps every original scene command/effect/cleanup and observes all thirty body calls and the port return. Town fixtures observe all 130 body calls across eleven complete exchanges. Final source attribution checks ordered native calls against the byte-exact source-command sequence, avoiding ambiguity from repeated short text.

These are focused automated emulator tests, not full natural route playthroughs or hardware verification. Outer natural activation is excluded. The town fixture excludes original nontext town conditions and market effects, so it does not prove original location/control behavior or economic outcomes. B172–B178, other B171 conditional branches, full catalogues and individual item/city/sail widgets remain offline-only. Following opening/port/sailing frames add no target editorial credit. The candidate's separate ordinary 4001-frame coldboot passes ten exact previously reviewed RGB pairs, the current captain getter and its own final read-only RAM snapshot; no historical RAM overlay is used.

Coverage is now 9933 completed: 6004 revisions and 3929 retentions. Historical source/prose/draft counters are 9936. All prior completion keys and unrelated ledger entries are preserved. Full editorial scope remains active, including earlier translations wherever contextual review is unfinished. Deferred graphics artwork and the later older-record technical re-audit remain separate. Preserve all ROMs, earlier translations and evidence. No promotion, commit/push, pruning or guide photos. All jobs from this checkpoint are terminal with exit code zero.

Next is clean B191–B210: 373 objects across twenty complete exchanges, comprising 352 speeches and 21 captions in ten menus, with no style objects or completed overlaps. Every source meaning is saved before current-ROM English dialogue extraction in this intake. These are meaning notes, not localized English drafts or completed editorial reviews. Historical exposure to related dialogue is not ruled out. The label-free B203 command at offset 78 is exactly `0020`, not an omitted caption.

Next source checkpoint: `work/analysis/Hodram_B191_B210_clean_20261104/complete_clean_meanings_checkpoint_v1.json`. Bind the 43 ordinary speaker identities and both applicable name consumers using exact compatible proofs plus fresh checks only where needed. Bind canonical item/attribute terms, the mentioned Rocco Alemkel name and Japanese cultural terms before localized approval. Then draft natural logical paragraphs, compare complete existing-English exchanges, document revisions/retentions and run fresh formatting and page reviews. Preserve the medicine rumors as reported claims, all negotiation prices/branches, the named Namahage ambiguity, the shachihoko/figurehead misunderstanding and the parrot's exact call-and-response humor. Do not invent diagnoses, magical effects, kinship, ranks or relationships.
'''
    updates = {document: text}
    for name in ['editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md', 'known_issues.md', 'todo.md']:
        path = Path('docs') / name
        updates[path] = ('# Current verified editorial checkpoint - 2026-11-04\n\n' + summary +
            '\n\nContinue from [the verified release and next-source checkpoint](' + document.name +
            '). Reuse completed checks. Earlier entries below are historical.\n\n' + path.read_text(encoding='utf-8'))
    mutation.mkdir()
    backup = mutation / 'ledger.before.json.gz'
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    encoded = encode_ledger(ledger)
    plan = []
    for index, (path, content) in enumerate(updates.items()):
        old = path.read_bytes() if path.exists() else None
        if old is not None:
            (mutation / f'{index}.before').write_bytes(old)
        plan.append(dict(path=str(path), before_sha256=sha(old) if old is not None else None, after_sha256=sha(content.encode('utf-8'))))
    save(mutation / 'mutation_plan.json', dict(documentation=plan, ledger_before_sha256=sha(before),
        ledger_after_sha256=sha(encoded), protected=protected, no_completion_credit_added=True, all_other_ledger_keys_preserved=True))
    assert LEDGER.read_bytes() == before
    for entry, (path, content) in zip(plan, updates.items(), strict=True):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(content, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    staged = LEDGER.with_name('editorial_review_current_v1.pending_B191_B210_intake.json')
    assert not staged.exists()
    staged.write_bytes(encoded)
    os.replace(staged, LEDGER)
    assert sha(LEDGER.read_bytes()) == sha(encoded)
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in protected.items())
    save(mutation / 'verified_mutations.json', dict(ledger_sha256=sha(encoded), completed=9933,
        next_clean_objects=373, source_meanings=373, no_new_completion_credit=True,
        all_prior_completed_scope_preserved=True, main_unchanged=True, full_goal_complete=False, guide_photos=False))
    print('Verified release and next 373-source-meaning handoff saved; 9933 completions preserved; full editorial goal active.')
