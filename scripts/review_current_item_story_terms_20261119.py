"""Review the full exchanges around three groups of inventory-name mismatches."""
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts import scan_current_item_story_terms_20261119 as scan
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = pairing.base, pairing.native, pairing.stage, scan.parent
ROOT = scan.ROOT
SOURCE, OUTPUT = ROOT / "selected_exchanges.json", ROOT / "contextual_review.json"
BLOCKS = ((214, 219), (), (61,), ())
CONTEXT = ("", "", "", "")
paired = SimpleNamespace(base=base,native=native,stage=stage,parent=parent,ROOT=ROOT,SOURCE=SOURCE,BLOCKS=BLOCKS)
SCENES = {
    (0, 214): "A sailor being pursued thrusts a book into Rafael's hands. Charles encourages Rafael to keep it, then reveals he wants to read it himself.",
    (0, 219): "Emilio asks for a weapon because he wants to get stronger. Rafael teases him, agrees to look only if he feels like it, and never promises to give him the axe.",
    (2, 61): "Clifford holds a companion hostage and demands the Proofs Lil has gathered. Their possible alliance changes the accusation. Lil chooses Camille's life, and conditional notices identify which specific clues are taken.",
}
NOTES = {
 (0,214): """5|A stranger calls to Rafael.|His abrupt address fits someone in a hurry.|
9|Rafael reacts to being addressed.|The short question is natural.|
14|The sailor offers the object and says to use it however Rafael likes.|Keep the imperative and free offer.|
17|Rafael is taken aback.|The one-word question sets up the interruption.|
22|The pursuer recognizes the sailor and orders him to stop.|The sharp command makes the pursuit clear.|
25|Rafael reacts with surprise.|Keep the original punctuation beat.|
30|The sailor calls goodbye as he leaves.|The informal farewell contrasts with the pursuer.|
34|The pursuer repeats the order.|Keep the urgent repetition.|
38|Rafael stammers and asks him to wait.|The existing stutter fits Rafael's surprise.|
43|Charles asks what the admiral is doing.|Keep the form of address and ordinary question.|
47|Someone forced the thing on Rafael.|Shoved into my hands describes the abrupt handover naturally.|
52|Charles asks what it is.|The question follows Rafael's account.|
56|Rafael thinks it is a book.|Keep the provisional identification.|
61|Charles reads the glassmaking reference book's title.|Name it as the item menu does and keep his thoughtful pause.|Let's see... the Glassmaking Guide.
64|Charles suggests keeping it.|His casual suggestion sets up his motive.|
67|Rafael begins to object.|The unfinished thought leaves Charles room to press the idea.|
72|Charles argues that one might as well accept a freely offered item.|The existing reason fits his apparently practical advice.|
75|Charles asks to see it afterward.|The polite request exposes his motive.|
79|Rafael realizes this was Charles's aim all along.|Keep the restrained punch line.|""",
 (0,219): """5|Emilio calls the admiral and says he wants a weapon.|Keep the drawn-out address and direct request.|
8|Rafael is surprised.|The short reply suits the unusual request.|
13|Emilio wants a weapon so he can get stronger too.|Make the purpose sound like an eager explanation.|I want to get stronger, too. That's why I want a weapon.
16|Rafael teases Emilio for wanting something other than food and asks the name.|Keep the tease and follow-up question together in the same turn.|
20|Emilio names the axe.|Use the inventory name in his excited reply.|The Minotaur Axe!
24|The name sounds strong, and Rafael asks where it is.|Keep his lightly amused reaction and practical question.|
28|Emilio only knows the Minotaur was said to have been on the island long ago.|Keep the hearsay, island and lack of other clues.|
32|Rafael finds the clue sparse and says he might look if he feels like it.|The existing condition sets up Emilio's premature celebration.|
36|Emilio cheers.|Keep his immediate enthusiasm.|
40|Rafael stresses again that looking is conditional.|Keep his correction and short question tag.|
45|Emilio cheers anyway.|Let him acknowledge the condition and celebrate in spite of it.|I'm still cheering!
49|Rafael reminds him he did not promise to give him the weapon.|Keep the distinction between looking and giving.|
53|Emilio groans in disappointment.|The short reaction lands the joke.|""",
 (2,61): """6|Clifford stops the group.|The abrupt order interrupts the scene.|
16|A crew member protests being seized.|Keep the startled cry and command to let him go.|
21|Camille protests, then recognizes someone.|The broken recognition fits the sudden reveal.|
35|An ally demands an explanation.|His formal indignation differentiates his voice.|
42|Lil recognizes Clifford and asks what is happening.|Keep the astonishment and exact identity.|
45|Clifford expresses relief at the death of people he considered pests.|The harsh line preserves his callous tone.|
48|Clifford thanks Lil for her earlier cooperation.|Keep the live name and his unsettling politeness.|
52|He says making the request after her help is painful.|His hesitation sets up the demand.|
55|He demands the collected Proofs in exchange for the hostage's life.|Keep both his demand and explicit condition.|
59|Lil calls the hostage-taking cowardly.|Her anger should remain immediate.|
70|A crew member protests that this is unlike Clifford.|The current protest leaves the surprise intact.|
81|Lil invokes their shared alliance and cooperation.|Keep the ally branch's appeal to their history.|
85|Clifford says that is in the past.|The abrupt dismissal follows the appeal.|
91|In the other alliance branch Lil calls him out for drawing a sword on an ally.|Keep the present alliance and accusatory tone.|
95|Clifford ends the alliance immediately.|The precise timing matters to this branch.|
102|Lil wonders if he intended this from the start.|Keep her dawning realization.|
106|Clifford admits that was his plan.|His bare apology preserves the coldness of his admission.|
118|A crew member realizes they were all deceived.|The quieter reaction follows Clifford's admission.|
125|Lil responds with dismay.|The brief line lets the betrayal land.|
129|Clifford admits he wanted the Proofs too.|The shorter name is clear after his explicit demand.|
133|The Crown tasked him with watching Spain and he cannot move freely.|Keep both his duty and the resulting constraint.|
137|He needed someone else to gather the Proofs and chose Lil.|The current line makes his manipulation plain.|
149|A crew member condemns how he used Lil.|Keep the outrage without assigning a new action.|
155|Lil says he used her completely and she cannot forgive him.|The angry direct address works after his explanation.|
159|He claims his conscience bothered him but says he had no choice.|Keep the reference to their alliance and preserve this as his own justification.|
170|Camille challenges his invocation of conscience.|Keep the sharp question and broken follow-up.|
177|Clifford asks Lil to understand because he thinks they share a dream.|The live name and tentative assumption work together.|
181|Lil scoffs at the idea that their dreams match.|The dismissive question and reply fit her anger.|
184|Clifford accuses Lil of gathering Proofs to dominate all seas.|The current accusation stays his interpretation of her motives.|
187|Lil denies that aim outright.|The short emphatic denial contrasts with Clifford's long accusation.|
191|Lil starts to explain her concern for people in need, then refuses to share her dream.|Keep the deliberate interruption and the change from vulnerability to anger.|
194|He regrets their aims differ but still intends to take the Proofs.|The calm closing demand restores his leverage.|
198|He would rather spare her companion and asks her to surrender them.|Keep the coercion beneath his appeal.|
201|Lil yields after a pause.|The brief assent fits the weight of her choice.|
213|Camille begs Lil not to hand them over.|Keep the live address and urgent objection.|
216|Lil says Camille's life matters more.|The existing response states her priority plainly.|
222|Clifford approves the choice and accepts the items.|Keep the cool courtesy before the notices.|
238|A notice reports the loss of the Thales Paper Map.|Use its exact inventory label and keep the existing loss notification.|Thales Paper Map was stolen!
250|A notice reports the loss of Ullr's Bow.|The item name already matches and the loss is clear.|
270|A notice reports the loss of the Periander Stone Map.|Use the exact inventory name for the item taken.|Periander Stone Map was stolen!
282|A notice reports the loss of the Aksum Gold Seal.|Keep the matching name and complete notice.|
302|A notice reports the loss of the Solon Leaf Map.|Align the item name with the list the player can check.|Solon Leaf Map was stolen!
314|A notice reports the loss of the Rigveda.|The approved name and plain notice already match.|
334|A notice reports the loss of the Cleobulus Cloth Map.|Match the inventory name and keep the fixed loss statement.|Cleobulus Cloth Map was stolen!
346|A notice reports the loss of Cambyses' Crown.|Keep the matching title and the direct system message.|
366|A notice reports the loss of the Chiron Bamboo Map.|Use the displayed item title and preserve the loss notification.|Chiron Bamboo Map was stolen!
378|A notice reports the loss of the Qin Palace Lamp.|Keep the matching title and complete notice.|
410|A notice reports the loss of the Bias Coin Map.|Make the notification name agree with the inventory.|Bias Coin Map was stolen!
425|A notice reports the loss of the Kediri Talisman.|Use the inventory title so the missing item is identifiable.|Kediri Talisman was stolen!
445|A notice reports the loss of the Pittacus Blade Map.|Keep the system voice and use the same title the inventory used.|Pittacus Blade Map was stolen!
457|A notice reports the loss of the Crystal Skull.|The existing title and action already match.|""",
}


def main():
    # The term scan shared this directory. Prepare the same source packet in
    # an isolated folder because the pairing workflow requires a fresh path.
    source_root = ROOT / "paired_selected"
    if not SOURCE.exists():
        scope = vars(pairing) | dict(parent=parent, ROOT=source_root, BLOCKS=BLOCKS, CONTEXT=CONTEXT)
        FunctionType(pairing.main.__code__, scope)()
        (ROOT / SOURCE.name).write_bytes((source_root / "paired_source.json").read_bytes())
    packet = base.load(SOURCE)
    scoped = {(g["route"],g["block"]):g for g in packet["groups"]}
    assert scoped.keys() == NOTES.keys()
    exchanges, edits = {}, {}
    for (route, block), prose in NOTES.items():
        rows = [line.split("|") for line in prose.splitlines()]
        assert [int(n) for n, *_ in rows] == [r["source_record_index"] for r in scoped[route,block]["records"]]
        exchanges[route,block] = 0,"\n".join(f"{meaning}|{reason}" for _,meaning,reason,_ in rows)
        for n, _, _, english in rows:
            if not english:
                continue
            title = english.removesuffix(" was stolen!") if route == 2 else {61:"Glassmaking Guide",20:"Minotaur Axe"}.get(int(n))
            edits[route,block,int(n)] = english, (title,) if title else ()
    implementation = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n                meaning, reason = note.split("|", 1)',
        'context=group["context"], source_meaning=note, localization_note=note,':
            'context=SCENES[route, block], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | dict(exchanges=exchanges, EDITS=edits)
    exec(compile(implementation, __file__ + "::item_story_review", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
