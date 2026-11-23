"""Audit the stored encounters, letter variants, menus, and nameplates."""

from inspect import getsource
from json import dumps
from types import FunctionType

from scripts import stage_hodram_B201_B220_20261122_v2 as stage
from scripts import verify_hodram_B131_B150_20261122 as template
from scripts import verify_hodram_B181_B200_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
INITIAL_PROOF = ROOT / "native_display.json"
PROOF, NAMES = ROOT / "native_display_menu_paths_v2.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
expansion = previous.expansion
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
panels = checked_text(previous.panels, {
    'ident == stage.CHARM_PANEL': 'ident in stage.FE_MACROS',
    'f"{name}: Charm +1!"': 'f"{name}: {stage.FE_MACROS[ident]} +1!"',
    'assert len(panels) == 21 and len(pictures) == 22': 'assert len(panels) == 30 and len(pictures) == 33',
})
verification = checked_text(template.verification, {
    'verify_menu = FunctionType(menus.verify_menu.__code__, menus.verify_menu.__globals__ | {"ROOT": ROOT})':
        'verify_menu = verify_menu_with_block(menus)',
    "len(entries) == 350 and fe_count == 23 and len(style_objects) == 1":
        "len(entries) == 350 and fe_count == 30 and len(style_objects) == 3",
    'assert [m["block"] for m in choices] == [132, 134, 135, 136, 140] and all(m["count"] == 2 for m in choices)':
        'assert [(m["block"], m["count"]) for m in choices] == [(201, 3), (205, 2), (210, 2), (210, 2), (216, 2), (216, 3)]',
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 8':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 22\n    assert all(sorted(i for slots in obj["slot_owner_sets"] for i in slots) == list(range(8)) for obj in style_objects)',
    '"hodram_B131_B150_progressive"': '"hodram_B201_B220_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the approved captain's caption. His response to the prophecy remains humbler than the title he is given in speech.",
        4: "Janus Pasar is the existing short nameplate and the letter's approved signature. A different crew speaker announces the letter.",
        7: "Cristina Erneco is the approved spelling in the earrings, sword and swan exchanges, including her fixed Charm notice.",
        11: "Jam Ludwyan is the short nameplate. Jam Jack Ludwyan is the approved separate signature within his castle letter.",
        12: "Yukihisa Shiraki is the short nameplate. Yukihisa Genjo Shiraki belongs in his signature, and the crew naturally refers to him by his given name.",
        14: "Emilio Ferog is the established speaker. His delight over the axe and his disappointment form the same exchange.",
        15: "Angelo Puccini is the speaker introducing the source Italian interjection. The parrot's echoes use speakerless panels.",
        16: "Gerhard Adernkatz shares Hodram's respect for Rocco and suggests asking at the tavern about Avalon.",
        17: "Al Shin is the established speaker telling Hodram the rumor about the red sword.",
        18: "Charles Rochefort reads or asks to read the books and distinguishes his own scientific interests from navigation.",
        19: "Carlo Sinat is the established caption in the rescue and rope bargain. The stat panels use the shorter given name as in source.",
        21: "Ian Dukov responds to the seller and asks Hodram for advice. His given name fits the decision menu and the stat notice.",
        23: "Manuel Almeida answers the concern Janus expressed about him in the letter. Preserve the named response as his own view.",
        24: "Sera Shahrbaraz remains the speaker assigned to the silent head shake. The action supplies her answer.",
        76: "Mikhail Letzel is the established scholar's caption. His curiosity about the book explains the older man's observation.",
        82: "Shopkeeper fits the source role for the merchant objecting to the disturbance in front of his business.",
        92: "Barkeep is the established tavern role and the form of address Hodram uses to ask about Avalon.",
        105: "Trader fits the merchant selling rope to Hodram. Carlo's familiar address supplies no personal name.",
        124: "Guard fits the role reporting the missing ornament. His deference belongs to his address to the daimyo.",
        130: "Daimyo preserves the specific feudal role. The guard addresses him as my lord.",
        145: "Innkeeper is the shared source occupation for the woman Jam asks about local sights.",
        147: "Guildmaster is the existing caption for the person pursuing the man with the glassmaking book. The shout supplies no individual name.",
        149: "Guildmaster is the source role of the enthusiast asking about Romance of the Three Kingdoms. His favorite commander is established in speech.",
        157: "Sailor fits the generic source role for the man giving away the book in a hurry.",
        169: "Alluring Woman reflects the source role label and fits the flirtatious book offer. Vivienne supplies her own name, and the tavern's reference to a witch remains hearsay.",
        170: "Mysterious Old Man preserves the source older-man role in encounters about unusual gifts or leads. Each exchange supplies its own story.",
        172: "Stranger fits the anonymous man Carlo helps at the port. His questions supply no relationship or occupation.",
        173: "Shady Man fits the anonymous earring seller and matches the approved recurring role.",
    }
''',
})
def verify_menu_with_block(menus):
    original = menus.verify_menu
    body = checked_text(getsource(original), {
        '''f"choice_{command['source_offset']}.png"''':
            '''f"choice_B{rows[0]['block']}_{command['source_offset']}.png"''',
    })
    scope = original.__globals__ | {"ROOT": ROOT}
    exec(compile(body, __file__ + "::menu-preview-path", "exec"), scope)
    return scope["verify_menu"]


def recover_menu_sheets():
    report, staged, draft = map(base.load, (INITIAL_PROOF, stage.PROOF, stage.OUTPUT))
    assert report["candidate_sha256"] == base.digest(stage.ROM)
    assert report["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert staged["manuscript_sha256"] == base.digest(stage.OUTPUT)
    assert all(base.digest(s["path"]) == s["sha256"] for s in report["sheets"] if "choice_230.png" not in s["path"])
    unchanged = [s for s in report["sheets"] if not s["path"].rsplit("\\", 1)[-1].startswith("choice_")]
    image = base.NdsImage.open(stage.ROM)
    ctx = scope["current_runtime"](image)
    library = scope["menus"]
    adapters = library.menu.adapters(ctx.arm)
    check = verify_menu_with_block(library)
    rows = {r["id"]: r for r in draft["records"]}
    groups = {g["block"]: g for g in staged["groups"]}
    for menu in report["menus"]:
        group = groups[menu["block"]]
        original_offset = menu["source_command_offset"]
        command, = (c for c in group["commands"] if c["source_offset"] == original_offset)
        originals = {original_offset: {"offset": original_offset, "whole_command_hex": command["source"]}}
        fresh = check(ctx.arm, originals, command, [rows[i] for i in command["record_ids"]], adapters)
        assert fresh["sheet"]["sha256"] == menu["sheet"]["sha256"]
        expected = {k: v for k, v in menu.items() if k not in ("block", "sheet")} | {"sheet": fresh["sheet"]}
        assert dumps(fresh, sort_keys=True) == dumps(expected, sort_keys=True)
        menu["sheet"] = fresh["sheet"]
    report["sheets"] = unchanged + [m["sheet"] for m in report["menus"]]
    assert len({s["path"] for s in report["sheets"]}) == len(report["sheets"])
    report["menu_path_recovery"] = {"source_report": str(INITIAL_PROOF), "sha256": base.digest(INITIAL_PROOF)}
    base.save(PROOF, report)
    print("Regenerated six uniquely named choice previews with the original proof hashes.")


scope = template.scope | previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::encounters-and-letters", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        if INITIAL_PROOF.exists():
            recover_menu_sheets()
        else:
            scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
