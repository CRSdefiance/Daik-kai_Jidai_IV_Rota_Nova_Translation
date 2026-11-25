"""Save all373 stored/catalogue checks and three prepared, unrun gameplay fixtures."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    releasepath=Path('work/maria335_B137_B151_release_v1/registered_release_verification.json');release=load(releasepath)
    paths=[ROOT/p for p in ['offline_display_approval_v1.json','final_native_v1.json','body_visual_review_v1.json','mixed_visual_review_v1.json',
        'plan_continuity_v3/automatic_plans.json','reconstruction_v2/reconstruction.json','reconstruction_v2/FE_storage_alignment.json',
        'FE_storage_diagnostic_v1.json','stored_v2/stored_native_verification.json','loaders_v2/verification.json',
        'stored_catalogue_all_v1/all373_stored_effective_body_bindings.json','display_selection_v1.json','display_fixtures_v1/fixtures.json']]
    approval,native,body,mixed,plan,rebuilt,amendment,diagnostic,stored,loader,catalogue,selection,fixtures=map(load,paths)
    assert approval['all373_final_pages_directly_viewed'] and approval['all_names_and17_captions_directly_viewed']
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(373,194,179,610)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['reconstruction_sha256']==digest(paths[5])
    assert len(list((ROOT/'stored_v2').glob('record_*.json')))==373
    assert catalogue['all373_physical_bodies_checked'] and len(catalogue['records'])==373
    assert catalogue['stored_sha256']==digest(paths[8])
    assert (loader['fresh_whole_archive_loads_andcache_hits'],loader['fresh_parent_cases'])==(303,606)
    assert loader['reconstruction_sha256']==digest(paths[5]) and rebuilt['composed_block_archive_andserialized_parent_inverses_exact']
    assert len(fixtures['fixtures'])==3 and [f['frames'] for f in fixtures['fixtures']]==[29681,11681,11201]
    assert [f['utterances'] for f in fixtures['fixtures']]==[80,5,4]
    assert selection['selected_source_bodies']==len(selection['selected_speech_ids'])==83
    for fixture in fixtures['fixtures']:
        assert digest(fixture['path'])==fixture['sha256'] and digest(fixture['fixture'])==fixture['fixture_sha256']
        detail=load(fixture['fixture'])
        assert detail['clean_andregistered_host_prefix_andexit_commands_identical']
        assert len(detail['original_initializers'])==7 and len(detail['source_bound_QA_host_opening_exit'])==40
        assert detail['padded_QA_block_bytes']<=9216 and detail['all_selected_command_bytes_andcomplete_speaker_controls_exact']
    paths.extend([releasepath,Path(__file__),Path('dk4tool/script/reviewed_FE_storage_padding_v2.py')])
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B152–B175 passes offline display andstorage:390 contextual reviews (153 revisions/237 retentions),373 directly viewed body pages,17 captions and33 names. '
        'Eleven phrase wraps improve,one page is reclaimed andone stored FE blank row is repaired. All373 catalogue lookups,610 branch cases,303 loads and606 handoffs pass. '
        'Three representative gameplay fixtures covering83 distinct bodies are prepared butunrun. Fifth gates andregistration remain;no worker is live. Integrated21,691,registered c97e9677,main andfull scope are unchanged.')
    document='docs/editorial_Maria390_B152_B175_stored_20261110.md'
    text=f'''# Maria390 B152–B175 offline storage complete — November 10, 2026

{summary}

Continue the same390 original source objects in24 complete SC3 exchanges. [The prose checkpoint](editorial_Maria390_B152_B175_prose_layout_20261110.md) preserves the clean-first meanings/drafts, individual contextual comparisons,153 revisions/237 justified retentions and47 scoped name reviews. [The display/storage checkpoint](editorial_Maria390_B152_B175_display_storage_20261110.md) documents every display finding, complete visual evidence andthe exact B164R99 padding repair. Preserve both histories; their earlier live-worker statements are superseded bythis terminal checkpoint. All first four individual gates pass; fifth gates remain false pending representative gameplay andintegration.

Work root:`work/Maria_B152_B175_clean_20261109`. Final plan:`plan_continuity_v3/automatic_plans.json`. All373 bodies/pages (341 progressive/32 FE),17 captions and33 scoped name strings pass native/visual checks. Eleven phrase wraps improve andthe complete124-character bargaining aside reclaims one premature page. Eight record-bound FE reserves preserve physical228px geometry. Final body evidence selects362 initial,10 first-refinement andone final farewell receipt:1492 alignment cases. All385 initial/superseded/final previews were directly viewed on48 sheets,with changed pages matched to their exact final compiled bytes. The18 reused/15 fresh name planes andeight menu sheets were also directly viewed. Exact source/current/compiled/preview references are in `final_native_v1.json`, `body_visual_review_v1.json`, `mixed_visual_review_v1.json` and `offline_display_approval_v1.json`.

Selected reconstruction:`reconstruction_v2/reconstruction.json`, research-only ROM SHA256 `{rebuilt['research_ROM_sha256']}`. All24 complete blocks,679 native commands and122 relative sites preserve clean/current/block/archive/serialized-ROM inverses and9216-byte allocations. `reconstruction_v2/FE_storage_alignment.json` binds exactly B164R99 block byte660,20→00,retaining its44-byte command,every command offset/extent/result/scope,allbranch operands andall373 compiled planes. The four malformed-owner controls reject. `reviewed_FE_storage_padding_v2.py` handles this qualified odd-length text case;the earlier even-length two-byte removal helper is not applicable. Both reconstruction ROMs andfailed producers remain preserved. No runtime,font,prose orviewport change occurred.

The journaled stored job82040 exited0:373 bodies/pages,194 freshly checked padding-dependent renders,179 exact compiled-plane reuses and610 relocated native branch cases. Every stored byte,glyph,complete first/internal/final plane,canary,bound,row andpagination check passes. `stored_v2` contains373 individual successful record receipts plus `stored_native_verification.json`. The initial nonjournaled40805 run's B164 blank-row failure remains history andreceives no whole-batch approval. All373 effective-body catalogue lookups also exited0,with complete buffer/SP/input/all-unowned4MiB guards. The amended archive passes303 loads/cache hits and606 parent handoffs in `loaders_v2`. These are offline native checks,not gameplay.

Three pinned research fixtures are created in `display_fixtures_v1/fixtures.json`,not yet run:

- `Maria390_town_random_menu0`:80 bodies/pages,two menus,29681 frames. It samples all17 town forecasts with nearby named speech,the full repaired wine exchange,Scents,phrase refinements,private bargaining andthe reclaimed aside,exact prices,50000,Wits,Namahage repeated FE calls andreturns,andGlassmaking Guide.
- `Maria390_two_andthree_menu1`:five bodies/pages,two menus,11681 frames. One normal Down selection for each menu tests both second options andtheir ordinary returns.
- `Maria390_delegation_menu2`:four bodies/pages,one three-option menu,11201 frames. Two normal Down pulses test You decide. at index2 andthe following dialogue.

The union is83 distinct bodies; no actual gameplay credit isclaimed yet. All fixtures copy exact complete selected commands behind the source-identical Maria B33 seven-command prefix and40 original nonspeech exit/effect/cleanup commands. Native QA buffers remainwithin9216 bytes;only the disclosed host block changes andwhole parent inverses pass. Preserve allthree generated ROMs andpins. The montage tests display/controller behavior;it does not activate original conditional scenes or simulate earned stats/items,trades,chronology,locations orsupernatural events.

Next run these fixtures with the qualified Maria controller observer (`scripts.run_maria335_B137_B151_display_v1.py` is an unchanged adapter available for reuse,or make an exact-named successor). Retain normal16-frame A pulses andthe existing isolated system-only unlock disclosure. Analyze complete actual body/header planes,all declared two/three-option menu panels,highlight changes andordinary A returns. Main fixture contains two menus;the alternative fixture also contains two,so do not reuse an auditor's old one-menu assumption. Verify allthree three-choice indices andboth two-choice options. Readable actual contact sheets andhost resupply/departure/sailing transitions stillrequire direct view. Use the stored exact body/name/menu proofs rather thanreplaying their native matrices. Actual selection pixels andnumeric modal return registers are distinct claims. No unvisited source conditions,full route orhardware credit.

After necessary gameplay checks,seal fifth gates andintegrate390 exactly once over registered c97e9677,including the exact odd-length FE padding correction in the pure release transaction. Require own startup/protected getters andexact clean-input patch. Registered parent remains718 manifest entries/114 accepted layers/53 checks. Preserve the Market format/pointers/six-section ARM9,ASCII right bounds,source25 v2 guard,names/fonts/graphics andallearlier layers. No new registered testing candidate orpromotion occurred here.

Integrated21,691 =13,046 revisions+8,645 retentions;historical source/prose/draft21,694. Native story remainder4,207 =Lil1,805+Maria2,402,including this unregistered390. Full storylines,earlier unfinished contextual passes,sharedtown/shop/random/player prose andspeaker names/roles remain in scope. Keep early Rafael/tutorial priority,no guide photos,deferred graphics artwork andthe later older-record technical re-audit separate. Main promotion requires user acceptance. No cleanup,commit orpush. All workers are terminal.
'''
    update=dict(new_credit=0,native_pixels_andvisual_checks_pending=False,stored_native_checks_pass=True,stored_native_checks_pending=False,
        native_catalogue_all373_pass=True,representative_gameplay_pending=True,registered_integration_pending=True,
        all_individual_fifth_gates_still_pending=True,representative_fixtures=3,planned_distinct_gameplay_bodies=83,
        actual_gameplay_observed=False,evidence=evidence)
    checkpoint(mutation=ROOT/'stored_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria390 B152–B175:complete offline display/storage/catalogue;three representative fixtures prepared,unrun.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False,current_batch_evidence=evidence,
            next_action='Run/audit/view three Maria390 gameplay fixtures,including multi-menu andallthree indices;seal fifth gates andregister cumulative successor once.'),
        additional_updates={'Maria_SC3_B152_B175_clean_20261109':update},summary=summary,document=document,document_text=text,completed=21691,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved complete Maria390 offline storage andthree unrun fixtures;registered parent and21691 credit preserved.')


if __name__=='__main__':main()
