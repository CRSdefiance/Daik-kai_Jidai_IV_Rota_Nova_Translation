"""Revisit Fernando's three related exchanges and Rafael's farewell wrap."""
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_rafael_fernando_coin_game_20261121 as parent
from scripts.review_hodram_alexandria_tutorial_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/analysis/fernando_parallel_routes_20261121")
PAIRED = ROOT / "paired_source.json"
SOURCE = ROOT / "paired_source_with_rafael.json"
OUTPUT = ROOT / "contextual_review_v2.json"
BLOCKS = ((178,), (169,), (127,), (136,))
FILES = (
    parent.REVIEW,
    Path("translations/hodram_B151_B170_contextual_final_review_v1.json"),
    Path("translations/lil_B122_B127_contextual_final_review_v1.json"),
    Path("translations/maria337_integrated_final_review_v1.json"),
)
CONTEXT = (
    "Fernando ends a wager with an invitation to play again, a farewell, and thanks for the drink.",
    "Hodram can wager a drink, then win and see Fernando infer a couple's breakup. Impressed, he asks Fernando to sail with him. Fernando leaves the answer to a coin toss.",
    "Camille sees Fernando bluff a patron into folding. Fernando explains his theory of luck and reading people. Camille reads Fernando's reaction to a question, and learns how Lil beat him at Old Maid to win him over.",
    "Maria can wager a drink, then win and see Fernando infer a couple's breakup. Xien challenges Fernando's claim of insight. Maria invites Fernando to join her company, and he answers by tossing a coin.",
)

# These two route copies use the same source for each paired speech.
COMMON = {
    (11, 10): ("Now that you're here, you've got to give it a try!", ("give it a try!",), "Fernando's familiar challenge opens the repeated encounter."),
    (16, 15): ("Well, a new face! Want to bet a drink? It's a simple little game.", ("bet a drink?",), "The newcomer gets the same drink wager and quick invitation."),
    (20, 19): ("See these coins? We take turns. Take one, two, or three at a time, your choice.", ("one, two, or three",), "Keep the alternating turns and all three legal numbers explicitly."),
    (60, 59): ("Tch. You got me. Haven't lost in a while. Here you go.", ("lost in a while.",), "The rare loss irritates Fernando, who grudgingly offers the drink."),
    (89, 88): ("Take that couple over there. We can't hear them. What do you think they're talking about?", ("that couple over there.", "they're talking about?"), "Identify the couple and ask Rafael's counterparts to judge without hearing them."),
    (96, 95): ("Come on, this one's easy. They're talking about breaking up.", ("breaking up.",), "Fernando predicts the subject of their talk before either person ends the relationship."),
    (108, 107): ("I've heard enough. I can't go along with the way you think anymore. Ever think about anyone but yourself?", ("way you think", "anyone but yourself?"), "Keep the woman's shift from frustration to accusation in the same anonymous voice."),
    (114, 113): ("Oh, really? Then I guess we'd better stop seeing each other.", ("stop seeing each other.",), "She takes his reply as confirmation and proposes ending the relationship."),
    (117, 116): ("If we both feel that way, then we're done.", ("then we're done.",), "His terse agreement closes the exchange without implying a marriage."),
    (132, 131): ("See her clench her fist under the table? She was holding back her anger. That's hardly sweet talk.", ("under the table?", "holding back her anger.", "hardly sweet talk."), "Fernando spots her fist and explains how the gesture reveals suppressed anger."),
    (143, 143): ("Sure. Pick up on things like that and you can read your opponent's moves.", ("things like that", "your opponent's moves."), "Fernando connects watching people to anticipating a move at the table."),
    (146, 146): ("Add my luck to that, and I can win.", ("and I can win.",), "Preserve the ability to win with both qualities, without claiming each wager is already won."),
    (157, 157): ("Well, I've got time on my hands. I'll flip this coin. If it comes up heads, I might just go with you.", ("time on my hands.", "comes up heads,"), "The coin must land heads and Fernando keeps his tentative offer."),
    (167, 167): ("This again? Well, I'll ask the coin one more time.", ("one more time.",), "Fernando makes the decision to consult his coin again."),
    (192, 192): ("Heh. I'm not putting my life in the hands of someone with bad luck. So long.", ("with bad luck.", "So long."), "The bad toss prompts a curt refusal and the original risk of entrusting his life."),
    (208, 208): ("Heh, that settles it. I'll bet my life on you!", ("my life on you!",), "The favorable toss seals his agreement in his own gambling metaphor."),
}

EDITS = {
    0: {75: (None, ("we cross paths.", "See you,", "thanks for the drink."), "Keep the farewell together while retaining the complete approved wording.")},
    1: {
        70: ("I'll pass for now. Tell me, were you really that sure you'd win?", ("that sure you'd win?",), "Hodram declines the drink and questions Fernando's confidence plainly."),
        74: ("Sure. It takes a sharp eye and good luck to win.", ("a sharp eye", "and good luck"), "Use conversational wording for both qualities Fernando credits."),
        77: ("I've got both. It's like I was born to gamble.", ("born to gamble.",), "Fernando follows up with the original boast about having both qualities."),
        81: ("You? Good at reading people?", (), "Hodram is skeptical of Fernando's claim to insight."),
        111: ("Think what you want. You're selfish too.", ("You're selfish too.",), "The man dismisses her opinion and sends the same charge back at her."),
        136: ("And he never once looked at her. Does that look like a man sitting across from the woman he loves?", ("never once looked at her.", "the woman he loves?"), "Keep the lack of eye contact throughout and the pointed question that follows."),
        149: ("It'd be a shame to use that talent only for gambling. How about joining my crew?", ("only for gambling.", "joining my crew?"), "Hodram sees use for the talent at sea and makes a direct offer."),
        211: ("Name's Fernando Dias! Guess this is another bit of luck!", ("Fernando Dias!",), "Preserve the original introduction and Fernando's parting remark about luck."),
    },
    2: {
        13: ("Damn it! I can't call that! I-I fold!", (), "The patron curses, refuses the raised bet, and stammers his concession."),
        24: ("Luck. Get it on your side, and even a reckless bluff can be your best play.", ("a reckless bluff", "your best play."), "Fernando explains how luck can turn even a risky bluff into a winning tactic."),
        32: ("Luck made you read it wrong. You figured I was bluffing to get you to raise.", ("you to raise.",), "Show what the patron guessed about the bluff and where Fernando credits luck."),
        39: ("Fernando, that was some game!", (), "Restore Camille's delighted address to Fernando."),
        42: ("Oh, Camille! You saw that? Barkeep, pour him a drink too. It's on me.", ("pour him a drink too.", "It's on me."), "Fernando recognizes Camille and offers him a drink on the same tab."),
        50: ("Thanks! Is that what you always mean when you say 'watch closely'?", ("'watch closely'?",), "Camille links the hand to Fernando's familiar advice, not a new phrase."),
        53: ("Heh. You're pretty sharp. That's right.", ("pretty sharp.",), "Fernando recognizes Camille's insight with dry approval."),
        57: ("You need luck, and you need to pay attention. That's insight. You're not going to win without both.", ("pay attention.", "without both."), "Fernando explicitly defines insight and says successful gambling takes both qualities."),
        65: ("How would I... Hmm. Is that even possible?", ("Is that even possible?",), "Camille starts trying to solve the question before doubting the premise."),
        77: ("Luck doesn't make winners. It favors people who already win.", ("people who already win.",), "Keep Fernando's paradox and frame it as his own theory."),
        85: ("Insight! The better you can read people, the better your odds of winning.", ("read people,", "odds of winning."), "Camille draws the conclusion about reading people and improving the odds."),
        89: ("You're sharp, Camille. I read him and won the early hands. So he read me wrong on the last one and lost.", ("won the early hands.", "and lost."), "Keep Fernando's earlier wins as the reason the patron misreads the final hand and loses."),
        96: (None, ("how you ended up",), "The question about joining Lil's crew works. Reflow around the original given-name substitution."),
        107: ("I-I told you before, didn't I? 'A lot of stuff happened...'", ("I told you before,", "'A lot of stuff happened...'"), "Fernando stammers and repeats the same evasive answer."),
        110: ("That's what I want to know. Don't tell me you lost a bet to FI?", ("lost a bet to",), "Restore Camille's answer to the evasion and his tentative deduction."),
        122: ("Ugh... You're a little too sharp.", ("a little too sharp.",), "Fernando begrudgingly turns his earlier compliment back on Camille."),
        125: ("That girl wouldn't let up. I said I'd sail with her if she beat me. Big mistake...", ("if she beat me.", "Big mistake..."), "Keep Fernando's annoyance, the wager, and his regret at setting the terms."),
        129: ("I can't believe you lost, Fernando. What happened?", ("you lost, Fernando.",), "Restore Camille's direct address and leave the question open for the story."),
        137: ("She didn't know poker, baccarat, or blackjack. Old Maid was the only game she knew!", ("poker, baccarat,", "the only game she knew!"), "Preserve every game he lists and why he had to play Old Maid."),
        141: ("What grown man can seriously ask, 'Which card is the Old Maid?'", ("Which card is the Old Maid?",), "Keep Fernando's incredulous punch line and the whole quoted question on one line."),
    },
    3: {
        69: ("You've still got a ways to go... And I'll pass on the drink. Were you really that sure you'd win?", ("pass on the drink.", "that sure you'd win?"), "Maria teases Fernando after his loss, declines the drink and asks about his confidence."),
        139: ("Amazing. You picked up on all that.", ("picked up on all that.",), "Maria's quieter admiration leads into the offer to put his skill to the test."),
    },
}
for (hodram, maria), revision in COMMON.items():
    EDITS[1][hodram] = EDITS[3][maria] = revision

KEEPS = {
    0: {},
    1: {
        24: "The final-coin loss and brisk invitation are clear.",
        33: "The short action label matches Hodram's direct register and starts the game.",
        35: "Pass clearly declines the wager.",
        47: "Fernando claims the one drink he won.",
        51: "Fernando enjoys the drink, thanks the player, and says goodbye in his own casual voice.",
        85: "The terse warning about appearances sets up the demonstration.",
        92: "Hodram guesses the man is trying to charm her.",
        100: "The visible question mark preserves his perplexed reaction.",
        104: "Fernando tells Hodram to watch for the answer.",
        120: "Hodram's silent beat leaves room for the couple's parting words to sink in.",
        124: "Fernando takes credit for calling it.",
        128: "Hodram is impressed and asks for the basis of the prediction.",
        140: "Hodram recognizes Fernando's sharp eye without losing his measured register.",
        153: "Fernando finds the invitation sudden and takes a beat before responding.",
        163: "Hodram puts aside the drink, then tells Fernando directly to join him.",
        214: "Hodram says he will count on Fernando's skill after Fernando credits luck.",
        228: "The dry complaint stands on its own conditional branch.",
    },
    2: {
        5: "The numbers and rising stake stay explicit.",
        9: "The clipped alternatives keep the pressure on the patron.",
        17: "Fernando lets the bluff land, then offers a laconic response.",
        21: "The patron's two stammers convey shock at the empty hand.",
        28: "Fernando says the patron expected a bluff and stops just before explaining the mistake.",
        36: "The short concession confirms the patron's defeat.",
        46: "The barkeep responds immediately to the drink order.",
        61: "Fernando turns his point about luck into a question for Camille.",
        69: "The compact answer names a habit of winning.",
        73: "Camille echoes the unfamiliar idea for clarification.",
        81: "Fernando deliberately trails off so Camille can supply the answer.",
        92: "Camille voices admiration before asking a personal question.",
        100: "Fernando coughs on the drink when Camille asks how he joined Lil.",
        103: "Camille checks on Fernando before repeating the question.",
        114: "The brief reaction conveys that Camille has struck a nerve.",
        118: "Camille recognizes the answer from Fernando's reaction.",
        133: "Fernando answers the challenge and holds back the punch line until the next line.",
        145: "Camille closes with the understated bad-luck callback.",
    },
    3: {
        23: "The original last-coin rule and the invitation fit Fernando's voice.",
        32: "The natural affirmative response starts the wager.",
        34: "The natural refusal declines the game without changing the tone.",
        46: "Fernando claims exactly one drink.",
        50: "Fernando enjoys the drink and takes his leave.",
        73: "This version already pairs a sharp eye with good luck in a natural phrase.",
        76: "Fernando's original boast fits his voice. Reflowing the phrase reproduced the existing layout exactly.",
        80: "Xien sets luck aside and challenges the sharper claim in his own measured register.",
        84: "The warning about appearances leads directly to the couple.",
        91: "Maria proposes a marriage proposal as a guess, without supplying a speaker the source leaves unspecified.",
        99: "The question mark leaves room for Maria's surprise.",
        103: "Fernando's brief instruction leads into the evidence.",
        110: "The man's terse reply returns the same accusation.",
        119: "Maria stays silent while the couple's breakup sinks in.",
        123: "Fernando's brief boast suits his confidence.",
        127: "Maria acknowledges the surprising inference and asks how he knew.",
        135: "Fernando's second observation and the rhetorical question are both intact.",
        149: "Maria offers to put Fernando's talent to the test and uses the original company substitution.",
        153: "Fernando registers surprise before he makes his counteroffer.",
        163: "Maria waves away the drink and firmly repeats the offer with the original company substitution.",
        211: "Fernando introduces himself by his established name and credits luck.",
        214: "Maria welcomes him directly after his introduction.",
        228: "The offhand complaint stands on a separate conditional branch.",
    },
}


def source_packet():
    frozen = base.load(PAIRED)
    assert frozen["candidate_sha256"] == base.digest(parent.ROM)
    scratch = ROOT / "rafael_full_paired"
    if not scratch.exists():
        bind = dict(parent=parent, ROOT=scratch, BLOCKS=((178,), (), (), ()), CONTEXT=CONTEXT)
        FunctionType(pairing.main.__code__, vars(pairing) | bind)()
    single = base.load(scratch / "paired_source.json")
    assert single["candidate_sha256"] == frozen["candidate_sha256"] and single["clean_sha256"] == frozen["clean_sha256"]
    rafael, = single["groups"]
    rafael["records"] = [row for row in rafael["records"] if row["source_record_index"] == 75]
    assert len(rafael["records"]) == 1 and rafael["block"] == 178
    base.save(SOURCE, frozen | {"groups": [rafael, *frozen["groups"]], "reference_packet": str(PAIRED),
                               "reference_packet_sha256": base.digest(PAIRED)})


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        source_packet()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    rows = []
    for group in packet["groups"]:
        route, path, block = (group[k] for k in ("route", "file_path", "block"))
        history = base.load(FILES[route])["records"]
        previous = {r["source_reference"]["offset"]: r for r in history if r["block"] == block}
        edits, keeps = EDITS[route], KEEPS[route]
        assert not edits.keys() & keeps.keys()
        assert edits.keys() | keeps.keys() == {r["source_record_index"] for r in group["records"]}
        for entry in group["records"]:
            index, selector = entry["source_record_index"], entry["selector"]
            prior = previous.pop(entry["source_offset"])
            assert prior.get("source_Japanese", prior.get("Japanese")) == entry["Japanese"]
            assert prior.get("source_selector") == selector
            current = logical(entry["current_English"])
            edit = edits.get(index)
            text, phrases, note = edit or (current, (), keeps[index])
            english = text or current
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            if route == 0:
                assert prior["english"] == current and prior["registered_reference"]["offset"] + 5 == entry["current_offset"]
            leading = "" if selector is None else f"{selector:02x}"
            refs = {side: dict(file_path=path, block=block, offset=entry[f"{side}_offset"],
                command_offset=entry[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                block_sha256=group[f"{side}_block_sha256"], exact_hex=leading + entry[f"{side}_body_hex"])
                for side in ("source", "current")}
            rows.append(dict(id=prior["id"], file_path=path, route=route, block=block, source_record_index=index,
                native_command_word=entry["native_command_word"], native_slots=entry["slots"], source_selector=selector,
                kind="typed-choice-label" if selector is None else "progressive",
                source_reference=refs["source"], current_reference=refs["current"],
                source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                Japanese=entry["Japanese"], previous_English=current, english=english, speaker=prior["speaker"],
                context=CONTEXT[route], source_meaning=prior["source_meaning"], localization_note=note,
                protected_phrases=list(phrases), review=dict.fromkeys(GATES, True) | {"formatting": not edit},
                decision="revision" if edit else "retention",
                finding="retention" if not edit else "wrap" if english == current else "prose and wrap"))
        assert route == 0 or not previous
    assert len(rows) == 121
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        records=rows, decisions=dict(Counter(row["decision"] for row in rows)),
        findings=dict(Counter(row["finding"] for row in rows)), new_editorial_credit=0,
        status="Contextual review complete. Revised pages await native verification."))
    print(f"Reviewed {len(rows)} records across the three Fernando scenes and Rafael's farewell.")


if __name__ == "__main__":
    main()
