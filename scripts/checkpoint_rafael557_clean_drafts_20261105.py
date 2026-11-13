"""Save the new clean-source editorial batch without duplicate orpremature completion credit."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha


def main():
    root=Path('work/analysis/Rafael_B141_B160_clean_20261105')
    old_qualification=root/'source_census_anddraft_qualification_v2.json'
    qualification=root/'source_census_anddraft_qualification_v3.json'
    q=load(old_qualification);drafts_path=Path(q['meanings_anddrafts']);drafts=load(drafts_path)
    assert q['source_objects']==len(drafts['records'])==557
    assert q['meanings_anddrafts_sha256']==sha(drafts_path.read_bytes())
    assert not q['completed_source_key_overlap'] and q['integrated_completed']==12712
    assert all(not any(r['review'].values()) and len(r['review'])==5 for r in drafts['records'])
    assert not qualification.exists()
    q=deepcopy(q)
    q.update(original_draft_qualification=str(old_qualification),original_draft_qualification_sha256=sha(old_qualification.read_bytes()),
        no_new_native_execution_formatting_orvisual_approval=False,
        structural_native_command_walker_executed_during_clean_intake=True,
        no_native_display_font_plane_page_or_gameplay_approval=True,
        existing_FU_codec_profile_andinverse_support_found=True,
        existing_FU_support=['dk4tool/dialogue/codec.py','dk4tool/dialogue/profiles.py',
            'dk4tool/script/rafael_story_rebuild_with_fu_v1.py'],
        current557_FU_dependencies_expansions_anddisplay_still_require_binding=True,
        no_repeated_source_walker_ornew_rendering_execution_for_this_metadata_clarification=True)
    save(qualification,q)
    release_path=Path('work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json')
    release=load(release_path)
    summary=("Rafael and all tutorials remain first. The next clean-source batch has 557 objects across B141–B160: "
        "549 speeches and eight captions. All 557 now have individual meanings and independent American English drafts, "
        "with zero overlap against the 12,712 integrated keys. Whole exchanges include the combat/investment tutorial, "
        "two-key treasure maps, alliances, Portugal's crisis, Arcadius's private identity and Charlotte's conditional message. "
        "A source reread made 13 draft refinements; four name substitutions initially changed to pronouns were restored. "
        "All 61 literal substitutions are preserved, including two FU full-name occurrences. Existing FU codec/profile/rebuild "
        "support is available; bind its current dependencies rather than restarting engine research. Current-English comparisons, "
        "approved names/items/titles, callbacks and all five per-record gates remain pending. No new display or gameplay approval "
        "or completion credit. Integrated totals stay 12,712; cumulative3bf3/main3cb8, all ROMs and full scope are unchanged.")
    text='''# Rafael557 clean-source editorial checkpoint — November 5, 2026

Rafael's storyline and all tutorials remain first. Every other storyline, earlier unfinished contextual pass, shared town/shop exchange, random scene, name, wrap/glyph issue and remaining player-facing prose stays in scope. No guide photos or main promotion.

## New editorial work

`work/analysis/Rafael_B141_B160_clean_20261105/all557_meanings_andindependent_drafts_v2.json` contains **557 clean-source meanings and independent drafts:549 speeches and eight labels across20 complete blocks**. The source packet retains every complete header, nested command, original offset/index and menu object. There are four two-choice menus, no4100 style alternatives and zero overlap with the12,712 integrated source keys.

Complete exchanges cover Hayreddin's gift, Albuquerque's commission and Fernan's combat/investment lesson, Uddin's alliance negotiations, six treasure-map mechanisms, the two-keys/seven-Proofs/fourteen-keys rule, Portugal's political crisis, Pereira's divided obligations and New World faction rivalries. Arcadius's reveal and Charlotte's entrusted message preserve privacy, the stated safety rationale, class difference, inability to write and the invitation's conditions. Do not add romance promises, family relationships, noble ranks or secret-plan details.

Current English was not extracted for this intake before the drafts. This makes no blanket claim about historical exposure. All wording is **unapproved draft material**: no current comparison, revision/retention decision, native formatting or final gate is inferred. Provisional names, titles and item wording must be bound before approval; do not globally rename actor8 from a private revelation.

The source reread records13 refinements: an alternative target rather than an additional Spanish target; an unfinished objection and awkward evasion without invented claims/jokes; enemies rather than softened ordinary rivalry; the source-supported governor title instead of nobility inferred from様; Escante's interrupted homeland sentence without supplying his secret; and ASCII punctuation. A draft token check caught four instances where FI had become a pronoun. Faithful quotation and natural address restore the original token counts. These are draft findings, not newly shipped defects or additional completed records.

## Reuse and outstanding work

`source_census_anddraft_qualification_v3.json` records exact membership, source references, zero completed overlap and61 preserved literal substitutions:FI41,FA8,FO10,FU2. FU occurs at B143R67 and B146R6. Existing support is already in `dk4tool/dialogue/codec.py`, the v26-and-later deep-route profiles and `dk4tool/script/rafael_story_rebuild_with_fu_v1.py`. Reuse it after matching current runtime, font, controls and actual expansions. Do not treat historic profile estimates as fresh formatting approval or convert FU toFI/a fixed name.

The existing native source-command walker was used for structural inventory only. No new font planes, formatted pages, live scenes or gameplay coverage were approved. V3 clarifies that scope while preserving the prior qualification and every draft; the source walker was not repeated. Changed final wording still needs fresh formatting and page review.

Next compare complete exchanges with the current cumulative3bf3 text, prioritizing the B143 combat/investment and B150 map tutorials. Bind public/private names, role labels, item/menu/city terms, FU and the earlier Charlotte callbacks. Keep individual source/context/localization/naturalness/formatting gates pending until their evidence exists. Then use the established native/stored/catalogue/loader and representative-test workflows, reusing exact compatible proofs, followed by registered integration and an exact clean-input patch.

The four original draft groups, amended consolidated draft, token-check failure producer and correction producer are preserved under the intake root or `scripts/`; the qualification links their hashes. All current retentions and translations remain intact.

Integrated totals remain **12,712 =7,283 revisions+5,429 retentions**; historical source/prose12,715. Verified cumulative **3bf3239736982e6398eda1f837f4c249b93e541128985013fbde02466bcbaa9c** and main **3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe** are unchanged. Two catalogue de corrections/global names, deferred artwork and the later older-record technical re-audit remain open and separate. Full goal active.
'''
    checkpoint(mutation='work/analysis/Rafael557_clean_draft_checkpoint_20261105',
        batch_key='Rafael867_qualified_cumulative_research_20261105',
        batch_updates=dict(new_credit=0,remaining_new_source_credit=0,all867_registered_andcredited_in_two_disjoint_families=True),
        new_entries={'Rafael_SC0_B141_B160_clean_20261105':dict(new_credit=0,source_objects=557,ordinary_speeches=549,
            choice_captions=8,choice_objects=4,physical_style_variants=0,source_blocks=list(range(141,161)),
            source_packet=str(root/'clean_source_packet.json'),source_packet_sha256=sha((root/'clean_source_packet.json').read_bytes()),
            source_meanings=557,independent_drafts=557,meanings_anddrafts=str(drafts_path),meanings_anddrafts_sha256=sha(drafts_path.read_bytes()),
            completed_overlap_census=str(qualification),completed_overlap_census_sha256=sha(qualification.read_bytes()),
            current_comparisons=0,remaining_current_comparisons=557,all_five_review_gates_pending=True,
            native_display_stored_andrepresentative_gameplay_pending=True,registered_integration_pending=True,
            all_source_literal_substitutions_preserved=True,FU_source_IDs=['DK4_MES_B143_R0067','DK4_MES_B146_R0006'],
            existing_FU_support_reuse_after_current_dependency_qualification=True,
            source_contexts_reviewed_as_exchanges_without_inferred_conditional_activation=True)},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael557 clean meanings/independent drafts; current comparison andbindings next',
            current_batch_not_yet_integrated=True,next_action='Compare complete exchanges againstcurrent3bf3;prioritize B143 combat/investment andB150 map tutorials. Bind names/items/titles/FU andcallbacks;reuse compatible proofs.',
            new_source_meanings=557,new_independent_drafts=557,new_current_comparisons=0,
            all_current_batch_five_gates_pending=True,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael557_clean_source_checkpoint_20261105.md',document_text=text,
        completed=12712,protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256']})
    print('Saved557 clean meanings/drafts andexact source/token census;zero credit. Integrated12712/currentROM/main/registry preserved. Full goal active.')


if __name__=='__main__':main()
