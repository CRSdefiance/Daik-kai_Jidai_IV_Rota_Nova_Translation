"""Review the two cave-in voice tables and both choice menus in Rafael B261."""

from inspect import getsource

from scripts import pair_rafael_B261_B280_20261122 as paired
from scripts import review_rafael_B221_B224_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_B261.json"
CARRY = paired.ROOT / "earlier_contextual_decisions_B261_B280.json"
DECISIONS = {
    261: """
270_0|||The front stone is the first choice and corresponds to a rising water level in the instruction.
270_1|||The left stone is the second choice and corresponds to a falling water level.
270_2|||The right stone is the third choice. It selects the unchanged water level and advances to the opening wall.
STYLE_342_0|||This crew voice addresses the admiral, calls out the collapsing ceiling and warns that they are in danger.
STYLE_342_46||The ceiling's coming down!|The speaker warns the admiral before naming the collapsing ceiling. Keep that second warning on one line.
STYLE_342_86|||The voice has an alarmed summons and a direct warning about the ceiling. Both short bursts fit.
STYLE_342_126|||The voice urges the group to escape after calling the admiral's attention to the ceiling. Keep its explicit invitation to flee.
STYLE_342_176|||The abrupt warning comes first without the admiral's title. Keep that difference before the collapse.
STYLE_342_212|||The older voice addresses the admiral and advises that they get out. The second sentence maintains its distinct phrasing.
STYLE_342_264|||The alarm and stammer convey a younger voice's surprise. Keep the contracted warning.
STYLE_342_298||It isn't safe to stay here.|The measured voice describes the ceiling and makes clear that staying is dangerous. Keep the full second statement together.
STYLE_852_0|||The second cave-in uses the same direct report and separate danger statement in this slot. Keep the body attached to this second branch.
STYLE_852_46||The ceiling's coming down!|The voice warns the admiral before naming the collapsing ceiling in the second wrong-answer path. Keep the warning intact here too.
STYLE_852_86|||The alarmed summons and direct collapse warning remain natural in the second original table.
STYLE_852_126|||The speaker names the collapse and urges escape in the other wrong-answer path. Keep the urgency.
STYLE_852_176|||The second cave-in retains the untitled Look out and names the immediate danger.
STYLE_852_214|||The older voice preserves the admiral's title and the suggestion that they leave the room.
STYLE_852_266|||Preserve the alarmed cry and stammer in the corresponding second slot.
STYLE_852_300||It isn't safe to stay here.|The last slot makes the same measured assessment in the other branch. Keep its complete second statement together.
1664_0|I am.||This answers the figurehead's question about whether Rafael is the one who awakened it. Keep the affirmative in the original first slot.
1664_1|I'm not.||This denies being the person who awakened the figurehead. Keep the distinct refusal and its original second slot.
""",
}
WRAPS = {
    "SC0_B261_STYLE_342_46", "SC0_B261_STYLE_342_298",
    "SC0_B261_STYLE_852_46", "SC0_B261_STYLE_852_300",
}


source = checked_text(getsource(prior.main), {
    '    records = []': '''    carry = base.load(CARRY)
    assert carry["candidate_sha256"] == packet["candidate_sha256"]
    pending = {row["id"] for row in carry["pending_records"]}
    records = []''',
    'zip(group["records"], decisions, strict=True)': 'zip((row for row in group["records"] if row["id"] in pending), decisions, strict=True)',
    '            records.append(entry)': '''            if entry["id"] in WRAPS:
                assert entry["decision"] == "retention" and entry["kind"] == "actor-style"
                entry.update(decision="revision", change_class="wrap-only",
                    prose_retention_reason="The existing English conveys this voice's warning accurately.")
            records.append(entry)''',
    'len(records) == 56 and len({row["id"] for row in records}) == 56': 'len(records) == 21 and {row["id"] for row in records} == pending',
    'for row in records) == 15': 'for row in records) == 16',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
