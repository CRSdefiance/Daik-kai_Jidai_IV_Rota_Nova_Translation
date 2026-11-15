"""Save the completed offline residual review without gameplay or release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
PROSE=Path('translations/hodram_B0_B41_contextual_review_v3.json')
RELEASE=Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json')

def main():
    paths={
        'prose':PROSE,'visual':ROOT/'offline_visual_approval_v1.json',
        'reconstruction':ROOT/'stored_reconstruction_v2/reconstruction.json',
        'stored':ROOT/'stored_v1/stored_native_verification.json',
        'catalogue':ROOT/'stored_catalogue_all_v1/all388_stored_effective_body_bindings.json',
        'loaders':ROOT/'loaders_v1/verification.json',
        'names':ROOT/'scoped_names_formatting_review_v1.json',
        'name_fields':ROOT/'name_field_checks_v1/native_name_fields_verification.json',
        'roles':ROOT/'role_bindings_v1.json','terms':ROOT/'scoped_terms_v1.json',
        'native':ROOT/'native_joined_v2/compiled_native_pages.json',
        'styles':ROOT/'native_objects_styles_v2/compiled_style_objects.json',
        'menus':ROOT/'native_objects_v2/complete_choice_objects.json',
    }
    d={k:load(p) for k,p in paths.items()};prose=d['prose'];stored=d['stored'];rebuilt=d['reconstruction']
    assert prose['records_count']==394 and prose['counts']==dict(revision=221,retention=173)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert prose['all32_tutorial_editorial_decisions_unchanged'] and prose['other393_decisions_exact']
    assert d['visual']['final_all389_pages_directly_viewed_or_exact_reused'] and len(d['visual']['findings'])==388
    assert d['visual']['three_menus_six_captions_directly_viewed'] and d['visual']['all42_scoped_planned_names_native_andvisually_checked']
    assert (rebuilt['speech_count'],rebuilt['style_physical_speech_count'],rebuilt['typed_choice_count'])==(341,47,6)
    assert len(rebuilt['changed_blocks'])==39 and rebuilt['relative_sites']==137
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'])==(389,172,217)
    assert stored['typed_labels_checked']==6 and stored['fresh_relocated_native_relative_cases']==685
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert d['catalogue']['all388_ordinary_and_style_bodies_checked'] and len(d['catalogue']['records'])==388
    assert (d['loaders']['fresh_whole_archive_loads_andcache_hits'],d['loaders']['fresh_parent_cases'],d['loaders']['exact_reused_parent_cases'])==(325,78,572)
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    for key in ['stored','loaders']:assert d[key]['reconstruction_sha256']==digest(paths['reconstruction'])
    assert d['catalogue']['stored_sha256']==digest(paths['stored'])
    assert d['names']['all42_planned_progressive_names_native_andvisually_checked'] and d['name_fields']['no_ROM_created']
    release,package=map(load,(RELEASE,PACKAGE))
    summary=('All 394 residual Hodram B0–B41 contextual decisions and offline display/storage checks are saved: '
        '221 revisions/173 justified retentions, 388 bodies/389 reviewed final pages, six captions and 42 scoped names. '
        'Four final wrap corrections, an earlier FE blank-row repair, a contrast-phrase wrap and one FO-substitution prose correction pass. '
        'Stored pages, 685 branch cases, 388 catalogue lookups and 325 archive loads pass. '
        'Representative gameplay, the three surname fixes in a mixed registered successor, and release integration remain. '
        'Integrated coverage stays 18,767; main and the registered candidate are unchanged.')
    document=f'''# Hodram residual offline display and storage checkpoint

{summary}

- [394 contextual decisions](../{PROSE.as_posix()}): exact clean/current references,221 revisions and173 justified retentions. All32 tutorial decisions remain; the full faction substitution follow-up changes only B3R6.
- [Final visual approval](../{paths['visual'].as_posix()}): all389 initial pages andsix changed pages directly viewed;383 unchanged record proofs reused exactly. All388 bodies have individual page references and dispositions. Three menus/six captions and42 planned progressive names are visually checked.
- [Stored verification](../{paths['stored'].as_posix()}):389 pages,172 fresh parity-dependent checks/217 exact plane reuses,six captions and685 native branch cases. Seven complete style objects retain47 physical alternatives/56 target slots;63 rejection cases pass.
- [Native catalogue](../{paths['catalogue'].as_posix()}): all388 complete pre-macro buffers pass original getters with RAM,input andstack guards.
- [Archive loading](../{paths['loaders'].as_posix()}):325 complete loads/cache hits,78 fresh parent cases/572 matching reuses.
- [Research reconstruction](../{paths['reconstruction'].as_posix()}):39 complete SC1 blocks only,777 commands/137 relative sites,exact archive andwhole-parent inverses. Research-only ROM `{rebuilt['research_ROM']}`,SHA-256 `{rebuilt['research_ROM_sha256']}`. It does not contain the proposed three surname changes andis not a testing release.
- [Scoped names](../{paths['names'].as_posix()}),[roles](../{paths['roles'].as_posix()}) and[terms](../{paths['terms'].as_posix()}): exact clean/current andnative consumer bindings. David Flahven,Georg Salzgitter andNagayoshi Kamuro have qualified28-byte exclusive surname proposals,12 directly viewed current/proposed planes andeight rejection cases. Retained names use18 fresh planes/20 exact reuses. Future conditional role assignment andfull catalogue UI remain unvisited.

The final visual changes keep “like him,” “Shouldn't we” and “All hands” together and keep the complete closing broadside instruction on page 2. B30R13 already ends its first row with “the man”; its candidate returns identical bytes and the good layout is retained. Earlier native feedback corrected one FE tutorial blank row and the me-or-FO comparison. B3R6 now reads “Look there! That's {{MACRO:FO}}, the fleet that's been muscling in on our waters!” The earlier possessive produced “Bergstrom Fleet's fleet.” Japanese identifies the encroaching fleet as FO. No other new prose changes; the earlier Sao Jorge spelling reconciliation remains.

All18 body glyph targets pass native checks. The two deliberately opaque source-script cries are complete,not globally normalized. The B15R80 source-defined empty utterance andpoem's separate source utterances remain intentional. A33-character menu caption was never shortened: its observer's32-byte read limit was corrected to the original bounded NUL-terminated object. Native FE row membership,complete leading/internal/trailing glyphs,pixels,bounds,consumption,pagination,allocation,controls andsubstitutions pass with no QA waiver.

Reuse provenance stays explicit: native backend/startup is the registered B301–B310 snapshot; complete ARM9,COMMON,font andall39 current blocks match the B311–B324 target exactly. New English/current bindings identify that latest target. These are offline native checks,not fresh startup,hardware oractual scene coverage. All394 fifth gates remain false pending the required gameplay/release sealing;new credit is zero.

Next use representative bounded gameplay for distinct bodies,FE/anonymous panels,pagination,allthree menu responses andreturns,plus the corrected surname headers. Use the proven9,216-byte QA capacity andsource-occurrence-based fixture generator;do not repeat the resolved overflow orduplicate-byte matching investigations. Then prepare a mixed registered successor using the Rafael5186 pattern: reviewed SC1 plus only the three owned surname spans. Preserve all706 predecessor entries,114 accepted layers andASCII right-bound runtime. Require exact parent inverse,clean-input patch,own startup andprotected getters before credit. Do not promote main without acceptance.

Preserve the failed initial FE run andcompleted-block recovery,the caption observer diagnostic,the v2-planner pre-output stale-prose-binding rejection,the missing-role-argument pre-output stop,the v1 caption-schema approval failure andthe first reconstruction's missing current-index metadata stop. The latter is fixed by byte-verified metadata aliases in storage_inputs_v2,with no prose orcompiled-byte changes. No process remains live at this checkpoint. Prior ROMs,evidence andweekend ZIP remain protected. Full editorial scope,early-game/tutorial priority,separate artwork andlater older-record technical re-audit continue;no guide photos.
'''
    evidence={str(p):digest(p) for p in [*paths.values(),Path(__file__)]}
    checkpoint(mutation=ROOT/'stored_checkpoint_v1',batch_key='Hodram_SC1_B0_B41_clean_next_20261107',
        batch_updates=dict(new_credit=0,current_English_comparisons=394,contextual_decisions=394,four_prose_gate_records=394,
            proposed_revisions=221,justified_retentions=173,remaining_current_comparisons=0,
            offline_final_pages=389,offline_body_records=388,offline_body_visual_complete=True,offline_caption_visual_complete=True,
            body_glyph_targets_native_checked=18,visual_wrap_corrections=4,FE_blank_rows_corrected=1,
            substitution_prose_followups=1,scoped_name_decisions=42,scoped_name_retentions=39,scoped_name_revisions=3,
            retained_name_planes_pending=False,scoped_names_pending=False,dynamic_roles_pending=False,scoped_terms_pending=False,
            stored_pages_passed=389,native_relative_cases_passed=685,stored_catalogue_lookups_passed=388,archive_loading_pass=True,
            remaining_offline_display_checks=0,remaining_display_checks=394,all_fifth_gates_pending=True,representative_gameplay_pending=True,registered_integration_pending=True,
            name_actual_headers_andregistered_layer_pending=True,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram residual394 prose/offline display/storage complete; representative gameplay andmixed integration remain.',
            next_action='Reuse389 checked pages,complete representative bounded gameplay; integrate SC1 plus three qualified surname fields through registered mixed successor.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,native_job_live=False,
            registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B0_B41_stored_20261107.md',document_text=document,
        completed=18767,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved394-record offline/storage checkpoint;18767 integrated,zero new credit,no main change.')

if __name__=='__main__':main()
