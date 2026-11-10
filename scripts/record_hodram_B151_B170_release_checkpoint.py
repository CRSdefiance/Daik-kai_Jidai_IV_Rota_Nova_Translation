"""Save the verified release handoff and next clean intake without duplicating credit."""
import gzip
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B151_B170_release_verified_20261102')
LEDGER = Path('translations/editorial_review_current_v1.json')
NEXT = Path('work/analysis/Hodram_B171_B190_clean_20261102/complete_clean_meanings_checkpoint_v1.json')


if __name__ == '__main__':
    mutation = ROOT / 'handoff_mutation_v1'
    assert not mutation.exists()
    release, completion, next_intake = map(load, [ROOT / 'registered_release_verification.json', ROOT / 'completion_checkpoint.json', NEXT])
    assert completion['new_credit'] == 642 and completion['counts']['completed'] == 9498
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['candidate_sha256'] == '7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399'
    assert next_intake['total_editorial_objects'] == next_intake['source_meanings_saved'] == 435
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 9498 and not prior['full_goal_complete']
    key = 'Hodram_B171_B190_clean_next_20261102'
    assert key not in prior
    ledger = dict(prior)
    ledger[key] = dict(**next_intake, checkpoint=str(NEXT), checkpoint_sha256=sha(NEXT.read_bytes()))
    linked = Path('work/analysis/Hodram_B171_B190_clean_20261102/linked_B89_crown_context_v1.json')
    assert load(linked)['source_context_question_resolved_without_restarting_B89']
    ledger[key].update(linked_crown_context=str(linked), linked_crown_context_sha256=sha(linked.read_bytes()),
        pending_linked_crown_source_question=False, native_identity_andterms_still_pending=True)
    summary = ('B151–B170 registered and credited once:642 reviews,269 revisions/373 retentions;650 pages/26 layout fixes. '
        'Two static labels use15 owned bytes/12 changed bytes after all earlier runtime/name stages. '
        'Exact clean patch andcandidate-own startup pass.9498 complete;experimental7774721f/main unchanged. '
        'Next435 clean meanings saved;no current-ROM English ordrafts. Full scope/ROMs/evidence/later audit preserved;no guide photos.')
    ledger['latest_checkpoint'] = summary
    assert all(ledger[k] == value for k, value in prior.items() if k != 'latest_checkpoint')
    release_doc = Path('docs/editorial_hodram_B151_B170_release_20261102.md')
    assert not release_doc.exists()
    text = f'''# Hodram B151–B170: registered cumulative release verified

642 whole-exchange reviews are integrated and credited once:269 revisions and373 justified retentions. All634 speeches/650 pages,eight captions/four menus,39 scoped name/term decisions and41 native name strings pass.26 layout corrections preserve the prose. Abkhaz/Elysion use a separate final fixed-slot data stage:15 owned prefix bytes/12 actual changed bytes. No font,viewport,allocation,pointer orruntime-code change is introduced by that stage.

The experimental candidate is `{release['candidate']}`,SHA256 `{release['candidate_sha256']}`. Its profile is `{release['profile']}`;use `scripts/build_integrated_release_with_static_text.py`. It runs every earlier grouped-fields/runtime/name driver unchanged,including ASCII right bounds andthe Emilio/Fernando/Samwell/Follower/Diogo/de-name repairs. All{release['complete_stack_entries']} manifest entries,{release['accepted_layers']} accepted layers and{release['passing_release_checks']} release checks pass. Main is unchanged;user acceptance is required before promotion.

The canonical base remains `out/raphael_natural_v2_accepted_base.nds`,SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. The previous registered parent is `{release['parent']}`,SHA256 `{release['parent_sha256']}`. Changes from that parent are20 SC1 blocks and12 ARM9 static-data bytes;all other files,components,graphics,names,fonts andruntime code are preserved.

- Manifest SHA256: `{release['manifest_sha256']}`.
- Registry SHA256: `{release['registry_sha256']}`.
- Clean input `work/clean.nds` SHA256: `{release['clean_input_sha256']}`.
- Patch: `{release['patch']}`,SHA256 `{release['patch_sha256']}`. It reconstructs the entire candidate exactly from that clean input.
- Release/startup/completion proofs andall642 exact source/current/final bindings: `work/analysis/Hodram_B151_B170_release_verified_20261102/`.
- Final reviews: `translations/hodram_B151_B170_contextual_final_review_v1.json` and `translations/hodram_B151_B170_scoped_names_final_v1.json`.
- New scene/static stage qualifications reject eight new invalid cases;the ten already completed static-data rejection cases andunchanged technical contracts are reused.

Offline checks cover all650 pages,all captions/names,700 relative cases and325 archive loads.331 stored parity pages are fresh native checks;319 exact compiled pages and610 unchanged parent handoffs are reused. All newly generated pages were visually reviewed.

Actual QA is three disclosed English source-content coldboots/43003frames:31 selected B156 speeches/all23 cinematic FE panels,two generated two-page spacing cases,Rafael0/Claudio/Gerhard/Cesare/Arcadius/Julio transitions,andboth long-menu captions/highlights/branches.134 captured body planes,nine headers andboth highlights match native output;six QA sheets were viewed. The candidate's separate4001-frame ordinary coldboot passes ten exact previously reviewed RGB pairs anduses its own final read-only RAM snapshot. These are focused automated emulator tests;no complete natural route playthrough orhardware verification is claimed.

Other conditional content,three other menus andfull catalogues remain offline-only. City87 andthe Elysion ship widgets are unvisited;their typed getters/copy,complete font planes,source capacities,compact source display envelopes andall-byte inverse pass. No individual conditional activation is required. Following opening/port/sailing frames add no editorial credit. Identical short text remains plane equivalence rather than proof ofa particular source occurrence. The earlier B133 initialized battle limitation remains source-controlled;do not replay it.

Coverage is9498 completed:5809 revisions/3689 retentions. Historical source/prose/draft counters are9501. Every prior record,ROM,translation andevidence artifact is preserved. Full editorial scope remains active;graphics artwork andthe later older-record technical re-audit stay separate. No guide photos.

Next: clean B171–B190 intake has435 objects:433 speeches andtwo captions inone menu,zero styles andzero completed overlaps. All435 source meanings across20 blocks are saved before current-ROM English extraction;no localized drafts exist. The earlier user tea screenshot exposure forB188R22 is disclosed,so no blanket meaning-before-any-prior-English claim is made. The linked crown-discovery context is now bound to18 previously completed clean B89 records without repeating orcrediting that review;see `linked_B89_crown_context_v1.json` in the next intake folder. Bind native identities/terms before localized approval. Then localize complete exchanges,compare prior English,andapply fresh formatting/visual checks while reusing compatible technical proofs. See `work/analysis/Hodram_B171_B190_clean_20261102/complete_clean_meanings_checkpoint_v1.json`.
'''
    # Preserve historical notes verbatim while making the current state first.
    updates = {release_doc: text}
    handoff = Path('docs/editorial_handoff_current.md')
    updates[handoff] = '# Current editorial handoff - 2026-11-02: B151–B170 release verified;next435 clean meanings\n\n' + summary + '\n\nContinue from [the verified release checkpoint](editorial_hodram_B151_B170_release_20261102.md). Reuse completed prose/display/gameplay checks. The linked B89 crown context is bound without duplicate credit. Next: native identity/term bindings,then logical English drafts/current comparison. No main promotion.\n\nEarlier entries below are historical.\n\n' + handoff.read_text(encoding='utf-8')
    for name in ['editorial_efficiency_workflow.md', 'translation_progress.md', 'known_issues.md', 'todo.md']:
        path = Path('docs') / name
        updates[path] = '## Current verified checkpoint - 2026-11-02\n\n' + summary + '\n\nSee [current release andnext source checkpoint](editorial_hodram_B151_B170_release_20261102.md). Earlier entries below are historical.\n\n' + path.read_text(encoding='utf-8')
    mutation.mkdir()
    (mutation / 'ledger.before.json.gz').write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    encoded = encode_ledger(ledger)
    plan = []
    for index, (path, content) in enumerate(updates.items()):
        old = path.read_bytes() if path.exists() else None
        if old is not None:
            (mutation / f'{index}.before').write_bytes(old)
        plan.append(dict(path=str(path), before_sha256=sha(old) if old is not None else None,
            after_sha256=sha(content.encode('utf-8'))))
    save(mutation / 'mutation_plan.json', dict(documentation=plan, ledger_before_sha256=sha(before),
        ledger_after_sha256=sha(encoded), no_completion_credit_added=True, all_other_ledger_keys_preserved=True))
    assert LEDGER.read_bytes() == before
    for entry, (path, content) in zip(plan, updates.items()):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(content, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    staged = LEDGER.with_name('editorial_review_current_v1.pending_B171_B190_intake.json')
    assert not staged.exists()
    staged.write_bytes(encoded)
    os.replace(staged, LEDGER)
    assert sha(LEDGER.read_bytes()) == sha(encoded)
    save(mutation / 'verified_mutations.json', dict(ledger_sha256=sha(encoded), completed=9498,
        next_clean_objects=435, source_meanings=435, no_new_completion_credit=True,
        all_prior_completed_scope_preserved=True, main_unchanged=True, full_goal_complete=False, guide_photos=False))
    print('Release andnext435-clean-meaning handoff saved;9498 completions preserved;full editorial goal active.')
