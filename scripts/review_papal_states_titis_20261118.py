"""Review the complete Papal States and Titis exchanges across the four routes."""

from collections import Counter
from pathlib import Path
import sys
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_regional_proof_dialogue_20261118 as parent
from scripts.review_london_guild_assignments_20261118 import TOKEN, base, logical

ROOT = Path("work/papal_states_titis_20261118")
SOURCE = ROOT / "paired_source.json"
SOURCE_SHA = "34fd88f1e424455cf39a41562196470e5c3abde8e984535c9841ec636da5daeb"
OUTPUT = ROOT / "papal_states_titis_prose_v2.json"
BLOCKS = ((246, 262), (237, 253), (234, 252), (207, 222))
GATES = ["source", "context", "localization", "naturalness", "formatting"]
CONTEXT = (
    "Carlo finds Filippo, a trader he knows, lost in thought. They tease each other before Filippo recounts his great-grandfather's story about papal trade. Their talk of a blessing leads to a possible discovery.",
    "Titis greets the captain by name, offers directions to nearby ruins, then tells them she is making an exception to her usual practice with visitors from abroad.",
)


def keep(meaning, note):
    return meaning, None, (), note


PAPAL = (
    keep("Filippo is silent, absorbed in thought.", "The Japanese pause and its existing glyphs start the exchange before Carlo interrupts."),
    keep("Carlo asks what is wrong and why Filippo is staring into space.", "The familiar name and the quick daydreaming question fit Carlo's teasing opening."),
    ("Filippo startles, recognizes Carlo and asks when he got back.",
     "Carlo? Is that you? When'd you get back?", ("Is that you?", "When'd you get back?"),
     "Restore the moment of recognition in a colloquial exchange between people who know each other."),
    keep("Carlo stopped by on business and jokes that Filippo will drive away customers if he keeps wearing that vacant expression.",
         "Retain the reason for the visit and the joke about the customers. The stare was already established by Carlo's first question."),
    ("Filippo objects to the teasing, then takes it as a sign Carlo has recovered.",
     "Mind your own business! You're giving me a hard time again, so you must be feeling like yourself.",
     ("Mind your own business!", "You're giving me a hard time", "feeling like yourself."),
     "Keep the sharp first reply and the concern underneath the teasing. The source leaves the details of Carlo's recovery unstated."),
    keep("Carlo says he is finally back in action and aboard their ship now.",
         "Both the return to work and the current crew are plain. The next turn lets Filippo notice the other people."),
    ("Filippo notices the customers and apologizes for thinking about a story his great-grandfather told him.",
     "Oh, customers! Sorry. I just remembered a story my great-grandfather told me.",
     ("Oh, customers!", "I just remembered", "my great-grandfather told me."),
     "Keep the specific family relationship and make the transition from apologizing to remembering sound conversational."),
    keep("Carlo asks what kind of story it was.", "The brief question hands the conversation to Filippo."),
    ("The story concerns trade in the Papal States. The pope once directly governed land almost as far as Venice.",
     "Trade in the Papal States. The pope once ruled directly over lands almost as far as Venice.",
     ("Trade in the Papal States.", "The pope once ruled directly", "as far as Venice."),
     "Keep direct rule and the extent of the territory. The first sentence answers Carlo's question in the trader's voice."),
    keep("Carlo has heard trade flourished in those lands at the height of papal power.",
         "The existing route wording keeps both the report and the relationship between trade and papal power."),
    ("The lords vied over what to donate to the pope and how much.",
     "Right. The lords tried to outdo each other with their gifts to the pope. What to offer, how much...",
     ("outdo each other", "gifts to the pope.", "What to offer, how much..."),
     "The trailing list keeps the two aspects of the competition and sets up what the traders gained."),
    ("Filippo's ancestors made a great deal just passing goods along, before circumstances changed.",
     "My ancestors made a fortune just passing goods along. But these days...",
     ("made a fortune", "passing goods along.", "But these days..."),
     "Keep their gains as intermediaries. The trailing contrast gives Carlo the opening to describe the decline."),
    ("The pope's power waned and trade with the Church shrank sharply.",
     "The pope's power waned, and trade with the Church all but dried up.",
     ("trade with the Church", "all but dried up."),
     "Preserve the sharp decline and its specific customer without implying the trade ended altogether."),
    ("Filippo says they again have to make a living by their own hard work and envies his great-grandfather.",
     "Now we're back to working for every coin we earn. I envy my great-grandfather.",
     ("every coin we earn.", "I envy my great-grandfather."),
     "Restore Filippo's envy and the contrast with his ancestors' easy profits."),
    keep("Carlo has heard objects associated with the pope sometimes turn up in former papal lands.",
         "The wording keeps the report as hearsay and leaves the type of object open."),
    ("Filippo thinks an object a pope once used might carry a blessing, and says he could use God's help himself.",
     "So they say. If a pope used it, it might carry a blessing. I could use some help from above!",
     ("If a pope used it,", "carry a blessing.", "I could use some help from above!"),
     "Keep the uncertain use of the object, the blessing and Filippo's personal aside in this religious context."),
    ("Carlo echoes the idea of divine blessing.",
     "A blessing...", (), "Carlo picks up the term Filippo just used. The pause lets his practical idea form."),
    keep("Carlo tells the admiral their talk may be serious. Finding something a pope treasured would be a major discovery.",
         "The existing conditional line turns their banter into a possibility without treating any artifact or blessing as proven."),
)
TITIS = (
    ("Titis recognizes the captain by their given name and welcomes them.",
     "Good to see you, FI!", ("Good to see you, FI!",),
     "Use a warm spoken greeting and preserve the original given-name substitution."),
    ("Titis asks if they are looking for ruins and says there are some nearby.",
     None, ("There are some nearby.",),
     "Keep the existing words and give the short directions their own complete line."),
    ("Titis normally keeps the location from visitors from abroad, but will make an exception for the captain.",
     "I don't tell visitors from abroad about the ruins. I'll make an exception for you.",
     ("visitors from abroad", "about the ruins.", "I'll make an exception for you."),
     "Restore the explicit exception, keep the ruins as the subject, and leave the reason for the exception unstated."),
)


def main():
    assert not OUTPUT.exists() and base.digest(SOURCE) == SOURCE_SHA
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    actors = base.load(Path("translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json"))["records"]
    rows, source_templates = [], {}
    for group in packet["groups"]:
        route, block, path = group["route"], group["block"], group["file_path"]
        family = BLOCKS[route].index(block)
        records = group["records"]
        source_text = [row["source_body_hex"] for row in records]
        assert source_templates.setdefault(family, source_text) == source_text
        for data, decision in zip(records, (PAPAL, TITIS)[family], strict=True):
            idx, selector = data["source_record_index"], data["selector"]
            meaning, proposal, protect, reason = decision
            previous = logical(data["current_English"])
            english = previous if proposal is None else proposal
            finding = "prose" if english != previous else "wrap" if protect else "retention"
            assert TOKEN.findall(english) == TOKEN.findall(previous) == TOKEN.findall(data["Japanese"])
            assert (english.isascii() or finding == "retention") and data["native_command_word"] == 0x4000
            src, cur = (dict(file_path=path, block=block, offset=data[f"{side}_offset"], command_offset=data[f"{side}_command_offset"],
                archive_sha256=group[f"{side}_archive_sha256"], exact_stored_hex=bytes([selector]).hex() + data[f"{side}_body_hex"])
                for side in ("source", "current"))
            src["record_index"] = idx
            rows.append(dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block, kind="progressive",
                native_command_word=0x4000, source_selector=selector, native_slots=[], source_reference=src, current_reference=cur,
                source_hex=src["exact_stored_hex"], current_hex=cur["exact_stored_hex"], Japanese=data["Japanese"],
                previous_English=previous, english=english, context=CONTEXT[family], speaker=actors[selector]["current_consumers"][0]["text"],
                source_meaning=meaning, localization_note=reason, protected_phrases=list(protect), finding=finding,
                decision="retention" if finding == "retention" else "revision", review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert len(rows) == 84
    counts = dict(Counter(row["finding"] for row in rows))
    base.save(OUTPUT, dict(source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=GATES, records=rows, decisions=counts,
        new_coverage_credit=0, formatting_and_registration_pending=True))
    print(counts)


if __name__ == "__main__":
    if sys.argv[1:] == ["--pair"]:
        env = vars(paired) | dict(ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=("Rafael", "Hodram", "Lil", "Maria"), parent=parent)
        FunctionType(paired.main.__code__, env)()
        assert base.digest(SOURCE) == SOURCE_SHA
    else:
        assert not sys.argv[1:]
        main()
