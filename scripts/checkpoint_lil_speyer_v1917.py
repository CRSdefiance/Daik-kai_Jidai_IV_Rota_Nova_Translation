"""Record 59 contextual prose reviews; retain native/display/release gates."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Speyer_checkpoint_v1917')
DOC = Path('translations/lil_speyer_encounter_editorial_manuscript_v1.json')
CHOICES = Path('translations/lil_speyer_choices_editorial_draft_v1.json')
SOURCE = Path('work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json')
PROSE = Path('work/analysis/lil_Speyer_prose_v1915/source_context_and59_prose_reviews.json')
PROBE = Path('work/analysis/lil_Speyer_body_probe_v1916/body_only_prose_layout_research.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, choices, prose, probe = map(read, (DOC, CHOICES, PROSE, PROBE))
    rows = doc['records'] + choices['records']
    ids = [r['id'] for r in rows]
    assert len(rows) == len(set(ids)) == 59 and len(probe['rows']) == 57
    assert prose['manuscript_sha256'] == probe['manuscript_sha256'] == sha(DOC.read_bytes())
    assert prose['choices_sha256'] == sha(CHOICES.read_bytes())
    assert prose['source_packet_sha256'] == sha(SOURCE.read_bytes())
    assert not any('error' in r for r in probe['rows'])
    assert all(all(r['review'][k] for k in ('source','context','localization','naturalness'))
        and r['review']['formatting'] is False and r['localization_note'] and r['source_meaning'] for r in rows)
    assert sum(r['editorial_decision'] == 'revise' for r in rows) == 39
    assert sum(r['editorial_decision'] == 'retain-wording' for r in rows) == 20
    raw = LEDGER.read_bytes()
    ledger = read(LEDGER)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1691,1807)
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert not set(ids) & set(ledger['contextual_story_natural_dialogue_pass_v1871']['record_IDs'])
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass'] += 59
    ledger['records_with_source_prose_drafts'] += 59
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] += 59
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = ids
    drafts = ledger['active_source_prose_drafts']
    for path, records in ((DOC,doc['records']),(CHOICES,choices['records'])):
        drafts['manuscripts'].append(str(path))
        drafts['route_record_subsets_pending'][str(path)] = [r['id'] for r in records]
    drafts.update(status='116-reviewed-COMMON-and59-Speyer-source-context-prose-open',
        note='Stockholm51 and London111 integrated in V1909. Speyer B12854 speeches, two choices and separate B25three-speech aftermath reviewed; native scene controls, choice association, fonts, relocation, representative gameplay and release pending.')
    ledger['coverage_units'].append(dict(id='Lil-Speyer59-source-prose',file_path='/data/SC2.DK4',blocks=[128,25],
        record_IDs=ids,status='source-context-prose-reviewed;native-controls-choice-fonts-map-actual-release-pending',
        manuscripts=[str(DOC),str(CHOICES)],source_context=str(SOURCE),proposed_revisions=39,proposed_retentions=20,
        completed_entries_added=0,source_prose_reviews_added=59,full_goal_complete=False))
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=348,completed_route_records=289,
                next='Validate the Hamburg Speyer encounter and separate aftermath against original event conditions, new speaker controls and typed choices; retain the full all-routes/shared/random/player prose objective.')
    ledger['formatting_watchlist']['Lil_Speyer59'] = dict(status='source-prose-reviewed;native-display-pending',
        manuscripts=[str(DOC),str(CHOICES)],source_context=str(SOURCE),body_only_probe=str(PROBE),
        pending_scene_presentation_prefixes_and_record_IDs={p:[r['id'] for r in doc['records'] if r['source_presentation_prefix_hex']==p]
            for p in ('1d','98','97','02','09','0e','14')},
        typed_choice_IDs=[r['id'] for r in choices['records']],
        no_control_choice_or_full_display_approval_from_body_probe=True,
        whole_preambles_macros_complete_glyphs_bounds_pagination_and_transitions_required=True)
    ledger['next_route_scene_editorial_packet'] = dict(file_path='/data/SC2.DK4',blocks=[128,25],
        manuscripts=[str(DOC),str(CHOICES)],source_context=str(SOURCE),source_prose_review_complete=True,
        editorial_review_complete=False,actual_activation_pending=True,source_relocation_reference_map_pending=True,
        note='Event128 is Hamburg Speyer cargo encounter, category7/town5/subtype3; not an Amsterdam dye continuation. B25 requires completed128 and has separate defeat aftermath conditions. Native full predicate and outer scheduler still require proof.')
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread'] == fresh['fresh_pass_records_integrated'] == 162
    fresh['record_IDs'] += ids
    fresh.update(fresh_pass_records_explicitly_reread=221,fresh_pass_records_pending_native_actual_release=59,
        latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICES),
        coverage_note='Stockholm51 and London111 explicitly reread and integrated. Speyer59 explicitly reread as full exchanges, prose reviewed, native/display/release pending. Prior historical reviews still require explicit reconciliation.')
    summary = ('V1917 Speyer59 clean-source/full-exchange prose review:39 proposed revisions and20 justified retentions, comprising Hamburg B12854 speeches/two choices and B25three-speech aftermath. '
        'Preserve the Hanseatic revival motive, reciprocal insults, merchant rivalry and complete war/investment/share tutorial. Correct reversed negation, Kamil to Camille and adjutant to verified First Mate. '
        'All57 body-only paragraphs encode; no source-control, native font, choice association, live activation or release approval from that probe. '
        'No ROM or completion changes:1691 historical completions(1277 revised414 retained),1866 source/prose reviewed. Fresh pass221 reread,162 integrated,59 pending. '
        'Registered V1909 and exact clean-input patch unchanged.116 incomplete COMMON, all broader routes/shared/town/random/player prose, separate graphics/all18 plaques and later older-record technical re-audit remain open. Full goal active;V1492 stays promoted.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1917-Speyer59-source-context-prose',proof=str(ROOT/'checkpoint_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=59,full_goal_complete=False))
    for key in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','unresolved_graphics_work',
        'reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert ledger['records_with_source_and_prose_pass'] == sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 1866
    assert len(set(fresh['record_IDs'])) == 221
    pending = LEDGER.with_name('editorial_review_current_v1917_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    Path('docs/lil_speyer_v1917_source_review.md').write_text('# V1917 Speyer full-exchange source review\n\n'+summary+
        f'\n\nManuscript: {DOC.as_posix()}\n\nChoices: {CHOICES.as_posix()}\n\nSource: {SOURCE.as_posix()}\n\nBody-only research: {PROBE.as_posix()}\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream:
            stream.write('\n\n## V1917 Speyer59 source/context/prose\n\n'+summary+'\n\nSee [review](lil_speyer_v1917_source_review.md).\n')
    text = HANDOFF.read_text(encoding='utf-8')
    text = text.replace('# Current editorial handoff - V1912','# Current editorial handoff - V1917',1)
    text = text.replace('1807 source/prose reviewed.**','1866 source/prose reviewed.**',1)
    text = text.replace('Fresh V1871 contextual pass: 162 explicitly reread and integrated (Stockholm51 + London111).',
        'Fresh V1871 contextual pass:221 explicitly reread;162 integrated(Stockholm51 + London111),59 Speyer entries pending native/display/release.')
    text = text.replace('reviewed: 1518 COMMON + 289 SC2. No active reviewed-incomplete route drafts.',
        'reviewed:1518 COMMON +348 SC2.59 Speyer source/prose entries remain incomplete.')
    start = text.index('### Exact next work')
    end = text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    next_work = f'''## Current working unit: Speyer B128 and B25 - V1917

{summary}

- Prose: {DOC.as_posix()};57 speeches. Choices: {CHOICES.as_posix()};two retained labels. Every record has exact clean/current references, source gloss and individual retention/revision notes.
- Source packet: {SOURCE.as_posix()}. Only B128/B25 were fully reviewed; B30/B58/B61 were inventoried, not editorially credited.
- Body-only probe: {PROBE.as_posix()};57/57 encode without errors or non-line-count warnings. Complete preambles, native glyphs, new speaker scope and choice menu remain pending.
- Native role selector02086314/index1 yields First Mate on copied V1909 state with all4MiB unchanged. Martin Speyer matches clean マルティン; no invented Lord or uncle relationship.
- Source B128 choice command2314 stores label0 at2320 and label1 at2352. Visible menu/native result association remains pending; storage order is not a result claim.
- Post-London snapshot: E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_revised_run_v1903_RESEARCH_ONLY/frame_086310_arm9_ram.bin. Completed events22,23,24,26,120;128 incomplete, so B25 prerequisite does not pass.
- Event128 is the Hamburg cargo encounter(category7,town5,subtype3), not an Amsterdam dye continuation. The Amsterdam dye lead from London remains unresolved. Native catalog Pedro デ Valdes contains a separate unreviewed player-facing name lead.
- Inventory1913's event80 mutation-detection error is classified1914 as an original LCG draw on a fresh disposable copy. No live RNG was changed; no unused/crash claim.

### Exact next work

1. Evaluate original event128 full predicate on disclosed copied destination/context inputs; map native scheduler/actual access. Keep offline eligibility separate from actual activation.
2. Map exact B128/B25 progressive controls, particularly Speyer1d and Retainer98/97, and both native choice responses. Use representative gameplay and focused distinct-behavior tests; no need to individually visit every conditional speech.
3. Approve complete native fonts/macros/leading-and-trailing glyphs/bounds/pagination, typed branch and choice relocation maps, guarded source-bound compiler, cumulative registered release and exact clean-input patch before completion credit.
4. Continue the full fresh contextual review of all storylines, shared town/shop/random scenes and remaining player-facing prose. Reconcile historical reviews explicitly.116 COMMON entries remain incomplete; graphics/all18 plaques and later older-record technical re-audit stay separate/open.

Do not repeat completed Stockholm/London checks absent a concrete risk. Preserve every ROM and earlier translation. Canonical baseline and promoted V1492 stay unchanged.

'''
    HANDOFF.write_text(text[:start]+next_work+text[end:],encoding='utf-8')
    save(ROOT/'checkpoint_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in (DOC,CHOICES)},
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),body_probe=str(PROBE),
        records_reviewed_added=59,proposed_revisions=39,justified_retentions=20,
        historical_completed_unchanged=1691,source_prose_reviewed_after=1866,
        fresh_contextual_reread=221,fresh_contextual_integrated=162,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        no_new_ROM_no_native_actual_orcompletion_claim=True,full_goal_remains_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_reviewed=1866,historical_complete=1691,fresh_contextual_reread=221,
        integrated=162,Speyer_pending=59,full_goal_remains_active=True))
