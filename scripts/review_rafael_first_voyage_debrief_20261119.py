"""Review Rafael's departure, loan, command tutorial and Mediterranean debrief."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as pair
from scripts import register_manuel_poem_cross_route_20261119 as parent
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = pair.base, pair.native, pair.stage
logical, TOKEN = workflow.logical, workflow.TOKEN
ROOT = Path("work/rafael_first_voyage_debrief_20261119")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((44, 47), (), (), ())
paired = SimpleNamespace(base=base, native=native, stage=stage, parent=parent, ROOT=ROOT, SOURCE=SOURCE, BLOCKS=BLOCKS)
SCENES = {
    44: "Clau and Janus surprise Rafael with the Carteira. Rafael asks Julio to finance the voyage independently of his father. Julio lends the money at interest, joins the crew and makes Rafael responsible. Clau and Julio bicker, Rafael gives his first order, and the game offers a choice of guided or independent preparations.",
    47: "After escaping the pirate threat, the crew considers Hayreddin, Pasha and the alternate Valdes situation. They agree to avoid provoking the region's powers, look for people in its major cities and improve their own readiness.",
}
NOTES = {
    44: """13|Clau says to come along and find out.|His repeated invitation makes the surprise playful.
17|Clau asks what Rafael thinks of men who go to sea.|Let the open question sound like a friend fishing for agreement. Keep the live name.
20|Rafael has no ready answer.|The hesitant reply fits the unexpected question.
25|Clau admires Prince Henry and Duke Leon.|Keep the named examples and the rush of admiration.
29|Clau calls the sea a man's romantic adventure.|His bravado sets up Rafael's familiar reaction.
33|Rafael has heard this before.|The brief aside fits his familiarity with Clau.
38|Rafael asks how they can go to sea without a ship.|His practical question sets up the reveal.
42|Clau accuses Rafael of having no imagination while he shares his dream.|The tease is about adventure. Keep the two friends' back-and-forth.
45|Clau interrupts himself as they arrive.|The quick announcement leaves the reveal to the next turn.
53|Janus greets the arrivals.|His restrained greeting contrasts with Clau's excitement.
57|Rafael reacts with wordless surprise.|Keep the two exclamation marks as the first reaction.
62|Rafael realizes a ship is in front of him.|Retain the short, breathless revelation.
67|Clau asks if he surprised Rafael and announces the Carteira's name.|Keep the emphatic reveal and the established ship name.
71|Clau and Janus repaired a wreck they took in.|Keep their joint effort and the wreck's condition. Use a familiar spoken cadence.
74|They need savings before they can sail someday.|The qualification checks Clau's enthusiasm and prompts Rafael's answer.
77|Rafael quietly proposes going.|The short suggestion preserves his sudden change of resolve.
82|Janus asks what Rafael means.|The one-word reaction fits the surprise.
86|Clau is confused.|The quick reaction lets Rafael explain.
90|Rafael reminds Clau he suggested sailing and proposes asking Julio for the money.|Keep the nickname he actually uses and the funding as a possibility.
94|Rafael is going to Julio's now.|The urgent intention follows his sudden resolve.
99|Clau calls after Rafael.|Keep the simple shout and name substitution.
103|Rafael calls for Janus and Clau to keep repairing the ship.|Use Clau here. Keep the request and Rafael's confidence as he runs off.
107|Clau calls for Rafael to wait.|Keep the shout and native name.
110|Clau realizes Rafael is the keenest of them.|The understated conclusion answers Rafael's abrupt change of pace.
114|Janus says Rafael picked up Clau's habit of acting the moment he decides.|The observation gives Clau a natural reason to disagree.
117|Clau says Rafael has always been like that but rarely shows it, then asks about repairs.|Keep the contrast and move naturally into his practical question.
121|Janus says the repairs are nearly done, then mentions he did most of them.|Restore the dry dig and leave it hanging for Clau to interrupt.
124|Clau brushes off the complaint and says Janus enjoyed himself.|The present idiom suits Clau's playful dismissal.
127|Janus agrees and suggests they go to Julio's too.|Keep the gentle concession and next destination.
131|Clau says he should be there for Rafael.|The boast reveals his loyalty and keeps the actual name.
135|Janus acknowledges Clau and gets him moving.|Keep the lightly impatient repetition without introducing another listener.
140|Julio indignantly asks what Claudio wants another advance for.|The full Claudio suits the scolding. Preserve the history of earlier advances.
144|Clau complains that Julio yelled with no warning and calls him an old man.|Keep his rude response and the clear start of the argument.
147|Rafael apologizes for asking so much.|The apologetic line contrasts with Clau.
152|Julio recognizes Rafael as the boy from the named household.|Use a complete American English question and preserve the surname.
155|Rafael apologizes for bursting in so abruptly.|The plain apology fits his politeness.
160|Clau insists their purpose this time is serious and tells Julio to stop being stingy.|His impatient demand belongs before Julio questions his work ethic.
163|Julio says he has never seen Claudio work properly and challenges his demand for trust.|The present English voices Julio's reason for hesitating.
167|Janus points out this is the consequence of Clau's usual behavior.|The English proverb keeps his dry rebuke.
170|Clau growls.|The short groan lets Rafael try again.
174|Rafael pleads and takes responsibility for proposing the voyage.|Keep his initiative and a natural final plea.
179|Julio hesitates over lending that much, even to Rafael, and asks what his father says.|The current question keeps the named address and turns to the family issue.
182|Rafael says he refuses to depend on his father for this and promises repayment.|Keep the resolve, the promise and the earnest plea.
187|Julio admires Rafael's independence yet still hesitates.|Let him recognize the reason and pause before Clau cuts in.
190|Clau says they will stop asking and tells Rafael and Janus to leave.|His abrupt reversal fits his embarrassment and preserves the named address.
194|Janus says he is coming and asks Clau to stop pulling him.|The physical irritation is explicit. Keep the short rejoinder.
197|Rafael apologizes for the unreasonable request and excuses himself.|He is polite while withdrawing. Use a compact spoken farewell.
201|Julio is silent.|Keep his pause before the crew goes out.
206|Clau admits he has no idea what to do after his bravado.|Make the self-awareness sound like Clau.
210|Janus asks why Rafael will not ask his father.|The direct question leaves Rafael to explain himself.
213|Rafael says his father treats him as a child and would oppose sailing.|The present reply keeps Rafael's reason and its certainty.
218|Rafael says things will only change if he acts now.|Keep the decision immediate and personal.
222|Clau praises Rafael's spirit in manly terms.|The rough praise and name prepare Janus's practical correction.
225|Janus says spirit alone cannot help without money to get started.|Use a dry reply that keeps the funding problem concrete.
229|Clau tells him to drop it and wonders whether they will have to earn the money bit by bit.|Keep his reluctant fallback. The Japanese leaves the source of the funds open.
233|Julio calls to the group from a distance.|The stretched shout works before Rafael identifies him.
237|Rafael recognizes Julio and wonders what he wants.|His curiosity fits the unexpected return.
241|Julio is relieved they are still there.|The repetition is natural in his relief.
245|Janus asks what Julio wants.|A polite short question suits his reserve.
249|Julio says he has been thinking it over.|The trailing thought gives Clau the opening to interrupt.
253|Clau impatiently asks Julio to say it.|The rude form of address is purposeful.
256|Julio calls Rafael by name and gives him something.|Retain the name and the reveal of the money in the following notice.
260|Rafael is surprised by what he has been handed.|Keep the disbelief before the system gives the amount.
264|The game reports receipt of 30,000 gold coins.|Retain the complete amount and the game's short reward wording.
268|Julio expects the loan back with interest now that he has handed it over.|Make the debt sound like spoken terms and preserve interest.
272|Rafael stammers and promises to work hard.|The eager response suits his surprise.
276|Julio worries where the money will end up and decides to watch over it.|Keep his pretext before he explains how.
280|Rafael does not understand.|Retain the wordless puzzle.
285|Julio explains he is coming aboard himself.|Keep the short reveal and his familiar impatience.
288|Rafael asks in delighted disbelief.|The short reaction gives Janus the next turn.
293|Janus welcomes the reassurance of a veteran navigator joining.|Retain both Julio's experience and Janus's relief.
297|Julio is embarrassed by veteran and says he has been away from sailing for a while.|Keep both modesty and the gap in experience.
300|Clau doubts that Julio will be useful.|The rude tease gives Janus something to push back against.
304|Janus objects to the insults and says Julio is a well-known navigator.|Keep the rebuke and Julio's established reputation.
308|Julio names Rafael captain.|Keep the Japanese pause between addressing Rafael and announcing the captaincy. The short opening line preserves that beat and accommodates longer names.
312|Rafael is surprised since Janus and Clau repaired the ship.|The unfinished objection lets Julio explain why he picked Rafael.
316|Julio entrusts the loan to Rafael as leader of the faction and makes him responsible.|Make the loan and personal accountability plain. Preserve the faction, given name and surname in source order.
320|Rafael is startled to be named the head of his faction.|Keep the live name and his hesitance.
324|Julio tells Rafael to aim high if he wants to make a name among great seafarers.|Keep the ambition in context, with an expectation instead of a loose scolding.
327|Julio names Rafael as ship captain, fleet admiral and head of the faction.|Each role remains distinct and both name fields and the company still come from the game. Keep the company inside the sentence so an abbreviation such as Castor Co. cannot create doubled punctuation.
330|Julio offers Claudio the leadership on condition that he work for free for life if trouble follows.|Keep the deliberately absurd threat and the full Claudio.
333|Julio asks if Claudio still agrees.|The short challenge gives the joke time to land.
337|Clau retreats and insists Rafael should lead, seeking Janus's support.|Keep the stammer, joke and native name.
340|Janus agrees and says he is not suited to the leadership.|His restrained answer suits him.
343|Rafael protests hesitantly.|Keep the short stammer.
348|Julio says making the effort is enough.|His reassurance lowers the pressure.
351|Rafael agrees to try.|The short acceptance resolves his hesitation.
355|Julio asks Rafael to use the loan to fund the venture.|Use the established term for their starting funds.
359|Rafael thanks Julio and promises to use the money carefully.|His direct gratitude answers the trust.
363|Janus thanks Julio for everything.|Keep his polite acknowledgement.
366|Clau says the old man has a good side after all.|Retain the backhanded compliment that provokes Julio.
369|Julio asks what the youngster thinks he is saying and calls him presumptuous.|The original rebuke fits their competing bluster.
372|Clau insults him and protests that he was giving a compliment.|The imperfect compliment makes the retort funny.
375|Julio says a little pain should make Clau recognize his greatness.|Keep the ridiculous self-praise in his mock threat.
378|Clau asks whether Julio wants to fight.|Keep the challenge short.
382|Julio boasts that he can still beat a youngster like Clau.|The mocking laugh and old man versus pup framing fit the banter.
385|Rafael asks both of them to stop.|The plea precedes his change of approach.
390|Julio insists he will not be satisfied until he punches Clau once.|Keep the threat in his voice and give it easier cadence.
394|Clau taunts Julio about breaking his fingers.|The quick comeback fits the escalating argument.
397|Rafael orders them to quit fighting as captain.|A sharp order marks the difference from his earlier plea.
401|Clau immediately defers to the captain.|Keep the exact repeated reply for the next beat.
405|Julio uses the same words as Clau.|The mirroring is the setup for the accusation of copying.
409|Clau accuses Julio of copying him.|Keep his rude indignation after the repeated line.
413|Julio denies that he would imitate Clau.|Retain the dismissive retort.
417|Janus reacts dryly to the pair.|The short aside is the scene's release of tension.
424|Julio tells Rafael to ignore Clau and says a good voyage depends on preparation.|Use a natural equivalent for the preparation proverb and keep the next action.
428|Julio says there is a lot to do and tells Rafael to follow closely.|Keep the instruction that prepares the guided option.
431|Rafael eagerly asks to be taught.|The brief reply shows he is willing to learn.
436|Clau grumbles that Julio is posing as Rafael's teacher because he knows a little about ships.|Keep the jealousy in his aside and preserve the live name.
439|Janus tells Clau to stop the cheek and come along.|The short dismissal returns the group to the task.
446|Janus proposes making preparations.|The direct setup works before the tutorial choice.
449|Janus asks if Rafael wants Julio to show him how or will prepare independently.|The full alternatives map directly to the two choices.
454|Rafael can choose to ask Julio for guidance.|The compact answer makes its purpose clear under Janus's question.
456|Rafael can choose independent preparation.|The existing short caption is distinct from asking for the lesson.
464|Julio says they will start at the trading facility.|Use the established Market label to match the town screen.
469|Julio advises visiting at least the trading facility, tavern and square in any town before sailing.|Use the visible facility names, keep the minimum list and the timing.
479|Julio welcomes Rafael's confidence and encourages him.|The warm reply supports the independent choice without promising success.""",
    47: """5|Julio cannot read Hayreddin's intentions, but expects travel in the Mediterranean to be easier now.|Keep his uncertainty and the qualified improvement.
17|Janus says they cannot survive being attacked by pirates like that every time they enter.|Keep the dangerous comparison and his wry tone.
44|Julio advises keeping clear of the Ottomans because the risk is too great.|Use a direct caution, with his reason.
48|Rafael asks why.|The brief question prompts the political explanation.
53|Julio says the Ottomans under Pasha hold roughly the eastern half of the Mediterranean, and the party is unlikely to win if targeted.|Keep the east, the approximate extent, the faction and the conditional danger together.
63|Rafael concludes they should put off the Mediterranean because of Pasha's influence there.|Keep this branch specific to Ottoman control.
70|Rafael concludes they should put off the Mediterranean because of Valdes and Pasha.|Preserve both powers in this alternate response.
77|Julio advises against forcing trade agreements or provoking them.|Keep the measured advice and natural phrasing.
81|Julio says they should still visit big cities to look for experienced navigators.|Recruiting gives them a reason to visit even while avoiding contracts.
92|Janus approves the plan.|The short response naturally acknowledges the advice.
102|Clau says they need stronger ships and to train themselves before sailing to other regions.|Use his practical voice and keep both kinds of preparation.
106|Julio agrees and reminds them to recruit navigators in major cities.|The reminder follows Clau's addition and keeps the earlier point.
110|Rafael is struck by how much they have to do.|His exclamation comes naturally after the list.
122|Janus says things are getting busy.|The light remark sets up Rafael's renewed resolve.
129|Rafael says they should get started.|The brisk response closes the conversation.""",
}
EDIT44 = {
    17: ("Say, FI... what do you think of men who go to sea?", ("men who go to sea?",)),
    42: ("Where's your sense of adventure? Can't a man dream?", ("your sense of adventure?",)),
    71: ("Janus and I took in an old wreck. She was nothing but scrap before we fixed her up.", ("Janus and I",)),
    90: ("You're the one who said we should go to sea, Clau! If it's money we need, we can ask Julio.", ("go to sea, Clau!",)),
    94: ("I'm going to see Julio right now!", ()),
    103: ("Janus, Clau, keep working on the repairs! I'm counting on you!", ("I'm counting on you!",)),
    117: ("He's always been like that. He just doesn't let it show much. So how are the repairs coming?", ("the repairs",)),
    121: ("Almost done. Though if you ask me, I did most of the work...", ("I did most of the work...",)),
    135: ("Yes, yes. I know. Come on.", ()),
    144: ("Don't just start yelling, old man!", ()),
    152: ("Ah, you're the boy from the FA family?", ("FA family?",)),
    174: ("Please, Julio! It was my idea. Isn't there anything you can do?", ("anything you can do?",)),
    187: ("You want to stand on your own. I admire that. I can see you've made up your mind, but...", ()),
    197: ("I'm sorry I asked so much of you. We'll see ourselves out.", ()),
    206: ("Well, I said my piece... Now what are we going to do?", ("what are we going to do?",)),
    225: ("That's fine, but we need money to get started. Courage won't pay the bills.", ("Courage won't pay the bills.",)),
    229: ("You had to bring that up... I guess we'll have to earn it bit by bit.", ("earn it bit by bit.",)),
    268: ("Now that I've lent it to you, I'll expect it back with interest.", ("back with interest.",)),
    276: ("Still, I'm worried about where my money will end up. I've decided to keep my eye on it.", ("keep my eye on it.",)),
    297: ("A veteran, eh? You'll make me blush. It's been a while since I last put to sea.", ("since I last put to sea.",)),
    304: ("Show some respect. Julio's a famous navigator.", ("a famous navigator.",)),
    308: ("FI, you're the captain.", ("you're the captain.",)),
    312: ("Me?! But Janus and Clau rebuilt her...", ("Janus and Clau",)),
    316: ("You lead FO, FI FA. I'm trusting you with this loan. It's your responsibility.", ("FI FA.", "It's your responsibility.")),
    324: ("You want to make a name for yourself among the world's greatest sailors, don't you? Then set your sights high.", ("greatest sailors,", "set your sights high.")),
    327: ("FI FA, you're captain of this ship and admiral of the fleet. You lead FO, too.", ("FI FA,", "captain of this ship", "admiral of the fleet.", "You lead FO, too.")),
    355: ("Good. Use the loan as your starting capital.", ("starting capital.",)),
    375: ("Maybe a good thump will teach you to recognize greatness.", ("to recognize greatness.",)),
    390: ("No! I won't be happy till I've given this fool a good punch!", ("a good punch!",)),
    397: ("Enough! Captain's orders. Break it up!", ("Captain's orders.", "Break it up!")),
    424: ("Now then, ignore that fool. A good voyage starts with good preparation. Let's get what we need.", ("good preparation.", "Let's get what we need.")),
    464: ("All right, let's get started. We'll head to the Market first.", ("the Market first.",)),
    469: ("Before you leave any town, visit at least the Market, Tavern, and Square.", ("the Market, Tavern, and Square.",)),
}
EDIT47 = {
    17: ("Right. If pirates like that attack each time we sail in, we won't last long.", ("we won't last long.",)),
    44: ("Even so, we'd best steer clear of the Ottomans. It's too risky.", ("of the Ottomans.",)),
    53: ("The Ottomans under Pasha hold about the eastern half of the Mediterranean. We can't beat them if they attack.",
         ("the Ottomans under Pasha", "the eastern half", "of the Mediterranean.", "We can't beat them if they attack.")),
    77: ("There's no need to push for a trading contract. We don't want to provoke them.", ("a trading contract.", "to provoke them.")),
    81: ("We can't ignore the big cities, though. We may find skilled navigators there. Let's at least look for people to recruit.", ("skilled navigators", "people to recruit.")),
    102: ("Yeah. We'll need stronger ships if we're going into other waters. We'd better toughen ourselves up, too.", ("stronger ships", "toughen ourselves up,")),
}
EDITS = {(0, block, ident): val for block, changes in ((44, EDIT44), (47, EDIT47)) for ident, val in changes.items()}


def main():
    packet = base.load(SOURCE)
    by_block = {g["block"]: g for g in packet["groups"]}
    assert set(by_block) == {44, 47}
    exchanges = {}
    for block, prose in NOTES.items():
        expected = [r["source_record_index"] for r in by_block[block]["records"]]
        lines = [line.split("|", 1) for line in prose.splitlines()]
        assert [int(n) for n, _ in lines] == expected
        exchanges[0, block] = 0, "\n".join(note for _, note in lines)
    implementation = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n'
            '                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=SCENES[block], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | {"exchanges": exchanges}
    exec(compile(implementation, __file__ + "::departure-and-debrief", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
