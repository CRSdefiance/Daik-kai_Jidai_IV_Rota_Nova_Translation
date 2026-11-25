"""Draft the swans, Three Kingdoms choices and imperial prophecy from clean Japanese."""
from scripts.draft_rafael_B221_B222_clean_v1 import ROOT
from scripts.seal_clean_independent_drafts_offset_v1 import seal_offsets


CONTEXT={
    223:"Cristina watches a pair of swans in the square and speaks to them as fellow travelers. She envies their closeness, notices a long shining object in their possession and reports the direction they seemed to fly. Keep the sighting tentative and let the sound effects punctuate her reactions.",
    224:"An enthusiastic reader asks if the party knows Romance of the Three Kingdoms. He recommends it if they do not and asks for a favorite general if they do. Only his fellow Zhao Yun fan gets the story about the spear. His reactions to Guan Yu and Zhuge Liang keep their respective nicknames, qualities and literary episodes.",
    225:"An older man recognizes the party's object as the sign described in a family tradition. He quotes Kublai Khan's prediction and interprets it as referring to Rafael. Rafael is incredulous and Claudio is skeptical. Keep the emperor's 200-year prediction distinct from the elder's more-than-300-year framing and preserve where he tells Rafael to search.",
}
DATA={
    223:{
        5:("Cristina admires the square, then notices movement in a small pond.","What a lovely square... Oh? There's something in that little pond. Is that...?"),
        9:("A swan calls.","Aah!"),
        13:("Cristina sees a pair of swans, wonders that they come here and asks whether they are traveling too.","Why, it's a pair of swans! So you fly here, too. Say, are you in the middle of a journey?"),
        17:("The swans make alternating honks and soft calls, with pauses.","Aah! Coo... Coo... Aah... ...Aah!"),
        21:("Cristina chuckles, says they are close and envies them.","Hee hee. You two are close, aren't you? I'm a little jealous."),
        24:("There is a rapid beating of wings.","Flap, flap, flap!"),
        28:("Cristina is startled, wonders where the birds are going and spots something they are carrying.","Oh! Where are you going? Wait, they're carrying something!"),
        32:("Cristina recognizes or considers their direction.","That way would be..."),
        36:("Rafael calls to Cristina.","Hey, Cristina!"),
        40:("Cristina addresses Admiral FI and excitedly tells him about the pair of swans.","Oh, Admiral FI! I saw a pair of swans!"),
        43:("Rafael is surprised they were on the pond in the square and assumes they are used to people.","Really? In the pond in the square? They must be used to people."),
        47:("The swans carried something long and shiny and seemed to fly near Amsterdam. Cristina asks whether to go look.","They were carrying something long and shiny. I think they flew off somewhere near Amsterdam. Want to go look?"),
    },
    224:{
        5:("A man asks whether the party knows Romance of the Three Kingdoms.","Hey, do you folks know Romance of the Three Kingdoms?"),
        22:("The man suggests giving it a read because it is fun.","I see. Give it a read sometime. It's a lot of fun."),
        32:("He is delighted they know it and asks who their favorite general is.","Oh, you do? Well, that makes me happy. Who's your favorite general?"),
        51:("He is delighted they share a favorite and thinks they will get along.","Really? He's my favorite too! I think you and I will get along."),
        54:("He praises Zhao Yun's solo ride through Cao Cao's army at Changban Bridge while holding Adou to his chest.","The part at Changban Bridge, where he holds Adou to his chest and rides right through Cao Cao's army all on his own? That's the best!"),
        58:("A rumor places the legendary spear said to have been used by Zhao Yun on a nearby peninsula.","I heard a rumor that Zhao Yun's legendary spear might be on a peninsula around here."),
        62:("He searched hard because he wanted it himself, never found it and thinks the party might succeed.","I wanted it myself, so I looked high and low. Never did find it. I thought you folks might have better luck."),
        72:("He calls Guan Yu the lord with the beautiful beard. Guan Yu is not his own favorite but is a fierce, wise and brave warrior.","You like Guan Yu, the lord with the magnificent beard? He's not my favorite, but what a warrior. Clever and brave."),
        78:("He calls Zhuge Liang a skilled strategist and finds his memorial moving. He ranks him about second.","Ah, the strategist Zhuge Liang. His Memorial on the Expedition brings a tear to your eye, doesn't it? He's probably my second favorite."),
    },
    225:{
        5:("The older man politely calls to Rafael.","Excuse me, sir."),
        9:("Rafael is surprised the man is calling to him.","Huh? You mean me?"),
        14:("He asks if he can see what Rafael has.","May I have a look at that?"),
        17:("Rafael asks which thing he means.","At what?"),
        22:("The man indicates that particular object.","That, right there."),
        26:("The older man is sure it matches the story passed down.","Hmm, yes. There's no mistake. It's just as the story says."),
        29:("Rafael is puzzled and says nothing.","?"),
        34:("More than 300 years before now, a great emperor named Kublai Khan ruled the continent.","More than 300 years ago, the continent was ruled by a great emperor named Kublai Khan."),
        38:("Even that great emperor eventually had to leave this world.","But even that great emperor's time came at last."),
        41:("The dying emperor told a retainer that the master of the ocean would come to this place 200 years later.",
            "He told his retainer, 'Two hundred years from now, the Master of the Ocean will come to this place."),
        45:("The prophecy calls the visitor a sea king with many foreigners in his service. He bears a gold seal from a land the emperor could not rule. The emperor orders the sword given to the brave visitor.",
            "He shall be a king of the sea, with many foreigners in his service. He shall bear the gold seal of a land I could not rule. Give my sword to that brave man.'"),
        48:("The older man's family descends from that retainer and has waited for the king of the sea.","My family descends from that retainer. We have waited for the king of the sea."),
        51:("The older man believes Rafael has at last arrived and directly addresses him as the Master of the Ocean.","And today, at last, you have come. Master of the Ocean, we have been waiting for you."),
        55:("Rafael is incredulous at being named master of the sea.","I'm the master of the sea?"),
        60:("Claudio cannot believe Rafael is the man the emperor predicted 300 years ago.","Him? He's the one an emperor prophesied about 300 years ago? No way!"),
        63:("The older man insists his eyes are reliable and calls Rafael the king of the sea.","No, my eyes have not deceived me. You are the king of the sea."),
        66:("He tells Rafael to search south of the Shandong Peninsula, where he should find the emperor's greatsword.","Search south of the Shandong Peninsula. You should find the emperor's greatsword there."),
        69:("The older man entrusts the greatsword to Rafael and begins to take leave.","I leave the greatsword in your hands. And now, farewell..."),
    },
}
CHOICES={
    (64,0):("Say the player knows the book.","I know it."),
    (64,1):("Say the player does not know the book.","I don't know it."),
    (242,0):("Choose Zhao Yun as the favorite general.","Zhao Yun"),
    (242,1):("Choose Guan Yu as the favorite general.","Guan Yu"),
    (242,2):("Choose Zhuge Liang as the favorite general.","Zhuge Liang"),
}


if __name__=='__main__':
    seal_offsets(ROOT,'B223_B225_clean_drafts_v1.json',DATA,CONTEXT,CHOICES,__file__,44)

