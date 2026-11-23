"""Review Rafael's complete resupply and first-voyage exchange."""

from inspect import getsource
from pathlib import Path

from scripts import register_rafael_deck_lesson_20261119 as parent
from scripts import review_rafael_deck_lesson_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path("work/rafael_first_voyage_20261119_v2")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v2.json"
BLOCKS = ((42,), (), (), ())
CONTEXT = (
    "Julio explains port resupply before the first departure. Rafael asks what to do at sea. "
    "Clau's rush to hunt pirates gives way to Julio's practical advice on travel, recruiting and trade. "
    "Julio then teases Rafael about the money he provided and reassures him.",
)
SPEAKERS = {0: "Rafael", 4: "Janus", 5: "Claudio", 6: "Julio Erneco"}

LESSON = {
    5: ("A hired crew needs food and water. The Port has both, and Julio asks Rafael to come along.",
        "Identify the supplies in the same thought and let Julio take Rafael to the named menu stop.",
        "Once you've hired a crew, you'll need food and water. Let's stock up at the Port.",
        ("you'll need food and water.", "stock up at the Port.")),
    9: ("The young fellow at the Port handles resupply automatically. Julio says it's easy.",
        "The singular attendant gives Julio's next 'he' a clear referent.",
        "The fellow at the Port takes care of resupply for you. Easy as that.",
        ("at the Port", "Easy as that.")),
    12: ("If funds are short, the attendant supplies only what they can afford.",
         "The direct response to a shortage follows the explanation of who handles resupply.",
         "If you're short on money, he'll give you as much as you can afford.", ("you can afford.",)),
    15: ("Declining the resupply offer lets them adjust the proportion of water to food. Julio rarely expects them to need it.",
         "Say what the player does and specify the mix of supplies. The final sentence keeps Julio's practical aside.",
         "Say no to resupply and you can change the mix of food and water. You won't need to do it often.",
         ("food and water.", "do it often.")),
    19: ("Sailors cannot work at full strength with too few supplies. Even a good ship then goes to waste. Watch what remains.",
         "Keep the sailor warning, the ship and the advice in their original order. Put the whole warning on one page.",
         "When supplies run low, the crew can't do its best. Even a fine ship won't help then. Keep an eye on what you have left.",
         ("a fine ship", "Keep an eye on")),
    22: ("Julio asks whether Rafael is ready.", "The quick check moves from instruction to departure.", None, ()),
    26: ("Rafael cheers their departure, then asks what they will do at sea.",
         "The turn from excitement to uncertainty sets up Clau's joke.", None, ()),
    30: ("Clau ribs Rafael for getting ahead of himself without thinking it through.",
         "Clau is teasing Rafael about his eagerness to sail.",
         "What? You got this excited without thinking that far ahead?", ("that far ahead?",)),
    33: ("Janus laughs and says he never expected to hear that from Clau.",
         "Address Clau directly so his immediate protest answers the tease.",
         "Ha! I never thought I'd hear that from you, Clau.", ("from you, Clau.",)),
    36: ("Clau angrily objects that Janus makes it sound as if he never thinks.",
         "The repeated 'think' lands as Clau's indignant defense.", None, ()),
    40: ("Janus apologizes with mock politeness, then invites Clau to share his supposed brilliant idea.",
         "The polite opening and dry invitation set up Clau's scramble for an idea.",
         "Oh, forgive me. I didn't know you'd given it any thought. Let's hear your brilliant idea.",
         ("Oh, forgive me.", "Let's hear your brilliant idea.")),
    43: ("Clau stalls and hesitates, then blurts out that he has an idea.",
         "The short stammer gives his sudden inspiration a comic pause.",
         "Huh? Oh, uh... I know!", ()),
    47: ("Clau proposes fighting pirates, boarding their ships and striking down ruffians one after another.",
         "Keep the boast about boarding and the rapid succession while giving the question a clean landing.",
         "How about going after pirates? I'll board their ships and knock those thugs down one by one!",
         ("going after pirates?", "I'll board their ships", "one by one!")),
    50: ("Janus sighs at Clau's boast.", "The curt reaction and pause puncture Clau's excitement.", None, ()),
    54: ("Rafael asks for a serious plan and says their current ability would get them killed.",
         "Rafael pulls the talk back to reality. His warning stays plainly about how unprepared they are.",
         "Let's think this through... We're nowhere near ready for that. We wouldn't make it out alive.",
         ("Let's think this through...", "make it out alive.")),
    59: ("Julio agrees and suggests making the rounds at ports such as those in the Mediterranean and North Sea.",
         "Preserve both regions as examples of the safer first trips Julio recommends.",
         "That's right. Start by visiting a few ports, say in the Mediterranean or North Sea.",
         ("Mediterranean or North Sea.",)),
    63: ("By visiting many ports they'll naturally learn about sailing and trading.",
         "The promise of learning along the way answers why they should make those stops.", None, ()),
    67: ("Rafael agrees and urges the group to recruit more companions.",
         "Rafael gets excited again, this time about inviting people to sail with them.",
         "Right! And let's find more people to sail with us!", ("to sail with us!",)),
    71: ("Julio is a little uneasy about continuing with only the present group.",
         "A spoken concern about the crew leaves room for Clau to take the remark personally.",
         "Mm. If we're going to keep sailing, I'm a little worried about the crew we've got.", ("the crew we've got.",)),
    74: ("Clau calls Julio old man and asks why Julio looked at him while saying that.",
         "The familiar rudeness and fuller question keep the gag and invent no family relationship.",
         "Old man! Why'd you look at me when you said that?", ("you look at me", "when you said that?")),
    77: ("Janus calms them and agrees that more companions would help.",
         "Let Janus defuse the joke before returning to the practical point.",
         "Easy now. He's right, though. It'd help to have more people with us.", ("He's right, though.", "It'd help")),
    80: ("Julio tells Rafael he has no doubt that he will find good people to sail with.",
         "Use the original first-name substitution and make the reassurance personal and direct.",
         "FI, you'll find good people to sail with. I'm sure of it.", ("people to sail with.", "I'm sure of it.")),
    84: ("Rafael softly answers Julio by name.", "The short name and trailing pause give the reassurance room.", None, ()),
    89: ("Janus adds that they need money to add ships and keep them running.",
         "Keep additions and upkeep as distinct expenses. The unfinished ending gives Julio his cue.",
         "We'll also need more money to buy more ships and keep them running...", ("more ships", "keep them running...")),
    92: ("Julio says trading repeatedly at different ports will build up their funds.",
         "The plain promise about the money adding up follows Janus's concern.", None, ()),
    95: ("Julio warns that neglecting trade will drain their money and reminds Rafael that it was his.",
         "Keep the warning practical and give the personal reminder its own beat before Rafael takes it seriously.",
         "But slack off on trading and you'll keep losing money. It was mine to begin with, you know. Be careful with it.",
         ("losing money.", "Be careful with it.")),
    99: ("Rafael thanks Julio and earnestly says he will earn enough to repay him.",
         "Rafael takes the debt seriously. The trailing thought lets Julio cut the tension.",
         "Thank you, Julio. I'll make sure I earn enough to pay you back...", ("Thank you, Julio.", "pay you back...")),
    103: ("Julio chuckles, says he was joking, and suggests that they get going.",
          "The familiar laugh and reassurance end the lesson on an easy invitation to leave.",
          "Ho ho ho! I'm only teasing. Don't worry about it. Well, shall we go?",
          ("Don't worry about it.", "Well, shall we go?")),
}

source = checked_text(getsource(workflow.main), {
    'assert data["selector"] in (6, 254) and (data["selector"] == 254) == (idx == 45)':
        'assert data["selector"] in SPEAKERS',
    ' and data["selector"] == 6': '',
    'block=43': 'block=42',
    'f"DK4_MES_B43_R{idx:04}"': 'f"DK4_MES_B42_R{idx:04}"',
    'kind="system-FE" if idx == 45 else "progressive"': 'kind="progressive"',
    'speaker="System" if idx == 45 else "Julio Erneco"': 'speaker=SPEAKERS[data["selector"]]',
    "Reviewed Julio's complete 12-turn Deck lesson.": "Reviewed 28 turns in the first-voyage exchange.",
})
env = vars(workflow) | globals()
exec(compile(source, __file__ + "::whole-exchange", "exec"), env)

if __name__ == "__main__":
    env["main"]()
