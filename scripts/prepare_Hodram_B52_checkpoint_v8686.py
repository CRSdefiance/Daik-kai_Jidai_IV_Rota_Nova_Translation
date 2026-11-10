"""Checkpoint all independent B52 production readers and explicit source-context correction."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    source_path=Path('scripts/checkpoint_Hodram_B52_v8674.py');source=source_path.read_text(encoding='utf-8')
    nodes={n.targets[0].id:n for n in ast.parse(source).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    proofs=ast.literal_eval(nodes['PROOFS'].value)
    proofs.update(production_references='work/analysis/Hodram_B52_references_production_v8677/references_production_validation.json',
        production_controls='work/analysis/Hodram_B52_controls_production_v8679b/control_production_validation.json',
        production_loaders='work/analysis/Hodram_B52_loaders_production_v8681/loader_production_validation.json',
        production_actual='work/analysis/Hodram_B52_actual_production_v8683/actual_production_validation.json',
        production_comparison='work/analysis/Hodram_B52_comparison_production_v8685/comparison_production_validation.json')
    summary=ast.literal_eval(nodes['SUMMARY'].value)
    summary=summary.replace('Remaining required work:source-bound production control-flow/loaders-census/references/actual/comparison readers andtheir meaningfulnegativecases;', 'The source-bound production control-flow/loaders-census/references/actual/comparison readers andtheir meaningfulnegativecases are now complete as qualified below. Remaining required work:')
    summary+='''

Independent production references8676/8677 now bind all five disjoint clean/current/final speech/typed-choice references and all14 independently parsed commands. The complete target archive/whole NDS match the reviewed reference; all324 unowned blocks/every other file/component and complete clean/current/block/archive/whole in-memory ROM inverses pass. Twenty actual changed reference/final-byte cases reject before mutation. This is offline evidence, not new gameplay or completion credit.

Source-context correction: original source-controls8620 actually used the own registeredV8543/captain1 input, notV8609. Original proofs and every earlier statement remain preserved as history; this explicit qualification supersedes any earlier assertion that8620 itself usedV8609. Stopped productioncontrolsV1/runner8679 caught the descriptor mismatch before native execution; it was not bypassed. Qualified helper hodram_B52_context_qualification_v1 and controlsV2/successor8679b retain distinct original input/report/snapshot hashes and verify full ARM9/COMMON/font/EV1 and complete actor tables equal acrossV8543/V8609. Full RAM snapshots differ:source f9cb82c64ce597d3c886c66a0280667b03f35b5b41f0c74430c6c16894838a8b versuscurrent f3a1ff71fca4a2707004d07befd628252586df255e2066e4adfdfc4f42fee6a8; both actor tables hash e6a9465ab883d1a8ddea20db4e2c95c26812ca3d41c7b5c1caf56f88ae149872. No historical RAM is transplanted or overlaid. Fresh ownV8609 native execution then matches all three source event getters,three stored dispatches,20 branch cases,four paired opaque structural decodes and50 distinct seeded ends/all six return words/ABI/unowned4MiB/canaries. The original50 caller kind2-forward/kind3-carry cases are explicitly reused through exact immutable artifact/script/complete current-clean instruction span and all recorded six-word guards, not replayed. Nine genuinely changed source/branch/end/sixth-word/caller/voice/query/opaque-evidence cases reject. OriginalcontrolsV1 andstopped runner remain;V2 is authoritative.

Productionloaders8681 binds the already completed325 whole native loads/cache hits,650 initial parent modes and326 original EV1 actions,including null action/full payloads/payload-plus8/cache-neighbor/SP/PC/ABI. All source/current/final command,speech andtyped references andevent52requires30/excludes74 are checked. Every shipped decoded section/overlay name/base/length/payload hash equals the immutable prior census input;the existing complete census is reused,notrescanned. Seven changed count/mode/offset/prerequisite/activation-scope/census-unit/typed-reference cases reject. No new native loader producer or gameplay capture.

Productionactual8682/8683 reconstructs both complete initialized opening fixtures independently:8 original initializer commands34bytes thenall14 original B52 commands/3speeches/4relatives/2labels/2distinctends atconstant34byte shift. Full fixture archives/everyotherfile/component/wholeparent-ROMinverses pass. The six existing immutable run plans,coldboot reports,ordinary unretimed inputs,readonly callbacks,whole resident scripts/instruction pointers,source/English selectedcommandtraces,bothchoice results,normal/flaggedends,unvisited opposite-response lists andfollowingcommands are independently read. All138complete body/name holds/12page occurrences/50,406frames pass exact source-qualified glyph/name masks andwholePNG identities;all3unique speeches are covered. Native display model planes are reused only by their frozen hashes and completed independent nativeproduction8667 proof,notrerendered. Seven actual fixture/body/name/end/scope/metadata defects reject. Existing initialized-fixture/naturalactivation/location/earnedprogress/livebacking/cancel/fullroute/hardware limits remain;no new capture.

Productioncomparison8684/8685 independently recomputes all199later wholeRGBpairs:93longwithdrawal/93longopposition/13focusedwithdrawal. Original paired commandtimings/menudurations/boundaryRNG/UIrequests/completeportrait-header comparisons/three final native component queries/wholeactors/captain1/rawcalendar/PRNG/returns/followingcommands all match the retained evidence. BoundaryRNG differences after the menu exist and remain:withdrawal source offsets68/104/112/164/166;opposition68/104/108/174/178/200/208/216/224;focusedwithdrawal the same five aslongwithdrawal. Longwithdrawal unequal finalcomponents/actors/calendar/PRNG/46RGBdifferences,opposition matching components/actors butunequalPRNG/13RGBdifferences,andfocused matching finalcomponents/actors/seed/calendar/all13RGBpairs remain distinct. Six deliberately changed timing/equality/RGB/seed/sampling claims reject. No harmlessness,causality,everyframe orfutureequivalence inference is added.

All source-qualified editorial/compiler/native/stored/menu/reconstruction/reference/control/loader/actual/comparison production readers now pass their necessary checks. Across policy243,reconstruction26,native10,menu12,references20,controls9,loaders7,actual7,comparison6 there are340 genuinely changed-input rejections;these are technical checks,not340 new prose decisions. Latest B52 manuscriptv6/namesv4/contractv1 still containsfive uncredited decisions,two revisions/three justified retentions. RegisteredV8609/mainV4701/canonical baseline andallcompletion counters remainunchanged. No jobsremainlive. AtomicwholeNDSintegration,buildercompatibility/registeredcumulativebuild/exactcleanpatch/ownstartup andonce-onlyfivecredit remainpending. Full editorial goalactive.'''
    old_next=ast.literal_eval(nodes['NEXT'].value)
    tail=old_next[old_next.index('Fullcopiedunfinishedinventoryremainsauthoritative:'):]
    next_text='''Continue from verifiedV8687/current registeredV8609. B52 allfive individual gates/manuscriptv6/namesv4/contractv1 andall independent production readers nowpass:policy243/reconstruction26/native10/menu12/references20/controls9/loaders7/actual7/comparison6 changed-input rejections. Reuse these completed proofs andall six terminal/reaped scene runs;do not rerun unchanged native/display/capture/reader tests. Sourcecontrols8620 usedV8543,explicitly qualified bycontext helper andcontrolsV2/8679b against full unchanged code/COMMON/font/EV1/actors andfresh ownV8609 consumer execution;wholeRAMsnapshotsdiffer andnohistoricaloverlayisused. OriginalfailedcontrolsV1/8679 andallolderfailures/producers/drafts remain. Latest controls module dk4tool/patch/hodram_B52_controls_v2.py is authoritative. No B52credit,registrylayerornewROM yet.

Next prepare the source-qualified atomic B52 stage and release configuration,sealing all471frozen compiler/native dependencies plus every independent production reader/evidence dependency and explicit complete registeredV8609 ancestry. Validate both direct-current and canonical.source/full-current.rom lifecycles with exactly one whole NDS-object commit after all guards;genuinely wrong-memory/changed-semantic cases must reject with zero mutation. Final plannedROM must byte-match the pinned reviewed B52 reference and complete whole-parent inverse;all324unownedblocks/files/components/12byteAdernkatz-plus8byteBlades/font/full123264payload remain.

For sole-builder integration inspect/reuse supported hooks. Existing late_story_editorial_release is fixed/equal-allocation andrunsbeforelateB51;it cannotapply B52's228to236 relocation aftercompleteV8609. A reusable late editorial extension may avoid new per-block builder namespaces in future. Any shared hook must be source-locked,ordered aftercompleteB51 beforefinalguards,andretain the complete originalbuilderinverse. If adding compatibility namespaces for frozen outcomes/B49/B50/B51,derive successors without editing executed originalmodules/configs,retain every originaldependency entry/hash and originalformat/body checks,andprove the full currentV8609 prefix reproduces byte-for-byte. Do not substitute current mutablebuilderhashes for frozenoriginalguards orsilentlybypassdependencychecks. Originalprofiles/ROMs/earliertranslations remainpreserved.

Thenregister the cumulative experimental profile through sole scripts/build_integrated_release.py,auditcomplete accepted stack/manifest/unchangedfiles/nativecontrols,verifyexactclean-inputpatchreconstruction andownordinarycoldboot/startup/context. Reusecompleted actual B52 scenes withtheir honest limits ratherthanrepeatallconditions orfullroutes. Credit exactlyfive reviewedsource decisions onceonly afternecessarychecks. No mainpromotion,separate requestedpackage,pruning,commitorpush. UseownV8609captain1context scripts/Hodram_B51_registered_route_context_v8612.py;nohistoricalRAMoverlay/captain2.

'''+tail
    changes={
        ast.get_source_segment(source,nodes['PROOFS']):'PROOFS = '+repr(proofs),
        ast.get_source_segment(source,nodes['SUMMARY']):'SUMMARY = '+repr(summary),
        ast.get_source_segment(source,nodes['NEXT']):'NEXT = '+repr(next_text),
        'checkpoint_v8674':'checkpoint_v8686','verification_v8675':'verification_v8687',
        'verification_v8671/verified_handoff.json':'verification_v8675/verified_handoff.json',
        'review_pending_integration_v8674':'review_pending_integration_v8686',
        'unfinished_editorial_scope_v8674':'unfinished_editorial_scope_v8686',
        'return prior,data':"""assert [data[k]['negative_count'] for k in ['production_references','production_controls','production_loaders','production_actual','production_comparison']]==[20,9,7,7,6]
    qualified=data['production_controls']['summary']['source_context_qualification']
    assert qualified['original_source_context_is_V8543_not_V8609'] and qualified['complete_ARM9_COMMON_font_EV1_andwhole_actors_equal'] and qualified['whole_RAM_snapshots_equal'] is False and qualified['no_historical_RAM_overlay_orcode_patch']
    assert data['production_actual']['summary']['whole_actual_frames']==50406 and data['production_actual']['summary']['complete_actual_holds']==138
    assert data['production_comparison']['summary']['later_full_RGB_pairs_recomputed']==199
    assert data['production_loaders']['summary']['complete_original_shipped_code_census_reused_by_every_decoded_unit_identity']
    for key in ['production_references','production_controls','production_loaders','production_actual','production_comparison']:
        for path,digest in data[key]['evidence'].items():assert sha(Path(path).read_bytes())==digest
    return prior,data""",
        'remaining_production_readers_atomic_registered_release_andcredit_pending=True':'all_independent_production_readers_and340_changedinput_rejections_verified=True,atomic_registered_release_andcredit_pending=True',
        'V8674':'V8686','V8675':'V8687',
        'B52 five format gates and frozen policy pass; production and registered integration pending':'B52 all independent production readers pass; atomic and registered integration pending',
    }
    root=Path('work/analysis/Hodram_B52_checkpoint_tools_v8686');assert not root.exists()
    receipt=derive(source_path,'scripts/checkpoint_Hodram_B52_v8686.py',changes)
    root.mkdir(parents=True);save(root/'derivation.json',receipt)
