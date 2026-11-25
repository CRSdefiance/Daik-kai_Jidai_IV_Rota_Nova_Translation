"""Review the bullfight, Cristina's recruitment and the London rescue."""

from inspect import getsource
from pathlib import Path

from scripts import register_rafael_east_asia_followup_20261121 as parent
from scripts import review_rafael_east_asia_followup_20261121 as preceding
from scripts import review_rafael_pereira_village_20261121 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_royal_audience_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "spanish_london_review_v3.json"
PRIOR = Path("translations/rafael_B81_B84_contextual_final_review_v1.json")
CATALOGUE = Path("translations/editorial_checkpoints/SharedText_20261110_v1/default_actor_names_current_20261120_v1.json")
BLOCKS = ((81, 82, 83), (), (), ())
CONTEXTS = {
    81: "Cristina holds Julio to his promise to see a bullfight. The crowd laughs at the picador. Rafael surprises Claudio by recruiting the picador, Emilio, through an invitation to sample food around the world.",
    82: "Mivor pursues Cristina over an engagement arranged by their families. Julio and Rafael invite her aboard. Cristina decides for herself, easily defeats Mivor when he challenges her, and asks to see her family's homeland.",
    83: "Cristina visits her hometown and rejects Mivor's pursuit. Both act when a boy falls into the sea. Mivor overcomes his fear of water, Cristina thanks him, and Rafael ends with a private observation about their rapport.",
}
TOKEN, logical, plan_progressive = preceding.TOKEN, preceding.logical, preceding.plan_progressive

# Editable English is a logical paragraph. Empty English keeps the installed wording.
DECISIONS = """
81 5||you promised to take me;remember?|Julio is her grandfather. The reminder of his promise continues their established family banter.
81 8|||Julio's mock forgetfulness leaves Cristina room to call him on it.
81 12|Grandpa! You're always talking about bullfights, and I've never even seen one!|talking about bullfights,;never even seen one!|Cristina chides her grandfather and contrasts his stories with her own experience.
81 16|What do you all think? It'll make a good story, at least. Come on, let's go!|make a good story,;Come on, let's go!|Cristina invites the crew and playfully offers the prospect of a good story.
81 20|||Claudio's clipped curiosity sounds like an easy response to her invitation.
81 23|||Rafael's short assent fits a spontaneous stop.
81 37|||Janus marvels at the size of the crowd in a conversational voice.
81 43|Spain's the greatest power in the world right now, you know. Ho ho!|the greatest power;Ho ho!|Carry Julio's boast as his own opinion and retain the time qualifier and satisfied laugh.
81 47|||Claudio punctures the boast without taking issue with Spain's status.
81 51|You've got an answer for everything. Show some respect for your elders!|an answer for everything.;some respect|Julio answers Claudio's wisecrack and switches to mock indignation.
81 54|I hear the bullfighter today is a crowd favorite.|a crowd favorite.|Rafael passes on what he has heard, setting up his mistaken recognition of the picador.
81 58|||Cristina's lighthearted guess answers the report about the popular performer.
81 70|Bet he's no match for me.|no match for me.|Angelo cuts in with a compact, confident boast.
81 77|||Julio turns everyone's attention to what is happening in the ring.
81 82|||The first spectator laugh sets up the crowd's playful jeer.
81 86|Make us laugh again today!||The spectator expects a repeat of the act. Keep the jeer playful.
81 90|What? That's the bullfighter everyone came to see?|the bullfighter;everyone came to see?|Rafael assumes the person in the ring is the star and asks in surprise.
81 94|||Julio corrects him using the existing matador and picador terms, with the role clear to an unfamiliar player.
81 98|The picador wears the bull down first. Then the matador goes in for the kill.|wears the bull down;goes in for the kill.|He explains the order and specific final act in plain spoken English.
81 102|||Emilio's drawn-out yell is exertion in the ring.
81 106|Ha ha! That fool's playing with the bull! Whoa! What a toss!|playing with the bull!;What a toss!|Use a loud spectator voice. Leave the object of the toss as open as the shouted source.
81 110|||Retain the louder second effort cry as separate from the crowd reaction.
81 114|||The patron laughs again while the picador is still the focus.
81 118|Get out of the ring!||The shopkeeper yells for the performer to leave as the crowd loses patience.
81 126|||A trader announces the headliner's entrance. The phrase fits the crowd's sudden turn.
81 130|||This is an excited shout during the entrance, with no extra evaluation.
81 134|||The anticipated event has arrived. The short cheer works in the crowd sequence.
81 138|||The enthusiastic whoop matches the sound of the spectator's cheer.
81 142|||Keep the shopkeeper's anonymous cheer within the crowd sequence.
81 146|||The trader calls for a good show with a short audible shout.
81 150|||Bravo is the actual borrowed cheer in the Japanese.
81 154|||The repeated cheer is one spectator's separate response.
81 159|(Crowd murmurs)|Crowd murmurs|The original speakerless cue names the sound as an action. Preserve its modal selector.
81 163|What if we asked him to join us?|asked him to join us?|Rafael floats the idea while his intended recruit stays unknown to Claudio.
81 168|Whoa, FI. Where did that come from?|Where did that come from?|Claudio addresses him by the same substituted name and is taken aback by the proposal.
81 171|||Rafael takes the performance as proof of ability. The short tag invites Claudio's agreement.
81 176|Well, sure, but...||Claudio concedes the point and gets cut off.
81 180|||Rafael playfully treats that concession as a decision.
81 185|||Claudio realizes Rafael is acting on the idea and calls after him.
81 189|||Rafael calls out to the recruit as he approaches.
81 194|||Emilio's questioning sound shows he was not expecting the approach.
81 198|Whoa! W-wait! You meant THAT guy?!|You meant THAT guy?!|Keep Claudio's verbal stumble and surprise when he sees Rafael approach the picador.
81 202|||Rafael's existing invitation to sail the open sea is direct. Emilio's next turn supplies the reference to a ship.
81 206|||Emilio's fear and unexpected concern about whether a ship sounds tasty set up the invitation about food.
81 209|...Tasty? Well, no, I guess not. Oh, I know! Let's go taste food from all over the world!|Let's go taste food;all over the world!|Rafael follows the odd objection and makes a shared invitation to taste good things.
81 213|||Emilio echoes the offer and chuckles before he makes up his mind.
81 216|That's right! I bet there are all kinds of things to eat out there!|I bet there are;things to eat out there!|Rafael shares his optimism about variety and leaves it a prediction.
81 220|R-really? All kinds of food? Lots of it? Then I'll go! To sea or anywhere else!|All kinds of food?;To sea or anywhere else!|Emilio latches onto both variety and abundance and agrees to go anywhere.
81 224|Then it's settled! What's your name? I'm FI FA.|What's your name?;FI FA.|Rafael introduces himself with both original name substitutions intact.
81 228|||Emilio's stammer and full approved name are part of his introduction.
81 231|||Rafael answers Emilio's introduction with an idiomatic welcome to the crew.
82 5|You won't leave me alone, will you?!|leave me alone, will you?!|Cristina has plainly had enough. The whole question stays together as her opening retort.
82 8|||Mivor leans into his melodramatic courtship and asks why her response is cold.
82 11|What's wrong with you? Who keeps following someone after she's made it this clear she can't stand him?|What's wrong with you?;she can't stand him?|Cristina questions his behavior and makes the rejection explicit.
82 14|Oh, you needn't be shy!||Mivor mistakes an explicit rejection for bashfulness in his affected register.
82 18|Ugh, I've had it. Our parents arranged the engagement without asking me. I've got no intention of getting married!|I've got no intention;of getting married!|Cristina specifies that the families arranged it without her and that she has no plans to marry.
82 21|Just hearing your voice makes me ever so happy!|hearing your voice;ever so happy!|Mivor turns an angry response into a florid compliment. Keep his eagerness and vocal flourish.
82 24|Idiot!||Cristina's one-word insult is the payoff to him missing her point again.
82 28|||Rafael quietly checks the identity Julio has described.
82 33|||Julio confirms Rafael's inference with a matter-of-fact answer.
82 37|Looks like things are a little complicated...|a little complicated...|Rafael tactfully comments on the quarrel instead of diagnosing the couple.
82 41|||Julio waves off Rafael's hesitation and calls out to his granddaughter.
82 45|Cristina! How've you been?|How've you been?|Julio's warm, everyday greeting follows his louder call for her attention.
82 49|||Cristina's familiar address and question show she was not expecting her grandfather in London.
82 53|||Julio just arrived and tells her that he is back at sea, the news that prompts her objection.
82 56||Mom and Dad;try to stop you!|Cristina warns him about both parents and reacts to it happening again.
82 59||if you don't tell them.|The conspiratorial laugh and simple condition sound like Julio teasing his granddaughter.
82 62|Grandpa, come on...||Cristina starts to protest before Julio turns the conversation around.
82 66|Anyway, what about you? Ever thought about going to sea?|Ever thought about;going to sea?|Julio changes the subject and invites her to consider a voyage.
82 69|||Mivor's horrified objection interrupts and makes Julio finally acknowledge him.
82 72|And who might you be?|who might you be?|Julio turns his attention to the interloper with a brusque but natural question.
82 75|He's the son of a friend of Dad's. Uh, what was his name again?|a friend of Dad's.;what was his name again?|Keep the exact family connection and Cristina's indifference to his name.
82 78|Oh, Cristina! There's no need to be bashful! And you must be her grandfather, sir?|no need to be bashful!;her grandfather, sir?|Mivor takes the forgotten name as shyness and addresses Julio with anxious courtesy.
82 82|||Mivor's emphatic given name and full self-introduction suit his ceremonious attempt to ingratiate himself.
82 85|Right, whatever it was. Next thing I knew, Dad and the others had made a promise on my behalf.|a promise on my behalf.|Cristina brushes his name aside and says her father and others made the arrangement without her.
82 89|||The pause before whatever this is carries Cristina's frustration with the supposed engagement.
82 92|||Julio processes the announcement quietly, which irritates Cristina further.
82 96|Is that all you have to say?!||Cristina wants a reaction and calls out Julio's mild acknowledgment.
82 100|Hmm. To this pale little fellow...|this pale little fellow...|Julio finally sizes up the suitor with the source's dry description.
82 103|I-it isn't because my parents told me to. I really do care about Miss Cristina...|my parents told me to.;Miss Cristina...|Keep Mivor's stammer, his insistence on his own feelings and his deferential address.
82 107|I guess Mom and Dad want me to quit swinging a sword around and settle down. I'm sick of hearing it.|swinging a sword around;settle down.|Cristina paraphrases her parents' expectation and makes her exasperation clear.
82 110|Hmph. Just like Herald. Maybe I raised him wrong...|I raised him wrong...|Julio singles out Herald and ruefully questions his own parenting.
82 113|||Mivor tries to interrupt and scarcely gets a word out.
82 117|You keep quiet! What were you saying about a ship?|What were you saying;about a ship?|Cristina cuts him off and makes Julio's offer the priority.
82 121|Oh, right! I was hoping you'd come along with me.|come along with me.|Julio recovers the thread and makes a personal invitation.
82 125|Your grandfather told me about you. Would you like to come aboard my ship?|Your grandfather;come aboard my ship?|Rafael makes a polite invitation and correctly names how he heard of Cristina.
82 130|||Cristina still needs to know who Rafael and his companions are.
82 133|Well... (One thing after another.) First, this is Admiral FI FA.|One thing after another.);FI FA.|Julio's aside remains private. Keep the original rank and both name substitutions.
82 136|||Cristina remarks on Rafael's youth without inventing an age.
82 140|Didn't you say it's hard to get a match with other schools as a woman? Why not travel the world and hone your swordsmanship?|as a woman?;hone your swordsmanship?|Restore other fencing schools, the barrier she described and Julio's invitation to train abroad.
82 143|I-I object!||Mivor's stammer and vehement protest make room for Cristina's quick answer.
82 147|||Cristina thinks briefly and then chooses the voyage without asking permission.
82 150|||Mivor repeats his objection over Cristina's decision in a suitably officious voice.
82 154|||Rafael politely checks whether it is all right to leave Mivor there.
82 158||No time like the present,;right, Grandpa?|The idiom answers Rafael and invites Julio to agree with her eagerness.
82 161|That's my granddaughter. You have the right idea!|That's my granddaughter.;the right idea!|Julio is proud that she is taking initiative and explicitly confirms their relationship.
82 164|Mivor, would you like to come with us?|come with us?|Rafael offers him a real invitation before Cristina brings up his fear of water.
82 168|||Mivor's unfinished stammer shows he cannot easily answer.
82 172|He can't swim. He's terrified of water. You can't follow us out there, can you?|terrified of water.;can you?|Cristina states both obstacles and pointedly turns to Mivor with the tag.
82 175|Then I've got no choice! A-a duel!|I've got no choice!;A-a duel!|Mivor decides a duel is his last resort and stammers even as he issues the challenge.
82 178|Whoa! W-whoa!||Rafael blurts out alarm at the sudden challenge without narrating a blow.
82 183|||Cristina's retort and strike cry show her impatience has carried into action.
82 187|Aaaah! Ow ow ow!||Keep the startled cry and repeated reaction to pain.
82 191|You couldn't beat a child with that stance.|with that stance.|Cristina judges his swordsmanship bluntly and keeps the specific stance criticism.
82 194|Hmm. You haven't gotten rusty.|haven't gotten rusty.|Julio appraises Cristina's skill approvingly after the brief fight.
82 197|No! My rapier! Father bought it for me!|Father bought it for me!|Mivor cries out about the rapier and remembers who bought it.
82 201|Come on, let's go! Sword matches are fun, and a voyage sounds pretty good, too!|Sword matches are fun,;a voyage sounds pretty good, too!|Cristina looks forward to sailing as well as fencing. Keep the subject and verb of her fencing aside together.
82 205|Say, Admiral, do you have any reason to go to Spain?|to go to Spain?|Cristina tries her idea out as a question about his plans.
82 208|||Rafael echoes the unexpected destination before she gives the reason.
82 213|||Cristina says whose homeland she wants to see and how much a single visit would mean.
82 216|Now, now. Don't go asking for everything.|Don't go asking for everything.|Julio's affectionate chiding follows her spontaneous request.
82 220|||Rafael proposes Seville tentatively. Let Cristina respond before implying the route is certain.
82 224||my kind of admiral!;This'll be fun!|Her delight and quick approval of Rafael follow his offer to visit Seville.
82 228|Same as ever, I see... FI, she's a handful. Look after her for me, would you?|Same as ever, I see...;would you?|Julio privately notes her familiar energy, then makes a personal request of Rafael.
83 5|||Cristina's quiet homecoming uses a natural phrase for the familiar air of London.
83 8|Take your time. Enjoy being back home.|Enjoy being back home.|Rafael encourages her to enjoy the visit without rushing.
83 12|Thanks. I'll walk around the port. I've always loved walking here.|walk around the port.;I've always loved walking here.|Her walk is a familiar pleasure, and she names the port where she will be.
83 16|All right. We'll be at the inn.|We'll be at the inn.|Rafael tells her where the rest of the crew is going without requiring her to meet him immediately.
83 20|||Cristina's two soft observations keep the calm before Mivor arrives.
83 23|Ohhh, a miracle! The power of love! Cristiiina!|The power of love!|Mivor comes in loudly, interprets the encounter as destiny and draws out her name for comic effect.
83 27|||Cristina recognizes him instantly and reacts before he gets close.
83 31||my love would reach you!|Mivor is elated and choking up before Cristina asks him to stop crying.
83 35|||Cristina stammers, notices the crowd and asks him to pull himself together.
83 38|Listen, we only stopped in London. I'm setting sail again soon!|we only stopped in London.;setting sail again soon!|Cristina says why she is there and makes clear she is leaving again.
83 41|||Mivor is momentarily wrong-footed by the news about her trip.
83 45|I said I'm not here for you!||Cristina stresses that her visit has nothing to do with him.
83 48|And I have absolutely no intention of marrying you!|no intention of marrying you!|Restore the emphatic boundary and make her meaning direct.
83 52|Nooo! What don't you like about me?|What don't you like about me?|Mivor draws out his protest and personalizes her decision.
83 55|It's nothing like that. I'm not thinking about marriage yet. Please just let it go, all right?|thinking about marriage yet.;let it go, all right?|Cristina clarifies her position and asks for a definite end to the pursuit.
83 59|I... understand. I'll let it go... Yes... Ah, my romance is over...|my romance is over...|Mivor reluctantly agrees and makes a melodramatic lament.
83 63|Whew. Now he'll leave me alone...|leave me alone...|Cristina exhales and expects the pursuit to stop before the emergency.
83 67|||The sudden alarm changes the scene before Cristina knows what happened.
83 71|||Mivor's wretched sigh turns into a questioning sound at the disturbance.
83 75|Ah! My boy!||Keep the mother's startled yell and the relationship supplied by her own words.
83 79|||Cristina reacts promptly to the mother's alarm.
83 84|||The mother states where her son fell and asks anyone nearby to save him.
83 88|||Cristina answers the mother directly and volunteers to jump in.
83 92|Hang on! I'm coming!||Cristina calls to the boy as her attention shifts from the mother to the rescue.
83 96|||Mivor calls out as Cristina heads into the water.
83 101|||Cristina reassures a frightened child without claiming she's his sister.
83 104|Boy: I'm scared! I'm scared!|I'm scared!|Keep the textual role inside the native speakerless panel and retain both repetitions.
83 107|You're all right now, okay?|all right now, okay?|Cristina tries to steady the boy in a warm voice and keeps the short tag together.
83 111|Let go of my neck! I-I can't breathe!|I-I can't breathe!|Cristina asks him to release his grip and stammers as it hampers her breathing.
83 114|Boy: I'm scared! I'm scared!|I'm scared!|The repeat shows that the reassurance has not calmed him. Keep the exact FE role format.
83 117|We're both going to drown at this rate!|going to drown;at this rate!|Cristina realizes the grip now endangers both of them.
83 120|Boy: Aah! I'm so scared!|I'm so scared!|Use the boy's cry and explicit fear. Leave his role within the speakerless panel.
83 123|N-no... I'm going under...|I'm going under...|Cristina's stammer and fragment show that her strength is giving out.
83 127|||The mother again calls for help, now with both swimmers in trouble.
83 133|Isn't anyone else here?||Mivor looks for another rescuer before facing his fear.
83 137|Cristina... Cristina... But the sea... The water...|But the sea...;The water...|Bring back his repeated cry and the separate way his fear makes him stall.
83 140|The water scares me. It scares me. It scares me... I can't do it, even for Cristina!|It scares me.;It scares me...;even for Cristina!|Retain the repeated thought and keep each repetition intact before his fear wins out.
83 143|||The repeated objection and the yell mark the instant when Mivor starts overcoming the fear.
83 146|The water scares me. It scares me. It scares me... But Cristina matters more!|It scares me.;It scares me...;Cristina matters more!|Match the earlier layout of the fearful repetition and reverse the outcome as he decides to act.
83 149|||Keep the repeated name building from panic to determination.
83 152|||The emphatic separate cry is the peak of the escalation before he dives.
83 156|||His theatrical self-announcement is funny even when he is about to act bravely.
83 160|||The short call promises immediate help and follows his self-announcement.
83 166|Ugh... (Coughs) M-Mivor? Where am I? What happened...?|Where am I?;What happened...?|Cristina comes round coughing and disoriented, and she recognizes Mivor tentatively.
83 170|||Mivor's melodramatic form of address returns when he realizes she's awake.
83 173|...I was drowning. Oh! The boy! Is he all right?|Is he all right?|Cristina remembers going under and immediately asks after the boy.
83 177|Yes, he's safe. His mother says thank you.|His mother says thank you.|Mivor reassures her before saying what the mother asked him to pass on.
83 181|Then someone saved us. I owe them my life. Where are they? I need to thank them.|I owe them my life.;I need to thank them.|Cristina assumes another rescuer came and wants to thank the person who saved her.
83 185|||Mivor hesitates and awkwardly points out that he's right there.
83 188|What?||Cristina fails to understand his first hint.
83 192|||His halting clarification finally states what he did directly.
83 195|||Cristina trails off when she remembers his fear of water.
83 199|I know, but... The moment I thought I had to save you, my mind just...|I had to save you,;my mind just...|Keep his incomplete recollection and the thought that overrides his fear.
83 203|||Mivor suddenly found himself swimming and remains astonished at himself.
83 206|You did that? I can't believe it...|I can't believe it...|Cristina starts to understand who saved her and is still stunned.
83 209|||Cristina remembers she needs to return to the inn and hesitates before leaving.
83 213|Are you all right to walk?|all right to walk?|Mivor checks whether she can manage the immediate trip.
83 217|||Cristina assures him she can get there without assistance.
83 221|Well, I'll be going, then...|I'll be going, then...|Mivor excuses himself quietly after she says she can manage.
83 226|Hey! It's you!||The boy recognizes Cristina. His familiar address needs no sibling label in English.
83 230|||Cristina's first concern on meeting him again is whether he is well.
83 234|Yeah, I'm fine. Thanks! Where's the man who saved me?|the man who saved me?|The boy thanks her and asks after the rescuer in a child's voice.
83 238|Thank you so much. What happened to the man who was with you?|the man who was with you?|The mother thanks Cristina and asks where Mivor has gone.
83 241|||Cristina asks the eyewitness to confirm that Mivor really jumped.
83 245||jumped right in.|The mother's recollection of his unusual shout explains what she saw without changing it.
83 248|He must love you very much.|love you very much.|The mother voices her own conclusion about him in everyday English.
83 251|...He really did it...||Cristina finally takes in the eyewitness account as corroboration.
83 255|Here. Please take this. It's a little something to thank you.|a little something;to thank you.|The mother offers a token of thanks without identifying an unspoken item.
83 260|||Cristina is momentarily at a loss and accepts the thanks softly.
83 264|We'd better go. Thank you again, truly.|Thank you again, truly.|The mother takes her leave and repeats her sincere gratitude.
83 267|||The boy's short goodbye needs no invented family relationship.
83 273|||The small framing phrase closes Cristina's account to Rafael at the inn.
83 277|...He really swam? That's incredible!|He really swam?|Rafael responds to the unlikely feat with impressed disbelief.
83 281|||Cristina is still processing the rescue despite telling the story.
83 285|||Use the everyday idiom when the person being discussed walks in.
83 291|||Cristina recognizes Mivor in a different, tentative voice after the rescue.
83 295|||Mivor replies just as quietly before she thanks him.
83 299|I never thanked you properly. Thank you, Mivor. You were... pretty impressive...|Thank you, Mivor.;pretty impressive...|Keep her gratitude and uncomfortable admission. It matters that the compliment is incomplete in delivery.
83 303|What?! Whaaaat?!||Mivor's repeated surprise swells before his exuberant follow-up.
83 307|Really?! You thought I was impressive? I'm so, so happy!|thought I was impressive?;so, so happy!|Mivor repeats her compliment back and his emphatic delight takes over.
83 311|||Cristina corrects his interpretation immediately, even though the thanks were sincere.
83 315|Doesn't matter! I'm just so happy! Cristiiina!|I'm just so happy!|Mivor waves off the correction and stretches her name as in his opening.
83 319|Oh, enough already! Let's get out of port. He's driving me crazy!|get out of port.;He's driving me crazy!|Cristina hastily wants to sail rather than face another outpouring.
83 323|||Mivor's pledge to wait is his reaction, independent of Cristina's decision.
83 326|They do make a good pair, for all their bickering.|a good pair,;for all their bickering.|Rafael's closing observation is his impression of their banter and rapport.
"""


source = checked_text(getsource(template.main), {
    '    decisions = {}': '''    catalogue = {r["actor_ID"]: r["progressive_nameplate"]
                 for r in base.load(CATALOGUE)["source_and_current_default_name_fields"]}
    decisions = {}''',
    'speaker=old["speaker"],': '''speaker=catalogue[selector] if selector != 254 else "System panel",
                       previous_ledger_speaker=old["speaker"],''',
    'context=CONTEXTS[block] if block in CONTEXTS else village_context(number)': 'context=CONTEXTS[block]',
    '            if changed:\n                assert selector != 254': '            if changed and selector != 254:',
    'assert len(records) == 197 and not earlier and not decisions': 'assert len(records) == 199 and not earlier and not decisions',
})
scope = vars(template) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
