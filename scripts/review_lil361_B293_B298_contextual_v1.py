"""Individual mountain, cliff and Istanbul comparisons; no final gates or credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save

ROOT = Path('work/Lil361_B283_B298_clean_20261110')
DECISIONS = r'''@293
12|D|Give the guide's refusal a natural complete sentence while preserving the map requirement even for this party.
25|R|Retain the clear acknowledgment that the required map has been brought; it matches the independent draft.
S194_0|R|Retain the polite complete map requirement and Admiral address.
S194_40|R|Retain the reserved complete map requirement and Admiral address.
S194_78|D|Restore the casual direct Admiral address and forward-travel warning.
S194_112|R|Retain the feminine complete conditional warning about lacking a map.
S194_146|D|Restore the rough voice's conversational refusal rather than the bland need-a-map formulation.
S194_184|D|Restore the older voice's direct Admiral address and firm cannot-proceed warning.
S194_216|R|Retain the child's natural map plea; it matches the independent draft exactly.
S194_244|D|Restore the older formal register and beyond-this-point emphasis.
69|D|Give Lil's relieved completed-climb reaction natural complete speech and retain finally.
72|D|Make the guide's farewell idiomatic while retaining that he leaves here.
75|T|Use the established full story term Proof of Conquest, replacing the awkward legacy Proof of Conqueror clue phrase while preserving Lil's confidence.|I'm sure these ruins hold a clue to the Proof of Conquest...
86|R|Retain the natural surprised why question; it matches the independent draft exactly.
93|R|Retain Lil's explicit intuition and natural gut-feeling wording, without inventing supporting evidence.
104|R|Retain the companion's natural caution and source sense that fear is useful here.
111|D|Restore a natural first-person observation rather than a clipped visibility note.
S908_0|D|Restore the polite complete fog alert while retaining urgency and the Admiral address.
S908_36|R|Retain the tentative fog identification and shared caution.
S908_70|D|Give the casual fog observation complete speech while retaining inability to see the surroundings.
S908_114|D|Preserve the feminine specific concern about where everyone is, with natural personal phrasing.
S908_174|T|Complete the rough complaint naturally without adding a stronger swear than this source reaction requires.|Damn... I can't see a thing through this fog.
S908_208|R|Retain the older voice's brief fog alert and specific footing caution.
S908_242|D|Restore the childlike exclamation and complete inability-to-see reaction.
S908_290|T|Keep the older formal observation concise while using the same fog term as the surrounding exchange.|Fog...
142|R|Retain the sudden-loss-of-visibility observation and natural FI concern; vanished is figurative visibility loss here.
149|D|Restore Lil's tree-collision realization as a complete comic beat after her angry who question.
S1420_0|D|Restore the polite voice's full request for a decision, distinct from the other alternatives.
S1420_20|D|Restore the casual direct Admiral address without adding a decision or event.
S1420_38|D|Give the rough voice its own idiomatic what's-the-plan question instead of repeating every other variant.
S1420_60|D|Restore the older companion's distinct spoken phrasing.
S1420_84|D|Restore the child's calling, worried question rather than the same flat formula as the adult variants.
S1420_110|D|Restore the older formal voice with a natural shall-we question.
186|R|Retain the direct natural FI request for a decision.
193|R|Retain Lil's thoughtful pause before the menu; no extra explanation is needed.
C1620_0|D|Restore the wait-for-a-while option rather than only a bare verb.
C1620_1|D|Restore the choice to leave the present place quickly; later separation is not stated in the caption.
S1686_0|D|Restore the polite complete wait-here confirmation question.
S1686_22|R|Retain the reserved hesitant wait-here confirmation and pause.
S1686_46|R|Retain the casual complete wait-here confirmation.
S1686_68|R|Retain the feminine natural you-mean confirmation.
S1686_90|R|Retain the rough voice's short incredulous waiting question.
S1686_108|R|Retain the older companion's economical confirmation of waiting.
S1686_124|D|Use the child's natural hungry complaint instead of the translated-sounding belly-is-empty phrasing.
S1686_172|D|Restore the older formal understanding and agreement without adding a new plan.
242|R|Retain the companion's natural surprised in-this-fog objection.
249|R|Retain Lil's confidence, separation warning and predicted clearing; the source itself is assertive here.
S2052_0|R|Retain the polite realization and natural good-call praise.
S2052_28|D|Restore the reserved thoughtful beat and measured praise rather than identical generic good-call wording.
S2052_54|D|Restore the casual direct Admiral praise and natural realization.
S2052_80|R|Retain the feminine enthusiastic realization and direct clever-Admiral praise.
S2052_108|D|Restore the rough voice's individual realization and Admiral address without introducing a collective we.
S2052_142|D|Restore the older companion's measured explicit Admiral praise.
S2052_170|R|Retain the childlike enthusiastic smart-Admiral praise.
S2052_206|D|Restore the older formal acknowledgment of her reasoning and Admiral praise.
278|R|Retain Lil's self-satisfied brief acceptance of praise; the casual Yep suits her voice.
284|R|Retain the teasing for-you qualification with exact FI substitution.
288|R|Retain Lil's lively rebuttal, echoing the retained good-call wording.
300|R|Retain the clear exact one-day elapsed notice.
304|R|Retain the clearing-fog celebration and energetic group departure instruction.
S2558_0|D|Restore the polite direct Admiral address in the serious-question reaction.
S2558_20|R|Retain the casual natural safety question.
S2558_42|R|Retain the feminine alarm at this fog and natural shared safety concern.
S2558_80|R|Retain the rough conversational incredulity; the source does not require a new threat.
S2558_102|D|Restore the older voice's natural are-we-really-going question rather than inverted travel notes.
S2558_122|R|Retain the childlike stammer and tentative safety concern.
S2558_154|D|Restore the older formal safety concern as a complete spoken question.
342|R|Retain the companion's natural fog-and-safety question.
348|R|Retain Lil's confident reassurance and immediate departure cue.
359|R|Retain the stammered urgent wait call; following the party supplies the implied context.
367|D|Give Lil's checking-on-everyone question natural complete speech.
S2942_0|R|Retain the polite tentative assessment that some people got separated.
S2942_38|R|Retain the reserved tentative separation report.
S2942_74|D|Restore the source's apparently qualification and causal visibility explanation.
S2942_126|D|Restore the feminine tentative missing-people assessment rather than strengthening it to must-have certainty.
S2942_180|D|Restore the rough voice's tentative separation report while retaining his resigned fog explanation.
S2942_238|R|Retain the older voice's explicitly tentative separation report.
S2942_274|R|Retain the child's missing-people realization and inferred fog explanation without asserting deaths.
S2942_330|D|Restore the older formal voice's appears qualification and connection to the fog.
396|D|Restore the source's tentative separation assessment and natural poor-visibility explanation.
403|D|Report a small crew decrease without the ambiguous lost-sailors wording that could imply deaths in this separation branch.
415|D|Restore Lil's recognition question as a natural complete reaction.
427|R|Retain the tentative arrival observation.
@294
5|D|Give the dead-end sign reading a complete natural clause while retaining Lil's puzzled reaction.
8|D|Restore the guide's reported knowledge of the recent rockfall and apology.
18|D|Make Lil's follow-up question complete while retaining the blocked-ruins conclusion.
24|R|Retain the polite alternative's clear consequence question.
31|R|Retain the guide's uncertain-length denial and conversational hesitation.
35|R|Retain Lil's natural how-long follow-up; the preceding a-while supplies its reference.
39|R|Retain the uncertain ten-or-twenty-year estimate and lack of visitors, without inventing a fixed reopening date.
51|R|Retain the FI decision request and natural objection to waiting so long.
57|D|Restore the guide's complete conditional alternative and somewhat dangerous cliff route in connected speech.
61|D|Give Lil's surprised cliff echo its natural definite article.
65|R|Retain the warning that even locals rarely dare attempt the climb.
69|R|Retain Lil's confident defiant climb challenge.
76|D|Restore explicit guidance to the cliff and natural meeting/map instruction, with R73 preserved as earlier credited context.
80|R|Retain Lil's map question; it matches the independent draft exactly.
84|D|Restore the hidden Christian settlement, even-the-guide limitation and tentative Mediterranean map lead in complete speech.
@295
5|R|Retain the institutional guild job request; we adds no new traveling party or relationship.
8|R|Retain the invited vassal king and collection display; His Majesty refers to the emperor as established by the complete exchange.
11|R|Retain Lil's natural single-word echo of the newly mentioned collection.
15|R|Retain the worldwide rarities collection and item desired before the display.
18|R|Retain Lil's natural question about the item; it matches the independent draft exactly.
22|D|Give the bound Heavenly Wristband name and reported leadership benefit complete natural sentences.
26|R|Retain Lil's mild interest without inventing enthusiasm or disbelief.
30|D|Restore the contact's complete speculative explanation of Ottoman imperial display.
33|R|Retain Lil's skeptical echo and natural comment about rulers' vanity, without inventing a political allegiance.
37|D|Restore the complete hearsay sentence about an imperial order to postpone the ceremony, rather than a clipped report.
40|D|Give Lil's incredulous child comparison complete natural speech.
43|R|Retain the plea, bring-here instruction and crucial one-day borrowing limit; no permanent surrender is claimed.
46|D|Restore the New World rumor and personal counting-on-you appeal in complete speech.
@296
18|R|Retain Lil's frustrated location question and the New World's size.
23|D|Correct the obsolete Constantinople dialogue name to source/current town Istanbul and restore Lil's personal delivery reminder.
39|D|Restore the natural found-it-yet question with the full bound wristband name.
@297
5|R|Retain the discovery thanks and exact one-day wait request.
13|R|Retain the emperor's delight, contact's saved standing and generous payment, naturally phrased without inventing a title.
16|R|Retain the precise25,000-coin reward receipt.
40|D|Correct the town name to native Istanbul and give the small market-share increase a clear complete system notice.
51|R|Retain the friendly local-information offer and natural just-ask invitation.
54|R|Retain the figurative real-gem praise for a ruins site and offer of guidance; no actual gemstone item is promised.
@298
6|D|Correct the stale Constantinople name to source/current Istanbul in the guild message.
'''


def main():
    out = ROOT / 'decisions_B293_B298_v1.txt'
    assert not out.exists()
    lines = [line for line in DECISIONS.splitlines() if line.strip()]
    assert sum(not line.startswith('@') for line in lines) == 121
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    save(ROOT / 'contextual_review_scope_B293_B298_v1.json', dict(records=121, complete_exchanges=6,
        whole_clean_andcurrent_exchanges_compared=True, individual_findings_andretention_reasons_saved=True,
        source_names_terms_fresh_display_andfinal_gates_pending=True, new_credit=0, full_goal_complete=False))


if __name__ == '__main__':
    main()
