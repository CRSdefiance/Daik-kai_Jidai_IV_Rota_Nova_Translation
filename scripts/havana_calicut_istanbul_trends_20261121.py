"""Review the medicine, dye and tobacco trends across the four storylines."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_sofala_malacca_osaka_trends_20261121 as parent
from scripts import sao_jorge_basra_trends_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = precedent.base, precedent.native
WORK = Path("work/havana_calicut_istanbul_trends_20261121")
SOURCE = WORK / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/havana_calicut_istanbul_trends_review_20261121_v1.json")
ROOT = Path("out/havana_calicut_istanbul_validation_20261121_v1")
ROM, PROOF = ROOT / "Havana_Calicut_Istanbul_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
NATIVE_ROOT, NATIVE_PROOF = ROOT / "native_display", ROOT / "native_display/native_display.json"
BLOCKS = tuple(tuple(b + d for b in (163, 164, 165)) for d in (39, 31, 27, 0))
CONTEXT = ("Medicine in Havana, dyes in Calicut and tobacco in Istanbul.",) * 4
PLACE = (
    "Two people in Havana talk about a report that medicine from a shop cured the owner of a house. "
    "One doubts the story before he and the other speaker decide to buy some.",
    "A Calicut shopkeeper and his companion discuss buying dye before other shops take the supply. "
    "One doubts the urgency while the other predicts a profit and talks him into delegating the purchase.",
    "Two people discuss tobacco in Istanbul. One expresses surprise that the other has never tried it and "
    "offers to let him try. Preserve the social pressure and the other man's hesitancy.",
)
MEANINGS = (
    (
        ("The first speaker asks if the other has heard the news.", "His casual question opens the gossip."),
        ("The other asks what he means.", "A short response invites him to name the subject."),
        ("The first speaker identifies the owner of the house as the subject.",
         "Keep the owner and house as the referent for the illness."),
        ("The second guesses he means the illness whose cause nobody could explain.",
         "The direct question recognizes the earlier story."),
        ("The first confirms that is the story.", "His quick agreement leaves room for the other's retort."),
        ("The second says everyone knows about that.", "The reply dismisses the old news before he hears the update."),
        ("The first asks if he knows what happened afterward.", "This question shifts the exchange to the new rumor."),
        ("The other echoes the reference to what happened afterward.",
         "The brief echo gives the first speaker a chance to tell him."),
        ("The first says he heard that medicine sold in stores cured the illness in one go.",
         "Preserve the sale in shops, sudden recovery and the speaker's source as hearsay."),
        ("The second incredulously asks whether a store-bought remedy cured an illness with no known cause.",
         "He repeats both parts of the claim before directly questioning whether it is true."),
        ("The first confirms the report and asks if it is remarkable.",
         "Keep his conversational enthusiasm and the questioning tag."),
        ("The second concedes that it is remarkable and then asks if it is true.",
         "The pause preserves the turn from agreement to doubt."),
        ("The first says it seems true and the medicine has a reputation for working on every illness.",
         "Keep the qualification about the story and attribute the universal claim to what people say."),
        ("The second is impressed and wants some if it works that well.",
         "His eagerness follows the supposed reputation and leads to the suggestion they buy it."),
        ("The first suggests going to buy some.", "Keep it as a casual invitation before the other's agreement."),
        ("The other agrees and says they should go.", "His brisk response ends the exchange."),
        ("The system forecasts that medicine may become popular in Havana.",
         "Use the game commodity and keep the forecast tentative."),
    ),
    (
        ("The shopkeeper concludes that only that dye can produce this color.",
         "The claim motivates the other speaker's immediate push to buy it."),
        ("The other agrees and says rival shops will buy up the dye unless they buy it soon.",
         "Keep the source's urgency and the competing shops' purchase."),
        ("The shopkeeper hesitates.", "The unfinished objection invites the impatient interruption."),
        ("His companion reproaches the delay because it will be too late when the dye sells out.",
         "The admonition and consequence keep the tension between the speakers."),
        ("The shopkeeper doubts the dye will sell out if they wait a little.",
         "Keep the response as skepticism about the need to rush."),
        ("His companion contradicts him, saying strong demand will make the dye sell out quickly.",
         "The blunt correction and confident prediction answer his hesitation."),
        ("The shopkeeper asks uncertainly if the other is right.", "The hesitant question will recur after the profit claim."),
        ("The companion insists he is right.", "The quick affirmative gives way to the shopkeeper's concession."),
        ("The shopkeeper agrees to leave the purchase to his companion.",
         "The concession authorizes the purchase without claiming it has happened."),
        ("The companion asks the shopkeeper not to sulk and claims that securing the color will ensure a profit.",
         "The teasing familiar address and exuberant prediction belong to the speaker."),
        ("The shopkeeper repeats his doubtful question.", "Retain the echo as a comic response to the sales pitch."),
        ("The companion insists again.", "The emphatic answer closes the exchange on his conviction."),
        ("The system forecasts that dyes may become popular in Calicut.",
         "Use the trade category Dyes and keep the forecast tentative."),
    ),
    (
        ("One man asks the other if he has ever smoked tobacco.", "The informal question starts the conversation."),
        ("The other asks in surprise whether he really has never tried it.",
         "His incredulity anticipates the comment about how fashionable it is."),
        ("The first admits he has never had the opportunity.",
         "The plain reply gives his reason without adding a judgment about smoking."),
        ("The other says tobacco is so popular that he is probably the only person in town who has not tried it.",
         "Keep the claim in the speaker's voice and keep its uncertainty."),
        ("The first stammers a question and admits he would like to try it.",
         "The hesitation and tentative interest develop in the same reply."),
        ("The other confirms his assessment, offers to let him try it and asks him to follow.",
         "Keep the brisk invitation and instruction together."),
        ("The first agrees with a stammer.", "The short assent preserves his hesitancy at the end."),
        ("The system forecasts a possible tobacco trend in Istanbul.",
         "Keep the named town and commodity and the notice's tentative wording."),
    ),
)

NEWS = ("Did you hear what happened next?", ())
SHOP_CURE = ("They say medicine from a shop cleared it up just like that.",
             ("medicine from a shop", "cleared it up just like that."))
DOUBT = ("Medicine from a shop cured an illness nobody could explain?",
         ("Medicine from a shop", "an illness nobody could explain?"))
RUMOR = ("Seems so. And people say it cures every illness.", ("And people say", "cures every illness."))
DYE_WAIT = ("There's no rush. I doubt it'll sell out that fast.", ("I doubt it'll sell out", "that fast."))
DYE_URGENCY = ("Why wait? Once it's sold out, it's too late.", ("Once it's sold out, it's too late.",))
DYE_PROFIT = ("Come on, don't sulk. If we can get that color, we'll make a profit for sure.",
              ("If we can get that color,", "we'll make a profit for sure."))
TOBACCO_CURIOUS = ("Y-you think so? I'd like to try it, too.", ("I'd like to try it, too.",))
TOBACCO_OFFER = ("Yeah. I'll let you try some. Come with me.", ("I'll let you try some.", "Come with me."))
CHANGES = {
    (0, 0, 3): ("You mean his mysterious illness?", ()),
    **{(r, 0, 6): NEWS for r in (0, 1, 3)},
    **{(r, 0, 7): ("What happened next?", ()) for r in (0, 1, 3)},
    **{(r, 0, 8): SHOP_CURE for r in (0, 1)},
    **{(r, 0, 9): DOUBT for r in (0, 1, 3)},
    **{(r, 0, 12): RUMOR for r in (0, 1, 3)},
    (0, 0, 13): (None, ("I want some too.",)),
    (3, 0, 13): (None, ("I want some too.",)),
    (2, 0, 14): ("Want to go buy some?", ()), (3, 0, 14): ("Want to go buy some?", ()),
    **{(r, 0, 16): ("Medicine may catch on in Havana.", ()) for r in (1, 3)},
    **{(r, 1, 0): ("Only that dye can make this color.", ()) for r in (0, 1, 3)},
    **{(r, 1, 1): ("Exactly. If we don't buy some now, the other shops will buy it all up.",
                    ("If we don't buy some now,", "the other shops will buy it all up.")) for r in (1, 3)},
    (1, 1, 3): DYE_URGENCY, (3, 1, 3): DYE_URGENCY,
    (2, 1, 3): ("What are you waiting for? Once it's gone, it's too late.", ("Once it's gone, it's too late.",)),
    **{(r, 1, 4): DYE_WAIT for r in (0, 1, 3)},
    (3, 1, 5): ("It will! It's so popular, it'll be gone in no time.", ("it'll be gone in no time.",)),
    **{(r, 1, 8): ("All right. I'll leave it to you.", ()) for r in (1, 3)},
    **{(r, 1, 9): DYE_PROFIT for r in (0, 1, 3)},
    **{(r, 1, 11): ("I'm telling you!", ()) for r in (1, 3)},
    **{(r, 1, 12): ("Dyes may catch on in Calicut.", ()) for r in (1, 3)},
    (3, 2, 1): ("Wait, you haven't tried it yet?", ()),
    **{(r, 2, 3): ("Really? It's all the rage! You might be the only one in town who hasn't tried it.",
                    ("It's all the rage!", "the only one in town", "who hasn't tried it.")) for r in (1, 3)},
    **{(r, 2, 4): TOBACCO_CURIOUS for r in (0, 1, 3)},
    **{(r, 2, 5): TOBACCO_OFFER for r in range(4)},
    **{(r, 2, 7): ("Tobacco may catch on in Istanbul.", ()) for r in (1, 3)},
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
    program = checked_text(getsource(precedent.verify), {'"len(lookup) == 156"': '"len(lookup) == 152"'})
    scope = vars(precedent) | globals()
    exec(compile(program, __file__ + "::all-native-pages", "exec"), scope)
    scope["verify"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "stage", "verify"))
    globals()[parser.parse_args().action]()
