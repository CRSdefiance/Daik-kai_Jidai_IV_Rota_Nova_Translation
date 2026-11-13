"""Assemble exact latest-parent references and checkpoint uncredited editorial progress."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT = Path('work/analysis/Rafael_B61_B80_clean_20261104')
RUNTIME = Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104')
RELEASE = Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

if __name__ == '__main__':
    current_path = RUNTIME/'all539_current_effective_qualified_v1.json'
    comparison_path = ROOT/'B61_B67_289_contextual_comparisons_latest_v1.json'
    assert not current_path.exists() and not comparison_path.exists()
    release = load(RELEASE)
    qualification_path = RUNTIME/'dependency_qualification.json'
    qualification = load(qualification_path)
    a_path = RUNTIME/'B61_B64_current197_exact_rebound_v1.json'
    b_path = Path('work/analysis/Rafael_B65_B80_current_20261104/current_effective.json')
    a,b = map(load, [a_path,b_path])
    assert a['runtime'] == b['runtime'] == qualification['runtime']
    assert a['current_ROM_sha256'] == b['current_ROM_sha256'] == release['candidate_sha256']
    groups = a['groups']+b['groups']
    assert [g['block'] for g in groups] == list(range(61,81))
    byid = {r['id']:r for g in groups for r in g['records']}
    assert len(byid) == 539
    save(current_path, dict(current_ROM=release['candidate'], current_ROM_sha256=release['candidate_sha256'],
        current_archive_sha256=a['current_archive_sha256'], runtime=a['runtime'], groups=groups, records=539,
        old197_exact_dependency_qualified_reuses=True, fresh342_original_catalogue_lookups=True,
        original_macro_expansion_not_executed_here=True,
        own_latest_snapshot_used_not_old_RAM_relabelled=True,
        constituent_bindings={str(p):sha(p.read_bytes()) for p in [a_path,b_path]},
        dependency_qualification=str(qualification_path), dependency_qualification_sha256=sha(qualification_path.read_bytes()),
        new_credit=0, guide_photos=False, producer_sha256=sha(Path(__file__).read_bytes())))
    paths = [ROOT/name for name in ['B61_B63_77_whole_exchange_comparison_v1.json',
        'B64_120_whole_exchange_comparison_v1.json','B65_B67_92_whole_exchange_comparison_v1.json']]
    rows = []
    for path in paths:
        for original in load(path)['records']:
            row = deepcopy(original)
            now = byid[row['id']]
            for key in ['source_hex','source_complete_preamble_hex','source_reference','current_hex',
                        'current_reference','current_record_index','current_stored_text','current_effective_hex',
                        'current_effective_text','current_comparison_paragraph','current_catalogue_selected','selected_native_pointer']:
                assert row[key] == now[key], (row['id'],key)
            row.update(current_ROM=release['candidate'], current_ROM_sha256=release['candidate_sha256'],
                current_binding=str(current_path), current_binding_sha256=sha(current_path.read_bytes()),
                original_comparison=dict(path=str(path), sha256=sha(path.read_bytes()),
                    current_ROM=original['current_ROM'], current_ROM_sha256=original['current_ROM_sha256']),
                latest_parent_current_reference_exact_reuse_qualified=True)
            assert row['review'] == dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
            rows.append(row)
    revisions = sum(r['decision']=='revision' for r in rows)
    retained = len(rows)-revisions
    glyph_records = [r for r in rows if 'Ｉ' in r['current_comparison_paragraph']]
    glyphs = sum(r['current_comparison_paragraph'].count('Ｉ') for r in rows)
    assert len(rows) == len({r['id'] for r in rows}) == 289
    assert (revisions,retained,glyphs,len(glyph_records)) == (123,166,12,9)
    save(comparison_path, dict(format='dk4-qualified-contextual-comparison-assembly-v1',
        translation_policy='natural-dialogue-v2', target_locale='en-US', records=rows,
        proposed_revisions=revisions, justified_retentions=retained,
        fullwidth_I_corrections=glyphs, fullwidth_I_affected_records=len(glyph_records),
        additional_source_copied_punctuation_normalizations=2,
        current_binding=str(current_path), current_binding_sha256=sha(current_path.read_bytes()),
        constituent_comparisons={str(p):sha(p.read_bytes()) for p in paths},
        qualification=str(qualification_path), qualification_sha256=sha(qualification_path.read_bytes()),
        all_first_four_individual_gates_pass=True, all_individual_fifth_gates_still_false=True,
        remaining250_comparisons_pending=True, no_new_pages_gameplay_ROM_orcredit=True,
        new_credit=0, guide_photos=False, producer_sha256=sha(Path(__file__).read_bytes())))
    sealed_path = ROOT/'B61_B80_all539_individually_source_first_drafts_v1.json'
    terms_path = ROOT/'trade_house_andBamboo_Assembly_Plan_binding_v1.json'
    summary = ('Rafael and all tutorials remain first. B61–B80 has all 539 clean meanings and independent drafts, '
        '289 contextual comparisons (123 proposed revisions/166 justified retentions), 12 full-width I fixes in nine speeches and two punctuation normalizations. '
        'All 539 current references and compatible dependencies are qualified on verified eb62870b; 250 comparisons and all fresh display checks remain. '
        'Trade house and Bamboo Assembly Plan match existing native terms. No new credit: 10774 integrated completions. Main, all ROMs and full scope preserved; no live jobs or guide photos.')
    document = Path('docs/editorial_rafael_539drafts289_comparisons_20261104.md')
    text = f'''# Rafael: 539 drafts and 289 comparisons — 2026-11-04

Rafael early story and all tutorial work remain first. All storylines, earlier translations, shared shop/town dialogue, random scenes, names/roles and remaining player-facing prose stay in scope. Preserve all translations, justified retentions, coverage, ROMs and evidence. No main promotion, pruning or guide-photo collection. Graphics artwork and the later older-record technical re-audit remain separate.

## Verified release retained

Current experimental cumulative ROM: `{release['candidate']}`. SHA256: `{release['candidate_sha256']}`. Its 669 entries, 114 accepted layers, eight final stages, 26 release checks, clean-input patch and own Rafael startup are already verified. Reuse `{RELEASE}` and `docs/editorial_rafael249_registered_and539_next_20261104.md`; do not repeat them. No build or emulator job is live.

10774 integrated completions remain (6356 revisions/4418 retentions). Historical source/prose/draft totals retain their existing difference of three. No completion credit is added for this new batch. The canonical main remains `{release['canonical_base']}`, SHA256 `{release['canonical_sha256']}`. No main promotion is authorized by automated validation.

## Editorial progress

All 539 source meanings and complete original scene/event context are preserved under `{ROOT}`. B68 is control-only, not omitted prose. All 539 independent logical-English drafts are assembled in `{sealed_path}`. Each constituent was sealed before its own current-English extraction. The first 197 were already compared before this final assembly; this is not a claim that all 539 were still unexposed at assembly time.

New draft constituents: `B65_B67_92_logical_English_drafts_v2.json`, `B69_B70_108_logical_English_drafts_v1.json`, `B71_B75_116_logical_English_drafts_v2.json`, `B76_B80_26_logical_English_drafts_v1.json`. All earlier versions/producers are frozen. The personal-gratitude and unspecified-enemy refinements preserve source referents before current-story comparison. All paragraphs preserve source macros and have no authored wrapping or padding.

`{comparison_path}` binds 289 individual comparisons to the latest exact current references: 123 proposed revisions/166 justified retentions. First four gates pass; every fifth gate remains false. Individual original comparison receipts and their hashes are retained. The village120 contributes 49 revisions/71 retentions; the next92 contributes 34 revisions/58 retentions; the earlier77 retains its 40/37 decisions.

Concrete corrections include the disconnected offer/offense/self-reflection echo, a source unloading action changed to loading, invented collective eleven-year-old departure, a false claim that nobody had ever helped Charlotte, first-person/collective errors, missing emotional context and stilted fragments. Working short responses, supportive lines, greetings, teasing and substantial migration narrative remain with individual reasons. Preserve Romani identity, reported prejudice, approximate dates, source-defined ages, private Eirene/public Arcadius, threatened versus completed annexation, and speculative rather than declared relationships.

Twelve unintended full-width I letters in nine speeches are corrected in proposed prose. Two copied full-width punctuation marks are normalized in their specific wordless/name-call records. Source-bound silent ellipses and deliberate unfinished thoughts remain. These counts are glyph/wording findings, not extra dialogue credit. No wrapping fix is claimed before fresh page formatting.

## Latest-parent dependency reuse and current text

`{qualification_path}` verifies that all 20 SC0 blocks61–80, COMMON/HELP/font/EV0, complete actor objects and all 66 fields belonging to 22 scoped speakers are exact across 4b10fd67 and eb62870b. Only SC0 blocks51–60 and actor35 given-name data changed; actor35 is outside this batch. Undoing the exclusive field recovers the entire parent ARM9. Native code, tables, pointers and allocations match. Both own snapshots are independently identified; old RAM is not relabelled as new gameplay.

`{current_path}` assembles all 539 current stored/effective references. The original197 native lookups are qualified exact reuses. The remaining342 lookups ran successfully on the latest ROM own Rafael snapshot after their drafts were sealed; extraction session53525 terminated exit0. Source commands/preambles and catalogue selection are bound. Macro expansion is not executed by this extraction and needs its normal later formatting proof. All250 B69–B80 current speeches are extracted but have not yet been read/compared. B68 has no speech.

The 22 individual name/role retentions in `translations/rafael_B61_B80_scoped_names_andterms_v1.json` remain, with their exact qualified prior getter proofs. New name-page visual checks and representative headers are pending. Global207/full-catalogue review remains open; actor40 full-middle フォン/current Ｆong spelling/width remains a separate in-scope text-name issue.

## Terminology and next action

`{terms_path}` binds trade house to exact current COMMON657 and Bamboo Assembly Plan to clean/current item186 with unchanged nonname metadata. The old657 directory guard correctly rejected a later repacked directory; its code/config remain unchanged. The existing parser then used independently verified complete current ARM9/COMMON locks and the exact current directory, recovering the registered657 text unchanged. This is a read-only binding, not a new renderer investigation or display approval.

Use **Bamboo Assembly Plan** in B70R214, generic **plan** in B70R218/B72R71, during their pending comparisons. Keep the original Diagram drafts as provenance. No item-name change is needed. The source-defined Estado objective is drafted as overseas trading network, not a city/country/new royal rank. Reconsider only against the complete clean source and existing current wording.

Next: compare the remaining250 as complete exchanges from the saved source/drafts/current files. Preserve the five Charlotte FE speeches in B69 as her portrait-free/CG dialogue, not system notices. Its exact visual gesture remains unconfirmed; add no invented kiss. Preserve the actual direct loss to Valdes in B77 and alternative reward/event paths. Then format all539 with the validated consumer widths and registered right-bound correction; review every new native page, scoped names and boundaries; check stored controls/branches/loaders and focused CG/pagination/transitions. Use representative gameplay and disclose unvisited lines. Integrate the substantial completed batch through all eight registered stages with an exact clean-input patch once necessary checks pass. No new pages, gameplay or ROM changes are claimed by this checkpoint.
'''
    checkpoint(mutation=ROOT/'539drafts289_comparisons_checkpoint_mutation_v1',
        batch_key='Rafael_SC0_B61_B80_clean_20261104',
        batch_updates=dict(new_credit=0, source_meanings=539, remaining_source_meanings=0,
            source_first_logical_drafts=539, remaining_independent_drafts=0,
            sealed_drafts=str(sealed_path), sealed_drafts_sha256=sha(sealed_path.read_bytes()),
            contextual_prose_comparisons=289, remaining_contextual_comparisons=250,
            proposed_revisions=123, justified_retentions=166,
            comparison=str(comparison_path), comparison_sha256=sha(comparison_path.read_bytes()),
            proposed_fullwidth_I_glyph_corrections=12, glyph_correction_records=9,
            proposed_scoped_punctuation_normalizations=2,
            current_binding=str(current_path), current_binding_sha256=sha(current_path.read_bytes()),
            current_bound_records=539, current_bound_uncompared_records=250,
            remaining_older_English_unselected_andunconsulted=0, remaining_current_bound_butunread_records=250,
            earlier_English_unconsulted=False, eb62870b_dependency_requalification_pending=False,
            dependency_qualification=str(qualification_path), dependency_qualification_sha256=sha(qualification_path.read_bytes()),
            trade_house_anditem_terms=str(terms_path), trade_house_anditem_terms_sha256=sha(terms_path.read_bytes()),
            CG_gesture_andEstado_final_wording_pending=True, Estado_source_based_logical_draft_saved=True,
            all_individual_fifth_gates_pending=True, actual_gameplay_records=0,
            exact_source_current_native_names_event_membership_drafts_andall_five_gates_pending=False,
            fresh_formatting_stored_visual_gameplay_andregistered_integration_pending=True,
            next_action='Compare remaining250, using bound Plan terminology; then fresh full-batch formatting/display, focused CG/transitions and registered integration.'),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            next_independent_drafts=539, next_contextual_comparisons=289,
            registered_cumulative_build_live=False, registered_cumulative_integration_next=False,
            current_batch='Rafael_SC0_B61_B80_clean_20261104',
            Rafael_early_story_andall_tutorials_first=True, full_editorial_scope_preserved=True, guide_photos=False)},
        summary=summary, document=document, document_text=text, completed=10774,
        protected={'translations/release_stack.json':release['registry_sha256'],
            release['candidate']:release['candidate_sha256'], release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Checkpoint saved:539 drafts/289 comparisons/123 revisions/166 retentions.250 comparisons and all display remain;10774 completions/main unchanged.', flush=True)
