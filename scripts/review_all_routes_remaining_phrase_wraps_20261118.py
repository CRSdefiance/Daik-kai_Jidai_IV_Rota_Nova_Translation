"""Review the next 30 phrase breaks with source-bound decisions for the surrounding turns."""

from inspect import getsource
from pathlib import Path

from scripts import register_all_routes_next_review_wraps_20261118 as parent
from scripts import review_rafael_early_phrase_wraps_20261118 as common
from scripts.source_locked_derivation_v5118 import checked_text

base, TOKEN, logical = common.base, common.TOKEN, common.logical
ROOT = parent.stage.review.ROOT.with_name("all_routes_remaining_phrase_wraps_20261118")
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v1.json"
LETTER = Path("releases/all_routes_editorial_20261118_dialogue_followup_candidate/verification/registered_review.json")

EXCHANGES = """
0,312|In the desert the crew suggests a turn, but Rafael trusts the map and presses on. Later responses vary by the navigators present.
234|Rafael questions the suggested turn, trusts the map and orders the party forward.|Keep the uncertainty in his first reaction and the confidence of the order.

0,313|A novice dancer has been asked to perform for the lord. She explains how one customer seeing her dance turned into a rumor that she is the best in the country.
14|She must dance for the lord at the next festival.|Her practical announcement gives Rafael a reason to ask how she learned.
17|Rafael did not know she could dance.|His light surprise invites her explanation.
22|She has just started dancing. The lord seems to have heard after she danced for a customer.|Both the source of the rumor and her uncertainty are clear.
25|The story grew until she was thought the best dancer in the country.|Keep the absurd scale of the rumor in a complete thought.
29|Rafael stammers and asks how this happened.|The short reaction fits his disbelief.
34|She says that is how rumors work and she cannot confess or improve quickly.|The dilemma remains hers, in her own voice.
37|Rafael asks what she will do.|The practical question leads out of the backstory.

0,317|The adviser recommends reading the Arabian Nights to the king as a way to lift the curse. Clau questions the approach and Rafael notices how the advice has drifted.
91|A translated edition may have a different title.|The conditional explains why the book might be harder to identify.
95|Rafael repeats the clue about the title.|The echo gives it weight before the advice continues.
100|Reading the book might lift the king's spirits.|The remedy stays provisional.
103|Clau thinks it sounds like playing host or babysitting and asks if it will work.|Let the comic correction land between the observation and the question.
107|The adviser cannot promise success and says sincerity matters when honoring the dead.|The invocation of the dead sets up Rafael's objection.
110|Rafael reminds him their task is to break a curse.|The hesitation preserves Rafael's confusion.
115|The adviser sees little difference and suggests they try something else if it fails.|His casual confidence works after Rafael's earnest objection.

0,318|During the reading the quoted invocation gives way to the specified tale. The next morning a guard asks whether they have broken the curse.
133|The reader clears his throat to begin.|The audible hesitation works before the formal text.
137|The reader invokes Allah, naming His graciousness and mercy.|The formal religious language and repetition suit a reading.
141|The invocation praises Allah and continues to praise the leader foremost among those sent to earth.|Keep the formal parallel and leave the quotation unfinished where the Japanese does.
146|The reader announces the tale of the merchant and the Ifrit.|The title identifies the quoted story.
151|Scheherazade addresses a fortunate king and starts a tale she heard.|Keep the embedded quotation and formal address within the reading.
160|Clau realizes he fell asleep.|His sheepish aside makes the shift to sunrise comic.
163|Rafael observes that morning has come.|The brief line orients the player in time.
168|The guard is relieved and asks whether they broke the king's curse.|The question leaves the discovery with the characters.

0,320|At the end of the search, Clau wonders whether going back would have been quicker and jokes privately about Rafael's insistence that the shortcut was worth it.
158|Rafael exclaims that he found it.|The excitement precedes Clau's practical concern.
163|Clau wonders whether turning back would have saved time.|The speculation keeps the comparison open.
166|Rafael still thinks the shortcut took less time.|His mild disagreement gives Clau a reason for his aside.
170|Clau agrees aloud and privately finds Rafael surprisingly stubborn.|Keep the audible concession distinct from the unspoken joke.

0,334|The guide brings Rafael's party by boat, then announces that they must go on foot. The same instruction appears in Hodram's route.
65|The guide has arranged for them to use a small boat.|The particular mode of travel sets up the following change.
68|Only the party may go. The guide wants the ruins kept secret from the sailors.|Both the restriction and confidentiality remain explicit.
81|The guide announces arrival and asks them to continue on foot.|Use the reviewed Hodram wording for the byte-identical body.
84|The guide sees what they were looking for.|The exclamation answers the anticipation created by the trip.

0,336|The party considers the warrior trial because the secret ruins may contain a key. The guide asks for the Tlaloc Knife as a test.
69|Rafael agrees to try.|His pause preserves the moment of decision.
74|Clau asks if he is sure.|The brief question invites Rafael's motives.
84|Rafael wants to test his ability as a warrior and has another reason.|The final hesitation leaves room for the clue in the next turn.
89|The ruins may contain a key to a Proof of Conquest, so Rafael thinks it is worth trying.|Keep the prospect tentative and the question intact.
96|The crewmate agrees and thinks secret ruins might conceal something.|The reasoning supports Rafael's interest.
100|The crewmate agrees that a key might be in those ruins.|Use the same name for what Rafael and the crewmate hope to find.
106|Clau accepts that possibility and agrees to help.|His change of mind follows the concrete incentive.
109|The guide thanks them and is ready to start.|The unfinished transition builds anticipation for the test.
112|The guide asks them to find something to show their skill with a sword.|State the purpose clearly and let Rafael ask what to find.
116|Rafael asks what the object is.|The question sets up the item name.
121|They are to find the Tlaloc Knife, rumored to be hidden somewhere in the New World.|The item, location and return instruction remain clear.
125|Rafael repeats the artifact name.|The echo emphasizes the new objective.

0,342|Charles recognizes the Alchemy Book, explains why he came to the New World and starts thinking aloud. Rafael cuts him off and gets back to the monk.
70|Rafael is startled by Charles's reaction.|The stammer makes Charles's outburst audible in context.
75|Charles came to the New World after hearing of a new material for experiments.|Keep his personal reason and the story's rumor.
78|Charles learned he needs the Alchemy Book to obtain the material.|Make the line consistent with Hodram's parallel and leave the thought unfinished.
82|Charles has no doubt the book points to a precious metal. He starts muttering about how to use it.|Keep the shared wording with Hodram and the shift into an aside.
85|Rafael interrupts to avoid a long explanation.|The uneasy interruption keeps his reason distinct from Hodram's.
92|He asks where the monk is now.|The question moves back to the original subject.
96|The reply is silence.|The pause leaves the question for the following story beat.

1,324|Charles is startled to see the Alchemy Book and explains his research. Hodram says there is no time and asks about the monk instead.
65|He is astonished to find the Alchemy Book here.|The stammer preserves his excitement.
69|Hodram wants to know what is going on.|His concise question draws out Charles.
73|Charles heard that an experimental material was found in the New World.|The rumor and its value to his work motivate his next line.
77|Charles discovered that getting the material requires the Alchemy Book.|Preserve the same meaning and the unfinished thought in Rafael's route.
81|The book is clearly a clue to a precious metal. Charles mutters about getting it to work.|The parallel Rafael line shares the same Japanese and sounds the same in Charles's voice.
84|Hodram says there is no time for a detailed explanation.|His direct refusal fits his practical response.
90|Hodram asks where the monk is.|His immediate question returns them to the task.
94|The reply is silence.|The pause lets the next account begin.

2,159|A recruit presumes he can join. Camille needles Lil about scowling and the recruit makes things worse with a joke of his own.
53|He wants to come along because he is tired of elephants and wants to see other countries.|His confidence preserves the unexpected reason he asks.
56|Lil objects that nobody gets taken aboard merely for asking.|Her indignation sets up Camille's teasing.
60|Camille warns Lil that scowling will give her wrinkles.|Keep the runtime name and his private teasing made public.
63|Lil splutters and protests at what Camille said.|The brief outburst keeps her shock and his name together.
66|Camille apologizes to the recruit and jokes about Lil's temper.|The apology and tease set up the recruit's reply.
69|The recruit calls her Tubby and praises his own tolerance.|The same comic insult gives Lil her next line.
73|Lil angrily challenges the insult and threatens him.|The stammer and threat follow the provocation.

2,163|The sailor boasts about a solo feat. Lil asks what he would have done if he could not turn back, and he answers with a maxim.
95|He cheerfully says he improvised.|His confident brevity helps explain the crew's amazement.
98|Lil asks if he was alone.|The short exclamation makes the risk clear.
102|Camille wonders whether the sailor is a genius.|His tentative admiration balances Lil's concern.
106|Lil asks how he would have reacted if turning back were impossible.|Use a past hypothetical and two complete questions.
109|The sailor asks them to listen to a famous saying.|His showmanship sets up the answer.
113|He asserts that determination is enough and believes it works for him.|The maxim preserves his swagger.
124|A crewmate thinks the man will be trouble.|The dry aside undercuts the boast.

2,167|The shipwright compares sails and explains how the wind hits a ship with several masts. The crew supplies the reason for the speed difference.
62|The shipwright approves and says they will go far.|His easy encouragement suits the tutorial.
65|He says a sailing ship depends on its sails.|The plain opening introduces the lesson.
68|He begins by comparing square sails with triangular sails.|Introduce the two kinds in a single phrase before explaining the difference.
71|He describes the square sail as one of the sails hung across the ship.|Keep the orientation in the explanation.
75|Square sails work well downwind but do not turn far enough for the best angle in a headwind.|The stated trade-off is the practical lesson.
78|A triangular sail is a lateen, aligned fore-and-aft and unable to turn crosswise.|Keep both the English nautical name and the contrast.
92|A staysail fits in front of a mast but would overlap a lateen.|The placement and restriction remain distinct.
95|The spritsail is square, at the bow, and small ships cannot fit it.|The three details are clear.
98|The jigger spanker is a fore-and-aft stern sail and large ships alone can fit it.|The explanation keeps both placement and size restriction.
101|A ship with two or more masts goes faster with wind from a slight angle than straight astern.|Keep the comparison and the rhetorical question without separating the subject early.
105|He asks one listener to explain why.|The direct invitation keeps the teacher's voice.
109|The listener answers that the masts are one behind another.|The succinct observation prepares the explanation.
112|The rear mast alone catches a wind from directly astern.|The consequence of the mast arrangement stays explicit.

2,168|Mikhail boasts about his memory and makes the woman uncomfortable. Camille acknowledges what he seems to know and Lil remains skeptical.
97|Mikhail brags about his knowledge and says he can guess the woman's bust size.|The uncomfortable boast is what they react to.
101|She calls him a dirty old man.|The outcry rebukes him directly.
105|He laughs.|His reaction makes the others' concern plausible.
109|Camille thinks the man is odd but apparently knowledgeable.|Keep the caution and break after a complete thought.
112|Lil thinks he is more than a little odd and seems lecherous.|The sharper reply fits her skepticism.
116|Camille needles Lil that she is safe.|The native given-name token remains part of the tease.
119|Lil objects to the implication but admits the crew may need him.|The reaction and concession preserve her change of approach.

2,169|Lil warns Mikhail about his conduct. Camille shifts from the teasing to the practical question of collecting the Proofs of Conquest.
107|Lil says he must be useful aboard her ship and warns him about touching her.|Her warning has force after the preceding incidents.
111|Mikhail dismisses her concern and laughs.|His reaction keeps the provocation alive.
115|Lil says that did not reassure her.|The reply closes her exchange with Mikhail.
119|Camille asks Mikhail how to collect the Proofs of Conquest.|Keep the addressee and the full established objective name.
123|Mikhail advises becoming the strongest force in the area because influential people often have clues.|The advice and the reason stay together.
126|He says an evil person who holds a clue may have to be defeated.|The qualification remains in his own account.
130|Lil jokingly reduces that advice to beating the villains.|The blunt wording suits her reaction.

2,174|Lil lets Julian join her. He immediately flirts, Lil threatens to toss him overboard, and Mihwa rebukes him for doing it in front of her.
98|Julian promises not to cause trouble.|His assurance sets up the immediate joke.
102|Lil agrees to bring him aboard.|Her direct consent keeps the setup clear.
106|Julian says merely sailing with someone as cute as Lil makes him happy.|The compliment supplies the trigger for both reactions.
110|Lil warns him she will throw him overboard if he says more.|Preserve the threat in a quick comic sentence.
113|Mihwa asks what Julian means to do about her.|Her question calls him to account.
116|Julian stumbles over a greeting.|His hesitation signals he knows he has a problem.
120|Mihwa objects to his flirting in front of her and tells him to go.|The rebuke stays specific to what he just did.

2,183|Three patrons disagree about the best art on display. Each defends the painter he wants to buy from.
25|The first patron advises buying the painter's work now.|Keep the recommendation that prompts disagreement.
28|A second patron prefers another work.|The strong preference fits the argument.
32|The first patron concedes that the other is good but prefers his choice.|Keep the concession and the unstated comparison target.
35|A third patron claims a different piece is clearly better.|The emphatic interruption raises the comic disagreement.
39|The first patron decides to buy his preferred painter's work anyway.|The exclamation makes the decision final.
42|The second patron chooses a work by the artist who painted the piece he likes.|The decision keeps the two choices distinct.

2,188|A lord admires fine glass, credits a skilled artisan and asks about its name. The retainer supplies the period term and the material.
14|The lord believes a famous artisan must have made such a fine piece.|The inference conveys his appreciation.
18|The retainer agrees formally.|The short assent keeps the difference in register.
22|The lord is surprised to learn pieces like it are in fashion.|Keep the discovery in a complete thought.
26|He asks what the piece is called.|His question invites the period term.
30|The retainer calls it giyaman and glosses it as glass.|The approved transliteration and contextual gloss preserve the cultural reference.
34|The lord repeats the new term.|The unfamiliar word stays with the character.

3,141|Sanghyeon introduces himself as Yifa's senior fellow student. He takes responsibility for her behavior and explains why he has come.
28|He gives his name and identifies himself as Yifa's senior in their school.|The student relation is clear without implying kinship.
32|He pays his respects because Maria is taking Yifa in.|His formal visit follows his introduction.
36|Maria repeats the connection to Yifa in surprise.|The unfinished question gives him room to explain.
40|He is ashamed and blames his poor guidance for Yifa's unruly ways.|Let him take responsibility in his own formal voice.
43|He says she left the mountain without permission to evade training and went abroad.|The objection follows the increasing seriousness he attributes to her actions.
47|Yifa does not know that people of their country are forbidden to leave it.|Keep the restriction in Sanghyeon's account.
51|Maria assumes someone came to take Yifa back.|Her question lets Sanghyeon clarify his objective.

3,146|Maria offers help with Yukihisa's search for a sword. He declines, and she suggests giving him a fleet and time to look on his own.
35|Maria has heard Yukihisa is looking for a sword.|The discreet statement lets him explain.
39|He suspects it may be only a rumor because their travels yielded no clue.|Keep his uncertainty and the reason for it.
42|Maria offers to help.|Her conditional offer keeps the exchange considerate.
45|He says the search is unrelated to their purpose and asks her not to trouble herself.|The courteous refusal motivates her solution.
49|She checks if he is willing to go to Japan on his own.|The alternative comes from Maria.
52|Yukihisa is surprised.|His short reaction lets her finish explaining.
56|Maria suggests putting him in charge of a fleet so he can search at his own pace.|Her offer keeps who commands and why separate.

3,170|On the purchase branch the seller wishes Ian the same romance as the celestial-maiden story. His dry answer gives her room for one last tease.
44|Ian agrees to take the item.|The terse purchase leads into the seller's good wishes.
48|The seller hopes Ian has a chance to fall in love with a celestial maiden himself.|Keep the comparison to the story and her playful tone.
52|Ian says he is not interested.|The polite refusal preserves the humor.
56|She regrets that such a handsome man is uninterested.|The compliment follows his refusal.
63|Ian declines in a separate branch.|His courteous rejection fits the purchase choice.

3,184|Cristina watches two swans, sees them fly away with something and tells Maria what she noticed.
20|Cristina envies how close the birds are.|The fond observation establishes her interest.
27|Cristina wonders where they are going and spots something they carry.|Use a complete first question and an immediate discovery.
31|She thinks over the direction they flew.|The unfinished thought introduces the next clue.
35|Maria asks what Cristina is watching.|Her ordinary question brings the sighting into the conversation.
38|Cristina explains that she saw a pair of swans.|The admiral's native name substitution keeps the greeting intact.

3,197|Julian's fanciful flirtation meets a dry answer. He tells her that is part of her charm, leaves, and she admits he got to her a little.
34|She accuses him of joking as usual.|The brief response fits their banter.
38|He imagines her turning him to stone so he could stay near her in moonlight.|The absurd image and romantic claim set up her retort.
42|She says she will not look after him even as stone.|The deadpan reply supports the joke.
45|He calls her cold but says that aloofness is charming, then says goodbye.|Preserve the affectionate complaint and let the goodbye land.
49|She says goodbye.|The plain answer leaves her reaction for the private aside.
53|She finds his comparison odd but admits it made her heart flutter.|The admission completes the emotional reversal.

3,200|Maria finds Yifa practicing late. Yifa explains why holding back against a sword is dangerous, then wonders about a rumored training uniform.
4|Yifa cries out while training.|Her short exertion leads into Maria's observation.
8|Maria observes the late practice and cautions against overdoing it.|The advice fits her concern for the recruit.
12|Yifa says it takes courage to face someone with a sword.|The plain statement prepares her specific warning.
15|Fear of the blade can make a halfhearted approach more dangerous. Resolve matters when stepping in.|Keep the concrete warning and conclusion together on one page.
18|Yifa heard of a uniform so tough it can chip a sword and asks if Maria knows it.|Keep the rumored material effect and the question without padded gaps.
21|Maria wonders whether that could be true.|The question stays tentative.
25|Yifa says it would let her go all out.|Her imagined benefit explains the appeal.
28|Yifa catches herself relying on gear and quotes her master's instruction to train first.|The recollection closes the scene on the same training theme.

3,208|Charles writes about an unearthly roar that helped a convoy hold its own. A chance encounter saved the ships, and he suggests investigation.
34|The ships tried to escape but were slower and looked doomed.|The mismatch explains why the roar matters.
37|Far west of Lisbon, they reportedly heard a roar that sounded otherworldly.|The distance and reported nature make the clue specific.
40|They rallied at the roar and fought the pirates on even terms.|Keep Charles's image of fighting like lions and the shift in fortunes.
43|After holding out, they were saved when the Spanish navy chanced by. The pirates scattered and the merchants escaped narrowly.|Use the exact same published wording as Hodram's letter and retain the near escape on one page.
46|Charles says the sound remains unexplained and they do not know whether it was natural.|Keep his curiosity distinct from an assertion of the supernatural.
49|Charles suggests investigation and signs his letter.|The considered proposal and signature remain separate.
56|Maria wonders if there is something to the story and wants to verify it.|The reaction keeps the report open to examination.
"""
CONTEXT, NOTES, selected_blocks = {}, {}, [[], [], [], []]
for exchange in EXCHANGES.strip().split("\n\n"):
    header, *notes = exchange.splitlines()
    identity, context = header.split("|", 1)
    route, block = map(int, identity.split(","))
    assert block not in CONTEXT
    CONTEXT[block] = context
    NOTES[block] = "\n".join(notes)
    selected_blocks[route].append(block)
BLOCKS = tuple(tuple(route) for route in selected_blocks)

REVISIONS = {
    (312, 234): ("You think so? The map says we're on course. Let's keep going.", ("The map says we're on course.", "Let's keep going.")),
    (313, 25): ("The story kept growing. Suddenly everyone thought I was the best dancer in the country.", ("The story kept growing.", "Suddenly everyone thought I was", "the best dancer in the country.")),
    (317, 103): ("Sounds like we're playing host. No, more like babysitting. You really think it'll work?", ("Sounds like we're playing host.", "No, more like babysitting.", "You really think it'll work?")),
    (318, 141): ("'Praise be to Allah, Lord of heaven and earth. And to our leader, foremost of those sent to earth...'", ("Praise be to Allah,", "Lord of heaven and earth.", "And to our leader,", "foremost of those sent to earth...")),
    (318, 151): ("Scheherazade said, 'Blessed king, I have heard that long ago...'", ("Scheherazade said, 'Blessed king,", "I have heard that long ago...")),
    (320, 170): ("Yeah, yeah. (Didn't think he was so stubborn.)", ("Yeah, yeah.", "(Didn't think he was so stubborn.)")),
    (334, 81): ("We've arrived. We'll go on foot from here.", ("We've arrived.", "We'll go on foot from here.")),
    (336, 89): ("Those ruins might hold a key to the Proof of Conquest. Isn't that worth a try?", ("Those ruins might hold", "a key to the Proof of Conquest.", "Isn't that worth a try?")),
    (336, 100): ("We might even find a key to the Proof of Conquest.", ("We might even find", "a key to the Proof of Conquest.")),
    (336, 112): ("First, a test of swordsmanship. I have something for you to find.", ("First, a test of swordsmanship.", "I have something for you to find.")),
    (342, 78): ("I know I need the Alchemy Book to get that material, but...", ("the Alchemy Book", "to get that material, but...")),
    (342, 82): ("It must point to a precious metal! Now, if I could just work out how to use it... (muttering)", ("It must point to a precious metal!", "Now, if I could just work out", "how to use it... (muttering)")),
    (324, 77): ("I know I need the Alchemy Book to get that material, but...", ("the Alchemy Book", "to get that material, but...")),
    (324, 81): ("It must point to a precious metal! Now, if I could just work out how to use it... (muttering)", ("It must point to a precious metal!", "Now, if I could just work out", "how to use it... (muttering)")),
    (159, 63): ("W-what?! Camille! How could you?!", ("Camille! How could you?!",)),
    (163, 106): ("What if you couldn't turn back? What would you have done?", ("What if you couldn't turn back?", "What would you have done?")),
    (167, 68): ("First, square and triangular sails. Here's how they differ.", ("First, square and triangular sails.", "Here's how they differ.")),
    (167, 101): ("Ships with two or more masts make better speed with wind at a slight angle than straight astern. Did you know?", ("Ships with two or more masts", "at a slight angle", "than straight astern.", "Did you know?")),
    (168, 109): ("He's an odd old man, all right. But he seems to know plenty.", ("He's an odd old man, all right.", "But he seems to know plenty.")),
    (169, 119): ("Mikhail, how do we go about collecting the Proofs of Conquest?", ("Mikhail, how do we go about", "collecting the Proofs of Conquest?")),
    (174, 110): ("One more word and you're overboard!", ()),
    (183, 32): ("Not bad. His work's better, though.", ("His work's better, though.",)),
    (188, 22): ("Hm. So these are in fashion.", ("So these are in fashion.",)),
    (141, 40): ("I'm ashamed to admit it. I failed to guide Yifa properly. I'm to blame for her unruly ways.", ("I'm ashamed to admit it.", "I failed to guide Yifa properly.", "I'm to blame for her unruly ways.")),
    (146, 45): ("It's no part of our mission. Please don't trouble yourself.", ("It's no part of our mission.", "Please don't trouble yourself.")),
    (170, 48): ("I hope you meet a celestial maiden and fall in love, too.", ("I hope you meet a celestial maiden", "and fall in love, too.")),
    (184, 27): ("Oh! Where are they going? Wait, they're carrying something!", ("Oh! Where are they going?", "Wait, they're carrying something!")),
    (197, 45): ("Aw, you're so cold. But that's part of your charm... Well, I'd better go. See you.", ("Aw, you're so cold.", "But that's part of your charm...", "Well, I'd better go. See you.")),
    (200, 15): ("Hold back for fear of the blade and you could get hurt even worse. You've got to keep your nerve.", ("Hold back for fear of the blade", "and you could get hurt even worse.", "You've got to keep your nerve.")),
    (200, 18): ("Oh! Ever hear of a training uniform so tough it can chip a sword?", ("a training uniform", "so tough it can chip a sword?")),
    (208, 43): ("They held out for a while. Then the Spanish navy happened by. The pirates scattered. The convoy managed to escape.", ("They held out for a while.", "Then the Spanish navy happened by.", "The pirates scattered.", "The convoy managed to escape.")),
}


def source_wording_matches(groups):
    local = {(g["block"], r["source_record_index"]): r for g in groups for r in g["records"]}
    with_hodram, = [r for r in base.load(parent.REVIEW)["records"] if r["id"] == "DK4_MES_B318_R0079" and r["route"] == 1]
    old_letter, = [r for r in base.load(LETTER)["records"] if r["id"] == "DK4_MES_B238_R0044" and r["route"] == 1]
    for key, earlier in (((334, 81), with_hodram), ((208, 43), old_letter)):
        assert local[key]["source_body_hex"] == earlier["source_hex"][2:]
        assert REVISIONS[key][0] == earlier["english"] and earlier["review"]["formatting"]
    assert local[342, 82]["source_body_hex"] == local[324, 81]["source_body_hex"]
    assert REVISIONS[342, 82] == REVISIONS[324, 81]
    assert local[342, 78]["Japanese"].replace("まで", "までは") == local[324, 77]["Japanese"]
    assert REVISIONS[342, 78] == REVISIONS[324, 77]


def main():
    paired, selected = map(base.load, (SOURCE, ROOT / "selected_wrap_leads.json"))
    assert selected["paired_source_sha256"] == base.digest(SOURCE)
    assert selected["queue_sha256"] == base.digest(QUEUE)
    assert selected["candidate_sha256"] == paired["candidate_sha256"]
    assert len(selected["records"]) == 30
    assert {(r["block"], r["source_record_index"]) for r in selected["records"]} <= REVISIONS.keys()
    source_wording_matches(paired["groups"])
    source = checked_text(getsource(common.main), {"len(resolved) == 8": "len(resolved) == 30"})
    scope = vars(common) | globals()
    exec(compile(source, __file__ + "::contextual-review-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
