"""Save394 prose decisions and qualified three-name proposals without release credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT
from scripts.review_hodram_B0_B41_contextual_v1 import OUT as PROSE
from scripts.review_hodram_B0_B41_names_v1 import OUT as NAMES

BATCH='Hodram_SC1_B0_B41_clean_next_20261107'
RELEASE=Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json')


def main():
    prose,names,release,package=map(load,(PROSE,NAMES,RELEASE,PACKAGE))
    assert prose['records_count']==prose['four_prose_gates_pass']==394
    assert prose['counts']==dict(revision=221,retention=173) and prose['all32_tutorial_rows_exact']
    assert len(prose['glyph_consistency_targets'])==18
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert (names['scoped_actors'],names['justified_retentions'],names['name_revisions'])==(42,39,3)
    visual=ROOT/'name_field_visual_approval_v1.json';approval=load(visual)
    assert approval['all12_current_andproposed_planes_directly_viewed'] and approval['only28_owned_data_bytes_change_with_exact_whole_ARM9_inverse']
    proof_path=ROOT/'name_field_checks_v1/native_name_fields_verification.json';proof=load(proof_path)
    assert len(proof['negative_cases_rejected'])==8 and proof['no_ROM_created']
    summary=('All 394 residual Hodram B0–B41 contextual decisions are saved: 221 proposed revisions and 173 justified retentions, '
        'preserving all 32 tutorial decisions. Eighteen body glyph targets remain for fresh display checks. '
        'The scoped name review has 39 retentions and three fixes: David Flahven’s full-width F, Georg Salzgitter and Nagayoshi Kamuro. '
        'The three fixes pass native getters, 12 directly viewed name planes, eight rejection cases and an exact 28-byte owned-data inverse. '
        'Body formatting, retained-name planes, roles/terms, stored/gameplay checks and registered integration remain. '
        'Integrated coverage stays 18,767; main and all ROMs are unchanged.')
    document=f'''# Hodram residual contextual and name checkpoint

{summary}

- [394 individual contextual decisions](../{PROSE.as_posix()})
- [42 scoped name decisions and exact references](../{NAMES.as_posix()})
- [Three exclusive surname-field proposals](../{ROOT.as_posix()}/name_field_inputs_v1/owned_fields_proposal.json)
- [Native proposed-name verification](../{proof_path.as_posix()})
- [Direct visual approval](../{visual.as_posix()})
- [Prior source/draft/current-intake checkpoint](editorial_Hodram_B0_B41_clean_tutorial_20261107.md)

The previous goal turn made concrete progress: all 394 source-first meanings/drafts were saved and 32 tutorial comparisons were completed. This turn completes the other 362 comparisons in whole exchanges, preserving the prior 32 rows exactly. Every prose record has exact clean/current positions and bytes, its individual finding, revised or retained logical English and four passing prose gates. All 394 formatting gates remain false. No prose is shortened for allocation, manually wrapped or given authored alignment.

Substantive findings include Indian traditions/homeland incorrectly changed to Hindu, losing southern Mediterranean from a threat, an omitted right-rear maneuver, unproved object loss or veteran history, Prett/Plett and Kuen/Kuhn inconsistencies, the sword’s registered Bloodstained Shamshir title, Aziza’s self-judgment shifted onto circumstances, and her father’s keepsake called a worthless relic instead of something unprofitable to pursue. Her father’s accidental death, sword’s sentimental value, exact one-million ransom and intention to quit piracy are preserved. The Indian Ocean is restored instead of Hindustan. Maria’s warning goes to Camille, not an invented warning mission to Lil. A full-width I in Hodram’s Camille question is a concrete body-font target. Source-script foreign cries remain opaque; the invented N-nooo is removed. No kinship, romance, new rank, confirmed optional participation, actual magical effect, steam propulsion or real-world biography is added.

The 173 retentions have individual reasons. Short tactical reports, natural nautical cheers, good complete questions, Hodram’s dry replies, Charles’s inventor humor, Gerhard’s formal counsel and Yukihisa’s deliberately formal swordsman voice are retained when they work. A short spoken phrase is not automatically defective. The poem retains three source-defined utterances, its repeated sea/mother comparison, unnamed-language hearsay and enduring bond, with no selected foreign language or invented maternal death. Distinct conditional speakers, all 56 physical style aliases and all six menu captions remain source-bound. The 18 body glyph targets are identified, not claimed as already native-rendered fixes.

All 42 referenced actors have exact clean/current component bindings and 84 original progressive/full-name getter cases with original owned-scratch/read-only memory guards. Approved Rafael, Hodram, Joakim, Maria and Camille remain. The name review distinguishes reference-only entries from on-scene speakers, preserves embedded anonymous Foreign Girl labels before Sera is identified, and treats region metadata as metadata. Sailor/Retainer remain generic roles rather than invented ethnicities or ranks. The wider207-entry name review and Cristina/Christina consumers remain open.

Three real nameplate defects are confirmed in both native consumers: David Ｆlahven, Georg ザルツギッター and Nagayoshi カムロ. Proposed ASCII forms are David Flahven, Georg Salzgitter and Nagayoshi Kamuro. Exactly three exclusive surname spans totaling 28 bytes change. All621 ordinary table fields and all aligned ARM9 references are scanned for aliases/interior ownership. The unchanged original terminators, adjacent16 bytes, pointers, section allocation, staged123,264-byte payload and every unowned ARM9 byte are guarded; the whole ARM9 inverse is exact. No source file, ROM or registry is changed. The research-only proposed ARM9 is `{proof['proposed_ARM9']}`, SHA-256 `{proof['name_data_plan']['target_ARM9_sha256']}`.

The current/proposed constructor fixtures execute 12 original name getter cases with full4MiB memory restoration. Twelve distinct native planes and24 consumer/style bindings pass independent pixels, complete character codes, leading/trailing glyphs and bounds. All twelve rows of the readable review sheet were directly viewed. The proposed F is the ordinary ASCII glyph; both romanized surnames are complete and legible. Eight malformed-parent/source/clean/adjacency/ownership/reference/control/review cases are rejected. These are offline native styles11 and1, not observed catalogue UI, a new cold boot or hardware. Actual changed headers and candidate-owned startup remain to verify. Retained-name planes still need exact compatible cache reuse or fresh checks; do not call the whole name-display gate complete yet.

Next bind the four dynamic selectors208/213/214/216 and remaining scoped terms, retaining207 only as the captain-control proof. Resolve the two opaque-cries’ exact native text consumers. Prepare all388 logical speech bodies and six captions with the validated consumer-specific formatter, preserving native prefixes and FI/FA/FO. Reuse matching earlier technical proofs and run fresh checks for changed text. View every generated page and review phrase continuity, short tags, sparse openings and page boundaries; then verify stored scripts and representative gameplay. Use the already qualified9,216-byte fixture capacity guard and source-occurrence-based fixture generator; do not repeat the resolved long-fixture return investigation.

This batch now needs a mixed registered successor like the qualified Rafael5186 workflow: reviewed SC1 blocks plus only these three separately qualified owned surname fields. A dialogue-only successor would omit the name fixes. Preserve all706 predecessor entries,114 accepted layers and the ASCII right-bound correction. Keep all other files/components exact, require complete parent inverses and reconstruct the entire cumulative candidate exactly from clean input. Required own-startup/protected-getter checks must also include the three corrected actors. No main promotion without user acceptance.

The current cumulative candidate is still [registered B311–B324](editorial_Hodram_B311_B324_registered_20261107.md), SHA-256 `{release['candidate_sha256']}`. Integrated totals remain18,767:11,311 revisions/7,456 retentions; no new completion credit is added here. All earlier drafts, source-meaning amendments, native receipts, failed producer attempts, ROMs and the weekend ZIP remain. No job is live. The complete editorial objective stays active across remaining routes, earlier unfinished contextual passes, shared town/shop/random dialogue, names and player-facing prose. Rafael/tutorial priority, separate artwork and the later older-record technical re-audit remain. No guide photos.
'''
    evidence={str(p):digest(p) for p in (PROSE,NAMES,visual,proof_path,ROOT/'scoped_names_current_v1.json',
        ROOT/'name_field_inputs_v1/owned_fields_proposal.json',Path(__file__))}
    checkpoint(mutation=ROOT/'contextual_names_checkpoint_v1',batch_key=BATCH,
        batch_updates=dict(new_credit=0,current_English_comparisons=394,contextual_decisions=394,
            four_prose_gate_records=394,proposed_revisions=221,justified_retentions=173,remaining_current_comparisons=0,
            remaining_display_checks=394,body_glyph_consistency_targets=18,scoped_name_decisions=42,
            scoped_name_retentions=39,scoped_name_revisions=3,stored_name_field_leads=0,
            qualified_name_field_fixes=3,qualified_owned_name_field_bytes=28,
            changed_name_planes_directly_viewed=12,name_field_rejection_cases=8,
            retained_name_planes_pending=True,scoped_names_pending=True,dynamic_roles_pending=True,scoped_terms_pending=True,
            all_fifth_gates_pending=True,representative_gameplay_pending=True,registered_integration_pending=True,
            name_actual_headers_andregistered_layer_pending=True,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram residual394 contextual decisions complete; three name fixes pass offline native/visual checks.',
            next_action='Bind roles/terms and retained-name planes; generate and inspect all388 body records/six captions. Then stored checks, representative gameplay and mixed registered dialogue-plus-three-surname successor.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,native_job_live=False,
            registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B0_B41_contextual_names_20261107.md',document_text=document,
        completed=18767,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved394 contextual decisions/42 name decisions/three qualified field fixes. All body display gates and integration remain; zero credit.')


if __name__=='__main__':main()
