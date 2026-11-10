"""Individual cave, elder and Angkor comparisons; final gates remain pending."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save

ROOT = Path('work/Lil361_B283_B298_clean_20261110')
DECISIONS = r'''@288
S24_0|D|Restore the danger of aimless wandering, rather than replacing that specific warning with only map safety.
S24_46|R|Retain the reserved warning about wandering blindly; it naturally conveys lack of direction in the jungle.
S24_98|R|Retain the casual emphatic danger warning and Admiral address.
S24_156|R|Retain the feminine map-and-getting-lost warning; it preserves this alternative's specific concern.
S24_216|D|Render the rough voice's reckless-life warning as a natural death-wish idiom rather than a bare suicide assertion.
S24_270|R|Retain the older voice's plain warning against aimless wandering.
S24_322|R|Retain the childish refusal and map complaint; the imperative plea fits the source's whining.
S24_384|D|Restore the older formal register, distinct from the identical older conversational wording.
37|D|Make Lil's plan to stay and rest a complete personal thought, retaining snakes, bugs and reluctance.
S606_0|R|Retain the natural morale warning and direct Admiral address.
S606_52|D|Restore the reserved companion's explicit Admiral address in the incredulous objection.
S606_82|R|Retain the idiomatic who-will-lead question and its command concern.
S606_120|R|Retain the feminine objection and clear explanation that someone must lead.
S606_192|D|Restore the rough voice's direct address and conversational incredulity.
S606_220|R|Retain the older voice's measured prediction of lower morale.
S606_268|R|Retain the child's short emphatic plea for the Admiral to join them.
S606_302|D|Preserve the older formal unheard-of objection without substituting only a blunt absurd judgment.
69|R|Retain the natural FI objection, actual admiral role and insistence that she come.
75|D|Restore Lil's petulant capitulation and repetition, rather than making her sound newly eager to lead.
86|R|Retain the casual reassurance and come-along instruction without inventing a position behind a particular companion.
92|R|Retain the pitch-dark cave observation and impulsive turn-back suggestion.
S1270_0|R|Retain the complete polite refusal and need to enter; it matches the independent wording exactly.
S1270_40|R|Retain the reserved succinct forward cue as a natural response to turning back.
S1270_66|R|Retain the casual stop-joking rebuke and urgent entry instruction.
S1270_108|R|Retain the feminine joking rebuke and direct Admiral invitation.
S1270_156|D|Restore the rough impatient get-moving voice, rather than implying the return route is literally unavailable.
S1270_194|R|Retain the older companion's firm dismissive response and shared entry cue.
S1270_234|D|Restore the child's explicit fear and need to proceed in complete spoken English.
S1270_302|R|Retain the older formal request and hesitant invitation to enter.
122|R|Retain the stammer and comic expectation that Lil should be encouraging them; the quoted line works in context.
128|D|Use Lil's hesitant informal agreement rather than the more formal yes.
140|R|Retain the natural FI question that exposes Lil's fear of caves.
144|R|Retain the stammered denial and approved Camille name; the wording fits Lil's defensive reaction.
150|R|Retain the muttered darkness complaint; its unfinished quality is natural under her breath.
169|R|Retain Mikhail's excited opportunistic thought without inventing what he intends to do.
172|T|Render humming as a vocal sound and familiar flirtatious address, preserving FI exactly without inventing an established relationship.|Hmm-hmm-hmm... Sweet FI...
175|R|Retain the pleased non-specific reaction without making the innuendo explicit.
179|R|Retain the stammered Mikhail address and unfinished my objection; it already preserves the joke without a body part.
182|D|Restore the unexpectedly polite apology that makes Mikhail's realization comic.
191|R|Retain the animal growl without identifying the creature before its reveal.
S2146_0|D|Replace the compressed bad-feeling note with a natural uneasy report of an unspecified presence.
S2146_32|D|Restore the older formal ominous feeling without asserting a real supernatural omen.
S2146_62|D|Restore the casual companion's expressed bad feeling, rather than reducing it to uh-oh.
S2146_92|D|Give the feminine voice a natural uncertain presence question and uneasy reaction.
S2146_126|D|Keep the rough voice's certainty of a presence and explicit bad feeling in complete speech.
S2146_166|D|Restore the older voice's spoken uneasy observation rather than note fragments.
S2146_198|R|Retain the child's hesitant sense of a presence and personal unease; the pauses work here.
214|D|Restore the source speaker's stammered appearance cry; dynamic identity remains conditional.
C2436_0|R|Retain the exact clear attack command and menu index.
C2436_1|R|Retain the exact clear escape command and matching menu order.
229|R|Retain Lil's frightened cry and immediate gunfire order.
233|D|Render the creature's cry as an animal vocalization rather than the English stage-direction word Roar.
237|R|Retain the effective cry of pain or alarm without adding an injury or actor identity.
241|R|Retain Lil's surprised agility observation.
S2592_0|D|Restore complete phrasing, explicit gunfire and the high friendly-fire risk without assigning every companion male identity.
S2592_72|D|Preserve the reserved voice's incomplete risk explanation and cramped space, with gender-neutral own people.
S2592_136|D|Give the casual voice a natural complete warning about possibly shooting companions.
S2592_200|D|Preserve the feminine objection and possible friendly-fire consequence in natural connected speech.
S2592_274|D|Restore the rough voice's emphatic consequence and natural tight-space warning.
S2592_332|D|Restore the older voice's claim that safe shooting is impossible in the cramped space.
S2592_400|D|Give the childlike Admiral warning a natural clause rather than a clipped space label.
S2592_462|D|Restore the older formal voice and especially high friendly-fire risk.
266|D|Connect increasing injuries to Lil's decision to use swords in natural spoken English.
S3254_0|D|Render breathlessness as vocal sounds and use managed rather than the stiffer somehow report.
S3254_32|D|Restore the reserved managed-to-defeat report without adding how narrowly it was achieved.
S3254_52|D|Preserve the panting casual voice's tentative belief that it is defeated rather than only a detached question.
S3254_86|D|Keep the feminine tentative defeat report with natural breath sounds.
S3254_120|R|Retain the rough triumphant defeat declaration.
S3254_134|D|Render the older voice's heavy breathing as a vocal reaction and keep hard-won success.
S3254_166|R|Retain the childlike Mr. Tiger personification and impressed observation after finally winning.
S3254_208|D|Restore the older formal victory report with natural breath sounds.
300|D|Restore the apparent-injury qualification while preserving that quite a few people were injured; no deaths or count.
S3558_0|D|Restore the polite voice's tentative inference about hunger and actual absence of pursuit.
S3558_44|R|Retain the explicit seems qualification and lack of pursuit; the source inference is clear.
S3558_92|R|Retain the casual inference from lack of pursuit rather than reading it as objective animal knowledge.
S3558_158|R|Retain the feminine relieved inference and explicit relief that it is not chasing them.
S3558_226|D|Restore the rough voice's register and marked inference from absence of pursuit.
S3558_300|D|Restore the older voice's explicit reasoning from no pursuit to probable lack of hunger.
S3558_364|D|Restore the child's tentative hunger assessment and observed no-chase report.
S3558_418|R|Retain the older formal seems qualification and clear absence of pursuit.
325|D|Replace the clipped safe report with Lil's relieved spoken reaction, without claiming no one was hurt.
335|R|Retain the light discovery and natural celebration of the cave exit.
@289
6|R|Retain the friendly FI greeting and welcome.
9|R|Retain the hostess's conversational negative answer about nearby ruins; no omniscient absence is claimed.
12|D|Restore a natural addressed question and the actual ancient-kingdom temple, without invented kinship.
15|R|Retain Lil's blunt identity question; it matches the independent draft exactly.
19|D|Restore that he is an elder from a nearby village, rather than implying he is this town's elder.
30|D|Give the embarrassed apology and FI instruction a natural conversational flow.
36|R|Retain the elder's forgiving chuckle and no-harm-done response.
39|R|Retain his confidence and deliberately unfinished qualification.
43|R|Retain Lil's exact echo of But so it responds to the retained preceding wording.
47|R|Retain the evasive never-mind dismissal and chuckle; adding a new warning would spoil the exchange.
50|R|Retain Lil's brief puzzled assessment of the encounter.
@290
5|D|Give Lil's frustrated inability to solve the Angkor riddle connected speech rather than disconnected no-good notes.
9|R|Retain the natural recollection and question; the quote's me is supported by the entity's complete B292 instruction and preserves the recurring pure-new-star motif.
13|D|Remove an unsupported male pronoun for the unseen entity while preserving gold/sun, silver/moon and Lil's recap.
17|T|Keep the established riddle quotation and sequence without assigning a gender to the entity.|Right. Then it said, "Yet a star's light remains unknown to me."
21|R|Retain the natural rare-metal hypothesis as a question, not a solved fact.
30|R|Retain the Admiral address, bound Alchemy Book title and reportedly unseen element.
34|R|Retain Lil's excited reaction; it exactly matches the independent draft.
38|D|Restore a complete reported-knowledge sentence and New World journey without inventing a mode of travel.
42|D|Express Lil's reasoning and eager certainty naturally rather than clipped clue notes.
46|D|Restore platinum as the metal long sought, without the added claim that a search may now be over.
50|R|Retain Lil's excited acceptance despite not knowing what platinum is; it suits her impulsive reasoning.
54|R|Retain the natural book reminder and bound item title.
57|R|Retain recognition followed by the practical load-aboard instruction.
61|D|Restore the source's tentative personal recollection about southern African mining.
@291
5|R|Retain the idiomatic stumped complaint and named Angkor riddle.
8|T|Keep the successful recurring riddle wording, but replace the note-like Meaning with a natural companion question.|"Adorn me in a new star's pure glow"... What could it mean?
11|D|Give Lil's gold/sun and silver/moon confirmation a complete natural question.
14|T|Preserve the affirmative recollection without assigning the unseen entity a gender.|Yes, that's what it said.
18|D|Restore the natural direct question about the star rather than a compressed noun fragment.
22|R|Retain the natural puzzle explanation and conditional solution; certainty is not overstated.
25|D|Remove the entity's unsupported male pronoun and restore Lil's reasoning as a tentative rare-metal question.
28|R|Retain the tentative platinum suggestion.
37|R|Retain Lil's natural unfamiliarity question about platinum.
40|D|Restore the source's should-be-mined uncertainty while keeping the book prerequisite.
44|R|Retain the direct book question; it exactly matches the independent draft.
48|T|Preserve vague alchemy recollection, hearsay and elapsed decade without assigning the unnamed author a gender or an exact year.|Something about alchemy. I hear it was written by someone who went to the New World over a decade ago.
52|D|Restore Lil's reflective New World phrase rather than an unpunctuated label.
58|R|Retain the enthusiastic recognition of platinum from the alchemy book and proposed solution.
62|R|Retain the practical decision to bring platinum aboard.
65|R|Retain the African source and merchant's natural purchase invitation.
@292
13|R|Retain the existing literary pure-new-star command and consistent riddle motif; it is more natural than the independent human paraphrase.
17|R|Retain the reflective light clue and natural question about what to bring.
31|R|Retain the idiomatic hauling grunt without inventing cargo quantity or speaker action beyond the effort.
35|D|Make Lil's delivery and uncertain question complete conversational speech.
42|D|Keep the wordless surprise using matching ASCII punctuation instead of mixed-width glyphs.
46|D|Give the entity's wise-visitor address natural elevated syntax while preserving the pure new-star light.
50|R|Retain the stylized command, storm at sea and subsequent peaceful sleep; the source elevated voice supports thy.
56|R|Retain Lil's casual observation of the coin's age without inventing its item identity.
68|R|Retain the companion's natural question about the mysterious words.
72|R|Retain Lil's ignorance and subjective impression that the voice sounded pleased.
76|R|Retain the companion's confident expectation of future usefulness as character belief, not a system guarantee.
'''


def main():
    out = ROOT / 'decisions_B288_B292_v1.txt'
    assert not out.exists()
    lines = [line for line in DECISIONS.splitlines() if line.strip()]
    assert sum(not line.startswith('@') for line in lines) == 134
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    save(ROOT / 'contextual_review_scope_B288_B292_v1.json', dict(records=134, complete_exchanges=5,
        whole_clean_andcurrent_exchanges_compared=True, individual_findings_andretention_reasons_saved=True,
        source_names_terms_fresh_display_andfinal_gates_pending=True, new_credit=0, full_goal_complete=False))


if __name__ == '__main__':
    main()
