"""Review Sera's memories, Nagarpur's procession and the sea-king legend."""

from inspect import getsource
from types import SimpleNamespace

from scripts import register_hodram_B54_B60_20261122 as parent
from scripts import review_hodram_B54_B60_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT, ARCHIVE = previous.ROOT, previous.ARCHIVE
SCOPE = tuple(range(61, 65))
paired = SimpleNamespace(PACKET=ROOT / "B61_B64_exact_current.json", CARRY=ROOT / "B61_B64_carried_decisions.json")
OUTPUT = ROOT / "B61_B64_contextual_v3.json"
GLYPHS = {"DK4_MES_B61_R0040", "DK4_MES_B62_R0079"}
CONTEXTS = {
    61: "Sera recognizes the place from her escape. Hodram initially takes it as a clue to her homeland, then rephrases his question until she understands.",
    62: "Hodram finds Sera away from the crowds. She remembers her homeland before the fires, struggles to explain what might be left, and worries about staying on a warship.",
    63: "Nagarpur mistakes the crew's presence for a request for a tip. His display of wealth and his entourage's contempt anger the crew.",
    64: "Sera gives Hodram the leaf and associates him with a sea king from her homeland. His dismissal of the story hurts her, and he apologizes and agrees to look for the treasure.",
}
DECISIONS = {
    61: """
9|||Sera recognizes something but gives only the opening words. Leave space for Hodram's question.
13|||Hodram asks what is wrong when Sera trails off.
17|I... know this place.|know this place.|She recognizes the place. Keep the hesitation without making her recognition uncertain.
21|What? Then your homeland's close by?|your homeland's close by?|Hodram jumps to a possible location for her home and asks her to confirm it.
24|||Sera quietly rejects his first inference.
28|I see... Did you come through here when they brought you away?|when they brought you away?|Hodram asks whether her captors took her along this route. This is his second guess.
32|||Sera corrects him by naming her escape from the Ottomans. The pause is part of her limited speech.
36|The Ottoman Turks! Did their empire destroy your country?|The Ottoman Turks!;destroy your country?|Hodram names the Ottomans and asks about the destruction of her country. The scale of the destruction is still his question.
40|?|?|Sera's puzzlement prompts Hodram to simplify the question. Use the regular question glyph.
44|Was that too hard to follow? I mean, Ottoman soldiers attacked your home, right?|Ottoman soldiers;your home, right?|Hodram simplifies the question to one about soldiers attacking her home. Her answer applies to this simpler question.
48|||Her paused yes confirms the attack described in the preceding turn.
52|||Hodram takes in the answer and responds quietly.
""",
    62: """
5|||Sera is silent when Hodram finds her away from the noise.
9|||Hodram recognizes her and asks what brings her to this spot.
12|||Sera describes the city with the few words she has, giving Hodram a reason to explain it.
16|Yes. This is a hub for Indian Ocean trade. Does the bustle bother you?|Indian Ocean trade.;Does the bustle bother you?|Hodram identifies the city's trade role and uses bustle, which Sera asks about next.
20|||Sera repeats the unfamiliar word. Keep it identical to the word in Hodram's question.
24|||He explains bustle by asking how she feels about crowds.
28|||She distinguishes surprise from dislike. Keep the small pause as she finds words.
31|I see. You aren't used to it. It's quiet here, though.|You aren't used to it.;It's quiet here, though.|Hodram understands her unfamiliarity with the crowd and comments on their quieter spot.
35|||Leave Sera's silence between the city and her memories of home.
39|...What's your homeland like?|What's your homeland like?|Hodram gently changes the subject. The word homeland gives Sera another term to ask about.
42|||She repeats the unfamiliar word before Hodram explains it.
46|||The explanation gives her the exact concept of the country where she was born.
50|||Sera pauses before she starts to describe home.
54|||The repetition and simple images fit a memory expressed in few words. Spring and the abundance of flowers stay explicit.
57|Rivers... springs... birds. Goats... sheep... And...|Goats... sheep...|Preserve the list and let the hesitations show Sera recalling each thing in turn.
61|Far away... you can see the sea.|you can see the sea.|Sera adds the sea in the distance. The quiet delivery leads to Hodram's echo.
65|||Hodram is interested that the sea could be seen from her home.
69|||The repetition of blue preserves the emphasis and simplicity of her reply.
73|It sounds beautiful. I'd love to see it.|It sounds beautiful.;I'd love to see it.|Hodram imagines the place and expresses a desire to see it. Sera then reminds him what happened.
76|||Keep the abrupt return from the beautiful memory to the fires.
79|!|!|Hodram reacts with wordless shock before he apologizes. Match the regular English punctuation.
83|...Right. I'm sorry.|I'm sorry.|Hodram remembers what she has already told him and apologizes for speaking without thinking.
86|||Sera tells Hodram by his given name that he need not worry. Keep the substitution.
89|||Her unfinished thought leaves the fate of the town unstated.
92|||Hodram picks up on the mention of the town and asks what she means.
96|||Sera admits she cannot express what she is trying to say. The broken delivery is intentional.
100|||Hodram pauses before offering a way forward.
104|If you have no home to go back to, you can stay aboard as long as you like.|no home to go back to,;as long as you like.|He offers to let her stay indefinitely if she has no home to return to.
107|A warship... No women allowed. I'd be in the way...|No women allowed.;I'd be in the way...|Sera recalls the restriction and worries that she would be a burden. Keep her words sparse.
110|You remember what I said before you knew our language...|before you knew our language...|Hodram is taken aback that she remembers what he said before she could speak with him.
114|It's all right. The crew likes your cooking. Nobody's going to object.|The crew likes your cooking.;Nobody's going to object.|Hodram says he does not mind, mentions the good reputation of her cooking, and assures her nobody will object.
118|||Sera responds with his given name and a pause. Keep the source substitution and her emotional restraint.
""",
    63: """
5|Make way for Nagarpur and his party! You there, Westerner! Clear the road!|Nagarpur and his party!;Clear the road!|The escort orders the road cleared, singles out Hodram as a Westerner, and announces the party.
8|||Hodram repeats the name in surprise before they see who is approaching.
12|||Gerhard's wary question conveys that he finds the large procession odd.
15|Ho ho ho! Make way, please! Hmm? You there. Did you want something from me?|Make way, please!;want something from me?|Nagarpur's affected politeness and laugh precede his assumption that Hodram wants something.
19|||Hodram is confused and explains that he was not trying to obstruct them.
22|Hmm, I see! You're after a tip. Here you go!|You're after a tip.;Here you go!|Nagarpur concludes without evidence that they want money and makes a show of tossing a tip.
34|What the hell gave you that idea?!|gave you that idea?!|Al Shin lashes out at Nagarpur's mistaken assumption.
41|||Gerhard interprets the act as an insult to his admiral and uses the original given-name substitution.
48|Ho ho ho! What, isn't that enough? Want some more? I've got money to spare!|isn't that enough?;money to spare!|Nagarpur thinks they object only to the amount and boasts that he has more than enough money.
52|Nagarpur... Now I remember. The Nagarpur Company. Notorious rich upstarts. They seem to run things here.|The Nagarpur Company;Notorious rich upstarts.;They seem to run things here.|Gerhard recognizes the company's reputation for recently acquired wealth and qualifies its local influence.
56|||Hodram dryly observes that Nagarpur has been making plenty of money.
60|||Nagarpur's threefold repetition makes his view of money into a boast the others can react to.
63|If money's everything to you, that's pathetic.|that's pathetic.|Hodram condemns Nagarpur's priorities rather than disputing that he is rich.
75|I like money myself. But anyone who thinks it's everything is rotten to the core.|I like money myself.;rotten to the core.|Fernando admits a liking for money and condemns those who believe it is everything.
82|||Nagarpur only half catches the criticism and asks what was said.
85|||The escort challenges Hodram again and keeps the same outsider address.
89|You're as ugly inside as you are outside. You make me sick. Let's go.|as you are outside.;You make me sick.|Hodram's insult turns the conversation into a direct dismissal, then he tells his crew to leave.
92|||Gerhard immediately agrees with Hodram's judgment.
96|Oh? You'd pick a fight with me? You've got a death wish, or something close to it...|pick a fight with me?;a death wish,|Nagarpur acts incredulous that they would cross him and trails off on their apparent recklessness.
100|||Nagarpur insists nobody can rival his wealth. The boast is already direct.
111|||Charles identifies Nagarpur's belief that money will solve any problem.
117|||Gerhard calls that view a severe delusion in his brief response.
121|Let him talk. All the money in the world won't help if you don't know how to use it.|All the money in the world;how to use it.|Hodram argues that wealth alone has little value when its owner lacks the ability to use it.
125|Ho ho ho! Instead of talking nonsense, why not figure out how to get as rich as I am?|Instead of talking nonsense,;as rich as I am?|Nagarpur airily dismisses the criticism and challenges them to learn how to make as much money as he does.
129|||Nagarpur orders his entourage forward and tells others to make way.
132|||The escort pushes through with the same terse command.
137|||Hodram concludes that he and Nagarpur have irreconcilable attitudes. The existing idiom fits.
140|I've never seen such rudeness! Let's show him how things work when he comes up against our fleet.|I've never seen such rudeness!;against our fleet.|Gerhard condemns the insult and urges using their fleet to teach Nagarpur how the world works.
""",
    64: """
11|Admiral FA, you truly are the king of the Indian Ocean. Please accept this.|Admiral FA,;of the Indian Ocean.;Please accept this.|The speaker addresses Hodram by surname, praises him as the king of the Indian Ocean, and offers the object.
17|||Sera speaks only Hodram's given name before offering her interpretation.
21|||His questioning sound invites her to explain why she called him.
25|...You... the king in the legend.|the king in the legend.|Sera identifies Hodram as the king from the legend using short, hesitant phrases.
29|||Hodram asks her to repeat or explain the surprising claim.
33|This.|This.|Sera draws his attention to what she is holding with one word.
37|||Hodram asks whether the object is for him and reacts before knowing what it is.
51|||His questions identify the leaf and then ask what it means and why it is for him.
55|||Sera introduces the story as a legend from her own country. Keep the source hesitations.
59|||Hodram echoes the word legend before she expands on it.
63|Silver hair... blue eyes. An iron ship. The sea king finds... the treasure passed down in the kingdom.|Silver hair... blue eyes.;An iron ship.;the treasure passed down|Sera names the physical traits, the iron ship, the sea king, and the kingdom's inherited treasure. Keep the choppy way she tells it.
66|Me? A king from a legend? In an iron ship?|In an iron ship?|Hodram questions both the identification and the description of the ship.
70|||The nod confirms her understanding of the story without additional dialogue.
74|||Hodram is quiet before laughing at the idea.
78|Ha ha ha! That's ridiculous. It's just a fairy tale.|That's ridiculous.;It's just a fairy tale.|Hodram laughs and dismisses the claim as a fairy tale, giving Sera a reason to feel mocked.
81|||Sera accuses him of making fun of her country's legend. Keep the given name and her pause.
84|Mocking it? But how am I supposed to believe a story like that? Silver hair and blue eyes? Hah! It sounds made up.|believe a story like that?;Silver hair and blue eyes?|Hodram protests that the traits sound contrived and laughs again, before realizing how his words sound to Sera.
87|||This time Sera says Hodram mocked her. The personal accusation is distinct from the earlier complaint about the legend.
90|||Hodram hesitates and says he did not mean it that way. The reply stays uncertain.
93|||Sera's silence gives Hodram time to apologize more directly.
97|I'm sorry. I really am. But there must be some mistake. It can't be me.|I'm sorry. I really am.;there must be some mistake.;It can't be me.|Hodram apologizes for the offense while still rejecting the idea that the legend refers to him.
101|||Sera uses his given name and insists he find the treasure. Keep her delivery brief.
104|Hm? All right, I'll look. I will. ...Don't look at me like that.|All right, I'll look.;Don't look at me like that.|Hodram finally agrees to search, repeats his promise, and reacts to her fierce look without putting words in her mouth.
""",
}

binding = checked_text(getsource(previous.bind_packet), {
    'receipt["successor_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)':
        'receipt["successor_sha256"] == release["predecessor"]["candidate_sha256"]\n'
        '    assert release["candidate_sha256"] == base.digest(parent.ROM)',
    'for g in groups) == 82': 'for g in groups) == 96',
    'len(carry["pending_records"]) == 79 and len(carry["reused_records"]) == 3':
        'len(carry["pending_records"]) == 95 and len(carry["reused_records"]) == 1',
})
review = checked_text(previous.source, {"len(records) == 79": "len(records) == 95"})
scope = previous.scope | globals()
for source in (binding, review):
    exec(compile(source, __file__ + "::linked-contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["bind_packet"]()
    scope["main"]()
