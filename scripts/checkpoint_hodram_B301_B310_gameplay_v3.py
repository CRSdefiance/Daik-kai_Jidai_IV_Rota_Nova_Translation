"""Preserve viewed gameplay and the narrow unresolved QA return risk without credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.prepare_hodram_B301_B310_formatting_v1 import ROOT,PROSE
from scripts.build_registered_hodram_B281_B300_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

def main():
    display=ROOT/'gameplay_display_review_v1.json';reuse=ROOT/'exit_trial_visual_reuse_v2.json'
    actual=ROOT/'actual_transition_pixels_v3/focused_actual_pixels.json'
    compact=ROOT/'actual_transition_sheets_v3/receipt.json'
    lead=ROOT/'fixture_terminal_operand_lead_v3.json'
    d,r,a,s=map(load,[display,reuse,actual,compact])
    assert d['all97_pages_directly_viewed'] and d['all4_menu_samples_directly_viewed']
    assert r['all_captured_full_frame_PNG_hashes_exact'] and r['both_long_runs_still_fault_after_last_page']
    assert (a['frames'],a['selected_utterances'],a['selected_pages'],a['complete_body_planes'],a['complete_header_planes'])==(5921,3,4,16,16)
    assert a['all_selected_pages_observed_in_exact_fixture_order'] and a['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert len(s['bottom_screen_sheets'])==1 and s['actual_dialogue_pages']==4
    assert all(digest(v['path'])==v['sha256'] for v in s['bottom_screen_sheets'])
    prose=load(PROSE);assert prose['counts']==dict(revision=127,retention=107) and len(prose['records'])==234
    assert all(v['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for v in prose['records'])
    release,package=map(load,[RELEASE,PACKAGE])
    summary=('Hodram B301–B310 retains234 contextual decisions and228 passing offline/stored pages. '
        'Representative gameplay displays96 utterances/97 pages and all four menus; every page is viewed. '
        'A separate three-utterance/four-page test successfully returns from Mihwas two-page offer to Hodram and the following resupply dialogue. '
        'The long QA sequence still faults at its ending; cleanup alone did not fix it. Resolve this narrow QA exit risk before fifth-gate sealing/integration. '
        'Integrated coverage remains18,133; main is unchanged.')
    evidence={str(p):digest(p) for p in [PROSE,display,reuse,actual,compact,lead,
        ROOT/'final_visual_approval_v6.json',ROOT/'stored_v1/stored_native_verification.json',
        ROOT/'focused_run_v1/terminal.json',ROOT/'focused_run_exit_v2/terminal.json',ROOT/'focused_transition_run_v3/terminal.json',
        ROOT/'focused_transition_capture_v3/frame_005921_final.png',ROOT/'lossless_space_recovery_v1.json',Path(__file__)]}
    document=f'''# Hodram B301–B310: gameplay display and return-risk checkpoint

{summary}

Reuse the [offline/stored checkpoint](editorial_Hodram_B301_B310_stored_20261107.md) for all234 exact source/current decisions, eight scoped names, terms,225 bodies/228 final pages,18 layout revisions, one justified layout retention, one FE split-word repair, one glyph correction, nine captions,190 branch cases,225 catalogue lookups and325 archive loads. Those checks pass and need no repetition. The contextual manuscript still has127 revisions/107 retentions and all234 fifth gates false. No integrated credit is added.

The [viewed display receipt](../{display.as_posix()}) covers one29,201-frame initialized sequence: all73 ordinary speeches and23 complete style commands at original startup assignments,96 utterances/97 pages,213 exact body holds and197 exact header holds. All97 pages were directly viewed on nine readable bottom-screen sheets. All four menu occurrences match their exact source keys, complete native caption/blank/highlight pixels and default option0, and their sheet was directly viewed. All eight FE notices, captain FI injury, Senior Monk/Mihwa headers, Kinkaku-ji, wolf treatment, revised departure wording and the two-page offer are observed. Another129 physical voice alternatives remain offline-only. Nondefault/cancel choices, original optional activation, branches, rewards, party assignments, full catalogue UI and hardware remain unvisited.

The first long sequence logs ARM9 Undefined instruction0x8D0008E5 at PC0x01FF9964 after the last page; its final screen remains on the offer. The next fixture adds the clean/registered B42 host's identical00c2 cleanup before00000000, without changing any of the100 copied dialogue/menu commands,96 bindings, initializers, controls or97-page expectations. It reproduces the fault. [Exact image reuse](../{reuse.as_posix()}) proves every captured full-frame PNG and all17 alternate review sheets identical between these two runs. The cleanup omission is established, but it alone is not a fix; crash cause and harmlessness are not established. Neither run approves the final return transition.

The [short focused test](../{actual.as_posix()}) has three utterances/four pages over5,921 frames: Mihwa B310 R13, both pages of R16, then Hodram B301 R21, with the clean/registered host cleanup. All16 body holds/16 headers pass. The single four-page sheet and [final screen](../work/Hodram_B301_B310_clean_20261107/focused_transition_capture_v3/frame_005921_final.png) were directly viewed; the latter shows the following Manuel resupply conversation. Native terminal output has no undefined-instruction message for this run. This proves the isolated two-page passage can return to the next speech and following native dialogue; it does not explain or excuse the long-sequence fault. These are three initialized QA runs/64,323 total frames, not three new sets of unique dialogue coverage.

A [source-bound exit-operand lead](../{lead.as_posix()}) compares the current B31000000000 terminal (native result0) with the clean/registered B30000000080 terminal (native result1) used by the earlier successful long B281–B300 fixture. Next qualify the QA interpreter exit contract and, if appropriate, test that already-proven end-action operand only in a new disclosed fixture. Preserve all production scene controls and every prior ROM/evidence file. Do not repeat editorial work, name/term review or unchanged display/storage checks. Do not seal fifth gates or register the batch until the concrete return risk is resolved or properly bounded by source/runtime evidence.

No test/build process remains live. Forty-six preserved research ROMs received lossless in-place NTFS compression; every before/after SHA-256 matches, with no moves/deletions. This recovered about1.01GB at the recorded moment. Main, registered B281–B300, clean/canonical inputs,114 accepted layers, ASCII right bounds and the weekend package remain unchanged. Integrated totals stay18,133 (11,009 revisions/7,124 retentions); historical source/prose/draft totals stay18,136. The full editorial goal remains active with Rafael/tutorial priority, every route/shared/town/random/player text and earlier unfinished contextual pass in scope. Graphics artwork and the later older-record technical re-audit remain separate. No guide photos.
'''
    checkpoint(mutation=ROOT/'gameplay_checkpoint_v3',batch_key='Hodram_B301_B310_clean_next_20261107',
        batch_updates=dict(new_credit=0,current_story_gameplay_utterances=96,current_story_gameplay_pages=97,
            actual_body_andmenu_visual_review_complete=True,all4_menus_pixel_checked=True,all8_FE_panels_observed=True,
            isolated_Mihwa_two_page_return_pass=True,focused_initialized_runs=3,focused_total_frames=64323,
            long_QA_return_risk_unresolved=True,cleanup_only_trial_did_not_resolve_fault=True,
            representative_gameplay_pending=True,registered_integration_pending=True,all_five_review_gates_pending=True,
            all_formatting_gates_pending=True,native_job_live=False,registered_build_live=False,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B301–B310:234 contextual decisions,228 stored pages,97 viewed live pages/four menus; isolated Mihwa return passes, long QA exit risk remains.',
            next_action='Qualify and test source-bound QA exit operand lead; preserve complete production controls and reuse finished editorial/display/storage proofs. Then seal234 fifth gates and register cumulative successor.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B301_B310_gameplay_risk_20261107.md',document_text=document,completed=18133,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved97 viewed gameplay pages and4 menus, successful isolated return and exact unresolved long QA risk. No credit or promotion; goal active.')

if __name__=='__main__':main()
