"""Publish the registered516 completion checkpoint and preserve the uncredited351 successor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


def main():
    root = Path('work/analysis/Rafael516_resume_release_verified_v2_20261105')
    release_path = root / 'registered_release_verification.json'
    release = load(release_path)
    credit = load(root / 'completion_checkpoint.json')
    assert credit['new_credit'] == 516 and credit['counts']['completed'] == 12361
    assert sha(release_path.read_bytes()) == credit['registered_release_sha256']
    summary = (
        'Rafael early story and all tutorials remain first. The prior 516 reviews are now registered, fully verified '
        'and credited once: 246 revisions/270 retentions. Candidate a51c79e4 has 680 manifest entries, all114 accepted '
        'layers/eight final stages, 26 passing release checks and an exactly reconstructable clean-input patch. '
        'The new explicit checkpoint workflow reused the completed canonical build and ran every original final-stage '
        'body/guard in129.9 seconds; ten bad-input cases were rejected. Exact same-identity4001-frame startup evidence '
        'binds captain0/route0 andboth Fernan getters; no new startup emulator run is claimed. Integrated totals are '
        '12361 =7082 revisions+5279 retentions. The next351 reviews remain five-gate research-ready and uncredited; '
        'the combined867 target remains3bf32397 research only. Next integrate351 after verified516. Main3cb8 unchanged; '
        'all ROMs, earlier work and full scope preserved. Two catalogue de corrections, global names, deferred artwork '
        'and later older-record re-audit remain open. No guide photos or promotion.'
    )
    document = '''# Registered Rafael516 integration checkpoint — November 5, 2026

Rafael's early story and all tutorials remain the first priority. Every other storyline, unfinished earlier contextual review, shared town/shop exchange, random scene, speaker label, wrap/glyph defect and remaining player-facing prose stays in scope. Preserve all translations, ROMs and evidence. No guide photos or main promotion.

## Registered and credited

The two reviewed batches B85–B100 and B101–B120 are now integrated once: **516 records = 246 revisions + 270 justified retentions**. `translations/rafael516_integrated_final_review_v2.json` preserves their exact source/current references, individual findings, all five gates and rebound final stored references. Obsolete intake pending flags are cleared only in this integrated successor; every earlier manuscript and proof remains intact.

The experimental profile is **all-routes-rafael516-checkpoint-v2-20261105**. Its candidate is `out/all_routes_rafael516_checkpoint_v2_20261105_candidate.nds`, SHA-256 **a51c79e4a3581fb49acb0c76de1d5093cb20aad3033bd670e56652575a71fe8f**. The neighboring manifest and xdelta patch are required artifacts. The candidate is byte-identical to the reviewed research target. Only the 29 owned SC0 blocks differ from verified678; every other file/component, accepted graphics, current names, font and registered runtime remains exact. The registered ASCII right-bound correction is preserved.

`work/analysis/Rafael516_resume_release_verified_v2_20261105/registered_release_verification.json` verifies **680 manifest entries, all 114 accepted layers, eight final stages and all 26 release checks**, all exact final record bindings and the clean-input patch. Applying the patch to clean SHA-256 **f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d** reconstructs the complete candidate exactly. Baseline invariants pass. `completion_checkpoint.json` and its compressed ledger backup prove once-only credit and unchanged earlier ledger prefixes/unrelated fields.

## Explicit canonical checkpoint reuse

The original failed516 build and frozen contract are preserved. Its completed canonical stage was correct; only a path separator at entry670 prevented the final stages. A separate experimental profile registers the qualified versioned contract and exact checkpoint continuation. All previous profiles, accepted layers, original drivers, original stage bodies and their native/parent/target/inverse guards remain intact.

`scripts/registered_canonical_checkpoint_resume_v1.py` qualifies the original ROM, manifest, terminal receipt, registry ancestry and dependency hashes. Ten negative cases reject a wrong ROM, source profile, missing registration, changed accepted layer or prior profile, changed final stage, reordered extensions, wrong manifest/contract and changed dependency digest. The manifest explicitly preserves original profile/registry/ROM/manifest/terminal provenance; it does not claim a new canonical-builder run.

All eight stages then executed successfully in **129.9 seconds**. Build terminal: `work/analysis/Rafael516_registered_resume_build_v2_20261105/completion.json`. Registration/negative-case proof: `work/analysis/Rafael516_registered_resume_v2_20261105/checkpoint_qualification.json`. New workflow instructions are appended to AGENTS and the build continuity protocol. No frozen driver, core or earlier profile was edited.

## Startup and honest observation scope

The existing `work/analysis/Rafael516_identity_coldboot_20261105/capture_report.json` booted these exact candidate bytes for4001 frames with ordinary New Game inputs and no savestate or RAM override. The registered verifier reuses that same-identity capture and all ten exact reviewed RGB pairs, verifies the complete staged payload and current runtime resources, then reads **captain0/route0** from its own snapshot. Both original actor35 getters return **Fernan Silveira** with the normal ASCII F from that snapshot. No new startup emulator run or full-catalogue UI visit is claimed.

See `own_registered_startup_verification.json` and `own_Fernan_name_getter_verification.json` beside the release verifier. Their collector terminal receipts pass with unchanged locked sources and no collector errors.

The integrated batch has498 speech variants/504 pages and18 captions. Its earlier disclosed initialized fixtures observed118 source variants/121 pages;380 variants remain offline-only. This is representative targeted emulator evidence, not original conditional scene activation, earned chronology, all source locations, a complete route or hardware testing. Per-batch menu/cursor/return observation limits remain in the release record.

## Next work and preserved scope

The next **351 B121–B140 reviews** remain research-ready:201 revisions/150 retentions, all five research gates,344 viewed/native body pages,10 captions,22 scoped public names, stored/catalogue/loader checks and132 observed variants/134 pages. No new351 credit was granted. Continue from `docs/editorial_Rafael351_research_ready_20261105.md` and the metadata-aligned v2 manuscripts. Its combined867 research ROM remains **3bf3239736982e6398eda1f837f4c249b93e541128985013fbde02466bcbaa9c**; preserve it and the47-block/three-inverse proof.

Next qualify the351 owned transaction on the now verified516 predecessor and integrate it through a registered continuation with exact final manifests, patch and startup bindings. Reuse compatible source, prose, native, visual and actual evidence. Do not repeat the completed102-minute canonical prefix unnecessarily. The867 scope must eventually credit only the remaining351, since516 is already credited.

The two catalogue particles remain **Dinis デ Albuquerque → Dinis de Albuquerque** and **Garcia デ Oviedo → Garcia de Oviedo**. They need their own qualified pointer-field owner and are not part of actor35's Fernan-only stage. Public progressive names are already correct; global207-name/full-catalogue UI review remains open. Deferred graphics artwork and the later older-record technical re-audit remain separate.

Integrated totals are **12361 = 7082 revisions + 5279 retentions**. Historical source/prose counts are12364. Main SHA-256 **3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe** and verified678/cc71ec06 remain unchanged. The full goal remains active.
'''
    registry_path = 'translations/release_stack.json'
    protected = {
        registry_path: release['registry_sha256'],
        'dk4tool/rom/nds.py': '27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        release['candidate']: release['candidate_sha256'],
        'out/all_routes_combined_help97_rafael330_20261105_candidate.nds': 'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448',
    }
    checkpoint(mutation='work/analysis/Rafael516_integrated_documentation_checkpoint_v2_20261105',
        batch_key='Rafael_SC0_B121_B140_clean_20261105',
        batch_updates=dict(new_credit=0, registered_integration_pending=True,
            next_registered_predecessor=release['candidate'], next_registered_predecessor_sha256=release['candidate_sha256']),
        additional_updates={
            'editorial_execution_priority_20261104': dict(new_credit=0,
                current_batch='Rafael351 B121–B140 research-ready; append to verified516',
                registered_build_live=False, registered_build_failed=False, registered_integration_pending=True,
                previous516_registered_verified_andcredited_once=True, next_action='Qualify/register351 successor after verified516; preserve completed prefix andall display evidence.',
                guide_photos=False),
            'Rafael867_qualified_cumulative_research_20261105': dict(new_credit=0,
                prior516_now_registered_verified_andcredited_once=True, remaining_new_source_credit=351,
                registered_integration_andclean_input_patch_pending=True)},
        summary=summary, document='docs/editorial_Rafael516_registered_checkpoint_v2_20261105.md',
        document_text=document, completed=12361, protected=protected)
    print('Published integrated516 checkpoint;351 remains research-ready/uncredited. All protected artifacts/main preserved;goal active.')


if __name__ == '__main__':
    main()
