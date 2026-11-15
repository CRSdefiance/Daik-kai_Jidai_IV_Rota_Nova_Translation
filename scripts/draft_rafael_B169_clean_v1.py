"""Draft Ian's complete tavern and recruitment scene from the clean Japanese."""
from scripts.seal_clean_independent_drafts_v1 import seal

CONTEXT={169:(
    "Ian works at a tavern where customers make intrusive remarks about his looks. A customer tries to touch him, Ian "
    "reacts, and the tavern keeper dismisses him after the confrontation. The same man returns with others to retaliate, "
    "Rafael intervenes, and the encounter ends with an offer to join the fleet. Keep the harassment and the tavern "
    "keeper's pragmatic response distinct. Descriptions of appearance and the crew's guesses about origin or romance "
    "remain the speakers' words. They establish no identity, origin or relationship."
)}

DATA={169:{
    7:("The tavern keeper asks Ian to carry something over.","Ian, would you take this over?"),
    11:("Ian answers promptly and politely.","Yes, sir."),
    16:("The woman points Ian out and admires his beauty.","That's him. Isn't he beautiful?"),
    20:("The man questions whether Ian is really a man.","Is that really a man?"),
    24:("The woman hushes him because Ian can hear.","Shh. He can hear you."),
    28:("Ian thinks it is happening again and resents being treated as a spectacle.","(Here we go again. Give it a rest. I'm not here to be stared at...)"),
    31:("The keeper asks Ian to take the other drink too.","Ian, this drink too, please."),
    35:("Ian answers after a pause.","...Yes, sir."),
    39:("The woman squeals with delight that Ian brought her drink.","Oh! Ian brought it over himself!"),
    42:("The man asks why she is so happy and grumbles jealously.","What's got you so excited? Tch. This isn't much fun."),
    45:("The keeper calls Ian to take something to another table.","Ian, hey. This goes to the table over there."),
    48:("Ian answers politely again.","Yes, sir."),
    52:("A customer taunts Ian as a young woman and asks him to pour his drink.","Hey, sweetheart. Pour me a drink, would you? Heh."),
    55:("Ian gives no answer.","..."),
    59:("The customer presses Ian with an invasive compliment about his looks.","You really are pretty, aren't you? Hmm?"),
    62:("Ian still does not respond.","..."),
    66:("The customer asks again if Ian is a man and draws attention to his pale skin with a leer.","Are you really a man? Skin that fair isn't something you see every day. Heh heh heh..."),
    70:("Ian sharply orders the customer not to touch him.","Don't touch me!"),
    74:("The customer cries out in pain.","Ow! Ow, that hurts!"),
    78:("The customer curses Ian as he stammers in anger.","Y-you bastard!"),
    82:("Ian privately realizes he has made a mistake.","(Damn it!)"),
    86:("The customer sarcastically calls this splendid treatment of a paying customer.","You... That's some way to treat a customer."),
    90:("Ian offers a strained, formal apology.","...Please forgive me."),
    94:("Rafael calls to the keeper and asks for a drink at his table.","Excuse me, sir. Could we get a drink over here?"),
    99:("The keeper tells Rafael he will be right there, then asks Ian for a word.","Yes, yes. Coming right up. ...Ian, a word?"),
    102:("The keeper suggests the tavern trade does not suit Ian.","Ian, I don't think you're cut out for this work."),
    106:("Ian addresses the keeper familiarly and trails off. The address establishes no kinship.","Sir..."),
    110:("The keeper is tired of trouble and says there are ways to handle customers without using a sword.","I've had enough trouble. There are ways to deal with a customer without drawing a sword."),
    114:("The keeper reluctantly asks Ian to leave the job.","I'm sorry, but I'll have to let you go."),
    118:("Ian quietly accepts his dismissal.","...I understand."),
    122:("Rafael notices that Ian looks out of place and wonders whether there is a reason. The observation is Rafael's.","With skin that fair and a face like that, he looks out of place here. I wonder what brought him here."),
    135:("Julio replies that people take many paths in life.","Life takes all kinds of turns."),
    142:("Claudio thinks Ian is too stiff for tavern work.","More to the point, he's not the tavern type. Too stiff, if you ask me."),
    145:("Rafael suggests trying to speak with Ian.","Should we go talk to him?"),
    151:("Ian thinks about losing his job, having no money and wondering what to do.","(Fired... I'm out of money, too. What am I going to do?)"),
    154:("Ian sees a ship offshore and longs to go back.","(There's a ship out there... I want to go back.)"),
    158:("The same customer taunts Ian as before and comments on meeting again.","Well, well, sweetheart! We keep running into each other today."),
    161:("Ian reacts in sudden alarm.","!"),
    165:("The customer laughs, says Ian is unlucky to be alone and calls to his men.","Heh heh. Bad luck for you, being out here all alone. Boys!"),
    169:("Ian stays silent as the group approaches.","..."),
    173:("The customer says Ian cannot get away and accuses him of humiliating him earlier.","Don't think you can get away. You made a fool of me back there!"),
    176:("Ian doubts he can take all of them and decides to target the apparent leader.","(Too many to take them all... I'll go for the one who looks like the leader.)"),
    181:("The leader berates his men for taking so long against one opponent.","What's taking you idiots so long? He's only one man! Get it together!"),
    184:("Another assailant leers at Ian's good looks and says his fighting is alluring too.","Heh heh. Pretty face, and you can fight. There's something about the way you fight, too."),
    188:("Ian pants and privately realizes he cannot even get close on his own.","Hah, hah... (I can't even get near him on my own!)"),
    191:("The leader thinks Ian is about to lose and tells his men to finish quickly.","Looks like it's about over... Come on, finish him!"),
    194:("The leader is startled by the interruption and asks who it is.","Wh... Who's there?!"),
    198:("Rafael says he could not stand by and asks whether he can help.","I couldn't just stand there watching. You don't mind if I help, do you?"),
    202:("The leader curses, says he only fights battles he can win and threatens that they will remember him.","Damn it... I only fight battles I can win. You won't forget this!"),
    207:("Rafael observes that Ian's face really is beautiful up close.","You really are handsome up close."),
    212:("Ian is silent after Rafael remarks on his looks.","..."),
    216:("Claudio teases Rafael for only just noticing and calls him slow.","You're only noticing now? You're a little slow, huh?"),
    227:("Julio wonders whether Ian's pale skin points to northern European origins.","That fair complexion... Are you from northern Europe, perhaps?"),
    234:("Ian says that looks are of no importance to him.","...Looks... What does it matter?"),
    237:("Claudio tells Ian to take it easy and not be so tense.","Easy now. No need to get so wound up."),
    241:("Ian says he was talking to himself, apologizes and thanks them for saving his life.","No, I was talking to myself. ...My apologies. Thank you. I owe you my life."),
    245:("Rafael is glad he reached him in time, then hesitates before saying he has a favor to ask.","I'm glad we got here in time. Um, actually... I have a favor to ask."),
    250:("Ian says he will help if it is something he can do.","If it's something I can do..."),
    254:("Rafael invites Ian to sail around the world with his group.","Would you like to sail around the world with us?"),
    258:("Ian is surprised by the offer.","What?"),
    262:("Rafael explains that seeing Ian fight showed him how skilled Ian is.","I saw you fight just now. I could tell how good you were."),
    266:("Rafael explains with modest qualification that he is an admiral who leads a fleet.","Believe it or not, I'm an admiral. I lead a fleet."),
    270:("Ian pauses in silence before Rafael worries he has surprised him.","..."),
    274:("Rafael wonders aloud whether his abrupt invitation is strange.","Oh, I guess that was a strange thing to ask out of the blue."),
    279:("Ian assures Rafael the offer is welcome and says he is a navigator who is currently out of work.","No, not at all. I'm grateful for the offer. I'm a navigator, though I'm out of work at the moment..."),
    283:("Claudio jokingly speculates that Ian must have made women cry all over the world.","Oh, yeah? I bet you've broken hearts all over the world."),
    286:("Rafael chides Claudio for being rude.","Clau, don't be rude!"),
    291:("Ian says he does not mind, addresses Rafael as admiral, requests a place aboard and introduces himself by his full name.","...I don't mind. Admiral, I'd be honored to sail aboard your ship. My name is Ian Dukov."),
}}

if __name__=='__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105','B169_clean_drafts_v1.json',DATA,CONTEXT,{},__file__,68)
