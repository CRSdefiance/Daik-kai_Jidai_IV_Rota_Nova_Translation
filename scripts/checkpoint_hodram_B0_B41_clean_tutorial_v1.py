"""Save all394 clean drafts and32 priority tutorial decisions without completion credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE
from scripts.amend_hodram_B0_B41_clean_meanings_v2 import ROOT, OUT as MEANINGS
from scripts.draft_hodram_B0_B41_clean_v1 import OUT as DRAFTS
from scripts.review_hodram_B29_tutorial_contextual_v1 import OUT as REVIEW

BATCH='Hodram_SC1_B0_B41_clean_next_20261107'
RELEASE=Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json')


def main():
    meanings,drafts,review,bindings,release,package=map(load,(MEANINGS,DRAFTS,REVIEW,
        ROOT/'current_binding_verification_v1.json',RELEASE,PACKAGE))
    assert meanings['records_count']==drafts['records_count']==394
    assert drafts['all394_logical_drafts_written_before_current_ROM_story_English_intake']
    assert review['records_count']==review['four_prose_gates_pass']==32
    assert review['counts']==dict(revision=21,retention=11) and review['remaining394_batch_comparisons']==362
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in review['records'])
    assert bindings['current_records']==341 and bindings['native_style_getter_cases']==56
    assert bindings['style_records']==47 and bindings['choice_records']==6
    assert all(not any(r['review'].values()) for r in drafts['records'])
    summary=('All 394 remaining Hodram B0–B41 source meanings and independent logical drafts are sealed. '
        'The complete 32-turn combat tutorial has contextual decisions: 21 proposed revisions and 11 justified retentions. '
        'Automatic-fire wording and displayed Batteries/Quarters labels are corrected in prose; 362 comparisons and all fresh '
        'display checks remain. Exact unchanged dependencies qualify reused native context; all 394 current objects are bound. '
        'Integrated coverage stays 18,767; no new ROM or main promotion.')
    document=f'''# Hodram residual clean drafts and priority tutorial review

{summary}

- [394 clean source meanings](../{MEANINGS.as_posix()})
- [394 independent English drafts](../{DRAFTS.as_posix()})
- [32 tutorial decisions with exact source/current references](../{REVIEW.as_posix()})
- [Complete current binding verification](../{ROOT.as_posix()}/current_binding_verification_v1.json)
- [Authoritative residual source scope](editorial_Hodram_B0_B41_source_scope_20261107.md)

The 39 complete residual exchanges contain 341 ordinary speeches, 47 physical alternatives/56 alias slots in seven style commands, and six captions in three menus. All 394 meanings were read as whole exchanges before eligible existing dialogue. All logical English drafts were then sealed before current intake. They preserve FI/FA/FO counts and contain no authored wrapping, padding or alignment. Each draft keeps explicit pending gates; it does not inherit comparison or display approval. Two symbol-based foreign cries retain their opaque source meaning and still require specific glyph/consumer review.

Forty-two actor-field references and two registered weapon names are source/current bound without opening eligible story English. One initial gloss called source actor7 Lil; the clean field identifies Cristina. The [v2 amendment](../{MEANINGS.as_posix()}) preserves the earlier seal and corrects that attribution before drafting. Other draft spellings follow the registered fields, including Kuhn, Maria, Camille and Aziza. These references do not approve the wider name catalogue. David’s surname still begins with a full-width F; Georg’s and Nagayoshi’s surname fields remain Japanese. Keep these scoped name/rendering leads and the earlier Cristina/Christina consumer distinction open; do not perform a global normalization or move them into deferred artwork.

B29 is the newly prioritized combat tutorial. All 32 source/current turns were read together. Twenty-one proposed revisions restore clear automatic gunfire, the Quarters boarding assignment, Batteries/Quarters/Deck terminology, Charles directing the gunners and automatic boarding at ship contact. They also repair clipped questions, the isolated adjective Willful, formal flag signaling and one mixed-width punctuation target. The suspected territorial violation remains uncertain. A possible mistake is not narrowed to misidentification. Eleven retentions individually explain why good wording works, including Gerhard’s formal authority statement, the existing T-tactic name and explanation, Hodram’s brisk delegation, Charles’s inventor enthusiasm, normal movement controls and the existing X/Deck instruction. The registered candidate’s complete shipinfo asset exactly matches the recorded Batteries/Quarters target, confirming these UI labels without a fresh graphics investigation. No claim is made that every retained line has optimal wrapping yet.

All 341 ordinary current records, 47 physical alternatives, six captions and 56 original style-getter cases are bound. To avoid another cold boot, the existing own-Hodram native context from the B301–B310 parent is reused only after checking complete current ARM9/font/payload and COMMON identity, all 39 selected current blocks byte-for-byte, equal archive block count and the original source/current preambles and command membership. Saved current references identify the latest registered B311–B324 candidate; the runtime receipt explicitly keeps the older snapshot’s identity. A negative qualification rejects the genuinely changed B311–B324 blocks. Original native catalogue/getter and memory guards still execute. This is offline native input reuse, not fresh gameplay or a relabeled historical snapshot.

The first scoped-reuse extraction wrote all 341 records successfully, then its wrapper erroneously entered main a second time. The existing output-directory guard rejected the redundant call before another output; that command exited1. The producer and outputs remain untouched. The [independent verification](../{ROOT.as_posix()}/current_binding_verification_v1.json) exits0 after explicit expected counts, every source/current reference and all current block bytes are checked. The separate object binder also exits0. Future extraction uses `extract_editorial_current_scope_reuse_v2.py`, whose non-main compilation context and single explicit call preserve the native guards. Do not rerun or overwrite the completed current intake merely to hide its original terminal status.

Continue the other 362 comparisons as complete exchanges while preserving these 32 decisions. Finish scoped names, town/ship/UI terms, natural read-throughs, fresh wrapping/native/visual/stored checks and representative gameplay, then register the reviewed batch through the cumulative workflow. All newly generated pages still require visual review. No English gameplay, native formatted preview, stored reconstruction or new batch release is claimed here. The B311–B324 registered cumulative ROM remains current, and main/weekend ZIP are exact. Integrated totals remain 18,767: 11,311 revisions/7,456 retentions. This checkpoint adds zero credit.

The full editorial objective remains active across all other routes, unfinished earlier contextual passes, shared town/shop/random exchanges, speaker names and remaining player prose. Rafael/tutorial priority, separate graphics artwork and the later older-record technical re-audit are preserved. No guide photos or main promotion. All earlier ROMs, drafts, approvals, evidence and failed producer attempts remain. No job is live.
'''
    evidence={str(p):digest(p) for p in (MEANINGS,DRAFTS,REVIEW,ROOT/'draft_names_andterms_reference_v1.json',
        ROOT/'current_binding_verification_v1.json',ROOT/'current_v1/current_effective.json',ROOT/'current_objects_v1/current_objects.json',Path(__file__))}
    checkpoint(mutation=ROOT/'clean_tutorial_checkpoint_v1',batch_key=BATCH,
        batch_updates=dict(new_credit=0,source_meanings_saved=394,localized_drafts_saved=394,
            source_meanings_pending=False,localized_drafts_pending=False,current_English_comparisons=32,
            contextual_decisions=32,four_prose_gate_records=32,proposed_revisions=21,justified_retentions=11,
            remaining_current_comparisons=362,remaining_display_checks=394,
            no_eligible_current_English_extracted=False,all_drafts_sealed_before_current_intake=True,
            all_current_objects_bound=True,source_identity_amendments=1,stored_name_field_leads=3,
            all_five_review_gates_pending=False,all_fifth_gates_pending=True,scoped_names_pending=True,
            representative_gameplay_pending=True,registered_integration_pending=True,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram residual394 clean drafts; combat tutorial32 contextual decisions saved.',
            next_action='Preserve the32 B29 decisions; review the other362 complete-exchange comparisons, then scoped names/terms and fresh display gates before registered integration.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B0_B41_clean_tutorial_20261107.md',document_text=document,
        completed=18767,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],
            package['zip']:package['zip_sha256']})
    print('Saved394 drafts and32 tutorial decisions;362 comparisons remain. No new completion credit; full goal active.')


if __name__=='__main__':main()
