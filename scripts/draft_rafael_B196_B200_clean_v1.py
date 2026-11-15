"""Draft the clean tea, furs, sweets, almonds and glass exchanges."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    196: "Two familiar speakers share tea and talk about their supply at home. She asks him to buy more tomorrow. Preserve their easy rapport without supplying a marriage or an age. The tea notice forecasts local fashion.",
    197: "The same two source roles talk about a cold spell and the wish for a fur coat. The man reports rising fur prices as hearsay already circulating in the scene. The distinct Stockholm notice still forecasts a wider fashion.",
    198: "The woman from the earlier food pitches insists the sample needs to be sweet. The subordinate asks how to make it sweeter and receives no recipe. Keep her affected repetition and his repeated dry replies.",
    199: "One man has a bad cough. The other has noticed more people coughing and repeats a report about a popular remedy using almonds, without recalling its name. The two agree to look for it. Keep the claim as a character's hearsay and leave the cause uncertain.",
    200: "A formal collector admires a piece of glass and orders an attendant to collect the glassware in town. The attendant identifies the object using the period term giyaman and its parenthetical gloss, glass. Preserve their different registers without assigning titles.",
}
DATA = {
    196: {
        6: ("The woman savors the tea and says it's wonderful.", "Ah, that's delicious. It doesn't get any better than this."),
        10: ("The man agrees that tea is wonderful.", "It really is wonderful, isn't it?"),
        14: ("She finds it strange that something so good never caught on before.", "How did something this good go so long without catching on?"),
        18: ("He agrees and says people have poor taste.", "Beats me. People have no taste."),
        22: ("She remembers they are almost out of tea at home and asks him to buy some tomorrow.", "Oh, we're almost out of tea. Would you pick some up tomorrow?"),
        26: ("He readily says he will buy some.", "Of course I will."),
        30: ("She says tea tastes wonderful and settles her mind.", "Tea really is lovely. It puts my mind at ease."),
        33: ("He jokes that they cannot live without tea.", "We'd never survive without our tea, would we?"),
        36: ("The notice forecasts tea becoming fashionable in Sofala.", "Tea looks set to catch on in Sofala."),
    },
    197: {
        6: ("The woman says it is bitterly cold.", "It's freezing. The cold goes right through you."),
        10: ("The man says it has not been this cold for some time.", "Yeah, I can't remember the last time it was this cold."),
        13: ("The woman wants a fur coat and feels she might freeze in this weather.", "I wish I had a fur coat. I'm going to freeze in this cold."),
        16: ("The man reports hearing the cold is selling furs and driving up prices.", "I hear furs are selling so well in this cold that the price is going up."),
        19: ("The woman has heard that too and again feels the cold.", "So I've heard. Oh, it's cold."),
        22: ("The man hopes it warms up soon.", "I just hope it warms up soon."),
        26: ("The woman agrees but still wants furs while the weather is cold.", "So do I. Till it warms up, though, I still want that fur coat."),
        29: ("The notice forecasts furs becoming fashionable in Stockholm.", "Furs look set to catch on in Stockholm."),
    },
    198: {
        5: ("The woman realizes the food is missing sweetness.", "Hmm... Something's missing. I know! It needs to be sweeter!"),
        9: ("The other speaker echoes her, unsure.", "Sweeter?"),
        13: ("She says the light flavor won't satisfy customers and repeatedly stresses sweet.", "Exactly! The customers won't be satisfied with anything this mild. Sweet is what matters. Sweet!"),
        16: ("The subordinate responds doubtfully.", "Well... you think so?"),
        20: ("She says it is certainly true because she says so.", "If I say so, you can be sure of it!"),
        23: ("The subordinate asks how to make it sweeter.", "I see. So how should I make it sweeter?"),
        26: ("She says working that out is his job.", "That's your job to figure out, isn't it?"),
        29: ("The subordinate responds grudgingly.", "...Yeah, yeah."),
        33: ("The woman insists sweet things will certainly catch on.", "Anyway, sweet things are sure to catch on."),
        36: ("The subordinate repeats his grudging reply.", "Yeah, yeah."),
        40: ("She repeats sweet, tells him to do his best and laughs.", "Just remember, sweet! Good luck! Oh-ho-ho-ho!"),
        63: ("The notice forecasts sweets becoming fashionable in Alexandria.", "Sweets look set to catch on in Alexandria."),
    },
    199: {
        6: ("One man reports a bad cough lately and coughs twice.", "I've had a terrible cough lately. Cough, cough."),
        10: ("The other asks if he is all right.", "Are you all right?"),
        14: ("He says he's all right though it is a little hard on him, then coughs.", "Yeah, I'm all right. It's just a little rough. Cough, cough."),
        17: ("The other realizes he has seen plenty of people coughing lately.", "Come to think of it, I've seen a lot of people coughing lately."),
        20: ("The coughing man wonders if a serious illness is going around.", "You think there's some nasty illness going around?"),
        24: ("The other has heard somewhere about a good remedy.", "I heard somewhere there's a good remedy."),
        27: ("The sick man is eager to know what it's called and coughs.", "Really? What's it called? Cough, cough."),
        30: ("The other forgot the name but heard it uses almonds.", "I forget the name, but they say it's made with almonds."),
        33: ("The sick man repeats almonds in surprise.", "Almonds?"),
        37: ("The other had the same reaction, which is why he remembers.", "That surprised me too. That's why I remembered the almonds."),
        41: ("The sick man asks whether it works and coughs again.", "Does it work? Cough, cough."),
        45: ("The other repeats a report that it works remarkably well and sells briskly.", "Supposedly it works like a charm. They say it's selling fast."),
        48: ("The sick man decides to try looking for it.", "In that case, I'll see if I can find some."),
        52: ("The other volunteers to look too.", "I'll look for it too."),
        56: ("The sick man thanks him and coughs.", "Thanks. Cough, cough."),
        60: ("The notice forecasts almonds becoming fashionable in Malacca.", "Almonds look set to catch on in Malacca."),
    },
    200: {
        6: ("The collector declares the object splendid, a genuine work of art.", "Splendid! A work of art, truly."),
        10: ("The attendant deferentially agrees.", "Just as you say."),
        14: ("The collector assumes something that fine must have been made by a renowned artisan.", "A piece this fine must have been made by a craftsman of some renown."),
        18: ("The attendant again assents deferentially.", "Indeed."),
        22: ("The collector had no idea such pieces had come into fashion.", "Hmm. I had no idea such things had come into fashion."),
        26: ("The collector asks what this object is called.", "What do they call this?"),
        30: ("The attendant calls it giyaman and glosses the word as glass.", "It's called giyaman. Glass."),
        34: ("The collector mulls over the unfamiliar name.", "Hmm. Giyaman, you say."),
        38: ("He will add it to his collection and orders all the town's glassware brought in.", "Very well! I'll add it to my collection. Go and bring me all the giyaman in town."),
        41: ("The attendant answers promptly and obediently.", "At once. As you command."),
        45: ("The notice forecasts glass becoming fashionable in Osaka.", "Glass looks set to catch on in Osaka."),
    },
}

if __name__ == '__main__':
    seal('work/analysis/Rafael_B181_B200_clean_20261105', 'B196_B200_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 56)
