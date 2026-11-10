"""Prioritize the complete32-turn battle tutorial; keep display gates pending."""
from copy import deepcopy
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT

DRAFTS=Path('translations/hodram_B0_B41_clean_drafts_v1.json')
CURRENT=ROOT/'current_v1/current_effective.json'
OUT=Path('translations/hodram_B29_tutorial_contextual_review_v1.json')

RETAIN={
5:'The brief excited sighting naturally begins Manuel’s exchange; repeating There from the draft is unnecessary.',
9:'The complete echo question naturally asks whether the sighted vessel belongs to Speyer and matches the draft.',
16:'Gerhard’s complete formal sentence naturally states the territorial limit on enforcement in this exchange; our waters is clear in context.',
19:'The startled question and sudden attack without warning naturally express the unexpected hostile gunfire, without inventing an advance ultimatum.',
67:'Hodram’s clipped question is natural in urgent tactical dialogue and clearly requests Charles’s plan.',
71:'The concise complete tactical answer names the source T tactic; the next turn explains it, so a new technical synonym is unnecessary.',
77:'Gunnery is yours is an idiomatic, decisive delegation and preserves Charles’s responsibility for the guns.',
85:'The slightly grand phrasing suits Charles’s excited inventor voice and preserves the new cannon test without inventing a new weapon type.',
88:'Steer and adjust the sails clearly conveys both native controls and the comparison to ordinary movement.',
102:'The complete instruction accurately preserves X, the menu and the Deck label; its existing wording is clear.',
116:'The complete direct request gives Manuel a natural closing prompt and preserves heading control.',
}

FIND={
13:'Replace the clipped type-identification fragment with a natural excited recognition while retaining Hanseatic cog.',
22:'Make the questions conversational while leaving the kind of possible mistake unspecified; misidentification is not explicit in the Japanese.',
26:'Preserve the source’s explicit flag signaling in a complete spoken order.',
30:'Make Charles’s request for the message a natural question.',
34:'Preserve the formal accusation’s suspected territorial violation, not just neutral possible entry.',
38:'Restore the formal request to stop for investigation instead of changing it to a bald command and an immediate demand for an explanation.',
41:'Replace mixed full-width exclamation glyphs with consistent ASCII punctuation; fresh native rendering remains.',
45:'Use a conventional alarm cry rather than an infant-like Wah.',
49:'Restore a complete spoken failure report and the source’s tentative judgment that the foe will not even look at the flags.',
52:'Replace the isolated adjective Willful with a complete voiced realization.',
56:'Make the before-trouble inference a complete natural sentence.',
59:'Restore a natural no-need-to-hold-back decision while preserving the good battle-stations order.',
62:'Make the antagonist’s rough insult and threat natural spoken English rather than a stiff naval-battle slogan.',
74:'Specify the enemy broadsides and preserve bow/stern maneuver, own broadside and concerted fire; do not teach a one-shot firing restriction.',
81:'Restore Charles personally directing the gunners while Hodram maneuvers, not merely saying the gunners obey.',
92:'Replace guns fire alone with the clear automatic-fire instruction.',
95:'Use the registered Quarters room label and preserve the boarding-leader request, without adding an independent military rank.',
98:'Combine the combat-assignment instruction and Deck location into one natural tutorial paragraph.',
106:'Replace gun deck and marines with the displayed Batteries and Quarters labels, retaining the Deck station.',
109:'Match Gerhard’s assignment instruction to the actual Quarters label.',
112:'State automatic boarding upon contact explicitly and retain the expected benefit of Gerhard’s boarding-leader assignment.',
}

REFINE={
22:'What are they doing? Is this some mistake?!',
26:'Signal them by flag!',
52:"So it's deliberate...",
56:'They mean to dispose of us before things get complicated.',
59:"Then we needn't hold back. All hands, battle stations!",
98:"Use the Deck screen to change your crew's assignments for battle.",
106:'In battle, it helps to have crew assigned to the Batteries, Quarters and Deck.',
112:'Boarding combat begins automatically when ships touch. Gerhard should do well as boarding leader.',
}


def main():
    assert not OUT.exists()
    drafts,current,verified=map(load,(DRAFTS,CURRENT,ROOT/'current_binding_verification_v1.json'))
    assert verified['all394_current_keys_bound_after_sealed_drafts']
    source=[r for r in drafts['records'] if r['block']==29]
    old=next(g for g in current['groups'] if g['block']==29)['records']
    assert len(source)==len(old)==32
    byid={r['id']:r for r in old}
    assert set(RETAIN).isdisjoint(FIND) and set(RETAIN)|set(FIND)=={r['source_reference']['record_index'] for r in source}
    asset=Path('translations/ship_battery_labels_v1.json')
    labels=load(asset)
    image=NdsImage.open(current['current_ROM'])
    shipinfo=image.read_file('/_pxl/shipinfo.pxl')
    assert sha(shipinfo)==labels['target_sha256']['/_pxl/shipinfo.pxl']
    assert labels['source_Japanese']=={'海兵詰所':'Quarters','武装砲台':'Battery / Batteries'}
    rows=[]
    for original in source:
        row=deepcopy(original);before=byid[row['id']];n=row['source_reference']['record_index']
        assert all(before[k]==row[k] for k in ('source_hex','source_reference','source_Japanese'))
        assert not any(row['source_macros'].values()),'This tutorial comparison does not infer macro expansion.'
        row.update(current_reference=before['current_reference'],current_hex=before['current_hex'],
            current_stored_English=before['current_stored_text'],current_English=before['current_comparison_paragraph'],
            current_effective_hex=before['current_effective_hex'],current_catalogue_selected=before['current_catalogue_selected'],
            current_reference_ROM=current['current_ROM'],current_reference_ROM_sha256=current['current_ROM_sha256'],
            independent_draft_English=original['english'])
        if n in RETAIN:
            english=before['current_comparison_paragraph'];decision='retention';reason=RETAIN[n]
        else:
            english=REFINE.get(n,original['english']);decision='revision';reason=FIND[n]
            assert english!=before['current_comparison_paragraph']
        assert english.isascii() and not any(t in english for t in ('\n','{LB','{ALIGN','{PAD}'))
        if n==22:
            row['source_meaning']='Gerhard asks what the attackers intend and whether some mistake has occurred; the kind of mistake is unspecified.'
            row['source_meaning_refinement_reason']='The source 勘違い alone does not establish mistaken identity. Retain the immutable clean-first draft/gloss as history.'
        row.update(english=english,editorial_decision=decision,editorial_finding=reason,
            localization_note=reason,retention_reason=reason if decision=='retention' else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            whole_exchange_read_aloud_review=True,scoped_room_terms_exact_to_current_shipinfo=True,
            current_English_conversation_comparison_pending=False,source_first_draft_not_final_comparison_approval=False,
            fresh_native_visual_stored_gameplay_andregistered_integration_pending=True,new_credit=0)
        rows.append(row)
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',records=rows,records_count=32,
        counts=dict(revision=len(FIND),retention=len(RETAIN)),four_prose_gates_pass=32,formatting_gate_pending=32,
        complete_exchange_blocks=[29],current_reference=str(CURRENT),current_reference_sha256=digest(CURRENT),
        all394_clean_first_drafts_sealed_before_current_intake=True,
        source_room_to_current_UI_terms=labels['source_Japanese'],current_shipinfo_sha256=sha(shipinfo),
        exact_existing_native_context_reuse=current['exact_native_context_reuse'],
        native_current_text_checks_not_new_gameplay=True,all32_speeches_unvisited_in_new_gameplay=True,
        remaining394_batch_comparisons=362,scoped_names_anddistinct_display_consumers_still_pending=True,
        registered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in (DRAFTS,CURRENT,asset,ROOT/'current_binding_verification_v1.json',Path(__file__))}))
    print(f'Saved32 complete-tutorial decisions: {len(FIND)} revisions/{len(RETAIN)} retentions. Display gates pending; no credit.')


if __name__=='__main__':main()
