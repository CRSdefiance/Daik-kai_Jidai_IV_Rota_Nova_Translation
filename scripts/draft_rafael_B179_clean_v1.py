"""Independent clean-source drafts for Manuel's invitation and flagship refit lesson."""
from scripts.seal_clean_independent_drafts_v1 import seal

CONTEXT={179:"Manuel stops to admire and appraise the party's ship. His affectionate language treats ships as living things, a personal philosophy that attracts Janus's interest. Rafael and Janus invite him aboard; he accepts, then offers or defers a lesson about refitting the flagship. Keep his measured, courteous and expressive voice. Preserve the separate morale, provision, medical, recovery and repair effects. Room and stat names are provisional until checked against the current UI."}
DATA={179:{
    5:("Manuel notices that the ship is well cared for.","Hmm. This ship has been very well cared for..."),
    8:("There is still room to do better; he starts to give an example.","Still, there is room for improvement. For example..."),
    11:("Rafael is puzzled and asks if something is wrong with the ship.","Is something the matter with this ship?"),
    16:("Janus asks if the man has business with their ship.","Is there something you wanted with our ship?"),
    20:("Manuel asks if they own it and praises it as a fine ship full of life.","Ah, you own her? What a fine ship. She's full of life."),
    24:("Privately Janus finds that a curious way of putting it.","(Well, that's an interesting way to put it...)"),
    27:("Manuel advises against neglecting upkeep. A ship is alive, and it rewards the care given to it.","Don't neglect her upkeep. A ship is a living thing. Give her proper care, and she'll repay you for it."),
    30:("Rafael is silent.","…"),
    35:("Manuel worries that he overstepped with his personal view, asks pardon if it offended, and excuses himself.","Oh, dear. Have I overstepped? That's just my own way of looking at things. Forgive me if I offended you. I'll be on my way."),
    38:("Janus calls after him and asks him to wait.","W-wait a moment, please."),
    42:("Manuel asks if something is the matter.","Is something the matter?"),
    46:("Janus is curious because the man seems so fond of ships.","Well... You seem very fond of ships. It made me curious."),
    50:("Ships bring back old memories. He introduces himself as Manuel and reveals he used to be a navigator.","Seeing a ship takes me back... My name is Manuel. Believe it or not, I used to be a navigator."),
    54:("Rafael takes in the revelation.","Is that so..."),
    59:("Janus privately points out that such devotion to ships is rare and considers having him aboard.","FI... You hardly ever meet someone who loves ships this much. If we could get him to come aboard..."),
    62:("Rafael agrees; he would feel secure with this man caring for the ship.","You're right. I'd feel better with someone like him taking care of our ship. I'm all for it."),
    67:("Janus asks Manuel to join and go to sea with them.","Well, then... Manuel, would you join us? We'd like you to sail with us."),
    71:("Manuel contemplates returning to sea and is deeply moved by their passion for it.","Back to sea again... Oh, I can feel your passion for the sea stirring something in me."),
    75:("Rafael excitedly asks if Manuel will accept.","Does that mean you'll come with us?"),
    80:("Manuel remembers the thrill of a ship's heartbeat shaking his soul, then apologizes for getting excited after a long time ashore.","The thrill of a ship's heartbeat, right down to your soul... Oh, pardon me. It's been a long time since I sailed. I got a little carried away."),
    84:("He thanks them for the offer and accepts.","Thank you for the wonderful offer. I'd be happy to join you."),
    87:("He offers the admiral advice on refitting the flagship's assigned rooms.","Well, Admiral, shall I offer a little advice on refitting the rooms on your flagship?"),
    102:("On acceptance, he will explain rooms that are especially useful for long voyages.","Very well. I'll go over the rooms that help you prepare for a long voyage."),
    106:("A persuasive person in the first mate's room or chapel helps resolve sailors' grievances.","Assign someone persuasive to the first mate's cabin or the chapel. They can help settle the sailors' complaints."),
    110:("People assigned to the galley and animal room reduce the fleet's consumption of water and food.","Put people in charge of the galley and the livestock room. They'll help the fleet use less water and food."),
    114:("A physician in the examination room treats fatigue, epidemics and injuries among companions and sailors.","With a doctor in the sickbay, your officers and sailors can get treatment for fatigue, disease and injuries."),
    118:("A sick or injured navigator recovers faster in a private room or recreation room.","A sick or injured navigator will recover faster if you assign them to a private cabin or the recreation room."),
    122:("A shipwright like Manuel repairs damaged ships from the timber room at sea and helps with refits and repairs in the shipyard.","A shipwright like me can repair damaged ships from the timber room while you're at sea. At the shipyard, I can help with refits and repairs too."),
    125:("He acknowledges the explanation was quick and asks whether it helped.","That was a quick run-through. I hope it helped?"),
    128:("The fleet's fate depends on the admiral's judgment; refits must be planned carefully and not neglected.","The fleet's fate is in your hands, Admiral. Don't neglect your refits. Plan them carefully."),
    134:("After a refusal he respectfully leaves decisions to the admiral.","I see. Then I'll leave it in your hands."),
}}
CHOICES={(179,0):("Accept the offer of refitting advice.","Please do."),(179,1):("Politely decline the refitting advice.","No, thank you.")}

if __name__=='__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105','B179_Manuel_refit_lesson_clean_drafts_v1.json',DATA,CONTEXT,CHOICES,__file__,33)
