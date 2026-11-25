"""Preserve sealed drafts, partial contextual decisions and current-build bindings."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_rafael5186_v1 import RELEASE,REGISTRY
from scripts.consolidate_hodram_B211_B230_clean_drafts_v1 import OUT as DRAFTS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B221_B230_contextual_v1 import CURRENT,OBJECTS,OUT as REVIEW,ROOT
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

TUTORIALS=Path('work/priority_tutorials_Rafael5186_v1.json')
STARTUP=ROOT/'own_parent_startup_v3/own_route_context.json'

def main():
    drafts,review,current,objects,startup,tutorials,release,ledger,package=map(load,
        (DRAFTS,REVIEW,CURRENT,OBJECTS,STARTUP,TUTORIALS,RELEASE,LEDGER,PACKAGE))
    assert len(drafts['records'])==277 and drafts['previous114_drafts_exactly_preserved']
    assert review['records_count']==136 and review['counts']=={'revision':86,'retention':50}
    assert review['remaining_contextual_comparisons']==141 and len(review['full_width_Latin_I_findings'])==9
    assert current['records']==241 and len(objects['style_records'])==29 and len(objects['choice_records'])==7
    assert objects['native_style_getter_cases']==32
    assert startup['actual_captain_getter']==startup['actual_route_word']==1 and startup['frames']==4001
    assert startup['candidate_sha256']==current['current_ROM_sha256']==release['candidate_sha256']
    assert len(startup['exact_own_RGB_reuse_of_prior_direct_visual_review'])==10
    assert tutorials['HELP_topics']==202 and tutorials['HELP_archive_exact_to_final_registered_HELP_parent']
    assert tutorials['Deck_current_text_allocations_andpointers_exact']
    assert ledger['records_editorially_completed']==17031 and not ledger['full_goal_complete']
    summary=('Hodram B211–B230 now has all 277 clean-first drafts sealed, preserving the earlier 114 exactly. '
        'Nine complete exchanges have 136 contextual decisions: 86 revisions and 50 justified retentions. '
        'Nine mixed-font I defects are identified. Another 141 comparisons, scoped name review and fresh '
        'display checks remain. Known HELP/Deck tutorial proofs reconcile with Rafael5186. Integrated coverage stays 17,031.')
    doc=f'''# Hodram B211–B230 resumed contextual review

{summary}

The [sealed drafts](../{DRAFTS.as_posix()}) cover 241 ordinary speeches, 29 physical personality alternatives and seven captions in three menus. All exact clean references, macros and source keys pass. The original 114 ordinary drafts remain byte-for-byte equivalent as JSON records; 163 further drafts are added. All 32 style alias slots across four physical objects retain their original membership. Block 222 contains no ordinary prose. These are source-grounded drafts, with no fifth-gate or integration credit.

The [136 individual comparisons](../{REVIEW.as_posix()}) cover complete exchanges in B221 and B223–B230, including B226's seven arrival variants and both Crusades-menu captions. Every decision has exact clean/current references, a specific finding, revised or retained English and four prose gates; formatting remains false. Fifty natural current paragraphs are retained individually, including dry Hodram questions, formal Gerhard statements, playful hero-role proclamation and intentional source ellipses. The other 141 comparisons in B211–B220 remain open.

Corrections include repeated this man/this woman self-reference; missing mythological context and uncertainty; a causal claim that an empress's tyranny caused her death; an instruction to hide Safia's hair where the source says Julian would not need her to uncover it; and Manuel replying the same as you to Gerhard when the source compares his activity with the Admiral's. Mail becomes Armor? rather than inventing an armor type and losing a question. A northern-Europe location becomes tentative again. Nine full-width Latin I characters in Ian's name are identified and corrected in the proposed prose: two ordinary speeches and seven personality variants. These are findings awaiting fresh native formatting and display validation, not shipped fixes.

The Crusades, Noritsune, Timur, Charles Martel and Attila passages preserve the characters' reported histories, cultural perspectives and explicit counterfactuals. They are not rewritten as modern historical commentary. Unnamed armor stays unnamed; clues remain rumors or inferences where the source qualifies them. Julian's flirtation does not establish a new relationship. The retained Do you know of the Crusades question has Yes/No menu replies; the independent draft's I have/I haven't would respond less naturally to that retained wording.

The current comparison packet comes from exact registered Rafael5186. Its own fresh 4,001-frame ordinary Hodram startup matches all ten reviewed opening captures and yields native captain 1 / route 1 with the complete staged payload and read-only current RAM. The [own-context proof](../{STARTUP.as_posix()}) uses no historical RAM overlay. The [241 ordinary bindings](../{CURRENT.as_posix()}) preserve source preambles and command kinds; [29 style and seven caption bindings](../{OBJECTS.as_posix()}) preserve all aliases and pass 32 original style-getter cases. This startup is not gameplay coverage of the reviewed B211–B230 scenes. No newly drafted page or conditional story event has been visually checked yet.

The startup helper's first attempt incorrectly counted explicit capture requests as all captures and stopped before emulation. The second encountered a core-load failure before frames. Both folders remain; the successful third runs the emulator separately from the native-check DLLs. No ROM was changed or retried from an unobserved live process.

The [priority tutorial reconciliation](../{TUTORIALS.as_posix()}) confirms all 202 HELP topics have credited five-gate reviews and that the entire HELP archive still equals the final registered HELP parent. The four reviewed Deck panels retain their exact text allocations and pointer fields. These proofs are reused without new editorial credit or gameplay claims. This scoped reconciliation does not declare every shared non-HELP tutorial or player-facing resource complete. Rafael's separate native SC0 census remains complete at 6,887 speech/style/caption objects.

Next finish the 141 remaining complete-exchange comparisons, review the 23 scoped speaker identities/role labels against the current build, then prepare fresh consumer-specific formatting and inspect every generated page. Reuse exact compatible native rules. Follow with stored reconstruction, representative scenes and required risk tests, then registered cumulative integration and once-only credit. Current Rafael5186, promoted main and the weekend test ZIP remain unchanged. All unfinished routes, shared/shop/town/random prose and wider name review remain in scope. Graphics artwork and the later older-record technical re-audit remain separate. No guide photos are collected.
'''
    evidence={str(p):digest(p) for p in (DRAFTS,REVIEW,CURRENT,OBJECTS,STARTUP,TUTORIALS,Path(__file__))}
    checkpoint(mutation=ROOT/'contextual_checkpoint_v1',batch_key='Hodram_B211_B230_clean_next_20261104',
        batch_updates=dict(new_credit=0,localized_drafts=277,ordinary_drafts=241,physical_style_drafts=29,
            caption_drafts=7,preserved_partial_drafts=114,previous114_drafts_exactly_preserved=True,
            all277_drafts_sealed_before_current_comparison=True,current_English_comparisons=136,
            proposed_revisions=86,justified_retentions=50,remaining_current_English_comparisons=141,
            proposed_mixed_width_Latin_glyph_fixes=9,current_stored_effective_bindings=277,
            no_current_ROM_English_extraction_in_this_intake=False,
            current_speech_bindings=str(CURRENT),current_speech_bindings_sha256=digest(CURRENT),
            current_object_bindings=str(OBJECTS),current_object_bindings_sha256=digest(OBJECTS),
            current_parent_own_Hodram_startup=str(STARTUP),current_parent_own_Hodram_startup_sha256=digest(STARTUP),
            prose_comparison_anddisplay_pending=True,scoped_current_name_review_pending=True,
            formatting_visual_stored_gameplay_andregistered_release_pending=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B211–B230: all drafts sealed; 136 contextual decisions complete.',
            next_action='Finish 141 contextual comparisons, scoped names and fresh formatting.',
            current_batch_not_yet_integrated=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,
            known_HELP_andDeck_priority_proofs_reconciled=str(TUTORIALS),guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B211_B230_contextual_20261107.md',document_text=doc,
        completed=17031,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved all drafts and 136 contextual decisions; 141 comparisons remain. Integrated credit unchanged at 17,031.')

if __name__=='__main__':main()
