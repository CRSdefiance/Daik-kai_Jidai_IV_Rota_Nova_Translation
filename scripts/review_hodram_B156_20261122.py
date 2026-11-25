"""Review the royal audience, Sera's farewell, and Gerhard's reunion."""

from scripts import review_hodram_B151_B155_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base,ROOT,paired = previous.base,previous.ROOT,previous.paired
OUTPUT = ROOT/"B156_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    156: "The king offers Hodram high command and any reward. Hodram asks to retire so the navy can develop without him. He says farewell to Sera and leaves her restoration in her people's hands. Gerhard surprises him by preparing a ship and refusing to let him sail alone."
}
DECISIONS = {
    156: """
6|His Majesty is waiting for you, Mr. FA.|His Majesty;Mr. FA.|The attendant respectfully summons Hodram using the original surname substitution. His Majesty refers to the waiting king.
11|||The king praises Hodram and credits his success with ensuring the country's prosperity. Keep the respectful use of the controlled surname and the king's own confidence.
14|I appoint you supreme naval commander. I expect our navy to grow even stronger under your command.|supreme naval commander.;grow even stronger|The king appoints Hodram to the highest naval command and says he expects its strength and achievements to grow. The role is explicitly granted here.
18|||Gerhard privately reacts with delight. Keep the brief parentheses separate from the king's words.
22|(There's no better man for the job!)|(There's no better man for the job!)|Charles voices private approval because he thinks the admiral is an ideal fit. The parentheses keep his reaction from sounding like an address to the king.
26|||Hodram repeats the title in an unfinished thought. The short reflection comes before he explains his real wish.
30|||The king says Hodram can name whatever reward he wants. Keep the open offer and the ceremonial question.
33|||Hodram pauses before asking permission to speak. Retain that separate beat.
37|May I tell you what I wish for, Your Majesty?|what I wish for,;Your Majesty?|Hodram asks formally whether he may state his wish. His deference fits the king's position and the unusual nature of the request.
40|||The king grants permission immediately. The brief imperative preserves his openness.
44|Then, if I may...|if I may...|Hodram begins with a deferential hesitation before thanking the king. He has yet to reveal the request.
48|||Hodram recognizes the appointment as a great honor. The interruption is genuine preparation for declining it.
51|||The king picks up the hesitation. His short response leaves Hodram space to continue.
55|||Manuel's silent question shows he also notices something unexpected. Keep the separate speaker.
59|If Your Majesty can forgive me for asking... I'd like to retire from the navy.|forgive me for asking...;retire from the navy.|Hodram asks to retire and treats the request as a personal indulgence. His reserve makes the unexpected choice clear.
63|||The king reacts in immediate shock. The brief exclamation prepares the crew's separate private reactions.
67|||Charles's stretched private outburst preserves his more expressive shock.
71|||Gerhard's private stammer responds specifically to Hodram's words. Keep the second voice distinct from Charles.
75|||The king asks what Hodram means. The urgent question follows his initial exclamation.
79|I've been thinking about it for some time.|for some time.|Hodram explains that this is a long-considered decision. The calm delivery contrasts with the astonishment around him.
83|||The king pauses rather than interrupting again. Preserve the turn as silence.
87|||Hodram credits his good fortune in his crew and says their help made it possible to build a navy of exceptional strength. The formal gratitude fits his explanation.
90|||He credits the king's kindness for trusting him despite his shortcomings and thanks him. The unfinished thought leads to his reasons for retiring.
93|||Hodram doubts he can maintain the navy's strength and bring future recruits into enduring military discipline. Keep the detailed distinction between building the navy and sustaining it.
96|||The king says Hodram's mere presence at the head of the navy frightens other countries and inspires his own men. The English keeps both effects as the king's argument.
99|||Hodram asks pardon for contradicting the king and says those effects are exactly what concern him. Keep the deference and reversal.
102|||The king responds with another short questioning sound. It gives Hodram room to explain his concern.
106|||Hodram fears that caution abroad would isolate the country and pride at home would cause a grave mistake. Keep both consequences and the conditional reasoning.
109|||Hodram argues his absence would make other countries less wary and his own officers and men more alert. Preserve the opposite effects he expects.
113|||The king thinks over Hodram's argument. The short pause precedes the final request.
117|||Hodram says he wants nothing else and asks the king to indulge his request. The formal petition fits the surrounding argument.
120|||The king takes a silent beat before granting the request.
124|||The king reluctantly accepts because it is Hodram's sincere wish. His regret belongs in his own speech and the pause precedes the decision.
128|||Hodram thanks him with the appropriate formality. The short response closes the official exchange.
132|||Manuel has his own silent reaction to the decision. Keep its native speaker and its place between the other responses.
136|||Charles thinks of his admiral and says no more. The parenthesis and trailing pause leave his feeling open.
140|||Gerhard has a separate silent beat after the others. Preserve his source-owned reaction.
154|||Sera addresses Hodram through FI and asks him to come to her country. The compact question suits her first appeal.
157|I don't think I'm made to live anywhere but at sea.|made to live anywhere|Hodram says he is the sort of person who can only live at sea. He speaks personally after the public formality of the audience.
161|||Hodram knows this sounds cold but says Sera and her people must rebuild the country themselves. Keep the distinction between visiting and restoring it for them.
165|||Sera hesitates before asking him more personally to come. Retain the exact FI and the emotional staging of her appeal.
168|||Hodram addresses Sera and denies being the legendary king. The placement distinguishes his reply from her adjacent speech.
172|||Sera says his status does not matter to her and falters before she can finish. Preserve the mounting repetition.
176|||The silent row on Hodram's side holds the beat after Sera falters. Preserve the original placement and deliberate pause.
180|||Hodram names Sera's rank as princess and himself as a retired officer. Both are stated here. Their different positions are his explanation for holding back.
184|||Sera's silent response lets his words land. Preserve the original staged pause.
188|Don't look so sad. It's not as if we'll never see each other again.|Don't look so sad.;each other again.|Hodram comforts Sera and says this is not a permanent goodbye. Keep his reassurance distinct from her following question.
193|||Sera's embedded caption is her name and the dialogue asks if they will meet again. Her question answers his reassurance without adding a new promise.
197|||Hodram confirms that they will. The embedded FI caption stays separate from the spoken reply.
201|||Sera is silent again under her own embedded caption. Retain the deliberate pause and name distinction.
206|||Hodram repeats that he means it and explains he is free to choose now. The embedded FI still identifies the speaker before his words.
210|||Hodram promises occasional visits to see the country's recovery. Keep the reason and the original FI caption.
213|||Sera answers softly under her name. The pause keeps the emotional restraint of the moment.
217|||Hodram asks Sirwood to look after Sera. The familiar request leaves her in trusted company without assigning a new formal role.
220|||Sirwood's imperfect phrasing still communicates that Hodram can leave it to him. Keep the hesitation and limited speech.
224|Sera taught you, did she? I look forward to seeing you again.|Sera taught you, did she?;seeing you again.|Hodram infers Sera taught Sirwood and says he looks forward to their next meeting. The short question conveys his pleasant surprise.
228|||Sera briefly calls Hodram by the original FI. Preserve the hesitation and exclamation.
232|||The separate silent row on the other side gives Hodram a pause between Sera's calls. Keep the staging.
236|||Sera urges him to come back. The broken phrasing suits her restrained insistence.
240|||Hodram promises to come. The short answer remains on his own side of the exchange.
244|||Sera leaves another deliberate silence after the promise. Preserve its layout.
248|||Hodram calls Sera in a quiet turn. Keep its original placement before his farewell advice.
252|It won't be easy. Take care of yourself.|Take care of yourself.|Hodram acknowledges the difficulties and wishes Sera well after calling her by name in the preceding beat.
256|(She nods.)|(She nods.)|Sera agrees in a gesture. The short stage direction keeps the gesture and shifts no speaker control.
260|See you again... Goodbye.|See you again...;Goodbye.|Hodram promises they will meet again, then says goodbye. The pause stays between the two thoughts.
271|Now then... Where should I go?|Where should I go?|Hodram wonders where to sail after the farewell. The new beat makes Gerhard's interruption a surprise.
275|||Gerhard announces they are ready to sail before Hodram expects to see him. The enthusiastic address belongs to the reunion.
280|||Hodram recognizes Gerhard in immediate surprise. Keep the short call.
284|||Gerhard asks for orders as if they were still serving together. The brief line sets up Hodram's objection.
288|||Hodram repeats his name and demands to know what he is doing. His raised voice shows the surprise has not passed.
292|||Gerhard lists the practical work he has done, including obtaining a ship and supplies. The matter-of-fact answer avoids the real question for comic effect.
295|||Hodram says he already arranged positions of responsibility for all his officers. His insistence is the setup for Gerhard naming the other appointments.
299|||Gerhard says Charles directs the Royal Academy institute and is delighted with its equipment. The established phrasing keeps Gerhard's fond account of him.
302|I wasn't asking about Charles...|wasn't asking about Charles...|Hodram tries to return to Gerhard's own appointment. The trailing objection lets Gerhard continue his evasion.
306|||Gerhard says Manuel chairs the maritime technology committee and is uncharacteristically solemn over the new ship plans. Preserve the contrast as Gerhard's observation.
310|No, I meant you! I left you in charge as supreme naval commander!|I meant you!;supreme naval commander!|Hodram makes his concern explicit and names the considerable duty he assigned to Gerhard.
314|It's not a job that suits me, Admiral. Leave me out of it.|a job that suits me,;Leave me out of it.|Gerhard asks to be excused because he does not consider the post a fit. His polite resistance comes after the comic deflection.
317|||Hodram says he chose Gerhard for ability, experience and standing among the crew. The pointed opening reflects his impatience.
320|||Gerhard says it is unfair to leave him with that burden while Hodram retires in comfort. The question lightly turns the accusation back on Hodram.
324|||Hodram briefly falters in response. Keep the comic pause before Gerhard gives his serious reason.
328|||Gerhard says defense should be the responsibility of the country's own people and calls himself an outsider. Preserve his view without naming an origin not stated here.
332|||Gerhard sees no reason to stay once Hodram leaves and promises to go anywhere with him. His loyalty has the directness the scene has been building to.
336|||Hodram pauses before answering that offer. The unspoken reaction gives his later joke a gentler effect.
340|I guess there won't be much romance on this voyage.|much romance on this voyage.|Hodram jokes that the trip is unlikely to be romantic. His understatement follows Gerhard's more serious pledge.
344|||Gerhard laughs and declares every woman they meet will take an interest in two handsome men. The exaggerated confidence answers Hodram's joke.
347|||Hodram calls him a hopeless optimist in the final aside. The original speakerless timing closes the scene.
""",
}
review = checked_text(previous.review,{"len(records) == 42":"len(records) == 86"})
scope = previous.scope | globals()
exec(compile(review,__file__+"::retirement-and-farewell","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

