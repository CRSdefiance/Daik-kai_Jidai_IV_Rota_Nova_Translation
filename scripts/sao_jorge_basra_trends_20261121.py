"""Review and validate two complete recurring town scenes on all four routes."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_seville_stockholm_trends_20261121 as parent
from scripts import review_seville_stockholm_trends_20261121 as precedent
from scripts import stage_seville_stockholm_trends_20261121 as compiler
from scripts import verify_seville_stockholm_trends_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native = compiler.base, compiler.native
WORK = Path("work/sao_jorge_basra_trends_20261121")
SOURCE = WORK / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/sao_jorge_basra_trends_review_20261121_v1.json")
ROOT = WORK / "research_v1"
ROM, PROOF = ROOT / "Sao_Jorge_Basra_Trends_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
NATIVE_ROOT, NATIVE_PROOF = ROOT / "native_display", ROOT / "native_display/native_display.json"
BLOCKS = ((191, 195), (183, 187), (179, 183), (152, 156))
CONTEXT = ("The wine fashion in Sao Jorge and the artwork market in Basra.",) * 4
PLACE = (
    "Two drinkers banter about wine in Sao Jorge. A skeptic orders a glass, gulps it down and wants more. "
    "The original enthusiast then orders one too. The forecast names the town and commodity.",
    "Three customers argue about art and make competing purchases in a shop. Once they leave, the shopkeeper "
    "can be frank with another visitor about their arguments and taste. The forecast names the town and commodity.",
)
MEANINGS = (
    (
        ("The first drinker calls out in surprise that the other is still drinking that stuff.",
         "The casual opening and jab set up the second man's offended reply."),
        ("The other drinker challenges him to say what is wrong with it.",
         "A brief, defensive retort fits the challenge and invites the first man's answer."),
        ("The first man says nothing is wrong but insists wine is the drink of the moment.",
         "Keep the repeated 'wine' and the quick shift from reassurance to salesmanship."),
        ("The skeptic repeats the word wine and asks whether it tastes good.",
         "The short second question reveals curiosity beneath his earlier defensiveness."),
        ("The first man declares that it is the best.",
         "The straightforward endorsement lets the skeptic ask how good."),
        ("The skeptic asks whether it is really that good.",
         "The simple follow-up keeps his growing interest audible."),
        ("The enthusiast says that if he has wine, he feels he needs nothing else.",
         "The joke is that wine alone is enough. Keep the casual claim in his voice."),
        ("The skeptic decides to try it and calls for one glass of the wine.",
         "His decision comes before the order. The address suits an ordinary Tavern."),
        ("The bartender acknowledges the request.",
         "A quick acknowledgment gives way to the sound of the wine being drunk."),
        ("The second man gulps the wine three times.",
         "The repeated drinking sound lets the first man ask for his reaction."),
        ("The first man asks how the skeptic likes it.",
         "A brief prompt gives the other man the next turn."),
        ("The skeptic exclaims at the taste and calls to the bartender for another glass.",
         "The eager, informal response reverses his first reaction and keeps the second order."),
        ("The first man calls for a glass for himself as well.",
         "The immediate echo leaves the first speaker joining in the order."),
        ("The system forecasts that wine may become fashionable in Sao Jorge.",
         "Keep the tentative forecast, Wine as the trade good and the installed town spelling."),
    ),
    (
        ("The observer reacts with brief curiosity.",
         "The single sound leads into overhearing the customers."),
        ("The first customer expresses strong admiration.",
         "The enthusiastic opening invites the next customer's skepticism."),
        ("The second customer asks if he really thinks so.",
         "The short question sets up the first customer's confident prediction."),
        ("The first customer predicts the artist will be remembered by future generations.",
         "The prediction remains the customer's opinion and concerns lasting fame."),
        ("The second customer gives a small acknowledgment.",
         "The reserved response leaves room for the buying advice that follows."),
        ("The first customer suggests obtaining one of the artist's works while there is time.",
         "The advice concerns acquiring a piece and follows the claim that the artist will be famous."),
        ("The second customer states his own preference for a different painting.",
         "The blunt preference makes the disagreement explicit."),
        ("The first customer grants that it is good but says it cannot match the first artist's work.",
         "Keep both the concession and his continued conviction."),
        ("The third customer interrupts the two men and insists a different work over there is better.",
         "The interruption and competing preference introduce the third customer without judging the work objectively."),
        ("The first customer says he will buy the original artist's painting regardless of the others' opinions.",
         "His defiance and the transaction decision finish his side of the argument."),
        ("The second customer announces his intention to buy a work by the artist who painted the one he likes.",
         "The pointing reference connects the choice to his favored painter."),
        ("The third customer says he will take the work he has chosen.",
         "The purchase decision completes the alternating sequence of customers."),
        ("The shopkeeper thanks the customers for their business.",
         "Keep a polite farewell to contrast with the shopkeeper's private reaction."),
        ("A loud door slam follows their departure.",
         "The separate sound effect marks the transition to the private conversation."),
        ("Once they leave, the shopkeeper wishes they would stop arguing in the shop every time.",
         "Keep the relief, irritation and repeated visits after his earlier politeness."),
        ("The observer asks the shopkeeper what the noise was about.",
         "A short question bridges the overheard argument and the shopkeeper's explanation."),
        ("The shopkeeper calls it a pastime for wealthy people.",
         "The dry remark puts the argument in its social context."),
        ("The observer repeats the description as a question.",
         "Keep a natural echo that leads directly into an explanation of what they collect."),
        ("The shopkeeper explains that collecting paintings has become fashionable lately.",
         "Paintings are the subject of their conversation. The system uses Artwork for the trade good."),
        ("The observer calls it a refined pastime.",
         "The polished compliment prepares the shopkeeper's dry criticism."),
        ("The shopkeeper says few of the collectors actually have an eye for art.",
         "His private judgment gives the visitor a reason to laugh."),
        ("The observer laughs and comments on the shopkeeper's frankness.",
         "The friendly reaction sets up the request to keep the criticism private."),
        ("The shopkeeper catches himself and asks the observer to keep it secret.",
         "Keep the quick reaction and the request for discretion."),
        ("The observer casually agrees to keep it to himself.",
         "A relaxed acknowledgment closes the private conversation."),
        ("The system forecasts an Artwork trend in Basra.",
         "The notice names the market commodity and town and keeps the forecast tentative."),
    ),
)

WINE_OPEN = ("Hey, you still drinking that stuff?", ())
WINE_CRAZE = ("Nothing wrong with it. But wine's the thing now. Wine!", ("But wine's the thing now. Wine!",))
WINE_PITCH = ("With wine, who needs anything else?", ())
WINE_ORDER = ("Guess I'll try it. Barkeep, a glass of that wine!", ("a glass of that wine!",))
WINE_REACTION = ("Now that's good! Barkeep, another!", ())
WINE_NOTICE = ("Wine may catch on in Sao Jorge.", ())
ART_FAME = ("I do. His name will live on for generations.", ("His name will live on", "for generations."))
ART_ADVICE = ("You should get one of his pieces while you can.", ("one of his pieces", "while you can."))
ART_INTERRUPTION = ("What are you two talking about? The one over there is best.",
                    ("What are you two talking about?", "The one over there is best."))
ART_PAINTER = ("I'll take one by this painter!", ())
ART_ORDER = ("I'll take this one!", ())
ART_IRRITATION = ("Finally, they're gone. I wish they'd quit arguing in my shop every time.",
                  ("I wish they'd quit arguing", "in my shop every time."))
ART_FRANKNESS = ("Ha! You don't mince words, do you?", ())
ART_NOTICE = ("Artwork may catch on in Basra.", ())
CHANGES = {
    (1, 0, 0): WINE_OPEN, (3, 0, 0): WINE_OPEN,
    **{(i, 0, 2): WINE_CRAZE for i in range(4)},
    **{(i, 0, 6): WINE_PITCH for i in (0, 2, 3)},
    **{(i, 0, 7): WINE_ORDER for i in (0, 2, 3)},
    (1, 0, 8): ("Coming right up.", ()),
    **{(i, 0, 11): WINE_REACTION for i in range(4)},
    (1, 0, 13): WINE_NOTICE, (3, 0, 13): WINE_NOTICE,
    (0, 1, 3): ART_FAME, (2, 1, 3): ART_FAME,
    **{(i, 1, 5): ART_ADVICE for i in range(4)},
    (1, 1, 8): ART_INTERRUPTION, (3, 1, 8): ART_INTERRUPTION,
    **{(i, 1, 9): (None, ("I'm buying his painting!",)) for i in (0, 2, 3)},
    (2, 1, 10): ART_PAINTER, (3, 1, 10): ("And I'll take one by this painter!", ()),
    (1, 1, 11): ART_ORDER, (3, 1, 11): ART_ORDER,
    **{(i, 1, 14): ART_IRRITATION for i in (0, 1, 3)},
    (3, 1, 17): ("A rich man's pastime?", ()),
    (3, 1, 18): (None, ("all the rage these days.",)),
    (1, 1, 20): (None, ("a true eye for art.",)),
    (2, 1, 20): (None, ("really have an eye for it.",)),
    (3, 1, 20): (None, ("a true eye for art.",)),
    **{(i, 1, 21): ART_FRANKNESS for i in (1, 2, 3)},
    (1, 1, 23): ("Of course.", ()), (3, 1, 23): ("Of course.", ()),
    **{(i, 1, 24): ART_NOTICE for i in (1, 2, 3)},
}


def review():
    scope = vars(precedent) | globals() | {"ROOT": WORK}
    FunctionType(precedent.main.__code__, scope)()


def stage():
    old = compiler.precedent
    workflow = old.workflow
    review_config = SimpleNamespace(OUTPUT=OUTPUT, SOURCE=SOURCE, BLOCKS=BLOCKS)
    scope = workflow.env | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, parent=parent,
                                review=review_config, paired=review_config)
    scope["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__,
                                                 scope | {"stage": workflow.stage})
    scope["rebuild_function"] = old.aligned.rebuild_function
    scope["stage"] = SimpleNamespace(system=SimpleNamespace(native_painter=compiler.current_fe_painter))
    FunctionType(workflow.env["main"].__code__, scope)()


def verify():
    old = display.precedent
    build = SimpleNamespace(PROOF=PROOF, ROM=ROM, parent=parent, review=SimpleNamespace(OUTPUT=OUTPUT),
                            current_fe_painter=compiler.current_fe_painter)
    program = checked_text(getsource(old.main), {"len(lookup) == 68": "len(lookup) == 156"})
    scope = vars(old) | dict(build=build, ROOT=NATIVE_ROOT, PROOF=NATIVE_PROOF)
    exec(compile(program, __file__ + "::native-pages", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "stage", "verify"))
    globals()[parser.parse_args().action]()
