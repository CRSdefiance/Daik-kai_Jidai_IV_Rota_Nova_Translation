"""Review the parallel coin game and Hodram's recruitment and Proof exchanges."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_diplomacy_and_friends_20261122 as parent
from scripts import review_current_story_wraps_20261122 as established
from scripts import refresh_story_wrap_queue_20261122 as queue


base, native = parent.base, parent.native
ROOT = Path("work/analysis/tavern_and_proof_exchanges_20261122")
REVIEW, PREFLIGHT = ROOT / "contextual_review.json", ROOT / "native_preflight.json"
CONTEXT = {
    (1, 169): "Fernando wagers a drink in the tavern coin game. After losing, he proves his ability to read people by predicting a couple's breakup. Hodram recruits for skill; Fernando lets his luck decide whether to join.",
    (3, 136): "Fernando makes the same tavern wager. Maria declines the drink, Xien doubts Fernando's eye, and Maria suggests the couple might be getting engaged. She asks him to put his talent to use with her fleet.",
    (1, 170): "Julio complains about the tavern's awful drink. His exchange with Hodram starts as banter about better liquor and turns to experience in trade, then to Julio presuming his invitation aboard. Gerhard objects and Hodram allows it.",
    (1, 173): "Gerhard wants to learn what the Proofs of Conquest mean. Mikhail offers their legend and practical advice about clues, ruins and the women at taverns. Hodram punctures Mikhail's attempt to make the advice sound romantic.",
    (1, 174): "Yifa approaches Hodram after leaving her teacher. Her 'binding spell' demo startles Gerhard, and Hodram recognizes the discipline and timing behind the stunt. He recalls his own teacher and checks her willingness to join a navy ship.",
}

# Ordinal | faithful source meaning | proposed wording | protected reading groups | rationale
FERNANDO = """
11|Fernando tells the player they should accept the challenge now that they are here.|||The impatient opening works in each version and points to the impending game.
16|He invites a newcomer to wager a drink and says the game is simple.|Well, a new face! Want to play for a drink? It's a simple little game.|play for a drink?;It's a simple little game.|Use the common tavern invitation and keep the stakes and reassurance intact. The wager is a drink and no money is implied.
20|Players alternate taking between one and three coins, their choice.|||Keep the inclusive range and taking turns in both versions.
24|The person who takes the final coin loses; Fernando starts the game.|||Both versions make the reversal clear before the choice.
47|Fernando claims his drink after winning.|||The short payoff names exactly what was wagered.
51|He enjoys the drink, thanks the player and says goodbye.|||The clipped farewell suits Fernando and closes the losing path.
60|Fernando hasn't lost for a while and hands over the reward.||Haven't lost in a while.|Carry the admission together after his irritated reaction.
74|A sharp eye and luck are important in gambling.|||Sharp eye sets up the demonstration of observation in both versions.
77|He has both and feels born to gamble.||born to gamble.|Keep the boast as a whole phrase before the skeptical reply.
85|He advises against judging people by appearance.|||The warning leads directly to his example.
89|He points to the couple and asks what they are saying, though the words can't be heard.||What do you think;they're talking about?|The question remains his test, and his confidence rests on watching them.
96|He says it is easy to tell the couple is discussing a breakup.||They're talking about breaking up.|Keep his confident answer together and leave the evidence for later.
104|He asks the player to keep watching.|||The short imperative gives the couple room to speak.
108|The woman has listened long enough and calls the man selfish.|||Both versions keep her exasperation and specify the conflict in outlook.
111|The man says she can think what she wants, but he thinks she is selfish as well.|||The countercharge without appeasement sets up her next line.
114|She suggests they stop seeing each other.||better stop seeing each other.|Keep the breakup proposal together and leave the sarcastic response as the opening.
117|He agrees their relationship is over if both feel that way.|||The concise outcome pays off Fernando's prediction.
124|Fernando asks if the player saw he was right.|||Called it fits his casual satisfaction.
132|Her clenched fist under the table meant she was holding in anger, not flirting.|See how she clenched her fist under the table? She was trying to keep her temper. That's hardly sweet talk.|clenched her fist;under the table?;That's hardly sweet talk.|Keep the clue, the inference, and Fernando's punch line in order across both versions.
136|The man never looked at her; Fernando asks if that looks like someone facing the woman he loves.|||The rhetorical question keeps the second clue and his confidence intact.
143|That insight lets him read an opponent's moves.|||Both installed versions sound like Fernando explaining his advantage.
146|His luck will take care of the rest.|||His second boast follows from the two qualities he named earlier.
153|The offer surprises him by coming out of nowhere.|||Either informal interjection fits his momentary surprise.
157|He has time to spare and agrees to go along if the coin comes up heads.|||Keep the condition, coin toss and hesitancy in both versions.
167|He asks the coin again after the player insists.|||The irritated question and speaking to the coin suit the joke.
192|Fernando won't trust his life to someone who's unlucky.|||His fatalism and curt exit are clear.
208|The toss settles it; Fernando will stake his life on the player.||I'll bet my life on you!|Keep the complete boast and its gambling metaphor after the toss.
211|Fernando names himself and calls the outcome luck.|Name's Fernando Dias! Chalk it up to luck!|Chalk it up to luck!|Use his established name and maintain the gambling joke through his introduction.
228|He complains that business or prospects have been poor lately.|||Both formulations keep the grumble brief on this alternate branch.
"""

ROUTE_TURNS = {
    1: """
70|Hodram declines the drink and asks about Fernando's apparent confidence.|||His restrained question leaves room for Fernando to boast.
81|Hodram doubts that Fernando has good insight.|||The short skeptical question is sharper than a formal objection.
92|Hodram guesses the man is courting the woman.|||He makes a tentative guess, without Maria's stronger assumption of a proposal.
100|Hodram reacts with silent puzzlement.|||The question mark gives Fernando the next word.
120|Hodram takes in the evidence silently.|||The pause leaves space before the explanation.
128|Hodram is surprised and asks how Fernando could tell.|||The question shows his curiosity after his earlier doubt.
140|Hodram recognizes Fernando's keen observational ability.|||His brief assessment is warmer without losing formality.
149|Hodram says the talent should be used beyond gambling and offers him a place aboard.|||The second question follows naturally and doesn't promise a rank.
163|Hodram sets aside the drink and again offers a berth.|||Come aboard is a forthright repetition of the invitation.
214|Hodram intends to rely on Fernando's skill.|||The measured response plays against Fernando's emphasis on luck.
""",
    3: """
69|Maria finds Fernando has room to improve, declines the drink and questions his confidence.|||The gently cutting remark distinguishes Maria's voice and keeps the wager separate.
80|Xien doubts Fernando's insight and sets aside luck.|||His skeptical interjection fits before the demonstration.
91|Maria guesses a proposal.|||Keep her specific guess, distinct from Hodram's idea of courtship.
99|Maria reacts with wordless confusion.|||Her reaction gives Fernando room to prove it.
119|Maria takes in the breakup without speaking.|||The pause belongs before Fernando calls attention to his prediction.
127|Maria is surprised and wants to know how he read the situation.|||The question is warm without endorsing his boast in advance.
139|Maria marvels at the amount of detail he picked up.|||She recognizes his observation as the source of the trick.
149|Maria invites Fernando to put his talent to the test with her company.|||The open invitation preserves FO and its purpose without inventing an occupation.
163|She sets the drink aside and insists he join her company.|||The imperative preserves the repeated invitation and FO.
214|Maria looks forward to having Fernando with her.|||Welcome aboard responds naturally to his voluntary commitment.
""",
}

HODRAM = {
    170: """
5|Julio declares something unacceptable.|||The outburst comes before its target is clear.
9|Hodram is puzzled.|||Keep the silent question.
13|Julio reiterates the objection at length.|||The emphatic syllables preserve his exaggerated delivery.
16|Hodram wonders if Julio is drunk.|||The parenthetical aside sets the tone without claiming he's certain.
21|Julio calls out to the people nearby.|||The sharp address is natural without naming them in advance.
25|Hodram says nothing.|||The silence leaves room for Julio to keep going.
29|Julio berates the younger generation.|||The familiar grumble sets up Hodram's aside.
33|Hodram thinks an old man's lecture is starting.||the lecture about young people.|Keep the thought together because the joke is about hearing the familiar lecture.
37|Julio calls drinking such terrible liquor disgraceful.|||Swill and disgraceful give the short accusation its tone.
40|Hodram is resigned to the encounter.|||The second private reaction carries weary humor.
44|Julio challenges Hodram's displeased expression.|||Sour look fits the quick question.
48|Hodram says Julio could simply stop drinking liquor he dislikes.|||The practical question answers the rant directly.
51|Julio says needing a drink means making do.|||The English idiom suits his practical excuse without a literal proverb.
54|Gerhard asks him to drink quietly out of consideration for others.|||The two brief instructions sound formal and irritated.
57|Julio admits he makes do with swill and complains.|||The unfinished sentence sets up his demand for a better drink.
61|He really wants a decent drink and asks Hodram to get one.|||The quick pivot sounds like Julio seeing an opportunity.
65|A better drink might persuade him to quiet down.|||Might keeps the joking condition he sets.
68|Hodram thinks this has become tiresome.|||Keep the short internal reaction.
72|Julio hurries him, saying his instinct tells him better liquor is available.|||His confidence without evidence grounds the next two choices.
86|Julio greets the affirmative answer with approval.|||The colloquial reply fits his sudden goodwill.
90|Hodram isn't a connoisseur, but knows liquor's value as cargo.||what it's worth;as a trade good.|Keep his commercial knowledge distinct from knowledge of vintages.
94|Julio has some experience of trade and is excited by the topic.||there's something;know a bit about.|Carry his boast softly after the immediate question about trade.
98|Hodram asks if Julio traded by ship.|||The simple question keeps the seafaring connection.
101|Julio calls himself a veteran.|||Old hand is a natural trader's boast and introduces no military service.
105|Hodram wants to ask for information.|||The careful request prepares the two approaches.
109|Julio asks what Hodram wants to know.|||His answer naturally introduces the choice.
125|Julio praises a straightforward attitude.|||The short response rewards honest inquiry without promising an outcome.
128|Julio decides to go along and asks where their ship is.|||The sudden presumption is the joke and should stay sudden.
133|Julio sees the test and won't fall for it.|||The terse rebuke suits this branch.
136|A contrary student needs education, starting with how to recognize good liquor.||We'll start with;recognize a decent drink.|Keep the turn to his chosen subject intact after his admonition.
139|Julio hurries Hodram to show him the ship.|||The impatient command leads to Hodram's surprise.
145|Hodram is bewildered.|||The short response gives Julio room to explain his presumption.
149|Julio assumes he will sail with them and says his lessons would take more than a day or two.||I've got plenty to teach you.;more than a day or two.|Keep the detail about duration and his certainty about joining intact.
153|Hodram is momentarily speechless.|||The pause sets up the introduction.
157|Julio names himself and greets them.|||Use the approved Julio Erneco spelling and familiar greeting.
160|Hodram returns the greeting after a beat.|||The clipped response shows his hesitation.
164|Gerhard objects that the admiral hasn't authorized bringing Julio aboard.|||The unfinished objection establishes who can permit it.
168|Hodram agrees to take Julio.|||The formality is understated and direct.
172|Julio is thrilled to be going to sea again.|||Retain the bright exclamation after the quiet assent.
181|Julio says not to mislead him or play dumb because he is older.|||The translation preserves suspicion and a direct demand.
184|Hodram says they were about to sail and look for some good liquor on the way.|Well... We're about to sail. I was going to look for some along the way.|We're about to sail.;along the way.|Retain the reluctant answer, and give Julio the exact cue for his excitement about sailing.
188|Julio is excited about the voyage and invites himself along.|You're going to sea? Splendid! I'll come with you, then.|You're going to sea?;I'll come with you, then.|The enthusiastic answer follows the mention of sailing and preserves his presumption.
192|Hodram is startled.|||Preserve the visual reaction in the same position.
196|Julio laughs and calls himself an active sailor.|||The three bursts capture his upbeat insistence that he still goes to sea.
200|Julio thinks he can still help despite his age.|||His age is relevant because he mentions it himself.
203|Gerhard protests that Hodram never approved Julio's boarding.|||Retain the repeated objection in this branch.
207|Hodram agrees anyway.|||The same assent ties the two paths together.
211|Julio gives his name and looks forward to traveling with them.|||The prospective greeting fits the decision to sail together.
""",
    173: """
5|Hodram asks what is wrong with Gerhard.|||The direct opening leaves room for his hesitation.
9|Gerhard wants to research the Proofs and hesitates over the available expert.|||The pause makes Mikhail's reveal work, and the title is consistent.
12|Hodram asks what is troubling him.|||A simple prompt keeps Gerhard's discomfort in focus.
16|Mikhail says proudly that he is the expert.|||None other than me and the laugh deliver the comic revelation.
19|Hodram sees what Gerhard meant.|||The small beat reflects recognition.
23|Gerhard finds it unfortunate that Mikhail is the one.|||The unfinished thought lets Mikhail challenge him.
26|Mikhail invites Gerhard to say what he thinks.|||The playfully pointed question needs no new rank or honorific.
29|Gerhard stammers that he respects Mikhail's knowledge.|||The unfinished reservation keeps his awkward diplomacy.
33|Hodram dismisses the aside and asks Mikhail to explain.|||The direct pivot matches his impatience.
36|Mikhail asks Admiral FI about interest in the Proofs.|||Keep the source title, FI and his proud laugh.
40|Hodram asks what the Proofs are for and wants to skip trivia.|||The restrained impatience is in character.
44|The Proofs are treasures found in the seas and are said to go to whoever rules each sea.|||Said to preserves the difference between legend and guarantee.
48|The ancient documents describe seven treasures and Seven Sages who marked their locations.|||Retain the numbers and the multiple maps.
51|The conqueror of each sea is fated to find its map in the legend.|||The gradual explanation and final caveat read naturally here.
55|Hodram is slightly disappointed to hear they're only treasures.||That's a little disappointing...|Keep his muted reaction together after the skeptical question.
58|Gerhard says the Proofs would let Admiral FI claim mastery of the seas in deed and name.|||His more ambitious interpretation follows naturally and keeps the FI address.
61|Hodram considers the idea of proof of mastery.|||The trailing thought shows that he is warming to it.
65|Gerhard asks him to think about the people who follow him.|||The crew's interests become the argument and the source title remains intact.
69|Hodram realizes a definite goal might motivate them.|||The question preserves his tentative acceptance.
72|Gerhard confirms that's what he meant.|||The brief agreement closes the aside.
76|Mikhail asks why they are whispering and jokingly boasts of his learning.|||The self-satisfied question matches his interruption.
80|Gerhard nervously agrees Mikhail knows a lot and asks him not to cause trouble aboard.|W-we're well aware of that. Just try not to make a scene aboard...|well aware of that.;make a scene aboard...|Keep the stammer and diplomatic concession without the awkward repeated know.
83|Mikhail laughs off the concern.|||The cheerful laugh answers Gerhard's anxiety.
87|Hodram asks how to collect every Proof.|||His practical question resumes the subject without an invented title.
91|A fleet must become strongest in a region, where powerful people often hold clues.|||Keep the distinction between a regional power and the individuals with information.
95|A wicked person holding a clue may have to be defeated.|||The conditional is important and avoids making violence a universal requirement.
99|Hodram considers the advice silently.|||The pause prepares the ruins step.
103|Discover ruins in the cities and solve the mystery of the sealed Proof.|||The sequence remains actionable and keeps the game's Proof terminology.
106|Gerhard asks how to find the ruins.|||His question leads directly to the advice about taverns.
110|Mikhail considers what he would do.|||The buildup sustains the joke before the one-word answer.
113|Gerhard waits for the explanation.|||The question mark retains the setup beat.
117|Mikhail's answer is women.|||The direct one-word surprise should stay isolated.
121|Gerhard cries Mikhail's name in reproach.|||The lengthened name translates the dramatic source delivery.
125|Mikhail tells him to calm down and says large cities have clues to nearby ruins.|||The practical answer makes sense after the seemingly frivolous response.
129|Women in taverns hear sailors from all over the world daily and have valuable information.|||The source emphasizes their access to conversations and the value of what they know.
132|They are unlikely to tell valuable secrets for nothing.|||The indirect warning invites Hodram's question about the price.
135|Hodram concludes that something has to be given in return.|||The pragmatic interpretation is the setup for Mikhail's lecture on gifts.
138|Mikhail urges him to think more romantically and says a gift should expect nothing, then jokes about winning a woman's heart.|Where's your sense of romance? A gift should come with no strings attached. It's just a way to win a woman's heart... Heh heh.|sense of romance?;no strings attached.;win a woman's heart...|Use four continuous rows for the advice and contradiction. Keep the laugh and the following challenge rather than inserting a blank row before the joke.
141|Hodram points out that winning her heart is getting something in return.|||The dry callback makes the contradiction clear.
145|Mikhail catches himself getting carried away.|||The brief embarrassment closes the joke without a new promise or instruction.
""",
    174: """
7|Yifa calls out to a handsome young man.|||Hey, handsome preserves the flirtatious address without suggesting kinship.
10|Hodram doesn't respond at first.|||The silence shows he hasn't taken the address as meant for him.
14|Yifa reiterates that she's talking to him.|||The renewed address keeps her persistence and casual teasing.
18|Hodram realizes she means him.|||The short question is a natural reaction.
22|Gerhard asks what the young woman is doing there.|||His formal tone contrasts with Yifa's familiarity.
25|Yifa asks for quiet and says she is in trouble.||I'm in a little trouble.|Keep her conspiratorial turn together after the request for quiet.
28|She identifies them as sailors and asks to come aboard.|||The question keeps her surprise request direct.
32|Gerhard finds her approach sudden and unusual.|||The short assessment prepares Hodram to ask for a reason.
36|Hodram asks what kind of trouble and why she wants passage.|||The two questions are practical and direct.
39|Yifa slipped away from her teacher and would be taken back if found.|||The condition gives her reason to be secretive without implying a crime.
43|Hodram is concerned that she ran off and asks what she's learning.|||His question keeps an opening for the demonstration.
46|Yifa studies Taoist arts.|||Use the established term without adding a specific practice she hasn't named.
50|She likes studying the arts but finds it tiresome sometimes.|||The familiar wording preserves the complaint without making her reject the training.
54|Her teacher caught her slacking and reprimanded her.|||Stick-in-the-mud sounds like Yifa's complaint and doesn't invent a punishment.
57|She will travel the world while training to prove herself to her teacher.||I'll sail around the world;show my master;Pretty great, huh?|Her boast keeps the intended journey, motivation, and request for approval.
60|Gerhard sighs about young women today.|||The trailing complaint is his reaction to her attitude.
64|Hodram respects her determination and asks what she actually knows of the arts.|||The skeptical question balances the compliment.
68|Yifa offers a demonstration and tells Gerhard to ready his sword.|||Old man and the direct challenge set up Gerhard's reaction without inventing a relation.
72|Gerhard is taken aback at being called old.|||The stutter fits his surprise.
75|Yifa confirms and warns him to get ready.|||The quick commands suit the playful demonstration.
78|Gerhard reacts briefly.|||The brief acknowledgment leaves room for her attack cry.
82|Yifa cries out as she makes her move.|||Preserve the lengthened exclamation as performance.
86|Hodram doesn't see what happened.|||The silent question retains the timing of the scene.
90|Gerhard wonders why nothing happened.|||The internal aside sets up Yifa's opening.
93|Yifa sees he has left himself open.|||The cue and jab are immediate.
98|Gerhard is startled and dodges.|||The short shout matches the sudden action.
102|Yifa praises the dodge and calls the move her binding spell.||That's my binding spell!|The boast follows the brief compliment as a complete statement.
106|Gerhard is puzzled by her name for it.|||The unfinished doubt is part of the joke.
109|Yifa teases him about how mysterious the arts are.|||The question lets her pretend to have proved her point.
113|Gerhard says that isn't what he meant.|||The quiet correction preserves the humor.
117|Hodram notices skill in how quickly she closed the distance on Gerhard.|It's no easy thing to close in on Gerhard that fast. You've got a good feel for when you're in range.|close in on Gerhard;when you're in range.|His judgment is about reading distance. It explains the result without asserting that the spell worked.
120|Gerhard agrees Yifa has done some kind of training.|||The restrained concession doesn't say he understands the technique.
123|Hodram recalls that his own teacher sent him to sea and shaped who he became.|||The brief disclosure gives a real reason he takes Yifa seriously.
127|He disapproves of leaving without a word, recognizes her determination and asks her name.|I don't approve of running off without a word, but you seem ready to see this through. What's your name?|without a word,;see this through.;What's your name?|Recognize her resolve in the terms shown by her plan and training, before the practical question.
131|Yifa says her name.|||Keep the approved spelling and enthusiastic delivery.
135|Hodram says his ship belongs to the navy and asks if she still wants to come.|||The question lets her accept the discipline explicitly.
138|Yifa understands that Hodram is strict and likes the challenge.|||The bold closing answer retains her enthusiasm without a claim about rank or orders.
""",
}

CHOICES = {
    (1, 169, 0): ("Accept the wager; decline the wager.", "Play and Pass are concise action labels following Fernando's invitation."),
    (3, 136, 0): ("Accept the wager; decline the wager.", "The first-person answers fit Maria's version of the tavern conversation."),
    (1, 170, 0): ("Say you have decent liquor, or say you don't.", "Yes and No answer the obvious question from Julio, and the affirmative preserves hesitation."),
    (1, 170, 1): ("Ask about an unfamiliar subject honestly, or test Julio on a familiar one.", "The two labels preserve the meaningful distinction between inquiry and testing him."),
}

PARALLEL_REFINEMENTS = {
    16: ("Well, a new face! Want to play for a drink? It's a simple little game.",
         "Want to play for a drink?;It's a simple little game.", "Let Fernando greet the newcomer, offer the wager and explain it in separate reading groups."),
    89: ("See that couple over there? We can't hear them. What do you think they're saying?",
         "See that couple over there?;We can't hear them.;What do you think they're saying?", "The conversational challenge gives the player the location, limitation and question without a stranded We."),
    114: ("", "we'd better stop seeing each other.", "The reply changes from sarcasm to suggesting a breakup. Keep the suggestion together."),
    132: ("See how she clenched her fist under the table? She was trying to keep her temper. That's hardly sweet talk.",
          "clenched her fist;under the table?;She was trying to keep her temper.;That's hardly sweet talk.",
          "Keep the visible clue, the inference, and Fernando's punch line in order across both versions."),
}
REFINEMENTS = {
    (1, 169, 77): ("", "It's like I was born to gamble.", "Fernando's two short thoughts build to his boast."),
    (3, 136, 76): ("", "You could say I was born to gamble.", "Give Fernando the same rhythm while retaining his current wording here."),
    (1, 170, 33): ("", "Here comes the lecture;about young people.", "The private joke stays in parentheses and the lecture is introduced in one phrase."),
    (1, 170, 90): ("", "I'm hardly a connoisseur.;what it's worth", "Retain the difference between knowing the drink and knowing what it fetches as trade cargo."),
    (1, 170, 94): ("Trade, you say? I know a thing or two about that!", "I know a thing or two about that!", "The modest idiom sounds like Julio finding a topic he can talk about at length."),
    (1, 170, 149): ("", "I've got plenty to teach you.;It'd take more than a day or two.", "Keep the explanation of the length of Julio's lessons as a complete sentence."),
    (1, 173, 80): ("W-we're well aware of that. Just try not to make a scene aboard...", "well aware of that.;Just try not to;make a scene aboard...", "Keep the courteous stammer and the concern about behavior aboard."),
    (1, 173, 138): ("Where's your sense of romance? A gift asks nothing in return. It's only to win a woman's heart... Heh heh.",
                    "Where's your sense of romance?;A gift asks nothing in return.;win a woman's heart...",
                    "Mikhail contradicts his own advice in the same beat, and Hodram's response echoes in return. Remove the earlier blank row."),
    (1, 174, 57): ("", "around the world and keep training.;I'll show my master what I can do!;Pretty great, huh?", "Yifa's travel plan, boast and question keep their shape and momentum."),
    (1, 174, 117): ("Closing in on Gerhard that fast is no small feat. You've got a feel for distance.",
                    "Closing in on Gerhard that fast;is no small feat.;You've got a feel for distance.",
                    "Hodram recognizes her judgment of distance rather than claiming the spell worked or attributing the result to reach alone."),
    (1, 174, 127): ("I don't approve of running off without a word, but you seem ready to see this through. What's your name?",
                    "without a word,;you seem ready;see this through.;What's your name?", "He can recognize her commitment while still reproving the way she left."),
}


def parse(text):
    decisions = {}
    for line in text.strip().splitlines():
        index, *details = line.split("|", 4)
        assert int(index) not in decisions
        decisions[int(index)] = details
    return decisions


def contextual_review(refined):
    assert not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    image = [base.NdsImage.open(p) for p in (native.CLEAN, parent.ROM)]
    clean_arm, arm = [i.read_file(native.ARM) for i in image]
    inventory, _, _ = native.scoped_inventory()
    names = {r["actor_ID"]: r["progressive_nameplate"] for r in base.load(established.CATALOGUE)["source_and_current_default_name_fields"]}
    common = parse(FERNANDO)
    checked, groups, choice_proofs = [], [], []
    for (route, block), context in CONTEXT.items():
        path = f"/data/SC{route}.DK4"
        clean_archive, active_archive = [i.read_file(path) for i in image]
        ah, ch = [native.digest(a) for a in (clean_archive, active_archive)]
        assert ch == release[f"target_SC{route}_sha256"]
        source, current = [native.IlnkContainer.parse(a).blocks[block] for a in (clean_archive, active_archive)]
        sh, th = [native.digest(a) for a in (source, current)]
        if block in (169, 136):
            aligned = {(i - int(route == 3 and i < 143)): value for i, value in common.items()}
            decisions = aligned | parse(ROUTE_TURNS[route])
            refinements = {i - int(route == 3 and i < 143): v for i, v in PARALLEL_REFINEMENTS.items()}
        else:
            decisions = parse(HODRAM[block])
            refinements = {}
        originals, deployed = [inventory(a, data)[0] for a, data in ((clean_arm, source), (arm, current))]
        assert len(decisions) == sum(cmd["word"] == 0x4000 for cmd in originals), ((route, block), len(decisions))
        choice_index = 0
        for clean, active in zip(originals, deployed, strict=True):
            assert clean["word"] == active["word"]
            if clean["word"] != 0x2100:
                continue
            key = (route, block, choice_index)
            gloss, reason = CHOICES[key]
            choice_index += 1
            values = []
            refs = []
            for cmd, block_sha, archive_sha in ((clean, sh, ah), (active, th, ch)):
                raw = bytes.fromhex(cmd["whole_command_hex"])
                values.append([x.decode("cp932") for x in raw[6:].split(b"\0") if x])
                refs.append(dict(file_path=path, block=block, command_offset=cmd["offset"], exact_command_hex=raw.hex(),
                    block_sha256=block_sha, archive_sha256=archive_sha))
            assert len(values[0]) == len(values[1]) == 2
            choice_proofs.append(dict(source=refs[0], current=refs[1], Japanese=values[0], english=values[1],
                source_meaning=gloss, localization_note=reason, decision="retention", context=context,
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True)))
        assert choice_index == sum(key[:2] == (route, block) for key in CHOICES)
        rows, _, _ = established.bind(arm, clean_arm, inventory, route, block, source, current, decisions)
        ids = []
        for ordinal, selector, (japanese, english), (sr, cr) in rows:
            prior = " ".join(english[1:].decode("ascii").split())
            meaning, replacement, protected, note = decisions[ordinal]
            if refined:
                replacement, protected, note = REFINEMENTS.get((route, block, ordinal),
                    refinements.get(ordinal, (replacement, protected, note)))
            localized = replacement or prior
            phrases = protected.split(";") if protected else []
            assert all(p in localized and len(p) <= 36 for p in phrases), ((route, block, ordinal), localized, phrases)
            change = "prose" if replacement and replacement != prior else "wrap_only" if phrases else "retention"
            ident = f"DK4_MES_B{block}_R{ordinal:04d}"
            ids.append(ident)
            for ref, bsha, asha in ((sr, sh, ah), (cr, th, ch)):
                ref.update(file_path=path, block=block, block_sha256=bsha, archive_sha256=asha)
            cr.update(candidate_sha256=release["candidate_sha256"])
            checked.append(dict(id=ident, route=route, file_path=path, block=block, source_selector=selector,
                kind="progressive", speaker=names[selector], context=context, source_meaning=meaning,
                Japanese=japanese[1:].decode("cp932"), previous_English=prior, english=localized, protected_phrases=phrases,
                source_reference=sr, current_reference=cr, source_hex=japanese.hex(), current_hex=english.hex(),
                localization_note=note, change_class=change, decision="retention" if change == "retention" else "revision",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=change == "retention")))
        groups.append(dict(route=route, file_path=path, block=block, record_ids=ids, context=context,
                            source_block_sha256=sh, current_block_sha256=th))
    assert len(checked) == 203 and len(choice_proofs) == 4
    counts = dict(Counter(row["change_class"] for row in checked))
    ROOT.mkdir(exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", groups=groups, records=checked,
        retained_choice_objects=choice_proofs, counts=counts, wrap_queue_sha256=base.digest(queue.OUTPUT),
        new_editorial_credit=0, stored_and_native_verification_of_changes_pending=True))
    print(f"Reviewed {len(checked)} spoken turns and {len(choice_proofs) * 2} choice labels across five objects. {counts}", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight"))
    cli.add_argument("--refined", action="store_true")
    args = cli.parse_args()
    if args.refined:
        ROOT = ROOT / "refined"
        REVIEW, PREFLIGHT = ROOT / REVIEW.name, ROOT / PREFLIGHT.name
    if args.action == "review":
        contextual_review(args.refined)
    else:
        original = established.preflight
        FunctionType(original.__code__, original.__globals__ | globals())()
