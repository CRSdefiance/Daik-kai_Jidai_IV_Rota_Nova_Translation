"""Review the farewell, Batavia feud, and the recovery of Kuhn's assets."""

from types import SimpleNamespace

from scripts import register_hodram_B61_B64_20261122 as parent
from scripts import review_hodram_B61_B64_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT, ARCHIVE = previous.ROOT, previous.ARCHIVE
SCOPE = tuple(range(65, 71))
paired = SimpleNamespace(PACKET=ROOT / "B65_B70_exact_current.json", CARRY=ROOT / "B65_B70_carried_decisions.json")
OUTPUT = ROOT / "B65_B70_contextual_v3.json"
GLYPHS = {f"DK4_MES_B{block}_R{number:04d}" for block, number in ((65, 14), (65, 77), (65, 120), (66, 68), (67, 15))}
CONTEXTS = {
    65: "Hodram realizes Sera has found someone from her country. She means to go home. Neither of them quite knows how to say goodbye, and the crew sees the parting.",
    66: "A port worker warns Hodram about the feud and then addresses Camille. Camille and Hodram recognize each other, but Camille is evasive about why he and Lil are apart.",
    67: "An intermediary brings Hodram to Maria. She tests his intentions, explains the cost of the Kuhn and Pereira feud, and weighs his offer against her own plan.",
    68: "Camille urgently asks Hodram to help Lil. Hodram gets a destination and agrees to take him before hearing the full story.",
    69: "Camille and Lil reconcile after the danger. She apologizes and takes him back aboard. Camille gives credit to Hodram, who describes his part modestly.",
    70: "Gerhard reports that Kuhn's hidden wealth has been found. Hodram directs it to the people Kuhn harmed, and Gerhard brings an unfamiliar find to his attention.",
}

DECISIONS = {
    65: """
6|||Sirwood calls out before Sera recognizes him. Preserve the exact circle, cross and punctuation glyphs used for their untranslated language.
10|||Sirwood is the approved name. The exclamation marks Sera's immediate recognition.
14|?|?|Hodram has only a puzzled reaction before Sirwood continues. Use the regular English question glyph.
18|||Sirwood has a longer excited utterance. Preserve the distinct original pattern of their untranslated language.
22|||Sera answers in the same language. Her different pattern and its emphatic punctuation stay as written.
26|||Hodram first realizes Sera might actually know the man. The startled question carries that change.
30|One of my people!|One of my people!|Sera identifies Sirwood with the people of her country. The line does not establish a personal relationship.
34|||Hodram's brief cry of surprise follows the identification. The abrupt existing reply fits.
38|||Sirwood's question is in the same opaque language. Preserve its exact symbol order and question glyph.
42|||Sera's answer remains in their language. Preserve the exact circle, cross and exclamation pattern.
46|So there were other survivors... No wonder they're glad to see each other.|other survivors...;glad to see each other.|Hodram learns that others survived and recognizes the emotion of the reunion. Remove the repeated filler.
49|||Hodram turns from surprise to relief for Sera. The quiet reassurance fits the discovery.
53|||Sera calls only his given name before speaking about leaving. Keep the exact runtime token.
57|||Hodram's short sound invites her to continue without guessing what she will say.
61|||Sera intends to return to her own country. The pause after her first word fits the moment before he accepts her decision.
65|||Hodram pauses and then agrees this is best. The subdued existing reply suits the farewell.
68|FI... You'll be king of the seas. I know it.|You'll be king of the seas.;I know it.|Sera tells him confidently what she believes will happen. Keep his given name and the established expression.
74|FI... When you become king of the seas...|When you become;king of the seas...|She starts a thought conditional on his becoming king of the seas and leaves it unfinished.
77|?|?|Hodram's quiet uncertainty gives Sera room to finish. Use the regular English question glyph.
81|When you do...|When you do...|She repeats the unfinished condition in her own short, hesitant words.
85|||The short prompt asks her to finish without teasing or supplying her conclusion.
89|...We can... see each other again.|see each other again.|She says they can meet again, with the same pauses. Do not add a promise or an explanation of her feelings.
93|Yeah. I hope so.|I hope so.|Hodram voices a quiet hope in response to hers. It is his wish, not a promise.
97|||Sera's original silence holds after they talk about meeting again. Preserve the standalone native ellipsis.
101|||Hodram warns her to be wary of Westerners, then includes himself. The wording already retains the pause and the uncomfortable self-judgment.
104|||Her silence after his warning gives her time to call to him again. Retain the separate original pause.
108|||Sera calls his given name more emphatically. Keep the controlled name and the exclamation.
112|||Hodram turns his attention back to her. His brief response leads into her own language.
116|||What Sera says this time remains unintelligible to Hodram. Preserve the exact glyphs in her final untranslated utterance.
120|!?|!?|Sirwood gives a wordless startled reaction. Preserve the punctuation order and use the regular English glyphs.
124|||Hodram asks what she said, confirming that the player should not get an invented translation of the previous utterance.
128|Nothing... Thank you...! Goodbye!|Thank you...!;Goodbye!|Sera waves off the question, struggles to get her thanks out, and finally manages her farewell.
132|Yeah... Goodbye.|Yeah... Goodbye.|Hodram pauses and returns the farewell in a low-key voice.
144|||Gerhard watches in silence. Keep his own speaker turn before Manuel's.
150|||Manuel has a separate silent reaction. Preserve the change of speaker.
157|||Gerhard asks if Hodram is sure about letting her go. The short question leaves the decision with Hodram.
161|...She's strong. I think she'll be all right.|She's strong.;she'll be all right.|Hodram trusts Sera's resilience. The line expresses his confidence without guaranteeing what happens to her.
170|||Gerhard's last silence follows Hodram's answer. This is a distinct speaker turn.
176|||Charles closes the scene with a silent turn, separate from Gerhard's.
""",
    66: """
6|You're new here. Clear out before Kuhn and Pereira drag you into their feud.|You're new here.;Clear out before;Kuhn and Pereira;drag you into their feud.|The port worker sees an unfamiliar face and bluntly warns him against getting caught in the feud.
26|Either way, I've got nothing to celebrate. Right?|nothing to celebrate.;Right?|He says neither victor would make him glad and turns his question to Camille. An English kinship or age label is unwarranted.
31|||Camille agrees with a slight stammer before recognizing Hodram.
35|||Hodram begins to recognize Camille. The startled fragment leaves room for Camille's reaction.
39|||Camille moves from puzzlement to recognition. The two short reactions retain the reversal.
45|Wait... Camille? Is that you?|Camille? Is that you?|Hodram recognizes and names Camille in surprise. He uses no English honorific.
49|||Camille addresses Hodram by the runtime given name and checks that he has recognized him.
52|||Hodram asks why Camille is there and where Lil is. Both direct questions fit the turn.
56|Well... We're working separately for now.|working separately;for now.|Camille stalls and acknowledges that he and Lil are operating separately for the time being. He gives no itinerary or reason.
59|||Hodram's puzzled sound shows he has noticed the evasion.
63|||Camille awkwardly excuses himself without offering any more detail.
68|?|?|Hodram is left puzzled before Gerhard speaks. Use the regular English question glyph.
72|Sounds like there might be more to it...|more to it...|Gerhard suspects there is a reason for Camille's behavior. The line stops short of claiming he knows it.
""",
    67: """
5|||The intermediary confirms the surname, conveys an unnamed person's request, and politely asks Hodram to come along. The existing questions keep the controlled surname and the stranger's discretion.
8|||Hodram's brief response makes clear he did not expect to be sought out.
12|||The intermediary reassures him that the meeting will take little time.
15|?|?|Hodram remains puzzled. The normal question glyph conveys the silent beat.
25|||This original silence leaves the person who summoned him free to speak first.
29|||Maria welcomes him before either has explained why he is there. Keep her simple greeting.
33|||Hodram pauses and then asks who she is. The timing fits his wary opening.
36|That depends. I might be your enemy.|I might be your enemy.|Maria introduces herself by a possibility and makes him wait for the condition.
39|||Hodram echoes her apparent threat so she can explain what she means.
43|||Maria makes her hostility conditional on whether he intends to exploit Asia. Her established term Westerner is relevant to her accusation.
47|||Hodram takes two beats before explaining his stated purpose. Preserve the original double ellipsis.
51|We have one goal. We want our country's navy to rank among the best in the world.|our country's navy;among the best in the world.|Hodram aims for a first-rate navy for his country. Ordinary language makes the claim sound like his own.
55|A noble story to tell while you're pushing people aside to get this far.|A noble story;to get this far.|Maria treats his claim as a lofty justification for the way he has advanced. Her reply is skeptical and personal.
59|||Hodram refuses to defend himself to her on those terms. His short answer keeps that distance.
63|But whenever I look at the fleet we've built, I can't help thinking how much more we could achieve.|the fleet we've built,;how much more;we could achieve.|The sight of the fleet they built stirs ambitions he cannot dismiss. He has not promised conquest or a particular objective.
66|Sailors the world over battle fiercely for the seas. For those of us who live at sea, there's no greater stage.|Sailors the world over;for the seas.;no greater stage.|Hodram sees the fierce competition for sea power as the greatest stage for people who live at sea. Keep the metaphor that Maria laughs at.
69|||Maria takes a silent beat before she laughs. It is part of the turn from suspicion to amusement.
73|||Maria lets out a laugh and asks how he says that with a straight face. The existing English carries the disbelief without adding an insult.
77|||Hodram lets her laughter hang before Maria speaks again.
81|Heh... Forgive me. I think I can trust you. All right. I'd like your help.|I think I can trust you.;I'd like your help.|Maria apologizes, tentatively decides he is trustworthy, and turns toward asking for help.
89|||Maria gives the full approved Maria Huamei Li after the short echo of his question.
98|What?! The Li family? What brings you here?|The Li family?;What brings you here?|Hodram recognizes the Li family connection and is surprised to find her in this place.
102|Scouting the enemy, you could say. Keep it to yourself. As far as anyone knows, I'm not here.|Scouting the enemy,;Keep it to yourself.;As far as anyone knows,;I'm not here.|She gives a qualified description of her visit and insists on secrecy. Her cover story is that she is absent.
111|FA, have you heard of Kuhn and Pereira?|have you heard of;Kuhn and Pereira?|Maria addresses Hodram by surname and asks about both men. Keep their names together.
126|||Hodram acknowledges that he knows them on this branch. Keep the positive response short.
132|||This branch has him echo only Kuhn's name. It leaves his familiarity open.
147|||This branch has him echo only Pereira's name. Keep the distinct query.
153|||On this branch he says he does not know them. The preceding pause fits.
165|They're prime examples. They're still at odds over who controls the Spice Islands and the fortunes they bring.|They're prime examples.;the Spice Islands;the fortunes they bring.|Maria identifies the two men as the best examples of her enemies. Their contest for control of the Spice Islands has huge profits at stake.
168|They'll do anything for their own gain. They shell towns, take them by force, and claim the spice lands as their own.|their own gain.;take them by force,;as their own.|Maria describes their bombardments, forceful occupation and appropriation of producing regions. The scope is shared by the two rivals here.
172|Kuhn's the worst of the two. He arrests anyone who so much as displeases him and crushes every uprising by force.|the worst of the two.;so much as displeases him;uprising by force.|Maria singles out Kuhn for arbitrary arrests of townspeople and determined suppression by force. She is describing the most severe of the rivals' methods.
175|I see... I understand what you mean by enemies. So how do you want me to help?|what you mean by enemies.;how do you want me to help?|Hodram understands Maria's category of enemies and asks her what sort of cooperation she wants.
179|||Maria says that the first thing he can do is stay out of her plan. The existing reply preserves the pointed instruction.
182|||Hodram's one-word echo shows the instruction took him by surprise.
186|I'll set them against each other and wear them down. Then I'll take the chance to drive them both out of Asia at once.|set them against each other;wear them down.;out of Asia at once.|Maria intends to weaken the rivals through fighting and take the opportunity to expel them both in one move.
190|||Hodram doubts whether it will go as smoothly as she says. The short question plays against her confidence.
194|||Maria qualifies the plan by admitting it will take time. Keep that limited concession.
198|||Hodram points out the cost of waiting while they continue their abuses. The existing expression makes his objection clear.
201|||Maria's silence lets his objection land before he offers a different approach.
205|||Hodram asks if she is willing to hear his proposal. The existing phrasing suits his direct manner.
209|||Maria pauses and then asks what he has in mind. Keep her guard up through the reply.
213|No need for schemes. I'll drive them out. That's it.|No need for schemes.;I'll drive them out.|Hodram proposes driving both rivals out himself, with no elaborate maneuvering. The curt close keeps his confidence.
216|||Maria asks whether he means to do it himself. Her brief question sets up his accusation.
220|||Hodram sees through her reaction and calls out the suggestion that she wanted him to volunteer. The current phrasing fits the exchange.
223|||Maria's small laugh acknowledges that he read her correctly.
227|You win. Enough games. I have my reasons, but right now I really can't spare a fleet to send this far.|Enough games.;right now;can't spare a fleet;to send this far.|She concedes the point, drops the games, and admits she cannot spare a fleet here at present for reasons she leaves private.
230|||Maria remains uneasy about trusting the whole task to his force alone. The hesitation keeps her doubt distinct from her admission.
234|||Hodram responds drily to her direct assessment. His reply is brief enough to preserve the pace.
238|Kuhn took over Portugal's interests here in no time, and only recently. He's no ordinary opponent. He won't go down easily.|Portugal's interests;in no time,;only recently.;won't go down easily.|Maria reminds him how recently and quickly Kuhn took over Portuguese interests in the region. She warns Hodram that he faces a formidable opponent.
241|Don't rush in and overreach. He'll hit back hard. And remember, I'm going ahead with my plan either way.|Don't rush in and overreach.;He'll hit back hard.;going ahead with my plan|Maria warns against reckless haste and a painful counterattack, then tells Hodram her original plan will continue.
244|||Hodram gives her leave to act as she wishes. The quiet dismissal fits after the warning.
""",
    68: """
5|||Camille calls Hodram by his given name and asks for help immediately. Keep the controlled name.
8|||Hodram recognizes Camille and asks what happened. His short line gives him the floor.
12|||Camille repeats Lil's name in distress. The existing break in his speech preserves his urgency.
16|||Hodram asks what he means before choosing what to do.
20|Kuhn's got her fooled! If we don't do something, she'll walk right into his trap!|Kuhn's got her fooled!;walk right into his trap!|Camille says Kuhn is deceiving Lil and warns she is about to fall into a trap. It has not happened yet.
24|I don't follow, but that can wait. Where is she?|that can wait.;Where is she?|Hodram sets aside his confusion to establish the location before doing anything else.
27|Batavia! I'm sorry. I'll explain everything later!|Batavia!;I'll explain everything later!|Camille names Batavia, apologizes for rushing him, and promises to give the explanation later.
30|||Hodram tells Camille to come with him at once. The immediate commitment fits the urgency.
""",
    69: """
6|Lil! Thank goodness we got here in time!|Thank goodness;got here in time!|Camille is relieved to reach Lil in time. Keep the relief on reaching her without adding a claim about what she did.
11|I'm sorry, Camille. I'm so sorry. You tried to stop me, but I... I believed that man anyway.|I'm so sorry.;You tried to stop me,;believed that man anyway.|Lil apologizes twice, stumbles over her words, and acknowledges that she listened to the man despite Camille trying to stop her.
14|||Camille immediately reassures Lil. His short reply leaves her room to finish.
23|If anyone deserves thanks, it's FI.|deserves thanks,;it's FI.|Camille directs Lil's gratitude to Hodram. Keep the controlled given name in the more conversational reply.
26|All I did was bring you here. I don't know the whole story, but it looks like you two can patch things up.|bring you here.;the whole story,;patch things up.|Hodram gives his contribution as transportation alone and cautiously expects the two to reconcile. The idiom is about making peace and establishes no romance.
30|Huh? Oh, um... Lil, could I come back aboard your ship?|come back aboard;your ship?|Camille stammers and then asks Lil directly if he can sail with her again.
34|Of course! Things were hard without you. You've got work to make up for!|Things were hard without you.;work to make up for!|Lil welcomes him back, admits how hard it was without him, and tells him to make up the work he missed. The teasing gives their reconciliation a lift.
38|Looks like that's settled.|that's settled.|Hodram observes that they have worked it out without making himself part of their dispute.
42|FI, you helped me when I couldn't even tell you why. Thank you. I mean it.|I couldn't even tell you why.;Thank you. I mean it.|Camille thanks Hodram sincerely for helping before he knew the circumstances. Preserve the given-name substitution.
45|Don't mention it. You two get along, all right?|Don't mention it.;get along, all right?|Hodram waves off the thanks and tells them to get along. The warm tag closes the scene without imposing a relationship.
""",
    70: """
6|Admiral, we've found Kuhn's hidden fortune.|Kuhn's hidden fortune.|Gerhard addresses his admiral and reports the discovery of Kuhn's hidden wealth.
9|||Hodram orders all the assets distributed to the people Kuhn hurt. The existing wording preserves the full amount and beneficiaries.
12|This turned up with the rest...|turned up with the rest...|Gerhard calls attention to an unidentified object he found with the recovered assets. He does not name it.
15|||Hodram's short response looks at the thing Gerhard has just singled out. The name of the object remains unstated.
""",
}

binding = checked_text(previous.binding, {
    'receipt["successor_sha256"] == release["predecessor"]["candidate_sha256"]':
        'receipt["successor_sha256"] == base.load(parent.parent.RELEASE)["predecessor"]["candidate_sha256"]\n'
        '    assert base.load(parent.parent.RELEASE)["candidate_sha256"] == release["predecessor"]["candidate_sha256"]',
    'for g in groups) == 96': 'for g in groups) == 128',
    'len(carry["pending_records"]) == 95 and len(carry["reused_records"]) == 1':
        'len(carry["pending_records"]) == 125 and len(carry["reused_records"]) == 3',
})
review = checked_text(previous.review, {"len(records) == 95": "len(records) == 125"})

scope = previous.scope | globals()
for source in (binding, review):
    exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["bind_packet"]()
    scope["main"]()
