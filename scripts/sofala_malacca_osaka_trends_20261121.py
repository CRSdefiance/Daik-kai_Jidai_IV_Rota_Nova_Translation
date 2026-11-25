"""Review the tea, almonds and glass town scenes in each storyline."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_sao_jorge_basra_trends_20261121 as parent
from scripts import sao_jorge_basra_trends_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = precedent.base, precedent.native
WORK = Path("work/sofala_malacca_osaka_trends_20261121")
SOURCE = WORK / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/sofala_malacca_osaka_trends_review_20261121_v4.json")
ROOT = WORK / "research_v2"
ROM, PROOF = ROOT / "Sofala_Malacca_Osaka_Trends_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
NATIVE_ROOT, NATIVE_PROOF = ROOT / "native_display", ROOT / "native_display/native_display.json"
BLOCKS = tuple(tuple(b + d for b in (157, 160, 161)) for d in (39, 31, 27, 0))
CONTEXT = ("The tea fashion in Sofala, almonds in Malacca and glass in Osaka.",) * 4
PLACE = (
    "Two people enjoy tea in Sofala. They wonder why it took so long to become popular, arrange to restock their "
    "tea for tomorrow and end with a shared declaration about how much they like it.",
    "Two people in Malacca compare observations about a cough. One remembers a report about a popular remedy "
    "made with almonds, and they each offer to look for it. Its efficacy remains something they have heard.",
    "In Osaka a collector admires an unfamiliar piece, asks what it is called and orders the other speaker "
    "to collect all the giyaman in town. The exchange uses the Japanese name and its source gloss, glass.",
)
MEANINGS = (
    (
        ("The woman says the tea is delicious and calls it the best.",
         "Her delight opens the exchange and invites the man's agreement."),
        ("The man agrees that tea is wonderful.",
         "The simple agreement names the subject before they discuss the fashion."),
        ("The woman wonders why something so delicious had never caught on before.",
         "Her surprise concerns how long it took, and the complete question leads into the man's joke."),
        ("The man agrees and jokes that people have poor judgment.",
         "The double meaning of taste suits both the tea and his opinion of other people."),
        ("The woman remembers that their household is low on tea and asks him to buy some tomorrow.",
         "Keep the shared supply, tomorrow and the polite request in two natural beats."),
        ("The man agrees to buy some.",
         "A quick affirmative reply answers her request directly."),
        ("The woman says the tea is delicious and puts her at ease.",
         "Keep both the taste and its comforting effect in her own voice."),
        ("The man says the two of them cannot live without tea.",
         "The playful exaggeration rounds off their conversation."),
        ("The notice predicts a possible tea trend in Sofala.",
         "Keep a tentative forecast with the game commodity and town name."),
    ),
    (
        ("The man says his cough has been bad lately and coughs twice.",
         "Keep the recent timing and audible interruption that draws the other man's concern."),
        ("The other man asks whether he is all right.",
         "The brief question fits a casual conversation."),
        ("The man reassures him, admits some discomfort and coughs twice.",
         "The reassurance and qualification precede the cough. Leave the exact symptom of his discomfort open."),
        ("The other man recalls seeing many people coughing lately.",
         "The observation about other people gives the sick man a reason to wonder about an illness."),
        ("The man wonders if a nasty illness is going around.",
         "The casual question conveys worry and speculation."),
        ("The other man has heard of a good remedy.",
         "The reported remedy offers a possibility and invites the question about what it is called."),
        ("The man reacts with surprise, asks the name and coughs again.",
         "Keep the urgent question and written cough as separate beats."),
        ("The other man has forgotten the name but remembers hearing that it contains almonds.",
         "Preserve the uncertain report and the ingredient the next speaker echoes."),
        ("The man repeats almonds in surprise.",
         "The single question gives the other man room to explain what he remembered."),
        ("The other man was surprised that almonds are used in medicine, which is why he remembered.",
         "The surprise comes before the reason he remembers almonds."),
        ("The man asks whether it works and coughs.",
         "The practical question returns the conversation to his immediate worry."),
        ("The other man has heard that it works amazingly well and therefore sells very well.",
         "Keep both claims attributed to hearsay and preserve the strength of the sales report."),
        ("The man decides to try to find some.",
         "The decision follows what he has just heard about it."),
        ("The other man offers to look for it too.",
         "The brief offer is a natural response to the plan."),
        ("The man thanks him and coughs again.",
         "The cough returns after his casual thanks and closes the exchange."),
        ("The notice forecasts a possible almond trend in Malacca.",
         "The forecast is about the ingredient and the town."),
    ),
    (
        ("The collector praises the object as a work of art.",
         "The short exclamations establish his admiration."),
        ("The other speaker deferentially agrees.",
         "The restrained reply gives the collector room to speculate about the maker."),
        ("The collector guesses that a renowned artisan must have made such a fine piece.",
         "Keep the artisan's reputation a supposition grounded in the quality of the object."),
        ("The other speaker politely agrees again.",
         "The brief affirmation maintains the exchange's deferential register."),
        ("The collector pauses and admits that he had no idea such pieces were fashionable.",
         "Keep his surprise at what he had overlooked before he asks the object's name."),
        ("The collector asks what the object is called.",
         "The short question gives the next speaker room to explain the term."),
        ("The other speaker identifies it as giyaman, with glass supplied as the Japanese line's gloss.",
         "Keep both words. The collector repeats giyaman and the system forecast calls the commodity Glass."),
        ("The collector repeats the unfamiliar name thoughtfully.",
         "The pause and repetition let the name sink in before he comes to a decision."),
        ("The collector decides to add the piece to his collection and orders all the giyaman in town brought to him.",
         "Keep both commands and the extravagant scope of the order."),
        ("The other speaker acknowledges the order deferentially.",
         "The formal assent ends the conversation without reporting a completed purchase."),
        ("The notice forecasts a possible Glass trend in Osaka.",
         "The system uses the standard trade good name and keeps the trend prospective."),
    ),
)

TEA_DELIGHT = ("That's delicious. It doesn't get any better.", ("It doesn't get any better.",))
TEA_PRAISE = ("It is. There's nothing like tea.", ())
TEA_DELAY = ("How did something this good go so long without catching on?",
             ("something this good", "go so long without catching on?"))
TEA_REQUEST = ("Oh, we're almost out of tea. Would you pick some up tomorrow?",
               ("we're almost out of tea.", "Would you pick some up tomorrow?"))
TEA_NOTICE = ("Tea may catch on in Sofala.", ())
COUGH_OBSERVATION = ("Come to think of it, I've seen a lot of people coughing lately.",
                     ("Come to think of it,", "a lot of people coughing lately."))
COUGH_QUESTION = ("Something nasty going around?", ())
COUGH_REMEMBER = ("I thought the same thing. Almonds in medicine? That's what stuck with me.",
                  ("I thought the same thing.", "Almonds in medicine?", "That's what stuck with me."))
ALMOND_SALES = ("They say it's selling like crazy because it works so well.",
                ("selling like crazy", "because it works so well."))
ALMOND_SEARCH = ("Then I'll see if I can find some.", ())
ALMOND_NOTICE = ("Almonds may catch on in Malacca.", ())
GLASS_ARTISAN = ("An artisan of some renown must have made a piece this fine.",
                 ("An artisan of some renown", "a piece this fine."))
GLASS_SURPRISE = ("Hm. I had no idea these were in fashion.", ("I had no idea", "were in fashion."))
GLASS_ORDER = ("Good! Into my collection it goes. Bring me all the giyaman in town!",
               ("Into my collection it goes.", "Bring me all the giyaman in town!"))
GLASS_NOTICE = ("Glass may catch on in Osaka.", ())
CHANGES = {
    **{(r, 0, 0): TEA_DELIGHT for r in range(4)},
    **{(r, 0, 1): TEA_PRAISE for r in range(4)},
    (0, 0, 2): (None, TEA_DELAY[1]),
    **{(r, 0, 2): TEA_DELAY for r in (1, 2, 3)},
    (1, 0, 4): TEA_REQUEST, (3, 0, 4): TEA_REQUEST,
    (0, 0, 6): (None, ("It puts my mind at ease.",)),
    (3, 0, 6): ("Tea tastes so good. It's so soothing.", ("It's so soothing.",)),
    (1, 0, 7): ("We can't live without tea.", ()),
    (1, 0, 8): TEA_NOTICE,
    (0, 1, 2): ("Yeah, I'm all right. Just a little rough. Cough, cough.", ("Just a little rough.", "Cough, cough.")),
    (1, 1, 2): ("Yeah, I'm all right. Just a bit rough. Cough, cough...", ("Just a bit rough.", "Cough, cough...")),
    (2, 1, 2): ("Yeah, I'm okay. Just a little rough. Cough, cough!", ("Just a little rough.", "Cough, cough!")),
    (3, 1, 2): (None, ("giving me a hard time,",)),
    (2, 1, 3): COUGH_OBSERVATION, (3, 1, 3): COUGH_OBSERVATION,
    **{(r, 1, 4): COUGH_QUESTION for r in (0, 1, 3)},
    (1, 1, 5): ("I heard there's a good remedy.", ()),
    (3, 1, 7): ("I forget the name, but I hear they make it with almonds.", ("they make it with almonds.",)),
    **{(r, 1, 9): COUGH_REMEMBER for r in (0, 1, 3)},
    (2, 1, 9): (None, ("odd enough to remember.",)),
    (1, 1, 11): ALMOND_SALES, (3, 1, 11): ALMOND_SALES,
    (0, 1, 12): ALMOND_SEARCH, (1, 1, 12): ALMOND_SEARCH,
    (1, 1, 15): ALMOND_NOTICE, (3, 1, 15): ALMOND_NOTICE,
    (0, 2, 2): GLASS_ARTISAN, (3, 2, 2): GLASS_ARTISAN,
    (1, 2, 4): GLASS_SURPRISE, (2, 2, 4): GLASS_SURPRISE,
    **{(r, 2, 8): GLASS_ORDER for r in (0, 1, 3)},
    (1, 2, 10): GLASS_NOTICE, (3, 2, 10): GLASS_NOTICE,
}


def review():
    driver = precedent.precedent
    program = checked_text(getsource(driver.main), {"assert len(groups) == 8": "assert len(groups) == 12"})
    scope = vars(driver) | globals() | {"ROOT": WORK}
    exec(compile(program, __file__ + "::complete-town-review", "exec"), scope)
    scope["main"]()


def stage():
    FunctionType(precedent.stage.__code__, vars(precedent) | globals())()


def verify():
    program = checked_text(getsource(precedent.verify), {'"len(lookup) == 156"': '"len(lookup) == 144"'})
    scope = vars(precedent) | globals()
    exec(compile(program, __file__ + "::all-native-pages", "exec"), scope)
    scope["verify"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "stage", "verify"))
    globals()[parser.parse_args().action]()
