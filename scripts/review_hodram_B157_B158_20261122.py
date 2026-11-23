"""Review Al and Angelo's recruitment and the advice that follows."""

from scripts import review_hodram_B156_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B157_B158_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    157: "Al is fired for refusing errands. Hodram sees an opportunity, challenges his attitude, and makes him decide whether to join the Swedish patrol fleet.",
    158: "Angelo asks for work and provokes Gerhard into a duel. Hodram sees his potential and makes him an offer. Angelo then explains trade beyond the Mediterranean, and Julio confirms the limits of European market share.",
}
DECISIONS = {
    157: """
5|||The employer tells Al he can leave and angrily fires him. The coarse register fits the shouting the crew overhears.
11|||Al takes the dismissal in stride and tells the man to do as he likes. The pause keeps his defiance controlled.
14|What was that? Were they fighting?|Were they fighting?|Charles wonders whether there was a quarrel. The two quick questions carry his surprise.
17|||Hodram hears the firing and guesses the man was a bodyguard. Preserve the question before he knows.
20|||Hodram asks directly who the man was. The short question opens the exchange with his employer.
24|||The employer says fighting is Al's only talent and unwillingness to follow orders got him fired. Keep both judgments in his voice.
27|||Hodram wants to know if Al is good at fighting. The brevity shows what interested him.
31|||The employer grants that Al is an exceptional fighter but resents having to ask him to carry bags. Keep both the grudging praise and the complaint.
34|He might be the perfect bodyguard, but I wonder how he'd get along with a crew. Too proud, maybe. Or just bad at working with others.|the perfect bodyguard,;get along with a crew.;working with others.|Charles questions Al's character, with pride and poor cooperation as possibilities. His opinion sets up Hodram's jab about his own teamwork.
37|You're one to talk about teamwork, Charles. Come on.|talk about teamwork,;Charles. Come on.|Hodram points out that Charles is hardly in a position to criticize. The familiar aside keeps the humor before they go.
41|||Charles checks that the admiral is serious. His surprise follows Hodram's decision to pursue Al.
45|I won't be satisfied till I've spoken to him myself.|spoken to him myself.|Hodram wants to hear from Al directly. He gives no guarantee that he will hire him.
50|There he is. Look at the build on him. Hard to miss, isn't he?|Hard to miss, isn't he?|Charles recognizes Al and comments on his physique. The tag stays with the remark it qualifies.
53|||Hodram considers Al without answering Charles. Preserve the silent beat as they approach.
57|||Al bluntly asks what they want. The short question is already in his voice.
61|Looks like you keep yourself in good shape.|in good shape.|Hodram comments on Al's evident training. The observation carries no assumption about a rank or job.
64|You can see that for yourself. What's it to you?|What's it to you?|Al dismisses the obvious comment and says his training is none of Hodram's business. The response is brusque.
67|Don't you get it? I came over because I think you've got potential. That attitude's doing you no favors.|you've got potential.;doing you no favors.|Hodram says he approached Al because he sees promise, then warns him that his response is hurting his chances.
70|||Al reacts with an incredulous exclamation before Hodram explains what he heard. Keep the direct challenge.
74|I heard you lost your job as a bodyguard. You've got more strength than you know what to do with.|job as a bodyguard.;know what to do with.|Hodram repeats the specific job loss and suggests Al has energy and talent to spare. This sets up Al's question about being hired.
77|You offering me a job? Who are you, anyway?|offering me a job?;Who are you, anyway?|Al understands the approach as a job offer and turns the question of identity back on Hodram.
80|||Hodram introduces himself through FI and names his own role as a Swedish Navy admiral commanding a patrol fleet. Both military details are source-stated.
83|||Al repeats the title in surprise and says he has no intention of becoming a sailor. Keep the contrast between the two thoughts.
86|Is that all the judgment you've got? You think I'm a worse bet than the man who just fired you?|judgment you've got?;the man who just fired you?|Hodram calls Al's judgment into question by comparing himself with the man who fired Al. The provocation belongs to Hodram.
90|||Al protests that they have only just met and asks why there is such a hurry. The answer shows why Hodram sounds demanding.
94|A man doesn't do himself any favors by dithering.|by dithering.|Hodram appeals to decisiveness in the gendered terms he uses in the Japanese. The pointed remark presses Al to decide.
98|||Al reacts with a frustrated sound before getting a clear offer. The existing short response suits him.
102|||Hodram offers to help and asks for a decision on the spot. His last line makes the choice Al's.
106|All right. I'll sail with you. I'm Al. Good to meet you.|I'll sail with you.;Good to meet you.|Al accepts and names himself in a brief, civil introduction. Keep the given name and the polite closing after his earlier brusqueness.
""",
    158: """
5|Hey, old man! Old man! Yeah, you!|Yeah, you!|Angelo calls directly to Hodram and repeats the deliberately rude form of address. Its repetition sets the tone for Gerhard's reaction.
8|||Hodram's questioning sound shows he has heard Angelo but has yet to answer. The quiet reaction contrasts with Angelo's call.
12|Yeah, you. I heard about you down at the port. You're the admiral, right?|down at the port.;You're the admiral, right?|Angelo repeats that he means Hodram and checks the rank he heard about. The title stays in his question.
16|||Angelo asks for a job aboard Hodram's ship and repeats old man. His confidence makes the request sound more like a demand.
19|||Gerhard takes offense and suggests ignoring Angelo. Keep the formal register of his complaint.
22|Hold on. I'm FI FA, captain of this ship.|captain of this ship.|Hodram holds the crew back and introduces himself with the original given-name and surname substitutions. Captain is the role he states.
26|||Hodram asks what Angelo can do and says he has no use for dead weight. The response is blunt enough to invite Angelo's boast.
31|Mamma mia! Isn't it obvious? I'm strong and I'm gorgeous!|Isn't it obvious?;I'm strong and I'm gorgeous!|Angelo's Italian exclamation begins a boast about strength and looks. The new wording retains both without making him speak formally.
35|||Gerhard dismisses the boasting and wants to go. The established reply lets Angelo answer him directly.
39|||Angelo rudely tells Gerhard to be quiet and says he is talking to Hodram. The gloomy old man insult is his characterization.
42|I've heard enough! Let's see how strong you really are. Draw!|I've heard enough!;really are.|Gerhard loses patience and challenges Angelo to prove his strength. The final command starts the duel.
46|||Angelo is pleased to accept the challenge. His quick invitation to come on sets the pace of the contest.
49|||Hodram orders both of them to stop. Keep the short command separate from Gerhard's answer.
53|||Gerhard asks Hodram to leave it to him and says he cannot ignore the insults. His loyalty and anger explain why he continues.
58|||Angelo boasts mid-duel, pleased that Gerhard has seen his strength. The short repeated challenge remains casual.
61|||Gerhard reacts under pressure before Hodram judges the fight. Retain the brief strain.
65|||Hodram notices that Angelo's boasts are backed by enough skill to corner Gerhard. Preserve his surprise.
68|I've got you now! You're finished!|I've got you now!;You're finished!|Angelo believes he is about to end the duel. The forceful English keeps his overconfidence before Gerhard's reversal.
72|Too easy!|Too easy!|Gerhard sees through Angelo's attack. The quick taunt turns Angelo's apparent advantage around.
77|||Angelo cries out when the duel turns against him. Preserve the separate reaction.
81|||Hodram expected Gerhard to prevail but is still intrigued by Angelo. The pause sets up his offer.
86|No way... That's the first time I've ever lost.|the first time I've ever lost.|Angelo is shocked to have lost for the first time. His defensive confidence gives way to disbelief.
89|It's a big world. Plenty of men are as good as you. Shall we go, Admiral?|Plenty of men;Shall we go, Admiral?|Gerhard puts Angelo's skill in perspective and then turns back to Hodram. His controlled formality contrasts with Angelo's shock.
93|||Hodram asks if Angelo wants to sail with him. The short invitation abruptly changes the conversation.
97|||Gerhard stammers in surprise at the offer. The sharp response is a separate turn.
101|He's certainly rude, but he's got a gift with a sword. He's still green, and look how hard he pushed you.|a gift with a sword.;look how hard he pushed you.|Hodram acknowledges the rudeness and inexperience while pointing to Angelo's skill. The last phrase makes the duel the evidence.
104|||Gerhard concedes the point after a pause. His agreement follows Hodram's account of the fight.
108|Travel makes people grow. I think he'll change, too. What do you say?|I think he'll change, too.;What do you say?|Hodram expects the voyage to help Angelo mature and asks for Gerhard's view. The opinion stays qualified.
112|||Gerhard defers to Hodram after hearing his reasoning. Preserve the original FI address and hesitant assent.
115|Y-you really mean it? After the way I talked to you?|really mean it?;the way I talked to you?|Angelo checks that the offer is sincere despite his own rudeness. His stammer conveys a new uncertainty after the duel.
119|Then make up for it with good work.|make up for it|Hodram asks him to repay the offense by working. The plain response accepts him without a lecture.
123|||Angelo agrees, thanks them, and gives his complete approved name. The laugh and concise thanks suit him.
142|By the way, Admiral. If you want to make money trading, quit scratching around in the Mediterranean.|make money trading,;in the Mediterranean.|Angelo pivots to trade advice and tells Hodram to think beyond small Mediterranean deals. Keep the same region and his directness.
146|||Hodram asks why. The brief question lets Angelo explain his reasoning.
158|||Julio is impressed that Angelo knows about trade. His approval interrupts the exchange as its own reaction.
164|||Angelo says the established routes look attractive, but larger powers have developed the region already, leaving little profit. Retain the reasoning and its limits.
168|||Hodram pauses over Angelo's explanation before he gets to the opportunity elsewhere.
172|||Angelo sees untapped potential in Africa and the New World. Keep his claim that a small investment can yield a large return.
175|||Angelo explains how the unusual goods can bring profit on round trips to Europe. His forecast retains the qualification.
178|You know your trade, too. I wouldn't have guessed.|know your trade, too.;I wouldn't have guessed.|Hodram is surprised that Angelo knows as much about commerce as fighting. The last thought is his reassessment.
181|Aw, I just picked it up from sailors.|picked it up from sailors.|Angelo deflects the compliment and credits the sailors he heard. The offhand reply contrasts with his earlier boast.
192|||Julio supports Angelo's advice. The brief emphatic turn allows him to explain the capacity issue himself.
195|||Julio explains that more cargo space cannot make up for difficult access to market share in Europe. The volume limit remains explicit.
201|Thanks for the tip. Let's see what's out on the open sea.|Thanks for the tip.;the open sea.|Hodram thanks Angelo for advice received right away and decides they should try sailing farther out.
""",
}
review = checked_text(previous.review, {"len(records) == 86": "len(records) == 73"})
scope = previous.scope | globals()
exec(compile(review,__file__+"::recruiting-Al-and-Angelo","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

