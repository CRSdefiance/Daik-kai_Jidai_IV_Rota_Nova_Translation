"""Stage Rafael's Mediterranean exchanges and Maria's two-page crew story."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import bind_maria_admiral_story_20261122 as maria
from scripts import cleanup_hodram_sera_nagarpur_and_kuhn_20261122 as checkpoint
from scripts import register_hodram_sera_nagarpur_and_kuhn_20261122 as current
from scripts import stage_hodram_sera_nagarpur_and_kuhn_20261122 as template
from scripts import stage_rafael_B84_training_20261122 as typed
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/rafael_athens_and_maria_crew_20261122/release")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("rafael_athens_and_the_proof_20261122.md")
ROOT = BATCH / "staged"
ROM = ROOT / "Rafael_Athens_And_Maria_Crew_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
CHOICES = {}
CONTEXT, DECISIONS = FunctionType(
    template.sections.load.__code__, template.sections.load.__globals__ | globals())()
review_source = checked_text(template.review_source, {
    'len(checked) == 108 and not choice_proofs and all(r["source_selector"] != 254 for r in checked)':
        'len(checked) == 106 and not choice_proofs and sum(r["source_selector"] == 254 for r in checked) == 4',
    'in six complete exchanges.': 'in two complete Rafael exchanges.',
    'assert route == 1 and block in BLOCKS and prior == " ".join(japanese[1:].decode("cp932").split())':
        'assert route == 0 and block == 48 and prior == " ".join(japanese[1:].decode("cp932").split())',
})
review_scope = template.review_scope | globals() | dict(ROOT=BATCH, established=template.review_scope["established"])
exec(compile(review_source, __file__ + "::Rafael-review", "exec"), review_scope)
preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))


MARIA_PHRASES = {
    15: ("Admiral FI", "that scary?", "I don't see it."),
    24: ("you wouldn't know.", "call her scary.", "rewards and punishments."),
    30: ("back then.", "Scary ain't the word.", "who gets rewarded", "who gets punished."),
    36: ("I remember something", "a while back..."),
    58: ("in triumph,", "a senior post", "as a reward."),
    61: ("with desertion", "in the face of the enemy.", "on the spot..."),
    68: ("gave his family", "a permanent officer's pension."),
    82: ("I couldn't bring myself", "to speak to her.", "I could hardly bear it."),
}
MARIA_REFINED = {
    15: "Is Admiral FI really that scary? Everyone says she is. I don't see it.",
    24: "You joined us later, so you wouldn't know. I wouldn't call her scary. She's strict about rewards and punishments.",
    30: "You weren't here back then. Scary ain't the word. She's real clear about who gets rewarded and who gets punished.",
    58: "When he returned in triumph, FI had gold and a senior post ready for him as a reward.",
    61: "Then she charged him with desertion in the face of the enemy. She sentenced him to death on the spot...",
    68: "The admiral gave his family the gold and promised them a permanent officer's pension.",
}
MARIA_MEANING = {
    7: "Young crew member addresses Ian.", 11: "Ian asks what it is.",
    15: "The young crew member hears the admiral is frightening but sees little reason for it.",
    24: "Ian explains her strict rewards and punishments to a later recruit.",
    30: "The informal answer makes the same distinction in a rougher voice.",
    36: "Ian agrees and remembers an incident.",
    41: "A man deserts during a battle with wokou, leaving allied ships surrounded.",
    44: "The desertion causes a grave defeat and many deaths and prisoners.",
    48: "The man realizes he has no place if he returns.",
    51: "He boards the celebrating Japanese flagship alone and takes the commander's head, reversing the defeat.",
    54: "The young crew member is impressed.",
    58: "The admiral prepares a senior position and gold to reward the victory.",
    61: "She immediately charges the man with desertion in the face of the enemy and sentences him to death.",
    64: "Silence after the verdict.",
    68: "The admiral gives his family the gold and promises continuing support at officer level.",
    72: "He cries, thanks her, and accepts the punishment.",
    82: "Ian recalls the admiral as frightening to approach and visibly sorrowful.",
    87: "Yukihisa recalls the same fear and sorrow in formal speech.",
    93: "The young crew member reacts in disbelief.",
    102: "Another crew member offers to tell the story in more detail.",
    106: "The young crew member politely declines to hear it again.",
    110: "The storyteller insists on explaining Maria's feelings and the company's lofty ideals.",
    113: "The young crew member announces bedtime and says good night.",
    116: "Ian also takes his leave.",
    128: "Yukihisa formally takes his leave.",
    135: "The storyteller protests, still trying to finish.",
}


def contextual_review():
    review_scope["contextual_review"](False)
    draft = base.load(REVIEW)
    bound = base.load(maria.OUTPUT)
    assert bound["candidate_sha256"] == draft["candidate_sha256"] == base.digest(parent.ROM)
    assert bound["clean_sha256"] == draft["clean_sha256"]
    assert bound["manuscript_sha256"] == base.digest(maria.MANUSCRIPT)
    assert {row["current_reference"]["offset"] for row in draft["records"] if row["change_class"] != "retention"} >= {
        289, 759, 427, 907}
    labelled = base.load(review_scope["established"].CATALOGUE)["source_and_current_default_name_fields"]
    names = {r["actor_ID"]: r["progressive_nameplate"] for r in labelled}
    context = ("The crew explains why Maria has a fearful reputation. Ian recounts both the reward for a victory and "
               "the sentence for desertion. The young listener learns what it cost Maria. A would-be storyteller "
               "tries to retell it and the others slip away.")
    ids = []
    for raw in bound["records"]:
        ident, selector = raw["id"], raw["source_selector"]
        ordinal = int(ident.rsplit("R", 1)[-1])
        revision = raw["decision"] == "prose"
        previous = " ".join(raw["current_English"].split())
        refs, bodies = {}, {}
        for side in ("source", "current"):
            command = bytes.fromhex(raw[f"{side}_command_hex"])
            body = command[5:command.index(0, 6)]
            assert body[0] == selector
            refs[side] = dict(command_offset=raw[f"{side}_command_offset"], offset=raw[f"{side}_offset"],
                exact_body_hex=body[1:].hex(), exact_command_hex=command.hex(), file_path=maria.ARCHIVE,
                block=maria.BLOCK, block_sha256=bound[f"{side}_block_sha256"], archive_sha256=bound[f"{side}_archive_sha256"])
            bodies[side] = body.hex()
        refs["current"]["candidate_sha256"] = draft["candidate_sha256"]
        row = dict(id=ident, route=3, file_path=maria.ARCHIVE, block=maria.BLOCK, source_selector=selector,
            kind="system" if selector == 254 else "progressive", speaker=names.get(selector, "Speakerless panel"),
            context=context, source_meaning=MARIA_MEANING[ordinal], Japanese=raw["source_Japanese"],
            previous_English=previous, english=MARIA_REFINED.get(ordinal, raw["proposed_English"]) if revision else previous,
            protected_phrases=list(MARIA_PHRASES.get(ordinal, ())), source_reference=refs["source"],
            current_reference=refs["current"], source_hex=bodies["source"], current_hex=bodies["current"],
            change_class="prose" if revision else "retention", decision="revision" if revision else "retention",
            localization_note=raw["finding"],
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=not revision))
        assert all(phrase in row["english"] for phrase in row["protected_phrases"])
        if raw["exact_registered_pages"]:
            row["retained_FE_pages"] = raw["exact_registered_pages"]
        draft["records"].append(row)
        ids.append(ident)
    draft["groups"].append(dict(route=3, file_path=maria.ARCHIVE, block=maria.BLOCK, record_ids=ids, context=context,
        source_block_sha256=bound["source_block_sha256"], current_block_sha256=bound["current_block_sha256"]))
    assert len(draft["records"]) == 132 and len(ids) == 26
    draft["counts"] = dict(Counter(row["change_class"] for row in draft["records"]))
    draft["maria_source_binding_sha256"] = base.digest(maria.OUTPUT)
    draft["macro_and_layout_revision_sha256"] = base.digest(Path(__file__))
    base.save(REVIEW, draft)


relocate_source = checked_text(getsource(typed.relocate), {
    'len(clean) == 217 and len(old) == 219': 'len(clean) == 62 and len(old) == 64',
    'for row in receipts if row["record_ids"]) == 9': 'for row in receipts if row["record_ids"]) == len(plans)',
})
relocate_scope = vars(typed).copy()
exec(compile(relocate_source, __file__ + "::Maria-continuation-aware-relocation", "exec"), relocate_scope)


def maria_commands(rows, clean, old, inventory, clean_arm, arm, prior_plans):
    old_commands, _ = inventory(arm, old)
    by_offset = {c["offset"]: c for c in old_commands}
    prepared = []
    plans = {}
    for row in rows:
        references = {}
        for side in ("source", "current"):
            ref = row[f"{side}_reference"]
            references[f"{side}_command_hex"] = ref["exact_command_hex"]
            references[f"{side}_command_offset"] = ref["command_offset"]
        if row["decision"] == "revision":
            plans[row["id"]] = prior_plans[f"3/{row['id']}"]["plan"]
        if pages := row.get("retained_FE_pages"):
            lead, child = pages
            assert lead["header_offset"] == references["current_command_offset"]
            offset = child["header_offset"]
            command = by_offset[offset]["whole_command_hex"]
            assert command[10:].startswith(child["exact_stored_hex"])
            references["current_FE_continuation"] = dict(command_offset=offset, exact_command_hex=command)
        prepared.append(row | references)
    new, commands, _ = relocate_scope["relocate"](clean, old, clean_arm, arm, prepared, plans, {"choice_objects": []})
    return new, commands, plans


stage_source = checked_text(getsource(established.stage), {
    '            if (route, n) == (0, 84):':
        '            if (route, n) == (3, 116):\n'
        '                new, commands, plans = maria_commands(rows, clean, old, inventory, clean_arm, arm, preflight["plans"])\n'
        '            elif (route, n) == (0, 84):',
})
renderer_source = checked_text(template.template.template.template.renderer_source, {
    '1: display.contexts.hodram_context()': '3: current',
    '1: "Hodram"': '3: "Maria"',
    'captain in (0,1)': 'captain in (0,3)',
    '                if route in (0, 1):': '                if route == 0:',
})
compiler_scope = template.compiler_scope | globals()
for source in (stage_source, renderer_source):
    exec(compile(source, __file__ + "::candidate", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        contextual_review()
    elif action == "preflight":
        preflight()
    elif action in ("stage", "native_display"):
        compiler_scope[action]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
