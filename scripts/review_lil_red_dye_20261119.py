"""Review Lil's alliance, Amsterdam handoff and map discovery as linked exchanges."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_current_item_story_terms_20261119 as parent
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = parent.base, parent.native, parent.stage.stage
ROOT = Path("work/lil_red_dye_source_20261119_v1")
SOURCE, OUTPUT = ROOT / "connected_source.json", ROOT / "contextual_review_v2.json"
BLOCKS = ((), (), (26, 129, 130, 131), ())
paired = SimpleNamespace(base=base, native=native, stage=stage, parent=parent,
                         ROOT=ROOT, SOURCE=SOURCE, BLOCKS=BLOCKS)
SCENES = {
    26: "After dinner, Clifford proposes an alliance to contain Spain. Lil challenges his credibility, and he offers the Red Dye while leaving the New World to his own campaign.",
    129: "Lil and Camille consider Clifford's directions in Amsterdam. The conversation shifts to a Dutch researcher's polder proposal, his funding obstacle and Lil's thoughts of home.",
    130: "Lil brings Clifford's letter to the Amsterdam barkeep. His confusion turns to recognition, and Lil receives the item she believes can decipher the map.",
    131: "Lil tests the Red Dye on the Old Parchment. Camille and his companions respond to the apparently blank surface as the map emerges.",
}
NOTES = {
 26: """454|Clifford returns to the main topic.|Keep the direct transition after Lil changes clothes.|
461|Spain appointed Valdes, one of its strongest naval commanders.|Keep his name, role and Clifford's alarm.|
472|The companion has also heard the news.|The brief confirmation answers Clifford's question.|
479|Lil is worried Spain's already powerful Armada will get stronger.|Keep the practical concern behind her reaction.|
483|Clifford shares that concern.|His agreement sets up the proposal.|
487|Lil wonders why the reportedly invincible Clifford is worried about Spain.|Keep her skeptical question and reference to reputation.|
490|Clifford hesitates because of Valdes specifically.|The unfinished reply leaves his concern audible.|
493|Lil realizes how formidable Valdes is.|The question follows Clifford's hesitation.|
497|Clifford proposes they join forces.|The plain offer starts the negotiation.|
500|Lil asks why he wants to work with her group.|Keep her surprise and question.|
504|Cooperation would make Spain less willing to attack.|The explanation and invitation to agree both fit.|
516|A companion sees merit but remains hesitant.|Keep the unfinished qualification.|
523|Lil doubts her ability to defeat the Spanish navy.|Her hesitation sets up Clifford's clarification.|
527|Clifford has not asked them to defeat it now.|Keep his reassurances distinct from his later ambition.|
530|Lil asks what he is proposing instead.|The brief challenge keeps the pace.|
534|Clifford asks her to join him in checking Spain's movements.|The existing terms make the defensive aim clear.|
537|Lil asks whether that is all.|The short question suits her surprise.|
541|They can contain Spain while each expands in other regions.|The conversational explanation preserves simultaneous expansion.|
544|Lil realizes they can sail elsewhere instead of staying in the North Sea.|Keep the specific examples of Africa and India.|
555|A companion sees the sense in the plan.|The short aside fits the original voice.|
562|Clifford agrees.|His brief confirmation leads into the route details.|
566|He will follow English policy west while Lil follows Dutch policy south through Africa to Asia.|The route directions and national policies already match.|
569|They will build up strength over time.|The unfinished sentence gives Lil room to finish the thought.|
573|Lil realizes they may someday defeat the Armada.|Keep the future possibility and her excitement.|
576|Clifford compliments her quick understanding.|The familiar reply suits his persuasion.|
580|Lil still hesitates.|Keep the brief interruption.|
584|Clifford asks whether there is a problem.|His casual question gives her room to challenge him.|
588|Lil is unsure she can trust him.|The existing hesitation sets up his personal defense.|
592|Clifford invokes being an English gentleman.|Keep this as his own claim to credibility.|
595|Lil rejects that defense.|The blunt objection sounds like her.|
607|A companion says anyone can make such a claim.|The formal objection backs Lil's skepticism.|
614|Clifford offers the Red Dye as a gesture of friendship.|Use the inventory title and keep him offering it as a gesture during negotiation.|Then how about the Red Dye as a token of friendship?
617|Lil repeats dye and asks what it is.|Keep the short puzzled echo.|
621|Clifford says the dye supposedly deciphers a map, then asks if she will join forces.|Keep the rumored function and the repeated offer distinct.|
633|A companion thinks they will have to trust him for now.|The qualified agreement preserves caution.|
640|Lil agrees reluctantly.|Keep the pause and brevity.|
644|Clifford welcomes the alliance.|His upbeat response contrasts with Lil's reluctance.|
647|He wants them to leave his New World opponents alone.|Keep the hostile idiom and request that they not engage on their own.|
650|The Amsterdam barkeep has the Red Dye, and Clifford directs them to the tavern.|Use the inventory title and shared occupational label. Keep the destination explicit.|The barkeep at the Amsterdam tavern has the Red Dye. Go see him.
654|Lil agrees and warns she will not forgive a betrayal.|The threat carries the tension into the later story.|
""".rstrip(),
 129: """12|Lil doubts whether the item she was sent to Amsterdam to find exists.|Use the inventory name and connect her doubt to Clifford's directions.|Clifford sent us to Amsterdam, but does the Red Dye really exist?
24|Camille suggests trusting what they were told.|Answer Lil directly and keep Camille's quiet optimism.|I think we can take his word for it.
36|The researcher interrupts, then asks if Lil is Dutch.|The sudden recognition starts a distinct conversation.|
39|Lil confirms her nationality and asks why.|Keep the brief clarification.|
43|The researcher says he is Dutch as well.|The light exclamation fits his greeting.|
47|He thinks a fellow Dutch person may understand.|The hesitant opening motivates his appeal.|
50|Lil reacts with puzzlement.|Keep the beat before he makes his case.|
54|He wonders if more good land would help poor people.|Keep the question and his stated purpose.|
57|Lil remembers the hardship in her own poor hometown.|The personal answer identifies why she listens.|
61|He grew up in a poor farming family and wondered how to add usable land.|Keep both his personal background and his goal.|
64|Lil incredulously repeats the proposal to make land.|The echo preserves her surprise.|
68|He suggests turning sea into land.|The excited explanation follows her question.|
72|Lil asks how.|Keep the brief request for an explanation.|
76|He plans to enclose coastal water with dikes, then pump it out.|The existing sequence preserves his proposal and result.|
79|He calls the method a polder.|The term stays while he introduces it.|
82|Lil admires the idea and urges him to start.|Her enthusiasm makes the funding setback matter.|
85|He would like to start but lacks funds.|Keep the hesitation and practical obstacle.|
88|Lil asks the cost.|The short question keeps the exchange moving.|
92|He estimates one million gold.|The exact approximate amount is clear.|
96|Lil reacts to the sum and suggests seeking government help.|Keep her surprise and practical suggestion.|
99|He has asked and aid still falls far short.|The current answer preserves the efforts and shortfall.|
103|Lil sympathizes.|The concise response leaves space for him to persist.|
107|He will not give up and hopes someone will invest.|Keep his determination and confidence as aspirations.|
111|Lil admires his determination and encourages him.|Her supportive words follow his resolve.|
123|A companion encourages him and hopes the dream comes true someday.|The formal encouragement fits alongside Lil's.|
129|The researcher thanks them.|Keep the brief sincere response.|
133|Lil wonders whether a polder could improve life back home.|Keep the unresolved question and her personal stake.|""",
 130: """5|Lil asks the barkeep about Clifford's gift.|The fragment conveys her tentative request.|
14|The barkeep asks what gift she means.|Keep the conversational repetition before she shows the letter.|
17|Lil produces the letter.|The trailing fragment fits the handover.|
21|The barkeep reads the letter, recognizes the recipient and asks her to wait.|Give the recognition a natural spoken line and let the letter show why he knows her.|Let's see... Ah, so you're the one. Wait here a minute.
25|The barkeep presents something.|The short offer works with its original scene cue.|
31|He confirms Clifford spoke to him and presents the item she expects.|Keep the confirmation and question.|
34|Lil realizes the gift is meant to decipher the map.|Keep her curious tone and the key metaphor.|""",
 131: """5|Lil thinks the Old Parchment is a map to the Proof.|Keep the known title and the unproven inference.|
15|Camille sees plain paper yet suspects there is a trick.|Keep his curiosity and the possibly hidden mechanism.|Looks like plain paper, but there has to be more to it...
20|A companion observes there is no writing and asks how it works.|Keep his blunt reaction after Camille's suspicion.|
26|Lil asks whether she can use the Red Dye.|Keep the exact item title and speculation.|
30|Lil reasons that the dye is the only possibility and becomes certain.|The existing escalation matches her quick confidence.|
42|A companion asks how she will use it.|The short question sets up her demonstration.|
57|Camille asks Lil to wait when he realizes what she's about to do.|Keep the live name and startled interruption.|
64|Lil says she will put the dye onto the parchment.|Make the physical action clear as she demonstrates it.|I'll pour it on the parchment!
76|A companion sees something appear.|The abrupt discovery follows Lil's action.|
82|Lil celebrates getting the map to the North Sea Proof of Conquest.|Keep her pride, region and distinction between map and Proof.|
92|Camille praises Lil and urges searching for the Proof.|Keep the live name and immediate response.|
98|A companion praises her and suggests finding the Proof.|Keep his different voice in the alternate response.|
105|Lil boasts that the North Sea is hers.|Keep the triumphant claim as part of her character.|""",
}


def main():
    intake, handoff = (base.load(path) for path in (ROOT / "paired_source.json", ROOT / "paired_handoff/paired_source.json"))
    for key in ("clean_sha256", "candidate_sha256", "profile"):
        assert intake[key] == handoff[key]
    groups = sorted(intake["groups"] + handoff["groups"], key=lambda r: r["block"])
    assert [g["block"] for g in groups] == list(BLOCKS[2])
    base.save(SOURCE, intake | {"groups": groups})
    exchanges, edits = {}, {}
    for group in groups:
        block = group["block"]
        selected = NOTES[block].splitlines()
        rows = [line.split("|") for line in selected]
        start, = (i for i,r in enumerate(group["records"]) if r["source_record_index"] == int(rows[0][0]))
        indices = [r["source_record_index"] for r in group["records"][start:]]
        assert [int(n) for n,*_ in rows] == indices
        exchanges[2,block] = (start,"\n".join(f"{meaning}|{reason}" for _,meaning,reason,_ in rows))
        for ident,_,_,text in rows:
            if text:
                phrases = ("Red Dye",) if "Red Dye" in text else ()
                if block == 129 and int(ident) == 12:
                    phrases = ("Clifford sent us to Amsterdam,", "does the Red Dye really exist?")
                edits[2,block,int(ident)] = text, phrases
    source = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n                meaning, reason = note.split("|", 1)',
        'context=group["context"], source_meaning=note, localization_note=note,':
            'context=SCENES[block], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | dict(exchanges=exchanges, EDITS=edits)
    exec(compile(source, __file__ + "::red_dye_review", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
