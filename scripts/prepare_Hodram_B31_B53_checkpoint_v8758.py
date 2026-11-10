"""Preserve the exact prior checkpoint while recording frozen/production progress."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_checkpoint_tools_v8758');assert not root.exists()
    source=Path('scripts/checkpoint_Hodram_B31_B53_v8746.py').read_text('utf-8')
    a=source.index('from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS as ACTUAL_PROOFS');z=source.index('\ndef inverse(',a)
    defs='''from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS as ACTUAL_PROOFS
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import validate_approved_batch
from dk4tool.dialogue.hodram_B31_B53_names_v1 import validate_scoped_names
PROOFS={**ACTUAL_PROOFS,
 'actual_review':'work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json',
 'formatting':'work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json',
 'manuscript':'translations/hodram_B31_B53_editorial_manuscript_v5.json',
 'names':'translations/hodram_B31_B53_speaker_name_review_v3.json',
 'metadata':'work/analysis/Hodram_B31_B53_metadata_v8748/explicit_route_binding.json',
 'frozen':'work/analysis/Hodram_B31_B53_policy_v8749/frozen_contract.json',
 'contract':'translations/hodram_B31_B53_native_contract_v1.json',
 'policy_validation':'work/analysis/Hodram_B31_B53_policy_validation_v8750/policy_validation.json',
 'production_reconstruction':'work/analysis/Hodram_B31_B53_reconstruction_validation_v8752/independent_reconstruction_validation.json',
 'production_native':'work/analysis/Hodram_B31_B53_native_validation_v8754/independent_native_validation.json',
 'production_references':'work/analysis/Hodram_B31_B53_reference_validation_v8756/independent_reference_validation.json',
 'production_controls':'work/analysis/Hodram_B31_B53_controls_validation_v8757/independent_controls_validation.json',
 'registered_release':'work/analysis/Hodram_B52_release_v8705/registered_release_verification.json',
 'registered_startup':'work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
}
SUMMARY="""The current verified experimental cumulative ROM is still V8704. Coverage remains 7,234 completed, 7,237 credited source/prose and drafts, 4,489 integrated revisions and 2,745 justified retentions. The three B31/B53 revisions have not been integrated or credited. B52 remains credited exactly once. Main V4701 and the canonical baseline are unchanged. Preserve every ROM, translation, draft, executed producer, proof and failure; no promotion, separate package, pruning, commit or push.

The full objective remains active: all four storylines and earlier translated dialogue, shared town/shop exchanges, random scenes, Help, remaining player-facing prose, all207 names/roles/aliases/custom names and retrospective premature breaks. The route subtotal5,634 is not the full-goal denominator; roughly20,000 remaining candidates is only a planning estimate. Every prior unfinished-scope key, value and lead is preserved. Graphics/all18 plaques and the later older-record technical re-audit remain separate.

Latest approved manuscript is translations/hodram_B31_B53_editorial_manuscript_v5.json; names remain v3. Metadata8748 adds explicit route1/Hodram/SC1/blocks31and53 to unchanged v4 rows. Every approved word, compiled/stored byte, source/current/final reference, individual reason and five gates is retained. B31 restores the speaker's own agency without naming the frightening man; B53 removes the invented bounty while retaining apparent wanted status and gruff caution. All three complete full216px pages use2/4/3 rows, zero QAissues, warnings or waivers, and no authored ordinary breaks or shortening.

Frozen contract8749 binds all approved batch keys, all three complete rows, two scoped name reviews, runtime, source/control/reference/native/actual evidence and734 immutable dependencies. It preserves the original full-width planner, base QA, font metrics, guards, pair phase and FI6/FA9/FO15 with zero source macros. The mutable integrated builder, registry, ledger and retention pins are deliberately excluded from accidental dependency pinning. All prior dependency entries and artifacts remain. Production modules are dk4tool/dialogue/hodram_B31_B53_{profile,layout,plan,names}_v1.py and dk4tool/patch/hodram_B31_B53_{reconstruction,native_guards,native_evidence,references,controls}_v1.py.

Policy8750 passes all three compiler positives, both scoped names and236 genuinely changed-input rejections. Production reconstruction8752 reproduces both independent blocks, the entire archive and whole reviewed ROM;51 changed control/reference/byte defects reject. Independent native8754 recomputes six complete Japanese/stored English pages and two current progressive name planes;12 semantic defects reject. Production references8756 independently parses all18 source/current/final commands, binds three disjoint canonical references and every inverse/unowned byte;20 defects reject without changing the original NDS object or its bytes. Native controls8757 independently executes three dispatches, four relative sites20cases, one unforced query, eight paired opaque structural decodes,50 normal-end cases,50 caller fragments and four EV1 getters;12 defects reject. These331 negative cases keep every frozen/trusted guard active and every protected file/ROM/registry/ledger unchanged.

The control reader uses the exact own-V8704 captain1 snapshot and original adapters. It reuses the already verified native glyph and whole-reference inputs by exact hashes rather than rerunning those stages. Normal ends preserve the existing parser-result second word independently of interpreter r3; the source's50 seeded cases and50 caller fragments preserve both channels. Keep the stopped8742 wrong-channel audit, qualified8742b reader, source-name8733 one-row failure and8733b19-glyph qualification, and formatting8745 receipt-path failure with8745b qualification. No original producer or artifact is rewritten.

Actual coverage is unchanged from8744: four terminal/reaped initialized whole-block cold boots,24,004 frames,76 complete body/name holds and four page occurrences. Long B31R0018 and B53R0007 are observed in both languages. Short B31R0013 remains offline-only; no original predicate or flag was forced to visit it. Source52->31->53 prerequisites do not establish a continuous conversation, original location, earned chronology, either B52 choice effect or the frightening man's identity. Opaque6311/6000/633F/623F/A000 are preserved without invented effect semantics.

B31 returns[0,1] at4016 in both languages; B53 returns[0,0] at4013 with separate interpreter mode1. Only the three documented decoded-length differences remain. Command duration, UI requests, boundary RNG and following commands match. All five sampled final components, whole actors, captain1, raw calendar and seed3325064553 match;68 later RGB pairs match through6001 frames. These remain bounded fixture observations, not natural activation, original eligibility/location, full catalogue UI, custom names, every-frame causality, broad future simulation, full-route or hardware proof. Source text fixtures use current English names/UI/code/font and eight original initializers34bytes. All earlier B52/B51/B50/B49/Gerhard/Rafael/Hodram/Lil limits remain intact.

Actor34 retention preserves the actual clean progressive/full-getter components and Fazul middle field; exact current mixed-width Ｆ storage remains. The source full getter's19th glyph wraps in the explicit216px literal test, with all characters complete. Actual progressive headers34/113 are verified; wider catalogue UI, all207 entries and wider Port Worker contexts remain open. Five existing research ROMs remain pinned; this turn creates no ROM or emulator capture.

Continue from verifiedV8759/currentV8704 without replaying completed source, prose, layout, native, independent reconstruction, name, actual or production checks. Remaining B31/B53 work: production loader/census, actual-scene and comparison evidence readers with meaningful changed-input tests; one whole-NDS atomic commit in both supported lifecycles and wrong-memory zero-commit checks; shared registered cumulative build, exact clean-input patch and own startup; then exactly three once-only completion decisions. Keep the full editorial objective and every previous artifact."""
NEXT='Finish B31/B53 production loader/census, actual andcomparison readers, then whole-NDS atomic validation/shared registered cumulative integration/exact clean-input patch/own startup andthree once-only credits. Latest immutable manuscriptv5/namesv3/contractv1;331 changed-input rejections pass. Keep actual shortB31 andfullcatalogue UI scope honest andall full-goal leads active.'
'''
    old="    assert data['formatting']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and data['formatting']['names_sha256']==sha(Path(PROOFS['names']).read_bytes())"
    new="""    assert data['metadata']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and data['metadata']['predecessor_sha256']==data['formatting']['manuscript_sha256']
    assert data['formatting']['names_sha256']==sha(Path(PROOFS['names']).read_bytes())
    validate_approved_batch(data['manuscript']);validate_scoped_names(data['names'])
    assert data['frozen']['contract_sha256']==sha(Path(PROOFS['contract']).read_bytes()) and data['frozen']['dependency_count']==734
    assert data['frozen']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())
    assert [data[k]['negative_count'] for k in ['policy_validation','production_reconstruction','production_native','production_references','production_controls']]==[236,51,12,20,12]
    assert data['production_native']['native_summary']['native_body_pages_recomputed']==6
    assert data['production_references']['positive_entire_archive_whole_reference_ROM_all323_unownedblocks_files_components_andallinverses']
    assert data['production_controls']['native_control_summary']['normal_seeded_ends']==50 and data['production_controls']['native_control_summary']['original_result_channel_cases']==50"""
    receipt=derive('scripts/checkpoint_Hodram_B31_B53_v8746.py','scripts/checkpoint_Hodram_B31_B53_v8758.py',{
        source[a:z]:defs,old:new,
        'Hodram_B31_B53_checkpoint_v8746':'Hodram_B31_B53_checkpoint_v8758','editorial_handoff_verification_v8747':'editorial_handoff_verification_v8759',
        'editorial_handoff_verification_v8731':'editorial_handoff_verification_v8747',
        'Hodram_SC1B31_B53_allfive_gates_actual_reviewed_pending_policy_atomic_andrelease_v8746':'Hodram_SC1B31_B53_frozen_policy_production_progress_pending_atomic_andrelease_v8758',
        'unfinished_editorial_scope_v8746':'unfinished_editorial_scope_v8758',
        "status='three-contextual-revisions-allfivegates-native-stored-independent-names-andactual-reviewed-frozen-policy-atomic-registered-pending'":"status='three-reviewed-revisions-frozen-policy-reconstruction-native-references-controls-pass-production-loaders-actual-comparison-atomic-registered-pending'",
        'latest_next_focus_v8746':'latest_next_focus_v8758',
        'prior_goal_turn_was_concrete_editorial_andnative_progress=True,current_turn_independent_names_actual_andformat_progress=True':'prior_goal_turn_was_concrete_independent_names_actual_andformat_progress=True,current_turn_frozen_policy_andindependent_production_progress=True',
        'V8746':'V8758','V8747':'V8759',
        'allfivegates, names andrepresentative actual verified;policy/atomic/release pending':'frozen policy and production native/reference/control checks pass;atomic/registered work remains',
        'new_credit=0,new_emulator_runs=4,new_actual_frames=24004,new_research_ROMs=5':'new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0,total_B31_B53_actual_runs=4,total_B31_B53_actual_frames=24004',
        'Hodram_B31_B53_actual_names_allfivegates_checkpoint=deepcopy(new[KEY])':'Hodram_B31_B53_frozen_policy_production_checkpoint=deepcopy(new[KEY])',
        'three contextual revisions/allfivegates/independent/names/actual complete;frozenpolicy/atomic/registered pending':'three approved revisions/frozenpolicy/production reconstruction-native-references-controls pass;remaining readers/atomic/registered pending',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        every_prior_ledger_value_scope_key_documentbyte_counter_candidate_registry_andprotected_ROM_guard_preserved=True,
        no_new_ROM_emulator_run_orcredit_this_turn_actual_totals_preserved_separately=True,
        full_editorial_objective_all_artifacts_graphics_andlater_olderrecord_reaudit_preserved=True,new_credit=0,full_goal_complete=False))
