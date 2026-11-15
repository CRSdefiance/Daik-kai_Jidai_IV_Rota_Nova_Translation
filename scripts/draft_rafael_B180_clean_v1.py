"""Draft the complete clean sailing lesson before opening current English."""
from scripts.seal_clean_independent_drafts_v1 import seal

CONTEXT={180:'An idle sailing instructor asks an admiral to hear his lesson. Conditional companions politely or formally decline, while the accepting path explains square and lateen sails, supplementary sails and how following winds affect multiple masts. Keep the instructor colloquial and friendly; distinguish fore-and-aft rigging from crosswise rigging, and retain the size and attachment restrictions. Nautical and in-game label spellings are provisional pending current term binding.'}
DATA={180:{
    5:('The instructor asks the admiral whether they want to hear his sailing-ship lesson.','Hey, Admiral! Want to hear a lesson on sailing ships?'),
    8:('Rafael is caught off guard.','Huh?'),
    13:('The instructor has been very idle lately and asks them to indulge him as a favor.','I’ve been bored out of my skull lately. Think of it as doing me a favor.'),
    31:('A companion politely objects to being underestimated.','Please don’t underestimate us.'),
    34:('Another companion agrees with the objection.','Mm-hmm. Quite right.'),
    46:('A companion replies in a formal register that they are past needing instruction about ships.','When it comes to ships, we hardly need lessons at this point.'),
    52:('The instructor accepts the refusal, agrees they look experienced, and decides to wait for somebody greener.','Fair enough. You look like you know your ships. I’ll wait for somebody who looks a little greener.'),
    63:('On acceptance, the instructor praises the attitude and predicts the listener will go far.','That’s the spirit. You’ll go far.'),
    66:('The instructor introduces sails as the essential part of a sailing ship.','It’s a sailing ship, after all. The sails are what keep it going.'),
    69:('He will start with the difference between square and triangular sails.','All right. Let’s start with the difference between square sails and lateen sails.'),
    72:('A square sail is a transverse sail rigged across the direction of the ship.','A square sail is rigged across the ship, from side to side. That’s what we mean by a transverse sail.'),
    76:('A square sail cannot be turned fore-and-aft. It works well with a following wind but cannot be set at the best angle in a headwind.','You can’t turn a square sail to lie along the ship. It does well with a following wind, but you can’t set it at the best angle in a headwind.'),
    79:('Those who know their sails call the triangular sail a lateen. It is rigged along the ship and cannot be turned crosswise.','The sailors who know their stuff call a triangular sail a lateen. Unlike a square sail, it’s rigged along the ship, and you can’t turn it crosswise.'),
    82:('A lateen can be angled well into a headwind but does not give as much speed with a following wind. He checks that the listeners are following.','You can get just the right angle in a headwind, but you won’t go as fast with the wind behind you. With me so far?'),
    85:('The next topic is additional sails that can be fitted.','Next up are the extra sails you can add.'),
    89:('The upper sail is properly called a topsail, a small transverse sail fitted high on each mast.','The proper name for an upper sail is a topsail. It’s a small sail you rig crosswise high on each mast.'),
    93:('A staysail is a small fore-and-aft sail ahead of a mast. It cannot be fitted in front of a lateen because the two sails overlap.','A staysail is a small fore-and-aft sail that goes in front of a mast. You can’t fit one in front of a lateen. They’d overlap.'),
    96:('Sailors call the bow sail a spritsail. It is rigged crosswise at the bow and cannot be fitted on small ships.','A sailor calls the bow sail a spritsail. It’s rigged crosswise at the bow, and you can’t fit one on a small ship.'),
    99:('The stern sail is also called a jigger spanker. It is fore-and-aft and effectively adds a small mast, so it fits only large ships.','The stern sail is also called a jigger spanker. It’s rigged fore-and-aft, but fitting it is like adding a little mast. You can only put one on a large ship.'),
    102:('On ships with two or more masts, wind at a slight angle from behind gives more speed than wind straight astern.','Did you know a ship with two or more masts goes faster with the wind a little off its stern than it does with the wind straight behind it?'),
    106:('He asks one of the listeners whether they know why.','How about you? Know why that is?'),
    110:('A listener reasons that the masts are lined up front to back.','Hmm... Because the masts are lined up fore and aft, I take it.'),
    113:('With wind straight behind, only the rear mast gets the wind, so the masts ahead are of no use.','Right. With the wind straight astern, only the rearmost mast gets any wind. The forward masts don’t help you at all.'),
    116:('The ship is fastest with the wind coming at an angle from behind, provided the sails are set to match.','That’s why you’re fastest with the wind coming at an angle from behind. Of course, you still have to set your sails to match.'),
    120:('The listener understands.','That makes sense!'),
    132:('The listener had not paid much attention to this before and is impressed to learn the reason.','Oh! I hadn’t really paid attention to that before. Now I see why!'),
    139:('The instructor thanks them for hearing him out and is about to return to work.','Thanks for hearing me out. Well, back to work.'),
}}
CHOICES={(180,0):('Politely ask to hear the lesson.','I’d like to hear it.'),(180,1):('Politely decline the offer.','I’ll pass, thanks.')}
DATA={b:{i:(m,e.replace('’',"'")) for i,(m,e) in d.items()} for b,d in DATA.items()}
CHOICES={k:(m,e.replace('’',"'")) for k,(m,e) in CHOICES.items()}

if __name__=='__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105','B180_sailing_lesson_clean_drafts_v1.json',DATA,CONTEXT,CHOICES,__file__,29)
