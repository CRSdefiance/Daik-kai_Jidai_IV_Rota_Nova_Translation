"""Stage/apply additive clean-first progress; all completed credits stay fixed."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_checkpoint_v8887')
LEDGER=Path('translations/editorial_review_current_v1.json')
PREVIOUS=Path('work/analysis/editorial_handoff_verification_v8876/verified_handoff.json')
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_partial_v1.json')
VIEW=Path('work/analysis/Hodram_B61_B70_source_review_v8884/source_context_names_display_review_before_current_English.json')
NAMES=Path('translations/hodram_B61_B70_speaker_name_review_v1.json')
KEY='Hodram_SC1B61_B70_224_source_native_current_bound_first44_prose_180_pending_v8887'
SCOPE='unfinished_editorial_scope_v8887'
EVIDENCE=[
 'work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json',
 'work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json',
 'work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json',
 'work/analysis/Hodram_B61_B70_clean_names_v8880/thirtytwo_clean_full_andprogressive_compositions_current_binding.json',
 'work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json',
 'work/analysis/Hodram_B61_B70_clean_context_v8882/complete_clean_linked_38_44_context_before_B61_B70_English.json',
 'work/analysis/Hodram_B61_B70_source_paths_v8883/all224_source_memberships_original_branch_cases.json',
 'work/analysis/Hodram_B61_B70_current_v8885/current_effective.json',
 'work/analysis/Hodram_B61_B62_prose_v8886/44_contextual_decisions_180_still_pending.json',
 str(DOC),str(VIEW),str(NAMES),
 'work/analysis/Hodram_B54_B60_release_v8866/registered_release_verification.json',str(PREVIOUS),
 *[f'scripts/{name}' for name in [
 'gloss_Hodram_B61_B70_clean_v8877.py','prepare_Hodram_B61_B70_source_controls_v8878.py','prove_Hodram_B61_B70_source_controls_v8878.py',
 'prepare_Hodram_B61_B70_names_v8879.py','prove_Hodram_B61_B70_names_v8879.py',
 'prepare_Hodram_B61_B70_clean_fullnames_v8880.py','prove_Hodram_B61_B70_clean_fullnames_v8880.py',
 'prepare_Hodram_B61_B70_source_display_v8881.py','prove_Hodram_B61_B70_source_display_v8881.py',
 'prepare_Hodram_B61_B70_context_v8882.py','inventory_Hodram_B61_B70_context_v8882.py',
 'map_Hodram_B61_B70_source_paths_v8883.py','review_Hodram_B61_B70_source_v8884.py',
 'prepare_Hodram_B61_B70_current_v8885.py','map_Hodram_B61_B70_current_v8885.py','review_Hodram_B61_B62_prose_v8886.py']]]

TEXT="""V8887 continues from verified V8876/current registered experimental V8865. The previous count-answer turn was a status restatement without goal progress; this continuation completes new source/native/name/current-comparison evidence and44 individual prose decisions. The full editorial objective remains active. No new completion or credited source-prose counters, ROM, registered build, emulator run, promotion, separate user package, pruning, commit or push. Preserve every prior ROM, translation, draft, producer, proof and failure. Counts remain7,319 completed/7,322 credited source-prose anddrafts/4,538 integrated revisions/2,781 justified retentions. The rough20,000 remaining figure is a planning estimate, not an audited denominator.

All224 complete clean-Japanese speeches in SC1B61-B70 now have first meanings before current English. Gloss8877 reuses the earlier44 value-exact and adds180 individual meanings, with full-exchange emotional/fidelity notes. Source controls8878 bind392 commands/224 six-byte preambles/60 relative sites300 native cases/15 unforced queries/83 paired opaque structural decodes/10 full four-byte normal ends250 seeded cases in own verified V8865/captain1 context. Original8100 at B66offset124 queries event44 with the original getter; its unforced opening result is0. Never replace that result, infer plot semantics from raw8000 values or conflate persistent end resultword with interpreter mode. Every original complete-input, canary, ABI, whole-memory and unchanged-runtime guard remains. No actual gameplay or event-eligibility claim.

Names8879/8880 bind16 source identities/voices,32 current and32 clean original short/full getters, and24 complete current native name planes. All24 planes on their sheet were directly viewed. Names review translations/hodram_B61_B70_speaker_name_review_v1.json retains16 scoped progressive labels with individual source/current references and reasons. Maria's full getter actually composes Maria Huamei Li; Camille's distinct full getter composes Marinus, without replacing the approved Camille Overijssel identity. Actor154 explicitly displays source 水夫/Sailor progressively and 配下/Retainer in the full consumer. Trader/Port Worker avoid invented age, kinship or rank; Sirwood is a name, not a Sir title. Referenced prose surnames Kuhn/Pereira bind exact clean/current table fields; do not substitute a historical person's identity or biography. All207 names/fullcatalogue/customnames, Al Shin/full-name contexts and Geronimo/Alonso sharedデ ownership/deployment/consumers remain open.

Source display8881 covers all224 dispatches/896 original macro alignments/224 complete native pages. All23 source sheets were directly viewed. FI15/FA3/FO0 bind default given Hodram6/surname Bergstrom9; these pages use current English names/UI, not an all-Japanese UI. No source FE panels occur in this batch; the prior FE calibration supplies no new scene coverage. Complete leading/internal/final glyphs, independent pixels, native consumption, bounds and pagination pass offline. Paths8883 bind all224 speech memberships to verified original branches and exact original kind2-forwarding/kind3-mode-carry code/50 prior cases. Across10 blocks there are176 unconditional and48 conditional speeches within these offline models. All15,830 combinations of the five tested native structural arguments preserve the binary equality-to-one speech classes; command paths are not claimed identical. Repeated query sites vary independently in the models, not necessarily in any attainable game state. No predicates, roster, flags, RNG or event results were forced.

Linked context8882 reads all45 clean speeches in B38/B44. B44's27 already-completed speeches supply prior Lil/Camille recognition without duplicate credit. B38's18 are source-only context, not newly completed prose: its false-flag fleet scene explains Maria warning Camille and Lil nearly doubting Maria. B38's additional selectors/opaque commands are not newly localized or approved by this reading. B64 gift branches and later leaf/legend segment remain conditional; B65 circle/cross speech is deliberately opaque and crew pauses are alternatives; B66's later recognition needs both tests; B67 has four alternative familiarity replies plus conditional introduction/secrecy lines; B69 restores the prior relationship without inventing romance or marriage. B70's mixed-in object remains unnamed.

First current comparison8885 follows all224 clean meanings, names, pages and context. It binds224 exact raw/effective English predecessors,392 complete source/current command pairs,300 current relative cases and15 unforced current queries in own V8865. Existing registered catalogue substitutions, including Camille and Maria lines, are preserved as exact effective predecessors rather than ignored. All224 positions remain disjoint from completed coverage. This comparison alone is not individual English editorial approval.

Prose8886 reviews the complete first two exchanges, B61/B62:44 individual decisions,32 revisions and12 justified retentions, in translations/hodram_B61_B70_editorial_manuscript_partial_v1.json. Each retains exact source/current references, original/effective wording, source gloss, finding, reason, and mapped neighbor pairs. The source/context/localization/naturalness gates pass; all formatting gates remain false. Sera's yes confirms soldiers attacking her home, not the earlier uncomprehended country-destruction question. Restore Indian Ocean, bustle-to-crowds vocabulary clarification, springs and every landscape detail, her unfinished town thought, the conditional open-ended offer, her callback to Hodram's earlier civilian-woman objection, timing before language learning, cooking praise and no-one-will-object reassurance. Keep learner speech respectful and the language unnamed. No invented deaths, historical naval law, romance or formal cook appointment. Ordinary wrapping remains formatter-owned; no authored linebreaks, padding, alignment, viewport narrowing or fit-driven shortening.

Next: finish individual whole-exchange prose decisions for the remaining180 speeches B63-B70 using current8885, first meanings8877, source review8884, all alternate-path memberships8883 and scoped name decisions. Keep the approved first44 values and reasons unless a contextual finding warrants a documented successor. Then complete automatic full-width English plans/native pages/direct views, stored relocation and complete references/inverses, representative gameplay/focused tests for distinct behavior and concrete risks, production/atomic checks and registered cumulative integration/exact clean-input patch/own startup. Credit the batch once only after necessary integration checks pass. No exhaustive natural playthrough or individually visiting every conditional line is required. Source-only, offline native, initialized gameplay, natural activation and hardware coverage must remain distinct.

Current registered experimental V8865 andits existing exact clean-input patch/648 manifestbatches/114 acceptedlayers/18 releasechecks/110 regressions/own4001-frame startup remain verified and unchanged; reuse all completed B54-B60 and older checks. MainV4701/canonicalbaseline stay unchanged. The source-display session84795 andcurrent-comparison session81856 both terminated successfully; do not replay them because an earlier state was quiet. The new work supplies zero emulator frames or actual scene headers. Preserve all earlier gameplay/offline limits, all measured main/focused duration, decoded-length, RNG, RGB, following-command and longB60 actor differences; no future-equivalence or causal claim.

All four storylines, earlier translated dialogue, shared town/shop/random, Help/restprose,207 proper names/roles/aliases/customnames andretrospective premature breaks remain in scope. Every prior unfinished-scope value anddocument byte is preserved. Keep all leads including contractions/questiontags/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wider104-105-113-147/JanusPasar-versusPasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159versusRetainer/oldernormalends/nineteenthcells/B47-B48-B50metadata. Graphics/all18 plaques andlater older-record technical re-audit remain separate. The full goal is incomplete.
"""

def protected_paths(old):
    c=old['current_integrated_candidate']
    return [Path(p) for p in ['translations/release_stack.json','scripts/build_integrated_release.py',c['path'],c['patch'],c['manifest'],
        'out/raphael_natural_v2_accepted_base.nds','work/clean.nds']]

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='stage':
        assert not ROOT.exists();old=read(LEDGER);previous=read(PREVIOUS);doc=read(DOC);view=read(VIEW)
        assert sha(LEDGER.read_bytes())==previous['ledger_sha256'] and previous['pass']
        assert old['goal_status']=='active' and not old['full_goal_complete'] and old['records_editorially_completed']==7319
        assert view['all23_source_sheets224_complete_native_pages_directly_viewed_before_current_English']
        assert len(doc['records'])==44 and doc['revised']==32 and doc['retained']==12 and len(doc['remaining180_records_pending_individual_prose_decisions'])==180
        assert KEY not in old and SCOPE not in old
        ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes())
        evidence={p:sha(Path(p).read_bytes()) for p in EVIDENCE+[__file__]}
        pending=dict(status='224-clean-native-current-bound-first44-prose-decisions-180-individual-prose-pending-all-English-formatting-actual-release-pending',
            total_uncredited_physical_speeches=224,source_first_meanings=224,source_native_pages=224,source_viewed_sheets=23,
            source_controls=dict(commands=392,preambles=224,relative_sites=60,relative_cases=300,queries=15,opaque_pairs=83,seeded_ends=250),
            source_name_actors=16,scoped_progressive_name_retentions=16,current_native_nameplanes=24,
            current_raw_andeffective_predecessors=224,individual_prose_decisions=44,draft_revisions=32,justified_draft_retentions=12,
            remaining_individual_prose_decisions=180,all_English_formatting_gates_pending=True,
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_view=str(VIEW),source_view_sha256=sha(VIEW.read_bytes()),
            names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),evidence=evidence,new_credit=0,new_emulator_runs=0,new_ROM=False,
            supersedes_pending_state_only='Hodram_SC1B61_B70_224_clean_candidates_first44_meanings_pending_native_andcurrent_English_v8870',
            full_goal_complete=False)
        new=deepcopy(old);new['latest_checkpoint']=TEXT;new[KEY]=pending
        scope_before=Path(old['unfinished_editorial_scope_v8870']['path']);scope=read(scope_before)
        assert sha(scope_before.read_bytes())==old['unfinished_editorial_scope_v8870']['sha256']
        (ROOT/'scope_before.json').write_bytes(scope_before.read_bytes());scope_new=deepcopy(scope);assert KEY not in scope_new;scope_new[KEY]=deepcopy(pending)
        save(ROOT/'unfinished_editorial_scope_inventory.json',scope_new)
        new[SCOPE]=dict(path=str(ROOT/'unfinished_editorial_scope_inventory.json'),sha256=sha((ROOT/'unfinished_editorial_scope_inventory.json').read_bytes()),
            all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,new_completion_credit=0,
            new_uncredited_clean_source_positions=224,remaining_individual_prose_decisions=180,graphics_andlater_technical_reaudit_separate=True,full_goal_complete=False)
        new['research_checkpoints'].append(dict(id='V8887-Hodram-B61-B70-source-native224-first44-prose',documentation='docs/editorial_Hodram_B61_B70_v8887.md',
            manuscript=str(DOC),source_review=str(VIEW),new_editorially_completed=0,new_registered_ROM=False,
            source_first_meanings=224,prose_decisions=44,draft_revisions=32,justified_draft_retentions=12,remaining_individual_prose_decisions=180,new_emulator_runs=0))
        save(ROOT/'ledger_staged.json',new)
        documents=[]
        for path,header in [('docs/editorial_handoff_current.md','# Current editorial handoff - V8887; V8865 current\n\n## B61-B70:224 source/native/current records;first44 prose decisions;180 pending\n\n'),
            ('docs/known_issues.md','## V8887: Hodram B61-B70 source/native andfirst44 prose checkpoint\n\n'),('docs/todo.md','## V8887 active full editorial continuation\n\n')]:
            p=Path(path);before=p.read_bytes();backup=ROOT/(p.name+'.before');backup.write_bytes(before)
            prefix=(header+TEXT+'\n').encode('utf-8');staged=ROOT/(p.name+'.staged');staged.write_bytes(prefix+before)
            documents.append(dict(path=path,before=str(backup),before_sha256=sha(before),staged=str(staged),staged_sha256=sha(staged.read_bytes()),prefix_bytes=len(prefix)))
        cp=ROOT/'editorial_Hodram_B61_B70_v8887.md';cp.write_text('# Hodram B61-B70 checkpoint V8887\n\n'+TEXT,encoding='utf-8')
        save(ROOT/'stage_manifest.json',dict(ledger_before_sha256=sha(LEDGER.read_bytes()),ledger_staged_sha256=sha((ROOT/'ledger_staged.json').read_bytes()),
            previous_verified_handoff=str(PREVIOUS),previous_verified_handoff_sha256=sha(PREVIOUS.read_bytes()),
            scope_before_path=str(scope_before),scope_before_sha256=sha(scope_before.read_bytes()),documents=documents,
            checkpoint_doc=str(cp),checkpoint_doc_sha256=sha(cp.read_bytes()),protected_files={str(p):sha(p.read_bytes()) for p in protected_paths(old)},
            evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
        print('Staged additive224-source/44-prose checkpoint; independent audit required; all credits andROMs unchanged.')
    elif mode=='apply':
        manifest=read(ROOT/'stage_manifest.json');audit=read(ROOT/'independent_staged_audit.json')
        assert audit['pass'] and audit['stage_manifest_sha256']==sha((ROOT/'stage_manifest.json').read_bytes())
        assert sha(LEDGER.read_bytes())==manifest['ledger_before_sha256']
        for d in manifest['documents']:assert sha(Path(d['path']).read_bytes())==d['before_sha256'] and sha(Path(d['staged']).read_bytes())==d['staged_sha256']
        for p,digest in {**manifest['evidence'],**manifest['protected_files']}.items():assert sha(Path(p).read_bytes())==digest
        target=Path('docs/editorial_Hodram_B61_B70_v8887.md');assert not target.exists()
        LEDGER.write_bytes((ROOT/'ledger_staged.json').read_bytes())
        for d in manifest['documents']:Path(d['path']).write_bytes(Path(d['staged']).read_bytes())
        target.write_bytes(Path(manifest['checkpoint_doc']).read_bytes())
        save(ROOT/'applied.json',dict(stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),ledger_sha256=sha(LEDGER.read_bytes()),new_credit=0,full_goal_complete=False))
        print('Applied independently audited progress; live verification required.')
    else:raise ValueError(mode)
