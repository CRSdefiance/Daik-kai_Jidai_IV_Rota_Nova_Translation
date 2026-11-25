"""Draft the clean cheese exchange and the complete six-price seller bargain."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    207: "Two tavern customers follow the smell of the house specialty. The barkeep boasts about the cheese and persuades them to try a serving. Preserve the two separate tasting beats, their excited praise and the distinct Veracruz forecast.",
    208: "A shady seller opens at 200,000. Refusals take him through 100,000, 70,000, 50,000, 40,000 and 30,000. Crew asides advise at particular offers. Success responses differ, the top-price branch can include a Charm notice, and the last refusal ends the conversation. Preserve the separate choices, exact figures and uncertainty about the item.",
}
DATA = {
    207: {
        6: ("The first customer notices a pleasant smell and asks if the other can smell it.", "Hey, do you smell something good?"),
        9: ("The other sniffs and agrees.", "Sniff, sniff... Yeah, I do."),
        13: ("The first asks the barkeep what the smell is.", "Hey, barkeep! What's that smell?"),
        17: ("The barkeep calls it the house specialty and says it has plenty of cheese and tastes wonderful.", "That? It's our house specialty. Plenty of cheese, and it tastes as good as it smells!"),
        20: ("The second customer asks if it really is good.", "Is it really that good?"),
        24: ("The barkeep says the answer is obvious.", "What kind of question is that? Of course it is!"),
        28: ("The first orders one for the pair.", "All right, bring us one."),
        32: ("The barkeep acknowledges it and promises to bring it shortly.", "You got it. Just a moment. I'll bring it right out."),
        35: ("The barkeep presents the food with the usual acknowledgment of the wait.", "Here you go. Thanks for waiting."),
        39: ("The first customer is impressed at how fast it arrived.", "Oh, that really was quick."),
        43: ("The barkeep urges him to humor him and try it first.", "Go on. Just trust me and take a bite."),
        46: ("The customer agrees to try it.", "All right."),
        50: ("The first customer chews.", "Munch, munch."),
        54: ("The second customer chews.", "Munch, munch."),
        58: ("The first bursts out with stretched praise for the taste.", "Oh, that's good!"),
        62: ("The second agrees enthusiastically and is amazed.", "This is good! It's amazing!"),
        65: ("The barkeep says he told them so.", "See? What'd I tell you?"),
        69: ("The first insists they need to tell everyone.", "We've gotta tell everybody about this!"),
        73: ("The other agrees and predicts to the barkeep that the dish will become wildly popular.", "Yeah! Barkeep, this dish is going to be a hit!"),
        77: ("The notice predicts cheese may become fashionable in Veracruz.", "Cheese may catch on in Veracruz."),
    },
    208: {
        5: ("The seller says Rafael looks like he has money and gives a furtive laugh.", "You look like you've got money. Heh heh heh..."),
        8: ("Rafael is silent.", "..."),
        13: ("The seller offers to sell something good for 200,000 and laughs again.", "I've got something good to sell you. How about 200,000 gold? Heh heh heh..."),
        25: ("Fernando suspects the seller may be asking too much.", "Hold on. You're not trying to fleece us, are you?"),
        43: ("The seller praises the buyer's generosity and assures him that the item will come in handy.", "You're a generous one. This'll come in handy, you'll see."),
        46: ("The system announces one point of Charm gained by FI.", "FI's Charm went up by 1!"),
        65: ("The seller yields and offers 100,000 with the same laugh.", "All right. How about 100,000 gold? Heh heh heh..."),
        77: ("Carlo privately tells the admiral a single cut to half the price suggests a hefty markup and that two more reductions are possible.", "(Admiral, he cut the price in half at the first refusal. He was asking far too much. I think we can get him to lower it twice more.)"),
        95: ("The seller laughs, praises the bargaining and says the item will be useful.", "Heh heh heh. You're good at this. It'll come in handy, you'll see."),
        111: ("The seller offers 70,000 and laughs.", "Well then, how about 70,000 gold? Heh heh heh..."),
        122: ("Fernando privately says he would try bargaining one more time.", "(If it were me, I'd try to get him down one more time.)"),
        140: ("The seller hands it over, predicts usefulness and laughs.", "Here you go. It'll come in handy, you'll see. Heh heh heh..."),
        157: ("The seller calls the buyer surprisingly tightfisted and offers 50,000 with a laugh.", "You're stingier than you look. How about 50,000 gold? Heh heh."),
        175: ("Julio privately says he would hold out one more time.", "(I'd hold out one more time if it were me.)"),
        183: ("Yifa privately urges getting him to lower the price further.", "(Let's see if we can get him to go lower!)"),
        202: ("The seller calls him a capable bargainer and hands over the item.", "You're pretty good at this. Here's the item. Go on, take it."),
        218: ("The seller offers 40,000, pauses and gives a short laugh.", "40,000 gold... Heh."),
        229: ("Carlo privately suggests it might now be time to buy.", "(I think this might be the time to buy.)"),
        248: ("The seller says he was beginning to think they would not buy and hands over the item.", "I was starting to think you'd never buy it. Here you go."),
        264: ("The seller pleads for a sale and accepts 30,000.", "Come on, buy it. I'll take 30,000 gold."),
        275: ("Julio privately says the price likely will not fall further.", "(I don't think he'll go any lower.)"),
        294: ("The seller grumbles about selling it cheaply and tells the buyer to take good care of it.", "Tch. I practically gave it away. Well, take good care of it, will you?"),
        310: ("After the last refusal, the seller sneers at their lack of judgment.", "Hmph! You've got no eye for a good thing."),
        314: ("The seller says he will sell to someone else and dismisses them.", "Forget it. I'll sell it to somebody else!"),
    },
}

CHOICES = {}
for offset in (218,582,832,1156,1370,1588):
    CHOICES[(208,0,offset)] = ('Choose to buy at this specific offered price.', 'Buy')
    CHOICES[(208,1,offset)] = ('Decline this specific offer and let the original branch proceed.', "Don't Buy")
if __name__ == '__main__':
    assert len(CHOICES) == 12
    # The original seal helper keys captions by block and index. The six menus
    # repeat the same two source captions, so preserve their full command references
    # and bind the common wording after checking every source object separately.
    from pathlib import Path
    from scripts.audit_story_glyph_consistency import load
    root = Path('work/analysis/Rafael_B201_B220_clean_20261106')
    choices = [r for r in load(root/'clean_choice_objects.json')['records'] if r['block']==208]
    assert {(r['block'],r['source_index'],r['source_command_offset']) for r in choices} == CHOICES.keys()
    assert all(r['source_Japanese']==('買う' if r['source_index']==0 else '買わない') for r in choices)
    wording = {(block,index): draft for (block,index,_),draft in CHOICES.items()}
    seal(root, 'B207_B208_clean_drafts_v1.json', DATA, CONTEXT, wording, __file__, 56)
