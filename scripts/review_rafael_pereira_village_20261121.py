"""Revisit four complete Rafael exchanges in SC0 blocks 61 through 64."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_spain_20261121 as parent
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical
from scripts.stage_hodram_alexandria_tutorial_20261121 import plan_progressive


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_pereira_village_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v2.json"
PRIOR = Path("translations/rafael_B61_B80_contextual_final_review_v1.json")
BLOCKS = ((61, 62, 63, 64), (), (), ())
CONTEXTS = {
    61: "Kuhn rages at his defeat. Pereira congratulates Rafael and sends him to face Spain. In the donation branch, Pereira gives 500,000 in military funds and the crew reacts.",
    62: "A respectful stranger offers a gift and leaves. Rafael sees an empty scabbard. Depending on the branch, Rafael or Arcadius connects it to the Proof of Conquest. Claudio is already convinced.",
    63: "Claudio confronts Rafael about asking Eirene to do heavy lifting. Rafael explains the argument to Eirene, who publicly goes by Arcadius. She reassures him, and Claudio has cooled off by the end of the meal.",
}
VILLAGE = (
    "The crew interrupts a buyer who is damaging Charlotte's goods. Rafael offers to help by buying them. Charlotte hears an offer of charity in his words and walks away.",
    "Rafael recognizes the condescension in his offer. The crew discusses what happened, and Charlotte returns to ask for a fair hearing and apologize.",
    "Arcadius and Janus explain what the apology took. Claudio changes his mind and wants to buy the lot. The crew and Charlotte reach a deal and introduce themselves.",
    "Charlotte explains her Romani family's migration, the false promises they were given, the discrimination they faced and how the village learned to support itself.",
    "Charlotte and Rafael acknowledge the hurt and the kindness in their first meeting. They agree to meet again. Rafael connects her community's lack of a homeland with his fear for Portugal, and the crew resolves to help.",
)

# Empty English keeps the current wording. Named phrases can request a reflow.
DECISIONS = """
61 12|||Kuhn's unfinished disbelief identifies the lost urn without adding a new claim.
61 15|Damn it! You'll pay for this!|You'll pay for this!|Make Kuhn's threat of retaliation sound like a threat rather than a statement about remembering.
61 22|Beaten by the likes of them... And I was so close!|Beaten by the likes of them...;And I was so close!|Keep Kuhn's contempt and disbelief in distinct beats as he realizes how close he came.
61 27|||Pereira's brisk congratulations retain the title and surname substitution.
61 31|We did it somehow. Thank you, Governor Pereira.|We did it somehow.;Thank you,;Governor Pereira.|Keep Rafael's modest relief and his explicit acknowledgment of Pereira.
61 42|Don't mention it.||Pereira waves off Rafael's thanks in the short branch.
61 64|Don't mention it.||Preserve the same familiar reply in the corresponding branch.
61 75|All right, no more nitpicking from me. Do it your way! Go beat Spain, or whoever gets in your way!|no more nitpicking from me.;Do it your way!;Go beat Spain,|Keep Pereira's encouragement, his own hands-off promise and the challenge against Spain or whoever else intervenes.
61 78|Governor...||Rafael's half-formed response echoes the actual title.
61 83|Hey, you're all right, old man!|you're all right, old man!|Give Claudio the source's familiar address and the grudging warmth Pereira plays off.
61 94|Ha ha ha! Indochina's governor is always a good guy!|Indochina's governor;always a good guy!|Pereira jokingly praises himself by title, echoing Claudio's compliment.
61 107|Ha ha ha! Indochina's governor is always a good guy! Here, Admiral FA. Take this.|Indochina's governor;always a good guy!;Here, Admiral FA.|Keep the parallel boast and preserve the separate gift and address in this branch.
61 113|||The speakerless reward notice preserves the exact amount, the donor and the game term military funds.
61 122|||Rafael's drawn-out disbelief leaves the size of the gift to the preceding notice.
61 129|||Janus's restrained surprise contrasts with Rafael and Claudio.
61 136|Whoa! Now that's generous! You're something else, Governor!|Now that's generous!;You're something else, Governor!|Keep Claudio's excitement and his distinctly informal praise of the governor.
61 147|||Jam's extended cheer fits the sequence of escalating reactions.
61 154|||Rafael's two short questions convey disbelief at the size of the gift.
61 158||Don't worry about it!;Now go give it your all.;I'm counting on you!|The reassurance and charge fit Pereira's confidence. Keep both imperatives on their own beats.
61 161|||Rafael's brief assent ends the exchange without diluting its energy.
62 5|FA, you're worthy to rule the seas around this continent. Please accept this.|worthy to rule;around this continent.;Please accept this.|Use a respectful but spoken address. Keep the continent's waters and the gift.
62 10|Could it have something to do with the Proof?!|to do with the Proof?!|Rafael recognizes the possible significance while the object is still unidentified.
62 15|||The quick change from thanks to surprise follows the stranger's departure.
62 19|||Claudio's clipped observation supplies what happened while Rafael was looking at the gift.
62 23|It looks like a scabbard, but there's no sword in it. What could that mean?|looks like a scabbard,;no sword in it.;What could that mean?|Keep Rafael's tentative identification and the empty scabbard as a question.
62 34|Could it be another key to the map for the Proof of Conquest?|another key;Proof of Conquest?|Keep Rafael's uncertainty and the key's relationship to the map.
62 40|This must be another key to the Proof of Conquest map.|another key;Proof of Conquest map.|Give Arcadius the more confident reading without claiming the Proof itself was found.
62 46||I'll bet it is!;the New World;is as good as ours!|Claudio's certainty and New World treasure boast keep the payoff in his voice.
63 5|||Claudio's invitation sounds short and urgent and preserves the given-name substitution.
63 9|||Rafael's small surprise and quick agreement suit the start of a private conversation.
63 14|...Could you think about her for a second?|think about her for a second?|Claudio begins mid-thought. Let Rafael ask who he means before Claudio names Eirene.
63 18|Huh? What are you talking about?||Rafael is genuinely unsure what prompted the complaint.
63 22||Eirene;help with the heavy lifting;didn't you?|Keep the exact name and the specific physical work prompting Claudio's concern.
63 25|||Rafael minimizes the effort before Claudio pushes back.
63 30|That's not the point! Eirene isn't as strong as the rest of us. You've got to look out for her!|That's not the point!;as strong as the rest of us.;look out for her!|Preserve the physical comparison and Claudio's protective anger.
63 34|Well... there was a reason I asked.|there was a reason|Rafael trails off and offers a defense without explaining it yet.
63 38|So having a reason makes it okay?!|makes it okay?!|Claudio challenges Rafael's defense in an immediate retort.
63 41|||Rafael pushes back at the anger instead of resolving the argument.
63 46|||Claudio dismisses him and leaves, setting up Rafael's complaint about the exit.
63 52|||Arcadius's concerned greeting follows the shift from the argument to the private conversation.
63 55|Oh, Arcadius... I've just got something on my mind.|Oh, Arcadius...;on my mind.|Keep the public address and Rafael's hesitation before he risks saying more.
63 60|||Arcadius heard Claudio's voice. Keep uncertainty about what was said.
63 63||(Oh, no...);hear what we were arguing about?|Separate Rafael's private panic from his question about what Arcadius heard.
63 67|No, I couldn't make out the words.|make out the words.|Arcadius heard the yelling without hearing the content.
63 71|||Rafael's short question makes the move to confidence clear.
63 75|||Arcadius gives quiet permission to continue.
63 79|Eirene, we were arguing about you.|we were arguing about you.|Rafael switches to Eirene's private name as he tells her what happened.
63 84|||Her short question is natural surprise in response to Rafael using her name.
63 88||Clau's angry with me.;heavy lifting?|Keep Rafael's personal stake and the callback to the physical work.
63 92|Oh... No one else was there. Everyone thinks I'm a man. Wouldn't it look odd if I didn't help?|No one else was there.;Everyone thinks I'm a man.;if I didn't help?|Keep both reasons helping made sense, including what the crew believes.
63 95||That's what I told him.;We didn't have a choice.;But he's furious.|Keep Rafael's justification and reaction to Claudio's anger in distinct beats.
63 100|||Let Eirene hear Rafael out before she answers.
63 104|||Rafael's description of the one-sided shouting and abrupt exit suits his hurt.
63 108||looking out for you too, Eirene.;It's not fair...|Keep Rafael's concern for Eirene and the upset admission that follows it.
63 113|I'm sorry, FI. Hiding that I'm a woman has put you in a tough spot.|I'm sorry, FI.;Hiding that I'm a woman;a tough spot.|Preserve Eirene's apology and her explanation in her own words.
63 117|No, it isn't your fault. Sorry I unloaded on you. Don't worry about it.|it isn't your fault.;Sorry I unloaded on you.;Don't worry about it.|Rafael reassures her first and then apologizes for venting.
63 122|...FI, I know how hard you're working as our admiral.|how hard;as our admiral.|Give Eirene a warm opening and preserve her praise of Rafael's effort as admiral.
63 126|You're the reason we all feel safe at sea.|we all feel safe at sea.|Keep her support grounded in how the crew feels sailing under him.
63 130|||Rafael's blush and question fit the sudden praise.
63 134|Nothing's wrong. FI, I just don't want you to push yourself too hard.|Nothing's wrong.;push yourself too hard.|Eirene explains her worry and keeps the original personal address.
63 138|||Rafael responds quietly to the kindness before Eirene offers advice.
63 143|You don't have to worry alone. Talking to someone can help, even if you're just venting.|worry alone.;Talking to someone;just venting.|Let Eirene connect Rafael's venting with the relief of sharing a worry.
63 146|||The big-sister simile conveys comfort and creates no family relationship.
63 150|You think so?||Eirene checks his impression in a gentle, surprised reply.
63 154|Yeah. I feel better than I did a minute ago. Thanks for listening.|I feel better;Thanks for listening.|Rafael confirms the effect she described and thanks her directly.
63 159|||Eirene still feels responsible for the trouble and repeats her apology in her own voice.
63 162|Clau and I have never fought like this before. I didn't know what to do, and I still don't.|never fought like this before.;I didn't know what to do,;and I still don't.|Preserve the first serious quarrel and Rafael's uncertainty without making him ask the same question twice.
63 166|Oh, that? Claudio will be fine. Give him something to eat and he'll probably forget all about it.|Claudio will be fine.;something to eat;forget all about it.|Eirene gently predicts how quickly food will change Claudio's mood.
63 170|||Rafael's uncertainty makes the meal payoff work.
63 175|Yes. He's easy to read. Come on, let's eat.|He's easy to read.;Come on, let's eat.|Keep Eirene's affectionate assessment and her invitation to eat.
63 179||Hey, FI!;Did you get enough to eat?!|Claudio's appetite is the first thing he asks about after the meal. Keep the question whole.
63 182|||Rafael stammers because Claudio is acting as though the argument never happened.
63 186|||Claudio notices Rafael's expression but stays unaware of the cause.
63 189||I just thought;in a good mood...|Rafael tries to explain his surprise without reopening the argument.
63 193|||Claudio moves on in the blunt, casual voice he used before.
63 197|||Rafael recognizes that Eirene predicted Claudio's reaction correctly.
63 202|||The last question turns Eirene's knowledge of Claudio into Rafael's innocent scholar joke.
64 5|Wow, I didn't think we'd find a village out here.|find a village out here.|Keep Rafael's surprise at finding a settlement in an out-of-the-way place.
64 9|It's a lonely-looking place. Doesn't feel like much happens here.|lonely-looking place.;much happens here.|Claudio remarks on the lack of bustle in his own casual voice.
64 12|Look closer. There are ships from other countries docked here, too.|ships from other countries;docked here, too.|Rafael notices the foreign ships after taking a better look.
64 17|||Rafael's short question shifts their attention to the commotion.
64 21|||Claudio suspects trouble without knowing what has happened.
64 25|||The short decision carries the scene straight to the argument.
64 31|Wait! Last time you said you'd pay more than that!|Last time;you'd pay more than that!|Make clear the buyer promised more at the earlier meeting. Charlotte is challenging today's offer.
64 35|That was then. For this lot today, I won't pay a penny more.|That was then.;a penny more.|Keep the buyer's refusal and his claim that today's goods warrant the price.
64 39|What's wrong with them? I picked out the very best our village makes!|What's wrong with them?;the very best|Restore Charlotte's effort in choosing the village's best goods.
64 43|||The buyer sarcastically echoes her claim before he starts breaking the goods.
64 47|Look how flimsy this is! I'm not paying full price for this junk. See? See?!|Look how flimsy this is!;paying full price;See? See?!|Keep his claimed price justification, contempt and repeated taunt as he breaks the goods.
64 51||Break anything else;you'll regret it!;worked hard to make those!|Charlotte warns him off and explains why the damage matters to the village.
64 55|Ow! What the hell are you doing, woman?!|What the hell;doing, woman?!|Keep the buyer's pain and sudden hostile outburst without adding an action the source leaves on screen.
64 58|||Charlotte's sharp cry gives way to Rafael's immediate intervention.
64 62|||Rafael's direct rebuke fits the strike he moves to stop.
64 67|||Claudio offers himself as the buyer's opponent in a short challenge.
64 71|||The buyer's scoff is the last thing he says before fleeing.
64 75|Hmph. He took off.|He took off.|Keep Claudio's disdain for the buyer who ran.
64 79|||Rafael's concern follows the rescue and is sincere even though his later offer lands badly.
64 84|||Charlotte's silence leads Claudio to press for an explanation.
64 88|Treating a girl like that... Was he just looking for an excuse to start something?|Treating a girl like that...;looking for an excuse;to start something?|Keep Claudio's disgust and the suspicion that the buyer manufactured a grievance.
64 91|||Rafael's offer to help her out is well meant and patronizing, which gives Charlotte something specific to repeat.
64 95|||The incredulous echo picks up the words Rafael will later recognize as patronizing.
64 98||What would a rich boy know?;Keep your pity!|Charlotte rejects the offer on her own terms and challenges Rafael's understanding.
64 102|What's with her?! We help her out and get a tongue-lashing for it!|What's with her?!;get a tongue-lashing for it!|Keep Claudio outraged that she complained after the rescue, with an idiomatic description of her response.
64 106|...Did the way we went about it really upset her that much?|the way we went about it;really upset her that much?|Rafael suspects something in their approach upset her before he understands what it was.
64 111|She didn't have to tear into us! We did save her, you know!|tear into us!;We did save her, you know!|Keep Claudio's insistence that the rescue earned them better treatment.
64 114|Easy, Clau. Getting mad'll make you hungry. Let's get something to eat and clear our heads.|Easy, Clau.;make you hungry.;clear our heads.|Keep Rafael's comic explanation and his proposal to reset over a meal.
64 119|Ah, so that's what happened...|that's what happened...|Janus hears the story after the fact and gives his measured reaction.
64 123|Makes your blood boil, doesn't it? What a piece of work!|Makes your blood boil, doesn't it?;What a piece of work!|Claudio expects the crew to share his outrage and follows it with a grumble.
64 126|No, it was my fault. Saying I'd 'help her out' probably sounded like I was looking down on her.|'help her out';looking down on her.|Rafael points to the same words Charlotte objected to and recognizes why they sounded condescending.
64 130|I really did feel sorry for her. No wonder she got mad. Did I hurt her? What should I do now?|feel sorry for her.;No wonder she got mad.;What should I do now?|Keep the admission of pity and the progression from understanding to worry.
64 134||let's not dwell;on what's already happened.|Arcadius turns Rafael away from the past and toward what he can change.
64 138|Once you see what you did wrong, the thing to do is make sure you don't do it again.|see what you did wrong,;don't do it again.|Keep the advice practical and let Arcadius answer Rafael's worry without excusing the mistake.
64 141|||Janus endorses Rafael's instinct to help with the established given-name substitution.
64 144||went about it wrong,;I'm sure she knows you meant well.|Janus acknowledges the clumsy approach and gives Charlotte credit for recognizing his intentions.
64 147|||Rafael's quiet thanks acknowledge both responses.
64 152|Hold on! She insulted us without a word of thanks! If anybody's to blame, it isn't FI...|Hold on!;without a word of thanks!;it isn't FI...|Keep Claudio's protest and the thought he drops before blaming Charlotte again.
64 155|...Forget it. Everybody on this ship is out of their mind. A ship full of softies.|Forget it.;out of their mind.;A ship full of softies.|Keep Claudio's abandoned objection and his exasperated affection for the crew.
64 158|||His post-meal remark ends the argument just before Charlotte returns.
64 162|||Charlotte hesitates and asks for their attention without sounding confident yet.
64 166|||Rafael's moment of confusion precedes Claudio's recognition.
64 171|||Keep the specific accusation that Arcadius calls out later.
64 174|||Charlotte's stammer and tentative request show how hard it is for her to return.
64 177|W-what?! Don't push your luck! You were the one who made such a show of turning us down!|Don't push your luck!;turning us down!|Keep Claudio's surprise and his complaint about the force of her earlier refusal.
64 181|I-I know you don't have to...|you don't have to...|Restore Charlotte's stammer and make clear she is asking without demanding.
64 184|||Claudio hands the choice to Rafael after a blunt aside.
64 187|I'll decide after I've looked at the goods. Can you bring them to the port office?|looked at the goods.;to the port office?|Rafael responds as a potential buyer with terms and a place to meet.
64 191|Thank you! If you're willing to look, I'll be there!|If you're willing to look,;I'll be there!|Charlotte values the chance to show the goods and promises to come.
64 194|I can't promise I'll buy them...||Rafael sets a fair expectation after agreeing to inspect the goods.
64 198|||Charlotte accepts the risk in a natural expression of having nothing to lose.
64 202|||The small false start shows she is building up to the apology.
64 206|I-I'm sorry about earlier!||Keep Charlotte's stammer and abrupt apology before she hurries away.
64 210|||Rafael's surprise gives her apology room to land.
64 215|||Charlotte ends the uncomfortable moment by promising to see him later.
64 219|Ah. She's got a good heart after all.|a good heart after all.|Janus recognizes the character beneath the earlier anger.
64 222|Calling her a rude woman was harsh, Clau.|a rude woman;was harsh, Clau.|Arcadius repeats Claudio's specific insult and gently rejects it.
64 225|She's the one who was harsh! We helped her, and she threw an insult at us on her way out!|She's the one who was harsh!;on her way out!|Claudio turns Arcadius's criticism back on Charlotte and recalls her parting words.
64 229|First it's 'keep your pity,' then it's 'buy these.' She's got some nerve!|'keep your pity,';'buy these.';She's got some nerve!|Keep the callback to Charlotte's actual rejection and Claudio's judgment about her return.
64 232|I'd call that courage, Clau.|call that courage, Clau.|Arcadius sees courage in the same action Claudio calls nerve.
64 235||Her face was bright red;she was trembling...;her family and the village.|Keep the physical signs of shame and the people she put ahead of her pride.
64 239|...She's a good person.|She's a good person.|Rafael recognizes what mattered to Charlotte after hearing the two explanations.
64 244|||Claudio's quiet agreement marks his change of mind before he proposes taking action.
64 248||get ready to unload the cargo!|Keep the sudden practical response and the instruction to unload.
64 252|You're getting ahead of yourself. We haven't even agreed on a price yet.|getting ahead of yourself.;agreed on a price yet.|Rafael answers Claudio's rush with the negotiation that still has to happen.
64 256|Come on, FI. You don't really need to inspect the goods, do you? Just buy the whole lot!|Come on, FI.;the goods, do you?;buy the whole lot!|Keep Claudio's sudden willingness to back Charlotte, his tag, and the proposal to buy everything.
64 260|||Rafael stammers at Claudio's turnaround.
64 265|He's pushy, all right. That's what I like about Clau. He gets right to the point.|He's pushy, all right.;what I like about Clau.;right to the point.|Janus balances the pushiness with his appreciation of Claudio's directness.
64 269|||Arcadius's short agreement keeps the focus on Claudio's change of heart.
64 274|||Rafael's plain confirmation closes the actual negotiation.
64 279||Now I can go back;everyone in the village.;They'll be so happy!|Charlotte's thanks and relief belong to the village as well as to her.
64 283|I never asked your name. I'm FI. What should I call you?|I never asked your name.;I'm FI.;What should I call you?|Keep Rafael's introduction, given-name substitution and recognition that he has not learned hers.
64 287|||Charlotte repeats Rafael's name before giving hers.
64 290|Charlotte... why did you build your village on such barren land?|why did you build;such barren land?|Rafael hesitates before asking about the choice of land.
64 295||We're Romani.;all over Europe...|Keep the named Romani identity and the history of travel.
64 298|||Charlotte's memory of holding her mother's hand and trying to keep up conveys her own childhood.
64 301|Then someone asked if we wanted to settle in the New World.|someone asked;settle in the New World.|Keep the invitation to migrate and leave the person who made it unnamed.
64 305|We were told there was gold everywhere, and miles of fertile land no one had touched.|gold everywhere,;miles of fertile land;no one had touched.|Both claims are reported sales promises in Charlotte's account.
64 309|We talked it over, scraped together what little money we had, and decided to cross the ocean.|We talked it over,;what little money we had,;decided to cross the ocean.|Keep collective deliberation, scarce money and the decision to cross.
64 313|My parents, everyone, had such high hopes at first. We'd have land and a village of our own...|high hopes at first.;a village of our own...|Preserve Charlotte's parents, the others and the prospect of a place of their own.
64 316|But we lost hope soon enough.|lost hope soon enough.|Let Charlotte's plain recollection pivot from the promises to what they found.
64 319|You can't find a gold mine by digging holes at random. All we could see was barren land stretching to the horizon.|find a gold mine;digging holes at random.;stretching to the horizon.|Preserve the futile digging and the landscape in her account.
64 322|They talked you into it just to take your money... That's unforgivable.|just to take your money...;That's unforgivable.|Rafael is angry at the people who profited by misleading the migrants.
64 326|||Charlotte describes despair and mutual encouragement before the decision to build.
64 330||never owned land before,;even growing crops was hard...;ever since we got here.|Her explanation links the farming difficulty to their lack of previous land.
64 333|Didn't you think about going back to your country when things got so hard?|going back to your country;when things got so hard?|Rafael assumes there is a country to return to, which gives Charlotte a specific premise to correct.
64 337||We Romani;have no country of our own.;nowhere to go back to.|Keep the reply in Charlotte's words and connect the lack of a country with nowhere to go back to.
64 340|If something went missing, people blamed us. If a terrible disease spread, they blamed us for that, too.|people blamed us.;a terrible disease spread,;they blamed us for that, too.|Charlotte is reporting accusations directed at her community. Keep both examples visibly attributed to other people.
64 343|Wherever we went in Europe, people looked at us like we were dirt.|Wherever we went in Europe,;like we were dirt.|Give Charlotte a natural expression of how people looked down on her community.
64 347|||Rafael has no immediate reply to her account.
64 352|Two or three years ago, we finally grew enough to feed ourselves. At last, we had a village of our own!|Two or three years ago,;enough to feed ourselves.;a village of our own!|Keep the approximate date, crop self-sufficiency and Charlotte's pride.
64 355|Then about a year ago, a ship happened to stop here. That's when we started getting new goods by barter.|about a year ago,;a ship happened to stop here.;getting new goods by barter.|Keep the chance visit, approximate timing and the start of barter.
64 358|Still, people often make us sell for next to nothing, like that man did. We don't have much choice.|sell for next to nothing,;We don't have much choice.|Keep Charlotte's lack of bargaining power and the connection to the earlier buyer.
64 363||When you helped me,;I was really happy!|Keep Charlotte's hesitation, gratitude and given-name address in this private admission.
64 367|I never thought anyone would stand up for me...|stand up for me...|Keep her disbelief that somebody would intervene in her defense.
64 370|Charlotte... I hurt you when I first spoke to you.|I hurt you;when I first spoke to you.|Rafael acknowledges the impact of his offer after she acknowledges his help.
64 375||You meant well.;I should've thanked you;for helping me.|Keep Charlotte's recognition of Rafael's intentions and her own wish to have thanked him sooner.
64 379|||Her question moves from apology to an explicit wish to see him at the village again.
64 383|||Rafael agrees without reservation.
64 388|||Charlotte checks his agreement in a single surprised question.
64 392|||Rafael answers that doubt with a promise.
64 397|||Keep Charlotte's warmth and insistence as she leaves.
64 401|||Rafael's farewell follows naturally from agreeing to return.
64 406|You promised!||Charlotte calls after Rafael as she leaves, reminding him what he just said.
64 410|She's gone... Wait, Clau? When did you get here?|When did you get here?|Keep Rafael's shift from watching Charlotte leave to discovering Claudio was present.
64 414|||Claudio's blunt, emotional reaction makes clear he was moved by what he heard.
64 418||She suffered in Europe;here in the New World.|Arcadius recognizes the hardship in both places.
64 422|||Rafael sees that Arcadius was there as well.
64 427|||Arcadius acknowledges overhearing and gives a modest explanation.
64 439|...When it looked like Spain might annex Portugal, I felt like I was about to lose my place in the world.|Spain might annex Portugal,;lose my place;in the world.|Rafael compares the threatened annexation to a fear of losing his own home.
64 444|But Charlotte and her people never had a place of their own to begin with...|Charlotte and her people;never had a place of their own;to begin with...|Keep Rafael's insight about their lack of a homeland in response to Charlotte's account.
64 451||Isn't there anything;we can do for them?!|Claudio wants to act after hearing her account. Keep his given-name address and question.
64 455|Let's think of a way to help the village grow. Even if we can't do it now, we might find a way to help someday.|help the village grow.;we can't do it now,;help someday.|Arcadius suggests thinking beyond their immediate visit without promising a particular outcome.
64 458|||Rafael agrees and resolves to act without claiming the problem is already solved.
64 462|||The pause gives way to Rafael reflecting on Charlotte.
64 467|||Rafael's brief repetition keeps his reflective silence around her name.
64 472|She was a wonderful young woman. So honest.|a wonderful young woman.;So honest.|Arcadius praises the straightforwardness Charlotte showed by returning and opening up.
64 476|Yeah.||Claudio's plain assent sounds like his usual voice.
64 480|||Rafael's trailing assent leaves room for the internal question.
64 485|||The final private question brings the scene back to what the crew can do.
"""


def village_context(number):
    return VILLAGE[sum(number >= start for start in (119, 219, 290, 363))]


def main():
    assert not OUTPUT.exists()
    packet, release, previous_review = map(base.load, (SOURCE, parent.RELEASE, PRIOR))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    decisions = {}
    for line in DECISIONS.strip().splitlines():
        key, english, phrases, reason = line.split("|")
        block, number = map(int, key.split())
        assert (block, number) not in decisions
        decisions[block, number] = english, tuple(phrases.split(";")) if phrases else (), reason
    earlier = {(r["block"], r["source_reference"]["offset"]): r for r in previous_review["records"]
               if r["block"] in BLOCKS[0]}
    records, plans, failures = [], {}, []
    for group in packet["groups"]:
        block = group["block"]
        for entry in group["records"]:
            number, selector = entry["source_record_index"], entry["selector"]
            old = earlier.pop((block, entry["source_offset"]))
            assert entry["Japanese"] == old["source_Japanese"] and old["source_selector"] == selector
            assert all(old["review"].values()) and entry["native_command_word"] == 0x4000
            jp, en = (bytes.fromhex(entry[f"{side}_body_hex"]) for side in ("source", "current"))
            prefix = bytes([selector])
            assert old["source_hex"] == (prefix + jp).hex()
            replacement, phrases, reason = decisions.pop((block, number))
            current = logical(entry["current_English"])
            english = replacement or current
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            refs = {side: dict(file_path=group["file_path"], block=block, offset=entry[f"{side}_offset"],
                               command_offset=entry[f"{side}_command_offset"],
                               archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                               exact_hex=(prefix + value).hex())
                    for side, value in (("source", jp), ("current", en))}
            changed = bool(replacement or phrases)
            row = dict(id=old["id"], file_path=group["file_path"], route=0, block=block, source_record_index=number,
                       native_command_word=0x4000, native_slots=[], source_selector=selector,
                       kind="system-FE" if selector == 254 else "progressive",
                       source_reference=refs["source"], current_reference=refs["current"],
                       source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                       Japanese=entry["Japanese"], previous_English=current, english=english,
                       speaker=old["speaker"], context=CONTEXTS[block] if block in CONTEXTS else village_context(number),
                       source_meaning=old["source_meaning"], localization_note=reason,
                       protected_phrases=list(phrases), decision="revision" if changed else "retention",
                       finding="prose and wrap" if replacement else "wrap" if phrases else "retention",
                       review=dict.fromkeys(GATES, True) | {"formatting": not changed})
            if changed:
                assert selector != 254
                try:
                    assert all(phrase in english for phrase in phrases), (number, english, phrases)
                    body, plan = plan_progressive(row, selector, en, jp)
                except (ValueError, AssertionError) as error:
                    failures.append((block, number, english, phrases, str(error)))
                else:
                    if body.rstrip(b" ") == en.rstrip(b" "):
                        assert not replacement, row["id"]
                        row.update(decision="retention", finding="retention")
                        row["review"]["formatting"] = True
                    else:
                        plans[row["id"]] = plan
            records.append(row)
    assert len(records) == 197 and not earlier and not decisions
    assert not failures, failures
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                         target_locale="en-US", review_gates=GATES, previous_sha256=packet["candidate_sha256"],
                         previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                         source_packet_sha256=base.digest(SOURCE), earlier_contextual_reviews={str(PRIOR): base.digest(PRIOR)},
                         records=records, plans=plans, decisions=dict(Counter(r["decision"] for r in records)),
                         findings=dict(Counter(r["finding"] for r in records)), new_editorial_credit=0,
                         status="Contextual review complete. Changed text awaits native formatting approval."))
    print(f"Reviewed {len(records)} records. {dict(Counter(r['finding'] for r in records))}.")


if __name__ == "__main__":
    main()
