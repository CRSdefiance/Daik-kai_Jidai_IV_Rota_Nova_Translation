"""Review both town trends and their route-specific speaker and name-substitution variants."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_havana_calicut_istanbul_trends_20261121 as parent
from scripts import sao_jorge_basra_trends_20261121 as precedent
from scripts import verify_london_guild_assignments_20261118 as macro
from scripts.source_locked_derivation_v5118 import checked_text


base, native = precedent.base, precedent.native
WORK = Path("work/hangzhou_veracruz_trends_20261121")
SOURCE = WORK / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/hangzhou_veracruz_trends_review_20261121_v2.json")
ROOT = Path("out/hangzhou_veracruz_validation_20261121_v2")
ROM, PROOF = ROOT / "Hangzhou_Veracruz_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
NATIVE_ROOT, NATIVE_PROOF = ROOT / "native_display", ROOT / "native_display/native_display.json"
BLOCKS = tuple(tuple(b + d for b in (167, 168)) for d in (39, 31, 27, 0))
CONTEXT = ("The sake trend in Hangzhou and the cheese trend in Veracruz.",) * 4
PLACE = (
    "Two people talk about sake, which leads them to want a drink. Julio overhears them and rushes off to buy "
    "some. Rafael has his own answer, while the other routes give Julio the fabled-drink inference and Admiral address.",
    "Two customers in Veracruz follow a delicious smell to the barkeep's cheese dish. They doubt his boasting, "
    "try it and change their minds. The barkeep gets the last word before they predict a fashion.",
)
SAKE_START = (
    ("One man says he tried an alcoholic drink named sake the other day.",
     "The recent encounter with sake opens the conversation and establishes what they are discussing."),
    ("The other says he tried it too.", "The short answer confirms his own experience."),
    ("The first says it was quite good and asks whether the other agrees.",
     "The casual compliment invites a quick affirmation."),
    ("The other has heard that sake is made with rice.",
     "The reported ingredient is the fact the other man reacts to."),
    ("The first expresses surprise that sake can be made from rice.",
     "His short question or observation follows naturally from the ingredient claim."),
    ("The talk has made the other man want sake and he asks if they should have a drink now.",
     "The desire leads naturally to an immediate invitation."),
    ("The first man welcomes the idea.", "The brief acceptance lets his companion propose they leave."),
    ("His companion calls for them to set out promptly now that they have agreed.",
     "The short sendoff ends the casual conversation before Julio interrupts."),
)
SAKE_RUSH = ("Julio says he cannot stand around and will go buy some of that sake immediately.",
             "The impulsive decision keeps Julio's personal enthusiasm and urgency.")
SAKE_NOTICE_NOTE = ("The notice predicts that sake may catch on in Hangzhou.",
                    "Keep the game commodity and town, and leave the forecast prospective.")
SAKE_END = (
    (
        ("Julio loudly expresses surprise and asks Rafael, by his substituted given name, if he heard.",
         "The Rafael variant keeps the complete outburst and question, with the original name substitution."),
        SAKE_RUSH,
        ("Rafael stammers, calls after Julio by name, pauses and reacts with resignation.",
         "The interrupted call and exasperated ending close the Rafael variant in his own voice."),
        SAKE_NOTICE_NOTE,
    ),
    (
        ("Julio stammers, concludes it must be the fabled drink, and asks the admiral by substituted given name if he heard.",
         "Keep the inference in Julio's voice and retain both the source title and given-name substitution."),
        SAKE_RUSH,
        SAKE_NOTICE_NOTE,
    ),
)
CHEESE = (
    ("A customer notices a good smell and asks whether his companion can smell it.",
     "The opening question gives the other man something to confirm."),
    ("The companion sniffs and agrees.", "The written sniff supplies the comic beat before his quick agreement."),
    ("The first man calls to the barkeep and asks what smells so good.",
     "The familiar address and question identify the next speaker without inventing the source of the smell."),
    ("The barkeep says it is their house specialty, made with plenty of cheese, and that it tastes good.",
     "His pride and enthusiasm invite the skeptical reply."),
    ("The other customer asks if it really tastes that good.", "The short question challenges the barkeep's boast."),
    ("The barkeep says it should go without saying.", "The playful retort keeps his confidence."),
    ("The first customer orders one for the two of them.", "The shared order follows their decision to try it."),
    ("The barkeep agrees and says to wait a moment because he will bring the dish right out.",
     "The prompt assurance sets up their surprise at how quickly he serves them."),
    ("The barkeep brings out the dish with a polite delivery phrase.",
     "The short service line bridges the order and the diners' reaction."),
    ("The first customer says it really was quick.", "The appreciative reaction pays off the barkeep's promise."),
    ("The barkeep asks them to humor him and take a bite first.",
     "A playful challenge moves from praise to tasting."),
    ("The first customer agrees to try it.", "The terse assent gives way to the sound of eating."),
    ("The first customer chews.", "The written chewing sound is one half of a two-speaker comic beat."),
    ("The second customer chews.", "Preserve the matching second sound before they speak again."),
    ("The first customer exclaims that it is delicious.",
     "His enthusiastic outburst reverses the doubt expressed before the tasting."),
    ("The companion reacts with his own surprised praise.",
     "His reply backs up the earlier exclamation and prompts the barkeep's response."),
    ("The barkeep points out that he was right.", "The pleased retort pays off his earlier confidence."),
    ("The first customer says they have to tell everyone about the dish.",
     "The excitement turns into an impulse to spread the word."),
    ("The companion agrees and tells the barkeep the dish will be a big hit.",
     "Keep the prediction in the customer's voice and the familiar address."),
    ("The notice forecasts a possible cheese trend in Veracruz.",
     "Keep the named commodity and city and the tentative outcome."),
)

SAKE_OPEN = ("I tried sake the other day.", ())
SAKE_RICE = ("I hear it's made from rice.", ())
SAKE_INVITE = ("All this talk's made me thirsty. How about a drink now?",
               ("All this talk's made me thirsty.", "How about a drink now?"))
SAKE_LEGEND = ("W-what?! It must be the fabled drink! Admiral FI, did you hear that?!",
               ("the fabled drink!", "Admiral FI", "did you hear that?!"))
SAKE_EXIT = ("I can't just stand here! I'm off to buy some of that sake!",
             ("I can't just stand here!", "I'm off to buy", "some of that sake!"))
CHEESE_SMELL = ("Something smells good, doesn't it?", ())
CHEESE_SNIFF = ("Sniff, sniff... Yeah.", ())
CHEESE_RECIPE = ("That's our specialty. Lots of cheese. It's delicious!",
                 ("That's our specialty.", "Lots of cheese. It's delicious!"))
CHEESE_SERVICE = ("Coming right up. It won't be a minute.", ("It won't be a minute.",))
CHEESE_CHEW = ("Munch, munch.", ())
CHEESE_HIT = ("Yeah! Barkeep, this'll be a hit!", ())
CHANGES = {
    **{(r, 0, 0): SAKE_OPEN for r in (0, 1)},
    **{(r, 0, 3): SAKE_RICE for r in (1, 3)},
    **{(r, 0, 5): SAKE_INVITE for r in (0, 1, 3)},
    (0, 0, 8): (None, ("What?! FI,", "did you hear that?!")),
    **{(r, 0, 8): SAKE_LEGEND for r in (1, 2, 3)},
    (0, 0, 9): ("No time to stand around! I'm off to buy that sake right now!",
                ("No time to stand around!", "that sake right now!")),
    **{(r, 0, 9): SAKE_EXIT for r in (1, 3)},
    **{(r, 0, 10): ("Sake may catch on in Hangzhou.", ()) for r in (1, 3)},
    **{(r, 1, 0): CHEESE_SMELL for r in (1, 3)},
    **{(r, 1, 1): CHEESE_SNIFF for r in (1, 2, 3)},
    (0, 1, 1): ("Sniff, sniff... Sure does.", ()),
    (2, 1, 2): ("Hey, barkeep! What's cooking?", ()),
    **{(r, 1, 3): CHEESE_RECIPE for r in range(4)},
    **{(r, 1, 7): CHEESE_SERVICE for r in (1, 3)},
    **{(r, 1, 10): ("Humor me. Take a bite.", ()) for r in (0, 1)},
    **{(r, 1, i): CHEESE_CHEW for r in (1, 2, 3) for i in (12, 13)},
    **{(r, 1, 14): ("Oh, that's good!", ()) for r in (1, 2, 3)},
    **{(r, 1, 15): ("Wow, this is good!", ()) for r in (1, 3)},
    **{(r, 1, 17): ("We've gotta tell everyone!", ()) for r in (1, 3)},
    **{(r, 1, 18): CHEESE_HIT for r in (0, 1, 3)},
    **{(r, 1, 19): ("Cheese may catch on in Veracruz.", ()) for r in (1, 3)},
}


def review():
    driver = precedent.precedent
    program = checked_text(getsource(driver.main), {
        '        assert len(turns) == len(MEANINGS[scene])':
            '        notes = CHEESE if scene else SAKE_START + SAKE_END[route != 0]\n'
            '        assert len(turns) == len(notes)',
        '        assert signatures == originals.setdefault(scene, signatures)':
            '        group_kind = scene, not scene and route == 0\n'
            '        assert signatures == originals.setdefault(group_kind, signatures)\n'
            '        if not scene:\n'
            '            assert signatures[:8] == originals[(0, True)][:8]\n'
            '            assert signatures[-1] == originals[(0, True)][-1]',
        '"|".join(notes) for notes in MEANINGS[scene]': '"|".join(turn_notes) for turn_notes in notes',
    })
    scope = vars(driver) | globals() | {"ROOT": WORK}
    exec(compile(program, __file__ + "::route-specific-complete-town-review", "exec"), scope)
    scope["main"]()


def stage():
    FunctionType(precedent.stage.__code__, vars(precedent) | globals())()


def verify():
    old = precedent.display.precedent
    build = SimpleNamespace(PROOF=PROOF, ROM=ROM, parent=parent, review=SimpleNamespace(OUTPUT=OUTPUT),
                            current_fe_painter=precedent.compiler.current_fe_painter)
    program = checked_text(getsource(old.main), {
        '    expand = display.progress_expander()': '    expand = display.progress_expander()\n'
                                                    '    expand_macros = macro.expander()\n'
                                                    '    current_names = macro.current_names(ctx)',
        '            if key not in cached:':
            '            if "{MACRO:FI}" in " ".join(plan["lines"]):\n'
            '                result = macro.paragraph(ctx, font, paint, expand_macros, fe_paint, current_names, row, value, plan)\n'
            '                assert len(result["layouts"]) == 4\n'
            '                text = value[1:].replace(b"FI", b"Lil")\n'
            '                lines = [macro.expected(line, {"FI": "Lil"}) for line in plan["lines"]]\n'
            '                lil = macro.raster(ctx, font, paint, text, lines, 1)\n'
            '                for item in [*result["layouts"][1:], dict(scope="Lil", pages=lil)]:\n'
            '                    page, = item["pages"]\n'
            '                    stress.append((f"SC{route} {ident} {item[\'scope\']}", bytes.fromhex(page["native_plane_hex"])))\n'
            '                if route == 0:\n'
            '                    old_body = bytes.fromhex(row["current_hex"])[1:].replace(b"FI", b"ABCDEFGHIJKLMNOP")\n'
            '                    old_pages = paint(ctx.arm, font, old_body)["pages"]\n'
            '                    before = [line for page in old_pages for line in display.visible_lines(page)]\n'
            '                    assert before == ["What?! ABCDEFGHIJKLMNOP, did you hea", "r that?!"]\n'
            '                    raf_text = value[1:].replace(b"FI", b"Rafael")\n'
            '                    raf_lines = [macro.expected(line, {"FI": "Rafael"}) for line in plan["lines"]]\n'
            '                    raf_page, = macro.raster(ctx, font, paint, raf_text, raf_lines, 1)\n'
            '                    result.update(previous_max_width_midword_break=before, Rafael_default_page=raf_page)\n'
            '                    stress.append((f"SC{route} {ident} Rafael", bytes.fromhex(raf_page["native_plane_hex"])))\n'
            '                result.update(target_hex=value.hex(), pages=result["layouts"][0]["pages"],\n'
            '                              initialized_Lil_pages=lil)\n'
            '            elif key not in cached:',
        '            result = cached[key] | dict(id=ident, file_path=path, target_command_offset=offset)':
            '            if "{MACRO:FI}" not in " ".join(plan["lines"]):\n'
            '                result = cached[key]\n'
            '            result = result | dict(id=ident, file_path=path, target_command_offset=offset)',
        '    receipts, previews, cached = [], [], {}': '    receipts, previews, cached, stress = [], [], {}, []',
        'len(lookup) == 68': 'len(lookup) == 125',
        '})(previews)': '})(previews + stress)',
    })
    scope = vars(old) | dict(build=build, ROOT=NATIVE_ROOT, PROOF=NATIVE_PROOF, macro=macro)
    exec(compile(program, __file__ + "::native-towns-and-name-expansion", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    p = ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("review", "stage", "verify"))
    globals()[p.parse_args().action]()
