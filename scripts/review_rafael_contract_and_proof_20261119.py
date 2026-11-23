"""Review Rafael's early trade lesson and four related story exchanges."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as source_workflow
from scripts import register_item_category_labels_20261119 as parent
from scripts import review_story_short_phrase_wraps_20261119 as review_workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = source_workflow.base, source_workflow.native, source_workflow.stage
ROOT = Path("work/rafael_contract_and_proof_20261119")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v5.json"
BLOCKS = ((25, 41, 45, 86, 120), (), (), ())
CONTEXT = ("Rafael's wake at sea, Proof explanation, town trade contracts, cannon inventor and the northern map account.", "", "", "")
paired = SimpleNamespace(parent=parent, base=base, native=native, stage=stage, ROOT=ROOT, SOURCE=SOURCE)
SCENES = {
    25: "After a victory, Clau boasts, while Manuel grieves the lives lost at sea. His three-part poem gives Rafael something to set to music and ends with a wish to welcome others.",
    41: "Clau asks Hans how to find Africa's Proof of Conquest. The crew offers competing meanings of power. Hans explains why the townspeople's trust matters and laughs at the scale of the task.",
    45: "Julio takes Rafael to Ceuta's Market. He explains how to sell the Lisbon goods and how to arrange future contracts, then the game shows the fleet's market share.",
    86: "An explosion interrupts Julio's plans for rum. A local leads the crew to Charles, eager to see him leave. Charles is baffled by the visitors until he sees how sailing and science fit together.",
    120: "A stranger approaches Rafael and Hans about the map. Hans vouches for Rafael, the stranger recounts the clan's flight, then gives directions and warns Rafael about the journey and the Proof.",
}
EXCHANGES = {
    (0, 25): (0, """Rafael confirms the victory.|The simple statement lets Clau supply the boast.
Clau calls it easy.|The quick laugh and boast fit his confidence before Manuel speaks.
Manuel grieves the people lost and restates it as a return to the mother sea.|He corrects himself quietly. Keep the metaphor and let his grief interrupt the celebration.
Rafael addresses Manuel, puzzled.|The incomplete question gives Manuel room to continue.
Manuel suggests consoling the spirits of the dead.|Honor is a natural invitation to commemorate the fallen before he recites the poem.
Rafael is confused.|The three question marks keep the silent reaction.
Manuel compares sea and mother, then hears his mother's distant heartbeat in familiar ripples.|Keep the repeated invocation and the sound image together. The previously short second page interrupts the first stanza.
He repeats the refrain and says some foreign lands use the same sound and written sign for both.|Keep the report tentative and preserve both the written and spoken resemblance.
He repeats the refrain and says the bond with both endures throughout life.|The existing last stanza closes the quotation and keeps the lifetime bond.
Rafael calls him a poet and asks if he can set it to music later.|The compliment and the request for permission sound affectionate without adding a relationship.
Clau agrees, admits he thought Manuel was just an older man who liked ships, and praises his talent.|His backhanded praise fits the quiet aftermath. Use the source's plain observation and smooth out the narrow rows.
Manuel says the sea accepts everything and hopes they can do likewise.|The simple parallel carries the poem into the closing exchange.
Rafael has no reply.|The silence is deliberate after the wish."""),
    (0, 41): (0, """Clau asks whether it is time they found a clue to Africa's Proof.|Keep the tentative challenge and the approved title.
Hans says rushing will not help.|The clipped answer gives Rafael room to ask how.
Rafael asks how they can find a clue.|The hesitant question fits his place in the discussion.
Hans says power worthy of one who would rule the seas must come first or the Proof will never turn toward them.|The existing reveal metaphor and qualification fit Hans's explanation.
Clau interprets power as having a big fleet.|The concrete example fits his voice.
Rafael offers competence as a navigator.|Keep his more personal way of thinking about power.
Arcadius offers financial power.|His short answer is one alternative in a run of guesses.
Julio wonders whether it means a large trading sphere.|The large trading network needs spoken English.
Hans says the guesses may all be right.|The existing generalization invites all the interpretations.
Rafael finds the task daunting.|A short reaction fits the accumulating requirements.
Hans adds that power alone will not suffice.|This is the pivot to the second part of the explanation.
Rafael is startled there is more.|The incredulous question gives Hans the floor.
Hans labels what follows his own theory.|His caution preserves the distinction between speculation and fact.
Hans suggests ruins around the world hold the secrets of the Proofs.|Retain his qualified belief and the worldwide scope.
Rafael repeats the word ruins, surprised.|The echo works before Hans confirms it.
Hans affirms.|One word is enough before Rafael's follow-up.
Rafael asks where the ruins are.|His plain question prompts practical advice.
Hans expects them in or near the main city of each cultural region.|Bring the answer into spoken rhythm and keep the location language together.
Clau says that still gives them no workable way to look.|The complaint balances Hans's general advice.
Hans says some residents may know and the party must first gain their trust.|Keep the tentative knowledge and give the second sentence its full phrase.
Rafael repeats the requirement of trust.|The brief echo prepares Hans's explanation.
Hans explains that ruins and old churches stand for local religion and culture, so outsiders are unlikely to be told.|The present English preserves the reason for local caution.
Hans lists requests, help for people in trouble and standing up to corrupt merchants or soldiers.|Keep all three examples and make the last sound like his spoken advice.
Clau compares it to charity.|The dry comparison sets up Hans's answer.
Hans says the necessary stature includes being able to gain many people's trust.|Present English keeps this as an aspect of the character needed to rule the seas.
Rafael says it sounds hard to become a ruler of the seas.|Echo the established idea rather than use an isolated, generic ruler.
Hans laughs and says no one has achieved it yet.|Give the laughter and confident explanation clear beats."""),
    (0, 45): (0, """Rafael wonders where Julio has gone.|The simple question works as he looks for Julio.
Julio calls Rafael over.|A short call matches the moment.
Rafael realizes Julio is at the Market.|Keep the registered Market label and the small pause.
Julio suggests selling a trade good bought in Lisbon, if Rafael has any, then adds a condition.|The current wording preserves the optional sale and the turn toward the contract rule.
Julio says a contract is needed to sell.|The rule is short and direct.
Rafael repeats the unfamiliar requirement.|The question fits a student asking Julio to explain.
Julio explains paying the local ruler a contract fee at the Palace or Governor's Office to gain trading rights.|Keep the fee and both facility names in readable phrases. The right belongs to that town.
Julio recommends arranging contracts in many towns and says the minimum fee is enough at first.|The advice should sound like Julio, with the minimum qualified to the early game.
Julio has already arranged Ceuta's contract and expects Rafael to handle the next ones.|Keep the completed favor and the shift of responsibility.
The party's share in Ceuta is 20 percent and it determines trading access to local stock.|Keep the native faction substitution, the percentage and the stock explanation.
Julio invites Rafael to sell what he wants.|Natural rhythm for an optional action after the explanation.
Rafael agrees.|The short acceptance leads out of the tutorial."""),
    (0, 86): (0, """Julio insists a sailor must have a rum in the Caribbean and urges them to the tavern.|Let his enthusiasm give way to the blast.
Julio stammers at the sound.|The short startled outburst interrupts his confident invitation.
The alarmed crew member cries earthquake, fire and the end of the world.|Let the exaggerated reactions come in a quick sequence.
Clau tells the panicked speaker to stop yelling.|The abrupt response suits his irritation.
Rafael says the blast startled him.|The simple reaction contrasts with the catastrophizing.
The local despairs of the bomb enthusiast doing it again.|The familiar, dismissive complaint sets up the nickname.
The speaker stammers in surprise at the mention of bombs.|Keep the sharp rise in alarm.
The local scoffs at the magician-of-blazing-explosions nickname Charles gave himself.|Blast Wizard sounds like the boast the local mocks and sets up Clau's reply.
Clau repeats part of the name and calls it ugly.|Keep the skeptical echo and the blunt judgment.
Rafael asks what kind of person the inventor is.|The uncomplicated question is a good opening for the explanation.
The local confirms he means eccentric Charles and says he would rather not discuss him.|Charles the Eccentric conveys the nickname without changing his given name.
Rafael is puzzled.|The short reaction prompts the explanation.
The local says the eccentric lives at the factory outside town, studies explosives and cannons, and produces the occasional nuisance.|Give the location, research and racket complete phrases. Keep the speaker's annoyance.
Rafael asks Julio if someone who makes bombs also needs to know about cannons.|The question starts the case for recruiting Charles.
Julio objects to treating bombs and cannons as the same, then allows their similarity.|Use the two beats of a reluctant concession.
The crew member draws out his calculation and predicts a large gain in combat strength.|The current line keeps his certainty and an advantage in battle.
Clau concludes the man might be useful.|The understated summary is a contrast to the grand calculation.
The local asks whether they are sailors and whether they will take Charles elsewhere.|Keep the eager shift from interest in the crew to getting Charles out of town.
Arcadius considers that being at sea would qualify as elsewhere.|The wry literal interpretation makes the exchange work.
Rafael tentatively agrees.|The short concession gives the local space to jump in.
The local almost admits they answered his wish, then hastily says Charles will help them.|Keep the near-confession and the quick cover-up. Let the break interrupt his thought while the words stay intact.
Clau remarks that things have taken an odd turn.|The casual aside fits his suspicion.
The local calls for Charles to answer him.|The unpolished question is appropriate for their familiarity.
Charles greets the older local politely and refers to their prior encounter.|Use a polite greeting without implying kinship.
The local rejects the pleasantry and complains that Charles did it again today.|A clipped dismissal and a complaint give the retort a spoken cadence.
Charles insists the experiment is not a failure, says he is close and starts another point.|Let his defense speed up and trail off when interrupted.
The local cuts him short and says he did not come to complain.|An abrupt interruption fits his efforts to get the visitors talking.
The local explains that the visitors want to talk to Charles.|The short introduction keeps the local in a hurry to leave.
Rafael greets Charles.|A plain greeting suits the abrupt introduction.
Charles wonders if he has met Rafael before.|The puzzled question preserves his distraction.
The local urges Charles to listen and assures him it must be a good offer.|The repetition of certainty shows how eager the local is.
The local leaves them to talk and bids Charles farewell.|Make the retreat brisk and natural.
Charles calls after the local.|The short attempt to stop him belongs just after the exit.
Charles decides science must be too hard for the local and excuses his lack of understanding.|His matter-of-fact tone shows that he misses the point.
Clau mutters that Charles is the person he cannot understand.|Contraction and a direct contrast fit his aside.
Charles asks whether Clau said something.|The polite check keeps the exchange moving.
Arcadius stammers a denial and tells Clau privately he said one thing too many.|Keep the private objection and the quick spoken cover.
Rafael starts to say bombs, corrects it to gunpowder and cannons, and explains why they came.|The existing false start deliberately echoes the trouble with the local.
Charles confirms his research and wonders whether they are from the Academy.|The excited switch of thought fits his reaction.
Charles decides they look neither scholarly nor like sponsors.|Give both guesses without formal syntax.
Clau objects to being judged and to the way Charles talks to them.|The quick protest fits his impatience.
Rafael apologetically asks Charles to disregard Clau and explains their invitation.|The current hedge and redirect preserve the social repair.
Rafael says they sail the world and would like his ability aboard their fleet.|Keep the recruitment pitch in Rafael's modest voice.
Charles registers that they are sailors, then changes the subject to science.|Let the shift have a clean spoken rhythm.
Rafael echoes science, confused.|The one-word question hands the conversation back to Charles.
Charles exclaims that science is wonderful.|A big declaration fits his rising excitement.
Rafael hesitates.|The tiny response conveys bewilderment.
Charles explains curiosity about what happens and firsthand experience.|The existing example preserves his teaching voice.
Charles says repeated experiments drive progress.|The short conclusion follows his example, preserving its brevity.
Arcadius responds that he supposes so.|The hesitant agreement contrasts with Charles's zeal.
Charles connects sailing to curiosity, courage and action expanding the world.|Keep the three qualities and the unfinished thought.
Charles calls the parallel wonderful and declares that sailing is science.|Put the enthusiasm and the idea into two clear spoken beats.
Rafael struggles to follow and asks if Charles will come with them.|The current line returns to the actual question without mocking him.
Charles accepts and celebrates it as a victory for science.|The enthusiastic answer lands the joke.
Clau still finds Charles incomprehensible.|The final mutter is the callback to his earlier aside."""),
    (0, 120): (0, """The stranger asks for a moment.|The polite opening fits his guarded approach.
Rafael responds with surprise and asks what he wants.|The current reply gives the stranger room to reveal why he stopped them.
The stranger knows they seek the Proof of Conquest.|Keep the approved name and the unsettling question.
Rafael asks how the stranger knows.|The quick question matches the surprise.
Hans suspects the stranger knows something about the map to the Proof.|Use a natural possessive relationship and keep the map tied to the Proof.
The stranger says he does, but cannot tell just anyone.|Use his own refusal in the first person.
Hans infers the stranger fears what a person with evil intentions would do with it.|The fear concerns the user's intentions. Keep the question and the conditional.
The stranger confirms the inference.|The terse reply suits his guarded manner.
Hans reassures him and says he has studied the Proof for years.|Keep Hans's credibility and the long study.
Hans vouches for Rafael as having the qualities of one who can rule the seas.|Keep Hans's certainty and the established meaning of the title.
The stranger pauses to consider.|The short hesitation makes Rafael's plea matter.
Rafael asks him to tell them whatever he knows.|The earnest request suits the appeal after Hans vouches for him.
The stranger agrees to tell them.|The spare assent opens the account.
The clan that guarded the map in China fled pursuit by those in power and is said to have gone far northeast.|Keep the pursuit, the distance and that this is a received account. Give the full account one page.
Rafael repeats the direction back to him.|The question emphasizes the distance just introduced.
The clan reached a northern village by an icy sea and its descendants presumably still live quietly there.|The existing explanation preserves the uncertainty and the isolated location.
Rafael repeats the location relative to China.|The brief reflection is a natural response to that detail.
The stranger directs them to the eastern coast near the base of a vast peninsula and the foot of a high peak.|Keep both landmarks and the coast together for the player.
The stranger warns an ordinary ship may not reach it and a halfhearted attempt could cost them their lives.|Preserve the warning and the uncertainty about the ship.
Rafael swallows nervously.|The internal response stays deliberately brief.
The stranger warns Rafael against handing over the Proof to anyone with evil intentions or succumbing to greed himself.|His existing warning marks both parts of the responsibility.
Rafael agrees and thanks him.|The respectful close suits the stranger's confidence."""),
}
EDITS = {
    (0, 25, 25): ("Let's pay our respects to those lost at sea.", ()),
    (0, 25, 33): ("\"The sea and a mother are alike. The lapping waves sound strangely familiar, like the distant echo of a mother's heartbeat.",
                   ("like the distant echo", "a mother's heartbeat.")),
    (0, 25, 36): ("The sea and a mother are alike. In some lands, they say, both may be written and spoken the same way.", ()),
    (0, 25, 48): ("You're right. I took you for an old fellow who just liked ships. You've got real talent.",
                   ("old fellow", "You've got real talent.")),
    (0, 41, 69): ("Hmm. A big trading network?", ()),
    (0, 41, 112): ("I'd look in or near the major cities of each region.", ("the major cities",)),
    (0, 41, 119): ("Some of the locals may know. First, you'll have to earn their trust.", ("earn their trust.",)),
    (0, 41, 131): ("Do favors for the townspeople. Help them out of trouble. If crooked merchants or soldiers prey on them, teach them a lesson...", ("teach them a lesson...",)),
    (0, 41, 141): ("Whew... It's hard to become the one who rules the seas.", ()),
    (0, 41, 146): ("Ha ha ha! Of course it is. No one's ever done it.", ()),
    (0, 45, 29): ("At the Palace or Governor's Office, pay the local ruler a contract fee for the right to trade in town.",
                   ("Palace or Governor's Office,", "a contract fee", "the right to trade")),
    (0, 45, 33): ("Get contracts in different towns. The minimum fee should be enough at first.",
                   ("Get contracts in different towns.", "The minimum fee")),
    (0, 45, 37): ("I arranged the contract in Ceuta. You'll handle the others yourself.",
                   ("I arranged the contract in Ceuta.", "You'll handle the others yourself.")),
    (0, 45, 58): ("All right. If you have anything you want to sell, go ahead.", ()),
    (0, 86, 5): ("First thing a sailor needs in the Caribbean is a glass of rum! Come on, let's go to the tavern.", ("a glass of rum!",)),
    (0, 86, 21): ("Aaaah! An earthquake! A fire! It's the end of the world!", ("the end of the world!",)),
    (0, 86, 55): ("He calls himself the 'Blast Wizard,' or some such nonsense.", ("the 'Blast Wizard,'",)),
    (0, 86, 58): ("Blast Wizard? What an awful name.", ()),
    (0, 86, 75): ("There's a factory outside town. An odd fellow lives there. He studies explosives and cannons. He makes that racket now and then.",
                    ("a factory outside town.", "An odd fellow lives there.", "He studies explosives and cannons.")),
    (0, 86, 83): ("Well, bombs aren't the same as cannons. Then again, I suppose they're not so different.", ()),
    (0, 86, 105): ("Oh! You're sailors? Would you take him somewhere else?", ()),
    (0, 86, 129): ("Oh! Just what I've been hoping... I mean, I'm sure he'll be a great help to you!", ("a great help to you!",)),
    (0, 86, 147): ("Never mind that! You've done it again today!", ()),
    (0, 86, 150): ("I told you before, it's not a failure! I'm this close to making it work. Besides...", ("making it work.",)),
    (0, 86, 153): ("All right, all right! I get it. I didn't come here to complain.", ()),
    (0, 86, 172): ("I'll leave you to it. See you, Charles!", ("See you, Charles!",)),
    (0, 86, 180): ("Science must be too hard for him. I can't blame him for not getting it.", ()),
    (0, 86, 184): ("If you ask me, you're the one who doesn't make sense.", ()),
    (0, 86, 213): ("Hmm... You hardly look scholarly. I don't suppose you're sponsors.", ("You hardly look scholarly.",)),
    (0, 86, 230): ("Ah, sailors! I see... Tell me, are you interested in science?", ("interested in science?",)),
    (0, 86, 272): ("It's wonderful just thinking about it! Sailing really is a science!", ()),
    (0, 120, 21): ("You sound like you know something about the map to the Proof.", ("the map to the Proof.",)),
    (0, 120, 24): ("I do. But I can't tell just anyone.", ()),
    (0, 120, 28): ("You're afraid of what someone with evil intentions might do with it?", ("evil intentions",)),
    (0, 120, 40): ("I'm certain this young man has what it takes to rule the seas.", ("to rule the seas.",)),
    (0, 120, 56): ("They say the clan guarding the map in China fled the rulers of the day and traveled far, far to the northeast.",
                    ("the map in China", "the rulers of the day", "far, far to the northeast.")),
    (0, 120, 72): ("Find the base of the vast peninsula. On its eastern coast, look at the foot of a high peak.", ("On its eastern coast,", "the foot of a high peak.")),
}


def pair():
    FunctionType(source_workflow.main.__code__, vars(source_workflow) | globals())()


def review():
    implementation = checked_text(getsource(review_workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (EXCHANGES[route, block],)\n'
            '        assert excerpts[0][0] == 0 and len(excerpts[0][1].splitlines()) == len(group["records"])',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n'
            '                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=SCENES[block], source_meaning=meaning, localization_note=reason,',
    })
    env = vars(review_workflow) | globals()
    exec(compile(implementation, __file__ + "::complete-early-exchanges", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    if not SOURCE.exists():
        pair()
    review()
