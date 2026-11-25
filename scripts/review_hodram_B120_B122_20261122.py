"""Review the Yuan story, the sandbar rescue, and the jade discovery."""

from scripts import review_hodram_B111_B114_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B120_B122_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    120: "A monk tests Hodram's purpose and recounts the Yuan invasion. The monk attributes Japan's escape to divine winds and asks Hodram to return with the emperor's keepsake.",
    121: "A crew member spots someone on a sandbar. The crew rescues a boy, and his grandfather insists on giving them a reward the governor once gave him for driving off bandits.",
    122: "A crew member calls the admiral over to see the jade. Carlo explains why the amount left as offerings suggests the building was important.",
}
DECISIONS = {
    120: """
7|||The monk quietly calls out to get Hodram's attention. The brief opening preserves his reserve.
11|||Hodram waits for the monk to say what he wants. The short answer is appropriate for a stranger's call.
15|You're looking for a treasure called the Proof of Conquest, aren't you?|the Proof of Conquest,;aren't you?|The monk already knows what Hodram is seeking and asks for confirmation. The full item name remains in his question.
18|||Hodram asks how the monk could know. The question keeps his unease before the monk explains his interest.
21|I see. You look like a man who commands troops. Am I right?|commands troops.;Am I right?|The monk infers that Hodram leads soldiers from his appearance. His question asserts no specific rank.
25|That's right. I've been given command of our national fleet. Why do you ask?|command of our national fleet.;Why do you ask?|Hodram confirms his specific post without identifying himself with an invented rank. His follow-up keeps him wary.
29|||The monk accepts the answer and decides to share what he knows. The pause makes the change in mood clear.
32|||The monk describes the Yuan invasion and attributes the claim about the empire's size to what is said of it. Preserve the distinction.
36|The Yuan army was undefeated on the mainland. Japan escaped disaster only by the grace of the divine winds.|undefeated on the mainland.;the divine winds.|The monk describes the Yuan army's reputation and credits the divine winds for Japan barely escaping. Keep the religious interpretation in his voice.
39|If his navy had been as strong as his army, the Yuan emperor might have conquered the world.|as strong as his army,;conquered the world.|The monk imagines what the emperor might have done with a navy as formidable as his land forces. Keep the counterfactual in his account.
43|||The established line preserves the claim that the Proof embodies the ambitions of monarchs whose achievements resembled the Yuan emperor's.
46|If you're the one to carry on the Yuan emperor's legacy, his keepsake will come into your hands.|the Yuan emperor's legacy,;come into your hands.|The monk treats possession of the emperor's keepsake as a sign of carrying on his will. The wording keeps the condition and prediction distinct.
50|||Hodram echoes the mention of the emperor's keepsake while considering the claim.
54|||The monk invites him back once he has it. The clear condition ends the exchange.
""",
    121: """
6|||Hodram is ready to leave. The direct suggestion gives the lookout an immediate reason to interrupt.
11|||The separate wordless cue marks that something has caught their attention.
SC1_B121_STYLE_64_0|||The first lookout is mildly surprised and points out a person on the sandbar. Keep the original physical body and its slot ownership.
SC1_B121_STYLE_64_24|||This variant uses a softer moment of surprise before pointing out the same person and location.
SC1_B121_STYLE_64_46|||The speaker's more deliberate out on preserves the location and gives the voice a distinct cadence.
SC1_B121_STYLE_64_70|||This informal voice notices someone. The source gives it no explicit sandbar reference.
38|||Hodram asks what is wrong before learning who is in danger. His manner is polite and brief.
42|||The grandfather is relieved to see travelers and pleads for his grandson. The family relationship is explicit.
45|||The crew echoes grandson before the boy calls out. Keep the original dynamic address and pace.
49|||The boy cries out to his actual grandfather. The kinship term belongs here.
53|||Hodram realizes that the child is drowning. The short exclamation leaves room for the crew's immediate replies.
SC1_B121_STYLE_324_0|||The first volunteer accepts responsibility in a direct but courteous way. Keep its distinct source slot.
SC1_B121_STYLE_324_18|||The short volunteer call matches the clipped source and the urgency of the rescue.
SC1_B121_STYLE_324_28|||This speaker specifically says they will go. Keep the first person rather than a general reassurance.
SC1_B121_STYLE_324_42|||The informal volunteer is confident and direct. The contraction fits the source register.
SC1_B121_STYLE_324_54|||The more deliberate request to be entrusted with the rescue keeps its emphatic turn.
SC1_B121_STYLE_324_76|I'll get him!|I'll get him!|This younger voice directly volunteers to go after the boy. The eager call distinguishes it from the other volunteer who also says they will go.
82|||The boy is frightened and crying after the rescue. Retain the cry before he can explain his fear.
86|||The grandfather first reassures the boy and then expresses relief. The familiar wording fits their relationship.
89|||He thanks the travelers repeatedly after confirming his grandson is safe. The repetition belongs to his emotion.
92|||Hodram redirects the thanks toward the child's safety. The simple answer suits the rescue.
95|I have nothing to give you... Wait, I know! Give me a moment!|nothing to give you...;Wait, I know!;Give me a moment!|The grandfather thinks he has nothing to offer, then remembers something and asks them to wait. The turn of thought remains audible.
99|||The grandfather asks them to take the item. Leave its identity open for Hodram's question.
103|||Hodram asks what the object is. His curiosity leads directly to its history.
107|||The grandfather says he drove off local bandits in his youth and received the gift from the governor. The recipient and reason remain explicit.
110|||He does not know the item's origins and only hears that it is valuable. Keep both qualifications.
114|You earned that for your bravery. I couldn't take something so valuable from you.|earned that for your bravery.;so valuable from you.|Hodram declines because the grandfather earned the reward for his achievement. The line does not claim how personally attached the grandfather is.
118|I can't let the people who saved my grandson leave empty-handed. Please, take it. It does me no good to keep it.|leave empty-handed.;Please, take it.;no good to keep it.|The grandfather insists on repaying the rescue. He reassures Hodram that keeping the item does him no good.
121|Well, then... Thank you. I'll accept it.|Well, then...;I'll accept it.|Hodram accepts with gratitude only after hearing why the grandfather wants him to have it.
126|||The grandfather wishes them safe travels. The short farewell lets the boy speak last.
130|||The boy gives a familiar farewell. Mister suits a child addressing a helpful stranger without adding kinship.
""",
    122: """
SC1_B122_STYLE_16_0|||The first variant directs the admiral to the discovery. The brief request fits the situation.
SC1_B122_STYLE_16_16|||This shorter call keeps the command to look without adding an object in the sentence.
SC1_B122_STYLE_16_30|Admiral! Look!|Admiral! Look!|The youthful call gets the admiral's attention in two quick beats. The gesture in the source carries this deictic reference without requiring awkward English.
27|||Hodram recognizes and admires the jade. The concise appraisal leads into Carlo's explanation.
39|||Carlo says the New World values jade as the East does. The familiar term and comparison remain.
42|All this jade was left as an offering. This building must have meant a great deal to the people here.|jade was left as an offering.;meant a great deal|Carlo reasons from the volume of jade offerings to the building's importance. The inference remains his, with no new claim about its purpose.
""",
}
review = checked_text(previous.review, {
    '"actor-style": "Runtime-selected lookout"': '"actor-style": "Runtime-selected crew member"',
})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::Yuan-sandbar-and-jade", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

