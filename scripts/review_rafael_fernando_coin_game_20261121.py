"""Record the contextual revisit of Fernando's game and recruitment."""
from inspect import getsource
from pathlib import Path

from scripts import register_rafael_refit_sailing_lessons_20261121 as parent
from scripts import review_rafael_refit_sailing_lessons_20261121 as workflow
from scripts.review_hodram_alexandria_tutorial_20261121 import GATES, TOKEN, logical
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/rafael_fernando_coin_game_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v1.json"
BLOCKS = ((178,), (), (), ())
CONTEXT = {178: "Fernando wagers a drink in a coin game. A loss lets Janus teach Rafael to leave one more than a multiple of four. After Rafael wins, Fernando reads a nearby couple's breakup and Rafael recruits him. Fernando makes his decision on a coin toss."}

REVISIONS = {178: {
    11: ("Now that you're here, you've got to give it a try!", ("give it a try!",), "Fernando jovially challenges a returning player."),
    16: ("Well, a new face! Want to bet a drink? It's a simple little game.", ("bet a drink?",), "The newcomer gets a friendly challenge and the original drink wager."),
    52: ("I almost feel bad, you buying me drinks every time. Well, don't mind if I do. Ah, that's good!", ("buying me drinks", "don't mind if I do."), "Fernando jokes about repeated losses before enjoying his winnings."),
    64: ("Like I said, FI, leave them with one more than a multiple of four. That's how you win.", ("a multiple of four.", "That's how you win."), "Keep Janus's reminder, given-name substitution and exact number strategy."),
    75: ("Heh. I'll play you again if we cross paths. See you, and thanks for the drink.", ("we cross paths.", "thanks for the drink."), "Fernando offers a rematch and thanks Rafael for the wager he won."),
    89: ("Hey, FI! Losing like that really burns me up! Let's play again!", ("really burns me up!", "Let's play again!"), "Claudio's impulsive frustration drives him to ask for a second game."),
    97: ("I'm good, sure. But luck alone won't get you far at the gambling table.", ("luck alone", "the gambling table."), "Fernando admits his confidence. His point about luck prompts Janus's realization."),
    107: ("FI, listen! I think I've found a way to win this game every time!", ("win this game", "every time!"), "Keep Janus's excitement, uncertainty and original address to Rafael."),
    116: ("Leave them with one more than a multiple of four. Keep doing that, and you'll make them take the last coin.", ("a multiple of four.", "take the last coin."), "Explain the strategy as the repeated move that forces the opponent to take the final coin."),
    124: ("Can you make that a little simpler?", (), "Claudio immediately asks for a more accessible explanation."),
    127: ("All right. Say there are five coins left, and your opponent takes one. What would you do?", ("five coins left,", "your opponent takes one."), "Keep the concrete five-coin setup and the first move."),
    131: ("That leaves four. I'd take three.", (), "Rafael gives the arithmetic and his move in the right order."),
    139: ("I'd take two... I get it! If I leave them five, I can win whatever they take next.", ("If I leave them five,", "they take next."), "Rafael realizes why leaving five works no matter which move comes next."),
    147: ("Nine works too. It's one plus four plus four. Whatever they take, I can leave them five and win.", ("one plus four plus four.", "leave them five and win."), "Keep the exact arithmetic, the opponent's freedom to take a legal number and the winning five-coin position."),
    151: ("You caught on fast, Admiral.", (), "Janus's brief compliment carries his fond respect before Claudio interrupts."),
    155: ("Hey, I haven't got a clue what you two are talking about!", ("you two are talking about!",), "Claudio's blunt admission contrasts with Janus and Rafael's quick exchange."),
    161: ("Shut up! You two get it and leave me out. That's what bugs me!", ("leave me out.",), "Keep both the outburst and Claudio's resentment at being left behind."),
    168: ("Ahh, nothing like a free drink. Come back anytime you want another game.", ("like a free drink.", "want another game."), "Keep Fernando's satisfaction and his invitation to come back."),
    192: ("I'll pass on the drink. You said you hadn't lost in a while. Are you usually that hard to beat?", ("lost in a while.", "that hard to beat?"), "Rafael declines the drink for now and follows up on Fernando's remark about his record."),
    199: ("I've got both. It's like I was born to gamble.", ("born to gamble.",), "The existing boast fits Fernando and retains both traits. Keep the gambling phrase together."),
    203: ("I don't know about your luck, but can you really read people that well?", ("read people that well?",), "Rafael is skeptical and asks about the ability Fernando is about to demonstrate."),
    211: ("Take that couple over there. We can't hear them. What do you think they're talking about?", ("that couple over there.", "they're talking about?"), "Fernando identifies the couple and asks Rafael to infer a topic without hearing them."),
    218: ("Come on, this one's easy. They're talking about breaking up.", ("breaking up.",), "Fernando says it is a breakup conversation before it actually ends."),
    231: ("I've heard enough. I can't go along with the way you think anymore. Ever think about anyone but yourself?", ("way you think", "anyone but yourself?"), "The woman's patience gives way to a direct complaint and accusation. Keep her generic role label."),
    237: ("Oh, really? Then I guess we'd better stop seeing each other.", ("stop seeing each other.",), "The existing response makes her decision clear. Keep the breakup phrase together."),
    257: ("See her clench her fist under the table? She was holding back her anger. That's hardly sweet talk.", ("under the table?", "holding back her anger.", "hardly sweet talk."), "Fernando identifies the physical clue, interprets it as suppressed anger and answers Rafael's earlier guess."),
    265: ("That's amazing! You picked up on all that?", ("picked up on all that?",), "Rafael is impressed that Fernando noticed those quiet details."),
    269: ("Sure. Pick up on things like that and you can read your opponent's moves.", ("things like that", "your opponent's moves."), "Fernando connects reading the couple to recognizing an opponent's next move."),
    275: ("Come sail with me! A talent like yours is too good to waste.", ("too good to waste.",), "Rafael's impulsive invitation follows directly from his admiration."),
    283: ("Well, I've got time on my hands. I'll flip this coin. If it comes up heads, I might just go with you.", ("time on my hands.", "comes up heads,"), "Preserve the coin's exact condition and Fernando's tentative agreement."),
    289: ("Forget the drink. Come with us!", ("Come with us!",), "On the repeat path Rafael skips the drink and asks again."),
    294: ("This again? Well, I'll ask the coin one more time.", ("one more time.",), "Fernando is the one who consults the coin again."),
    320: ("Heh. I'm not putting my life in the hands of someone with bad luck. So long.", ("with bad luck.", "So long."), "A bad toss leads to the original refusal and a curt goodbye."),
    336: ("Heh, that settles it. I'll bet my life on you!", ("my life on you!",), "A favorable toss earns Fernando's trust. Preserve the wager metaphor and excitement."),
}}

RETENTIONS = {178: {
    20: "The turn order and choice of one to three coins are plain.",
    24: "The last-coin rule and Fernando's teasing lead-in are both intact.",
    33: "The upbeat acceptance announces the player's actual choice.",
    35: "The brief polite refusal clearly declines the game.",
    67: "Rafael admits he slipped up after Janus reminds him of the strategy.",
    79: "Fernando attributes the loss to bad luck and claims only the drink.",
    93: "Rafael restrains Claudio's impulse and recognizes Fernando's experience.",
    100: "Janus echoes the reference to luck as he realizes something.",
    103: "Claudio gives Janus the opening to explain.",
    111: "Rafael is surprised and prompts him to continue.",
    120: "Rafael admits he needs a clearer explanation.",
    136: "Janus resets the example to five and changes his opponent's move to two.",
    143: "The concise confirmation lets Rafael develop the next example on his own.",
    158: "Janus teases Claudio for lagging behind without adding hostility.",
    181: "Fernando grudgingly acknowledges the rare loss and offers the due reward.",
    196: "Fernando names both insight and luck as necessary qualities.",
    207: "Fernando warns Rafael against judging by appearances, then demonstrates.",
    214: "Rafael's affectionate interpretation makes Fernando's contrary inference land.",
    222: "Rafael's short reaction conveys that he is puzzled.",
    227: "Fernando directs Rafael to watch the couple for himself.",
    234: "The man dismisses her opinion and levels the same accusation back at her. Keep his generic role label.",
    240: "The man's terse line ends the relationship by mutual agreement.",
    243: "Rafael's silent beat gives the breakup room to register before Fernando speaks again.",
    248: "Fernando claims his prediction was right with the original confident tag.",
    252: "Rafael immediately asks how Fernando knew.",
    261: "The man looking away throughout is the second clue. Fernando's question carries the inference.",
    272: "Fernando returns to good luck as the other part of his success.",
    279: "Fernando reacts to the unexpected invitation before making his offer.",
    339: "Fernando gives his full approved name and attributes the result to luck.",
    342: "Rafael gives the new recruit a brief friendly welcome.",
    357: "Fernando's complaint about slim pickings retains his curt tone on the separate conditional path.",
}}


source = checked_text(getsource(workflow.main), {
    'assert len(rows) == 62': 'assert len(rows) == 65',
    'in the complete refit and sail-rigging lessons.': 'in the complete coin game and recruitment exchange.',
})
scope = vars(workflow) | globals()
exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
