"""Save the complete research gate before the registered cumulative integration."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT = Path('work/Maria_B0_B32_clean_20261109')


def main():
    ready_path = ROOT/'research_final_v1/research_completion.json'
    ready = load(ready_path)
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'],ready['revisions'],ready['retentions'],ready['body_pages']) == (301,178,123,303)
    for path, expected in ready['evidence'].items():assert digest(path) == expected
    actual_path = ROOT/'gameplay_review_v1.json'; actual = load(actual_path)
    assert (actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances']) == (92,96,207)
    assert actual['ordinary_default_menu_return_to_next_fixture_speech_observed']
    assert actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']
    release = load('work/hodram_residual_release_v1/registered_release_verification.json')
    summary = ('Maria301 research is complete: 178 dialogue revisions/123 retentions, 35 wrap improvements, '
        '303 checked pages and 36 scoped names pass five gates. Representative emulator QA observes '
        '92 utterances/96 pages, 14 headers, the menu/A return and resupply/sailing; 207 bodies remain offline-only. '
        'Registered cumulative integration, clean-input patch and candidate startup are next. '
        'Integrated coverage stays 19,161; registered f166991f and main remain unchanged.')
    text = '''# Maria301 complete research checkpoint — November 9, 2026

All 301 individual natural-dialogue-v2 research reviews now pass five gates:
178 revisions and 123 justified retentions. All 36 scoped name/role reviews pass
with native getter/font evidence; 14 progressive headers are observed. Full
catalogue UI layout and future conditional assignments remain unvisited.

Continue with registered cumulative integration. The final source/current/stored
references and individual decisions are in
`translations/maria_B0_B32_final_review_v1.json`; scoped names are in
`translations/maria_B0_B32_scoped_names_final_v1.json`. The sealed handoff is
`work/Maria_B0_B32_clean_20261109/research_final_v1/research_completion.json`.
No new completion credit is assigned before registration.

Reuse [the stored checkpoint](editorial_Maria301_stored_20261109.md): all 303
final offline pages are directly viewed, with 35 wrap improvements, two justified
layout retentions and one reclaimed page. All 635 branch cases, 299 catalogue
lookups, 303 complete loads and 606 parent handoffs pass. The mixed I and eleven
punctuation targets are checked. No dialogue wording changes during formatting
or gameplay review; all native controls, substitutions and unowned components
remain exact.

`gameplay_review_v1.json` seals one broad display run and two narrow exit probes,
42,683 emulator frames total. The broad run observes 92 distinct utterances/96
pages from eight source-ordered display exchanges, including all four two-page
speeches, the four-row Havana taunt, B14's corrected I, the complete B32 style
object/default voice 4 and 14 complete progressive headers. All actual planes
match the final native previews. The eight compact body sheets, one full-scene
sheet, menu sheet and two exit sheets are directly viewed.

The B29 menu is observed between its exact preceding and following commands.
Its default highlight is complete at frame 17,640; ordinary A at 17,680 returns
to the following speech at 17,685. Other choices, cancellation, numeric native
returns and original story branches have offline evidence, not controller-visit
claims. 207 body variants, including six alternative lookout voices, remain
offline-only. No natural activation, original locations, earned chronology,
full route or hardware coverage is claimed. All runs use the existing isolated
system unlock, not earned progression, with no savestate or RAM/model overrides.

The prefix/tail-only QA sequence did not establish a full town return. Preserve
it and the first short exit probe as diagnostic evidence. The versioned 620-byte
exit fixture retains all 47 original B33 nonspeech setup/effect/cleanup commands
in source order and passes the two dialogue pages, original crew notices,
Hangzhou resupply and departure to the ordinary sailing screen. Frames 6,480,
7,440 and 9,001 are directly viewed. Host setup and the longer input schedule
changed together, so no isolated causal claim is made. This is a QA-fixture
adjustment, not a production dialogue/engine fix; production B33 is unchanged.

Next register the exact 32-block SC3 transaction over the verified cumulative
Hodram residual candidate, preserving all 708 existing manifest entries, 114
accepted layers, the registered ASCII right-bound correction and all earlier
runtime/name/text layers. Produce the exact clean-input patch, candidate-owned
startup and required protected-getter evidence, then credit these 301 reviews
once. Do not rebuild old source/prose/native proofs or promote main without
acceptance. Integrated totals remain 19,161=11,532 revisions+7,629 retentions;
remaining native story objects remain 6,737 until integration, including this
batch. Shared/UI prose remains in the full objective as well.

Registered candidate f166991f and main all-routes-unified-v4701 are unchanged.
Preserve every ROM and earlier translation/evidence. No process is live. No
guide photos. Deferred graphics artwork and the later older-record technical
re-audit remain separate. The full editorial goal remains active.
'''
    checkpoint(mutation='work/Maria301_research_checkpoint_20261109',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria301 five-gate research complete; registered integration next.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=False,
            next_action='Register cumulative 32-block SC3 successor, exact clean-input patch, own startup/getters; credit301 once.',guide_photos=False),
        additional_updates={'Maria_SC3_B0_B32_clean_20261109':dict(new_credit=0,
            research_completion=str(ready_path),research_completion_sha256=digest(ready_path),
            final_review=ready['manuscript'],final_review_sha256=ready['manuscript_sha256'],
            gameplay_review=str(actual_path),gameplay_review_sha256=digest(actual_path),
            all301_individual_five_gates_pass=True,all_fifth_formatting_gates_pending=False,
            stored_andrepresentative_gameplay_pending=False,representative_gameplay_pending=False,
            observed_utterances=92,observed_pages=96,offline_only_bodies=207,
            registered_integration_pending=True)},
        summary=summary,document='docs/editorial_Maria301_research_20261109.md',document_text=text,
        completed=19161,protected={'translations/release_stack.json':release['registry_sha256'],
            release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],
            release['patch']:release['patch_sha256'],
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Saved complete Maria301 research checkpoint; integrated19161 andmain unchanged; registered integration next.')


if __name__ == '__main__':
    main()
