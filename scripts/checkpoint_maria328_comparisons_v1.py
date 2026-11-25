"""Save source-first editorial progress without changing release identities orcompletion credit."""
from collections import Counter
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint


def main():
    proposal_path = ROOT/'all328_contextual_proposals_v1.json'
    draft_path = ROOT/'all328_independent_drafts_v1.json'
    meaning_path = ROOT/'all328_clean_meanings_v1.json'
    current_path = ROOT/'current_v1/current_effective.json'
    objects_path = ROOT/'current_objects_v1/current_objects.json'
    proposals, drafts, meanings, current, objects = map(load,[proposal_path,draft_path,meaning_path,current_path,objects_path])
    assert proposals['records_count'] == len(drafts['records']) == len(meanings['records']) == 328
    assert (proposals['proposed_revisions'], proposals['justified_retentions']) == (139,189)
    assert Counter(r['kind'] for r in proposals['records']) == Counter({'ordinary-speech':289,'physical-style-alternative':24,'typed-menu-caption':15})
    assert all(r['contextual_comparison_saved'] and r['finding'] and not any(r['review'].values()) for r in proposals['records'])
    assert all(r['retention_reason'] for r in proposals['records'] if r['decision'] == 'retention')
    assert meanings['source_meanings_sealed_before_independent_drafts'] and drafts['current_English_not_consulted']
    assert proposals['FE_source_panels'] == 27 and proposals['dynamic_source_selectors'] == {'207':13,'208':1}
    assert len(proposals['glyph_targets']) == 20 and len(objects['style_objects']) == 4 and len(objects['choice_objects']) == 5
    assert objects['native_style_getter_cases'] == 32 and current['original_current_catalogue_lookups'] == 289
    assert current['runtime'] == objects['runtime'] == proposals['runtime']
    release_path = Path('work/maria303_release_v1/registered_release_verification.json')
    release = load(release_path)
    assert digest('translations/release_stack.json') == release['registry_sha256']
    assert current['current_ROM_sha256'] == release['candidate_sha256']
    paths = [proposal_path,draft_path,meaning_path,current_path,objects_path,
        ROOT/'clean_source_packet.json',ROOT/'source_selection_v1.json',
        ROOT/'current_inputs_v2/projection.json',ROOT/'current_inputs_v2/sealed_drafts.json',
        ROOT/'B73_B86_contextual_proposals_v1.json',ROOT/'B87_B95_contextual_proposals_v1.json',release_path,Path(__file__)]
    evidence = {str(p):digest(p) for p in paths}
    summary = ('Maria B73–B95 now has 328 clean-source meanings, independent drafts and individual contextual comparisons '
        'across 21 complete exchanges: 139 proposed revisions and 189 justified retentions. The pass finds an untranslated '
        'pilgrimage greeting, Cristina inconsistencies, a malformed prayer, missing puzzle conditions, overconfident rumors '
        'and two Kanji-corrupted rescue styles. All 20 non-ASCII targets have proposed ASCII text. Names/terms, role consumers, '
        'final prose gates and fresh display checks remain; every individual gate is still false. No new ROM or credit. '
        'Integrated 20,361, registered d42dcd8e, main and the full editorial scope are unchanged.')
    text = '''# Maria328 contextual-comparison checkpoint — November 9, 2026

**328 clean-first meanings, independent English drafts and source/current decisions are saved across 21 complete exchanges.** There are 139 proposed revisions and 189 individually justified retentions. This is editorial progress, not completion credit: scoped names/terms, role consumers, the final complete-prose reread and all five individual gates remain pending. No new ROM, formatted pages or gameplay observations are claimed.

Continue under `work/Maria_B73_B95_clean_20261109`:

- `all328_contextual_proposals_v1.json` is the selected comparison manuscript. Every row has exact clean/current references and bytes, its Japanese, faithful meaning, whole-exchange context, unchanged independent draft, selected paragraph, finding and any retention reason. All 328 individual review objects remain false. The two disjoint decision producers/receipts are `review_maria_B73_B86_contextual_v1.py` / `B73_B86_contextual_proposals_v1.json` (121 decisions: 57 revisions/64 retentions) and `review_maria_B87_B95_contextual_v1.py` / `B87_B95_contextual_proposals_v1.json` (207 decisions: 82 revisions/125 retentions).
- `all328_clean_meanings_v1.json` was saved before `all328_independent_drafts_v1.json`; both preceded this intake's current-ROM English extraction. Their historical unconsulted markers describe that saved stage, not a blanket claim about all past exposure. Approved item-label records were consulted separately from story prose. Independent drafts are preserved even when the existing English was retained or a comparison refined the draft.
- `clean_source_packet.json` and `source_selection_v1.json` preserve the exact clean blocks and completed native source inventory. Block/count pairs: 73/13, 74/22, 75/15, 76/15, 77/11, 78/10, 81/5, 82/2, 83/8, 84/4, 85/7, 86/9, 87/38, 88/50, 89/10, 90/3, 91/8, 92/21, 93/21, 94/25, 95/31. Numeric block order is not a claim of earned chronology.
- `current_inputs_v2` provides metadata-only views for the existing guarded binders: 289 ordinary speech objects, 24 physical style alternatives and 15 captions in five three-choice menus. Every source span, style header/alias and caption pointer/order is bound to the original command bytes. The first projection stopped at the census's kind naming; its partial `current_inputs_v1` remains preserved. No source, draft or ROM bytes were changed to make that projection pass.
- `current_v1/current_effective.json` binds all 289 current stored/effective bodies on the registered Maria303 candidate's own startup context. `current_objects_v1/current_objects.json` binds all 24 physical alternatives across four style objects, with 32 original eight-slot getter cases, plus all 15 captions/five menu objects. Clean handler/role ranges, source alias equivalence, current command maps and native input/owner/unowned-memory guards pass. These are offline current-text bindings, not fresh page rendering or gameplay.

The whole-exchange review preserves Charles's amber/science enthusiasm and an unnamed island rumor; Julio's explicitly supported grandfather relationship with Cristina and shield wish; Samwell's animal-armor rumors and cooking joke; Janus's uncertain Aristarchus attribution; Emilio's personal culinary search and Hestia's Pot; Yukihisa's formal blade appreciation; pilgrimage and Christian prayer context; the riddle questions and separate outcomes; the cult leader's village threat and the blanks/fireworks bluff; the villager's religious assumptions as his own beliefs; Istanbul's timed round-trip results; the monk's challenge to Maria's hatred and warning about her own motives; and the grandfather/child rescue and reluctant gift acceptance. No kinship, military rank, army allegiance, denomination, named reward or original-event outcome is inferred from generic metadata.

Concrete proposed corrections include: the still-Japanese B85R4 greeting; five Cristina spellings and the lost doting-parent/grandfather joke; the Father/Son/Holy Spirit prayer; an armor rumor presented as an assured stun effect; Maria's promise to keep a rumor in mind mistranslated as an instruction to Samwell; Emilio's personal search made into a crew obligation; generic capitals substituted for Istanbul; missing slight share increase; the32-contact riddle omitting contact with the floor and incorrectly saying the crawling babies stand; personal ignorance made into a universal unknown origin; and familiar big-sister address implying kinship in the rescue farewell. The source's wrong puzzle guesses stay wrong in their own branches. A strong fatal travel warning is preserved while the ordinary-ship difficulty remains uncertain.

**20 current non-ASCII targets require fresh glyph/display checks.** Two physical rescue styles, `SC3_B95_STYLE_400_18` and `_42`, currently expose `濡ot it!` through the original consumer. Both have natural ASCII proposals; they are real text/encoding defects within this goal, not deferred artwork. B85R4 remains Japanese in the current consumer. The other targets include full-width reaction punctuation and mixed-width ellipses. `glyph_targets` in the selected manuscript binds every exact source/current reference and proposed text. None is claimed visually corrected yet.

**Next reconcile scoped names, items, locations and native role/style consumers, then reread the complete selected English.** Established candidate item labels include Muramasa, Peacock Mail, Jaguar God's Vest, Minerva Shield, Hestia's Pot and Aristarchus Telescope; bind their clean/current pointer fields before final term approval. Confirm the Conqueror's Proof and Santiago Cathedral consumers rather than silently replacing them with draft aliases. Bind static speaker names and roles, spoken references and both name consumers. Source selectors207/208 occur in 13/1 ordinary speeches; do not assign them invented fixed identities. The four style objects have 24 physical alternatives across eight-slot aliases; all alternatives, including the corrupted pair, stay in scope. The 27 FE panels include source-staged question prompts and narrator/trap messages and require their distinct consumer rules. Two FI tokens are preserved; FA/FO/FU do not occur in these selected source bodies.

After source/context/localization/naturalness approval, compile logical paragraphs with the validated consumer widths. Preserve every original speaker/layout preamble, style alias, runtime token, menu order and relative branch. Review every newly generated page in readable sheets and check complete glyphs, bounds, allocation, terminators and pagination. Reuse exact compatible technical proofs; test distinct behavior and concrete risks, including dynamic/style voices, FE prompts, menu returns and the corrupted first glyphs. Keep offline checks distinct from actual initialized emulator scenes and unvisited original conditions. No exhaustive natural activation or guide photos are needed. Integrate only after the necessary checks through registered Maria303 and an exact clean-input patch; main promotion still requires user acceptance.

Registered candidate remains `work/maria303_release_v1/all_routes_maria303_candidate.nds`, SHA-256 `d42dcd8edbd9c04b1f1e26813d1feef06fada22e9c7a5a525ac637931d780679`, with714 entries/114 accepted layers/49 release checks. Preserve the market terminator allocation/pointers, six-section ARM9, ASCII right-bound fix, source25 guard and previous B54R507 correction. No registered build was started this turn. Integrated totals remain20,361; native story objects remaining remain5,537 (Lil1,805/Maria3,732). This328-object intake has zero credit. All unfinished storylines, prior contextual passes, shared shop/town/random exchanges, names and other player prose remain in scope. Deferred graphics artwork and the later older-record technical re-audit stay separate. All ROMs, earlier translations, drafts, decisions and evidence are preserved. No job is live.
'''
    checkpoint(mutation=ROOT/'comparison_progress_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria B73–B95:328 clean drafts andcontextual decisions saved;139 revisions/189 retentions.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            proposed_revisions=139, justified_retentions=189, native_job_live=False, registered_build_live=False,
            guide_photos=False, next_action='Reconcile scoped names/terms and207/208/style roles;complete selected-prose reread before final prose gates.',
            current_batch_evidence=evidence),
        additional_updates={'Maria_SC3_B73_B95_clean_20261109':dict(new_credit=0,
            source_meanings_saved=328, independent_drafts_saved=328, contextual_comparisons_saved=328,
            proposed_revisions=139, justified_retentions=189, meanings_drafts_contextual_comparisons_andall_five_gates_pending=False,
            source_only_no_current_English_read=False, source_meanings_anddrafts_preceded_current_comparison=True,
            selected_contextual_proposals=str(proposal_path), selected_contextual_proposals_sha256=digest(proposal_path),
            final_scoped_names_terms_role_consumers_prose_reread_andall_five_gates_pending=True,
            all_fifth_formatting_gates_pending=True, current_text_source_binding_complete=True,
            new_native_pages_oractual_gameplay_approval=False, current_batch_actual_gameplay_observations=0,
            registered_integration_pending=True, progress_evidence=evidence)},
        summary=summary, document='docs/editorial_Maria328_comparisons_20261109.md', document_text=text, completed=20361,
        protected={'translations/release_stack.json':release['registry_sha256'], release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'], release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Checkpoint saved:328 meanings/drafts/comparisons,139 proposed revisions/189 retentions;zero credit;full scope active.')


if __name__ == '__main__':
    main()
