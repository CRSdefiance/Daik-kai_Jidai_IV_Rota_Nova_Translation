"""Prepare a reversible zero-credit checkpoint preserving the full editorial objective."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive

PROOFS={
 'source':'work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json',
 'clean_names':'work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json',
 'first_gloss':'work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json',
 'B39_context':'work/analysis/Rafael_B49_prerequisite_gloss_v8077/complete22_clean_B39_glosses_explicit_B49_prerequisite_context_only.json',
 'names':'work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json',
 'C281_structural':'work/analysis/Rafael_B49_C281_structural_v8080/exact_C281_source_original_structural_boundary.json',
 'source_controls':'work/analysis/Rafael_B49_source_controls_v8081/source_EV0_56_relative_sites280_cases13_raw_predicates1_query25_seeded_ends.json',
 'paths':'work/analysis/Rafael_B49_source_paths_v8082/156250_compositions_distinct_complete_text_paths_and61_source_memberships.json',
 'B41_source':'work/analysis/Rafael_B49_event41_context_v8083/complete_clean_SC0_B41_EV0_andcoverage_before_current_English.json',
 'mentioned_names':'work/analysis/Rafael_B49_mentioned_names_v8084/three_clean_mentioned_identities_six_native_getters_component_only_review.json',
 'refined_gloss':'work/analysis/Rafael_B49_branch_gloss_v8085/61_refined_glosses256_paths_B39_B41_context_before_current_English.json',
 'B41_context':'work/analysis/Rafael_B49_branch_gloss_v8085/27_complete_clean_event41_context_glosses_no_new_credit.json',
 'current':'work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json',
 'effective':'work/analysis/Rafael_B49_effective_v8087/all61_effective_English_templates122_original_dispatches_no_FE.json',
 'prose':'work/analysis/Rafael_B49_prose_v8088/61_contextual_decisions256_paths_individual_revisions_retentions.json',
 'logical':'work/analysis/Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json',
 'plan':'work/analysis/Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json',
 'initial_native':'work/analysis/Rafael_B49_pages_v8091/61_complete_native_paragraphs61_pages244_compiled_alignments.json',
 'final_native':'work/analysis/Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json',
 'rejected_plan_note':'work/analysis/Rafael_B49_pages_refined_v8092/rejected_extra_article_phrase_priority_andguard_capacity_note.json',
 'source_names':'work/analysis/Rafael_B49_source_name_planes_v8093/61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json',
 'name_sheet':'work/analysis/Rafael_B49_name_review_assets_v8094b/review_sheet_receipt.json',
 'native_review':'work/analysis/Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json',
 'branches':'work/analysis/Rafael_B49_archive_tools_v8096/56_exact_source_current_relative_operands_bound_to280_native_cases.json',
 'relocation':'work/analysis/Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json',
 'stored':'work/analysis/Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json',
 'final_controls':'work/analysis/Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json',
 'older_metadata_lead':'work/analysis/Rafael_B48_relocation_metadata_v8099/historical_root_label_stale_actual91_records_oneFI_authoritative_arrays_unchanged.json',
}
SUMMARY="""Current registered cumulative ROM remains V8066; main V4701 is unchanged. Counts remain 7,082 completed, 7,085 source/prose records and drafts, 4,411 integrated revisions and 2,671 retentions; SC0 has 279 and the route subset has 5,482. B48 is complete and credited once. Its 637 manifest batches, 114 accepted layers, 18 release checks, 110 regressions, exact clean-input patch and own-current startup remain verified. B49 has no completion or source/prose credit and is not integrated.

B49's complete contextual manuscript is translations/rafael_B49_editorial_manuscript_v2.json: 61 speeches, 31 revisions and 30 individually justified retentions. Complete clean Japanese, seven clean identities, all 22 B39 prerequisite speeches and all 27 B41 variant-context speeches preceded current English. Event49 requires39 and excludes151; query41 selects the Africa/New World versus New World/far East suggestion. Event41 is Hans's theoretical advice about strength, ruins and local trust,not an Africa-clear or Proof-obtained flag. Native source checks cover 56 relative sites/280 cases,13 raw predicates,one completion query and25 seeded value-carry ends. The 156,250 structural result compositions produce 256 distinct complete text paths of44-59 speeches,42 common/19 conditional. The unforced opening composition predicts50; no B49 path is yet actual gameplay. ClaudioR107 andJanusR112 are alternatives,as areR238/R244;ArcadiusR405 andRafaelR409 are selected together. No party,state,role,roster,funds,seed orresult is forced.

The review corrects trade house versus Guild,competence versus trust,I'll only say this once versus a stronger warning,Lil's rejection of Camille's wording advice,prospective territorial ambitions,Spain's intended encroachment andthe storm-passed joke. It preserves working banter,the tentative pact request,common-enemy argument,grudging loyalty andRafael's qualified decision without new kinship,rank,romance,identity reveal,already-signed alliance orguaranteed outcome. R388's effective catalogue English differs from raw storage;retain the working words,normalize its two full-width I glyphs,andpreserve FI. Exact source/current/effective references andall individual findings are bound. All61 formatting gates remain false.

Seven original progressive/full name pairs,fourteen getters,seven voice mappings and28 default macro alignments pass. Three mentioned identities/six getters bind Hodram Joakim Bergstrom,James Clifford andMartin Speyer for component-only review. Preserve approved Hodram,Joakim andCamille;keep Hodram's deliberately unfinished Ber... something joke anddo not add James to the surname-only Clifford line. Janus Pasar remains distinct from Pasha. Source-compatible Lil Argot,Claudio Manaus,Julio Erneco,Arcadius Eudoxios andCamille Overijssel have scoped retentions. Full-name middles Eirene andMarinus remain in their own getters. Full207 review,actual headers,custom names andcatalogue UI remain open.

Final automatic plan is work/analysis/Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json. Initial a andexperimental b/d plans are preserved;d is not final. The private c planner keeps coherent phrases within the same row count anddoesnot penalize a short complete sentence as a broken internal row. Five compiled paragraphs change from a: R43 keeps its question andWho gave together;R142 keeps navy guy andthe unfinished name;R213 keeps fight out of me;R244 keeps Head west/New World/far East;R405 keeps North Sea. No prose,row count orpage count changes. English remains216px/four physical rows,with unchanged fonts,global profile,body NUL guard andsource controls00/02/04/05/06/08/09. The exact16source00 objects have15unique bodies. Private measured macros remainFI6/FA6/FO10;the source has twoFI andnoFA/FO. There are noFE objects.

All61 English paragraphs produce61 complete single native pages. Initial compiled proof has244 fresh alignments;final c binding has20fresh/224exact reused. Full first/internal/final glyph masks,bounds,consumption andpage origins pass. All61 clean Japanese pages andseven style11 names pass. Lil/Camille literal cases are8fresh;five exact names/20cases are reused through unchanged code,font,text andwhole-actor startup bindings. Synthetic full-getter strings haveCamille4fresh/Arcadius4reused cases;they are explicitly not actual catalogue UI. All12 final sheets were directly viewed;17total views include the five superseded body sheets. Preserve the failed original name-sheet assembly andits plane;its four lost un-serialized case results are not claimed reused.

All22 original line-break-count infos andthree exact weak-ending warnings remain with individual row reasons: R213line1the/fight,R244line2to/the,R405line1the/North. Each exception binds ID,source,logical English,compiled bytes,line,next/last words,original issue andreason. No diagnostic is removed or global weak rule relaxed. The rejected alternative Head west to the New World, or solve needs36text cells plusphase/continuation protection,38against36available. Keep c's complete-word to/the boundary;do not drop words,weaken guards oradd a fifth row merely to force that alternative. Preserve the broader weak-before-row,page-boundary-before-readability andphrase-coherence retrospective leads.

Research-only reconstruction is work/analysis/Rafael_B49_relocation_v8096/SC0_B49_RESEARCH_ONLY.DK4. Original3976stored/3974logical/tail2 becomes3792stored/logical/tail0. All61 complete preambles,154commands,56nested spans,13raw predicates,query41,sevenA000effects,C281,all37nonrelative controls andthe full four-byte end at3788 remain. All280 relocated relative cases andcomplete clean/predecessor block/whole predecessor archive inverses pass;342otherSC0blocks are exact. Stored validation has31parity tails/124fresh alignments and30exact bodies/120reused;all61planes equal viewed pages with no extra orblank page. All61 final actor/voice/body dispatches,14relocated predicates/queries with scratch restoration,and25seeded normal ends pass. Full effects andC281 actual transitions are not yet claimed.

The first C281 probe incorrectly used the predicate handler andfailed with an unmapped read;preserve that producer. The correct structural decoder binds its exact81c2 bytes/two-byte extent under clean/current code with opaque callees explicitly bridged. Do not treat it asC200,remove it orclaim full effect execution. A separate immutable note records B48's stale all15/zero-macros relocation root-label wording: authoritative arrays andindependent production prove91records/oneFI. Preserve the frozen original andretain this diagnostic lead for the later older-record technical re-audit;do not replay orre-credit B48. No new emulator run,ROM,full-reference loader/caller proof,actual scene audit,frozen policy,atomic stage orregistered release exists forB49 yet. All sessions are terminal/reaped. Preserve every ROM,translation,draft,failure,executed producer andproof;full goal active."""
NEXT="""Continue from verified V8101/current registered V8066. Use translations/rafael_B49_editorial_manuscript_v2.json andspeaker_name_review_v2.json. Final plan is8090c,not a/b/d;final native proof8092 binds20fresh/224reused cases. Source/name proof8093,viewed review8095,research relocation8096,stored8097 andfinal controls8098 pass. Reuse all verified source/context/identity/branch/current/effective/prose/logical/native/stored/inverse checks unless a concrete change orrisk justifies a repeat. All61formatting gates stayfalse pending actual/reference/release.

Build andpin a full isolated research reference fromV8066 plus the exact reviewedSC0archive. Prove342otherblocks andeveryotherfile/component exact,all343native load/cache paths/686parent modes,the154command maps/56relative operands,originalEV0entry8 andshipped callers. Use own-current Rafael input work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json. Preserve the complete154-command B49 exchange after all original B44initialization in paired disclosed Japanese/English entry fixtures,includingC281,all37nonrelative controls/sevenA000effects,branches,query41 andfullend. Do not flatten branches,omit effects orforceRAM/party/roles/roster/funds/seed/conditions/results. Choose an adequate ordinary input/capture horizon for44-59speeches plus initialization/transitions;the opening50composition is not yet observed. Focus onC281's transition into the confrontation,Lil/Camille portraits andcomplete headers,trade-house/region shifts,normalreturn andconcrete risks. All61paragraphs are single-page in both source/native proofs;no invented page-turn test is needed. Conditional Janus/Julio/Arcadius/regional/alternate destination content may remain explicitly native-only unless a distinct display orconcrete risk warrants another scene.

Measure complete source/English glyph masks,names,selected commandresults/UIrequests andnormalvaluecarry. Preserve timing,RNG,later components/calendar/RGB differences andcausal/future-state limits without retiming inputs to hide them. Only then approve formatting,freeze exact source-bound policy/three narrow warning scopes,complete meaningful independent atomic challenges,register after the completeV8066stack andbuild via build_integrated_release.py. Verify full-reference equality,clean-input patch andown-current startup. Expected manifest638from637,accepted114/mainV4701unchanged. Credit61/31revisions/30retentions onceonly after checks:projected7143completed/7146source-prose-drafts/4442revisions/2701retentions,SC0 340,route5543. Those are not currentcounts.

Keep the full objective across allfour storylines,earlier translations,sharedshop/town/random/Help/remainingprose,all207names/roles/aliases andretrospective prematurewrapping. Preserve allpriorunfinishedinventories,twelvecontraction/question-tagleads,unscannedrecords beyond558plans,the inherited planner leads andall older item/counterpart/display leads. Keep Pasar distinct from Pasha without global replacement;retain Cristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159 versus Retainer consumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andevery other recorded lead. Keep graphics/all18plaques andlater older-record technical re-audit separate,includingnormal-end valuecarry,source-onlyB35R65/B48R129nineteenth cells,the B48 stale relocation label andall measured timing/highlight/RNG/component/calendar/RGB/fixture-reentry limits. Preserve every artifact. No separate unified package,promotion,pruning,commit orpush;full goal stays active."""

GATES='''def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7082 and prior['manifest_batches']==637
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==61 and doc['revised']==31 and doc['retained']==30
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records'])==7 and all(r['native_name_plane_directly_viewed'] and not r['review']['formatting'] for r in names['records'])
    review=data['native_review'];assert review['manuscript_sha256']==sha(DOC.read_bytes()) and review['names_sha256']==sha(NAMES.read_bytes())
    assert review['native_page_count']==61 and len(review['all_original_infos'])==22 and len(review['narrow_warning_exceptions'])==3
    assert len(review['directly_viewed_sheets'])==12 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in review['directly_viewed_sheets'])
    assert data['final_native']['plan_sha256']==sha(Path(PROOFS['plan']).read_bytes())
    assert data['final_native']['fresh_compiled_alignment_cases']==20 and data['final_native']['reused_compiled_alignment_cases']==224
    assert data['relocation']['relocated_native_skip_cases']==280 and len(data['relocation']['groups'][0]['command_map'])==154
    assert data['relocation']['complete_clean_source_block_reconstructed_exactly'] and data['relocation']['all_full_predecessor_archive_bytes_reconstructed_exactly']
    assert data['stored']['fresh_native_alignment_cases']==124 and data['stored']['exact_reused_native_alignment_cases']==120
    assert len(data['final_controls']['final_dispatches'])==61 and len(data['final_controls']['relocated_predicates_andqueries'])==14 and len(data['final_controls']['normal_seeded_ends'])==25
    assert data['paths']['distinct_text_path_count']==256 and data['paths']['structural_compositions_evaluated']==156250
    return prior,data
'''
if __name__=='__main__':
    source=Path('scripts/checkpoint_Rafael_B48_native_stored_v8044.py').read_text(encoding='utf8')
    a=source.index('PROOFS=dict(');b=source.index('\ndef restore(',a)
    c=source.index('def gates():');d=source.index("if __name__=='__main__':",c)
    changes={
        source[a:b]:'PROOFS='+repr(PROOFS)+'\nSUMMARY='+repr(SUMMARY)+'\nNEXT='+repr(NEXT)+'\n',source[c:d]:GATES,
        'from scripts.complete_Rafael_B47_v8018 import COUNTERS,AFTER':'from scripts.complete_Rafael_B48_v8071d import COUNTERS,AFTER',
        'from scripts.checkpoint_Rafael_B48_prose_v8033 import PROOFS as PRIOR_PROOFS\n':'',
        'B48':'B49','v8044':'v8100','v8045':'v8101','V8044':'V8100','V8045':'V8101',
        'editorial_handoff_verification_v8034':'editorial_handoff_verification_v8072',
        'rafael_B48_editorial_manuscript_v3':'rafael_B49_editorial_manuscript_v2',
        "OLD_KEY='Rafael_SC0B48_source_context_prose_logical_pending_layout_release_v8033'":"OLD_KEY='Rafael_SC0B49_source_gloss_pending_controls_current_andrelease_v8071'",
        "status='91-source-context-prose-native-stored-approved":"status='61-source-context-prose-native-stored-approved",
        "block=48,objects=91,revisions=42,retentions=49":"block=49,objects=61,revisions=31,retentions=30",
        'all91_final_formatting_gates_false=True,native_pages=92,source_commands=163,relative_sites=28,relocated_cases=140':'all61_final_formatting_gates_false=True,native_pages=61,source_commands=154,relative_sites=56,relocated_cases=280',
        'viewed_final_sheets=17':'viewed_final_sheets=12','original_QA_infos=37,exact_warning_exceptions=2':'original_QA_infos=22,exact_warning_exceptions=3',
        'stored_fresh_alignment_cases=192,stored_exact_reused_alignment_cases=172':'stored_fresh_alignment_cases=124,stored_exact_reused_alignment_cases=120',
        'B48_native_pages=92,B48_names_native_planes=9,B48_final_viewed_sheets=17':'B49_native_pages=61,B49_names_native_planes=7,B49_final_viewed_sheets=12',
        'B48_stored_fresh_alignment_cases=192,B48_stored_exact_reused_alignment_cases=172':'B49_stored_fresh_alignment_cases=124,B49_stored_exact_reused_alignment_cases=120',
        'B48_all163_commands28_relative_sites140_cases_full_inverses_pass':'B49_all154_commands56_relative_sites280_cases_full_inverses_pass',
        'V8013':'V8066','currentV8013':'currentV8066',
        '6991completed;B48 91decisions/92pages/nine names/stored controls':'7082completed;B49 61decisions/61pages/seven names/stored controls',
    }
    absent=[key for key in changes if key not in source];assert not absent,absent
    print(derive('scripts/checkpoint_Rafael_B48_native_stored_v8044.py','scripts/checkpoint_Rafael_B49_native_stored_v8100.py',changes))
