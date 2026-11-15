"""Draft the tobacco, cooking lesson, and sake scenes from the clean source."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    204: "One man admits he has never tried tobacco. Another plays up how common smoking is in town, then offers to show him and tells him to follow. The skeptical reaction and hesitant assent stay separate from the local fashion notice.",
    205: "Three women praise a meal. The third shares her secret, chili peppers, and offers to show her friends how to cook with them. Keep the expense question, personal wish to use them at dinner, immediate offer and explicitly stated friendship.",
    206: "Two men talk about tasting sake and hearing that it is made from rice. They decide to go for a drink. Julio's conditional aside makes his immediate enthusiasm and desire to buy some clear. Rafael protests as Julio takes off. Neither purchase nor recipe is stated.",
}
DATA = {
    204: {
        6: ("The man asks whether the other has ever smoked tobacco.", "Hey, have you ever tried smoking tobacco?"),
        10: ("The other realizes the question might mean he has not yet tried it.", "Wait, you mean you've never smoked?"),
        13: ("The first admits he has not had a chance yet.", "No. Never had the chance, to tell you the truth."),
        16: ("The other is surprised because smoking is fashionable and guesses he may be the only one in town who has not tried it.", "Really? It's all the rage! You're probably the only person in town who hasn't tried it."),
        20: ("The first stammers and says he would like to try it too.", "Y-you think so? I'd like to try it too."),
        23: ("The other affirms it and offers to let him try, telling him to follow.", "I do. All right, I'll let you try it. Come with me."),
        26: ("The first hesitantly assents.", "O-okay."),
        30: ("The notice predicts tobacco may become fashionable in Istanbul.", "Tobacco may catch on in Istanbul."),
    },
    205: {
        6: ("The first woman relishes the meal and says she has never had cooking this good.", "Oh, that was delicious. I've never had such wonderful cooking in my life."),
        10: ("The second agrees and praises the lively flavor.", "Indeed. What a lively flavor!"),
        14: ("The first asks how such delicious food is made.", "How do you make something that delicious?"),
        17: ("The third laughs and reveals her secret ingredient.", "Hee hee. This is the secret."),
        21: ("The first reacts with wordless curiosity.", "?"),
        25: ("The third names chili peppers, says they are a kind of spice and praises how well they suit local ingredients.", "They're called chili peppers. I'm told they're a kind of spice. They go wonderfully with the ingredients we get around here."),
        29: ("The first wonders politely whether they are expensive.", "Oh, aren't they terribly expensive?"),
        33: ("The third reassures her that they are not especially expensive.", "Not really."),
        37: ("The first is relieved and considers using them in tonight's cooking.", "Oh, that's a relief. Perhaps I'll use some in tonight's dinner."),
        40: ("The second wants to cook with them too.", "I'd like to cook with them too."),
        44: ("The third offers to teach them how right away.", "Well then, shall I show you how to cook with them right now?"),
        47: ("The first reacts with delighted surprise.", "Oh, really?!"),
        51: ("The second expresses gratitude for the kindness.", "How kind of you!"),
        55: ("The third says it is only natural since they are friends.", "Of course. We're friends, after all."),
        59: ("The notice predicts chilies may become fashionable in Seoul.", "Chilies may catch on in Seoul."),
    },
    206: {
        6: ("One man says he recently tried a drink called sake.", "I tried a drink called sake the other day."),
        10: ("The second says he did as well.", "So did I."),
        14: ("The first says he liked it and seeks agreement.", "Pretty good, isn't it?"),
        18: ("The second says it is apparently made from rice.", "I hear it's made from rice."),
        22: ("The first is surprised anyone makes it from rice.", "Huh. They can make it out of rice?"),
        26: ("The second says the conversation has made him want a drink and invites the other for one now.", "All this talk's made me want a drink. How about we go have one now?"),
        30: ("The first likes the idea.", "Oh, that sounds good."),
        34: ("The second says they should get going now that they have decided.", "That's settled, then. Let's get going."),
        46: ("Julio reacts with loud surprise and asks FI if he heard.", "What did they say?! Did you hear that, FI?!"),
        49: ("Julio says he cannot stand around and will immediately go to buy some of this drink called sake.", "Well! No time to stand around! I'm going to buy some of this sake right now!"),
        52: ("Rafael stammers for Julio to wait and trails into resigned frustration.", "W-wait, Julio! ...Oh, boy."),
        60: ("The notice predicts sake may become fashionable in Hangzhou.", "Sake may catch on in Hangzhou."),
    },
}


if __name__ == '__main__':
    seal('work/analysis/Rafael_B201_B220_clean_20261106', 'B204_B206_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 35)
