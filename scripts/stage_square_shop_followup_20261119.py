"""Review the Square's retail replies, town conditions and country briefings."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import checkpoint_shared_display_owners_20261119 as shared
from scripts import register_rafael_iberian_aftermath_20261119 as parent
from scripts import stage_square_country_briefings_20261115 as precedent
from scripts.stage_shared_notices_storage_v1 import relocate

base, native = parent.base, parent.native
ARM, CLEAN, COMMON, GATES = precedent.ARM, precedent.CLEAN, precedent.COMMON, precedent.GATES
ROOT = Path("work/square_shop_followup_20261119/research_v1")
ROM = ROOT / "Square_Shop_Followup_RESEARCH_ONLY.nds"
STORED = PROOF = ROOT / "staged.json"
MANUSCRIPT = ROOT / "contextual_review.json"
NUMBERS = (656, 657, 658, *range(682, 709))
PENDING = shared.OUTPUT
PRIOR_COUNTRIES = Path("releases/all_routes_editorial_20261115_square_country_briefings_candidate/verification/registered_review.json")
PRIOR_CONDITIONS = Path("releases/all_routes_editorial_20261115_square_samples_wraps_candidate/verification/registered_review.json")
FACILITY_FIELD = 0x11A8F4

# Both the question tag and the complete directions belong on a single line.
EDITS = {
    657: ("You're a sailor, aren't you? Try the Market for bulk trade.",
          ("You're a sailor, aren't you?", "Try the Market for bulk trade.")),
    683: ("Business? People are collapsing from the epidemic! Are you kidding me?",
          ("People are collapsing", "from the epidemic!", "Are you kidding me?")),
    693: ("Spain's thriving, isn't it? I hear people abroad call it 'the empire where the sun never sets.'",
          ("Spain's thriving, isn't it?", "the sun never sets.")),
    696: ("Istanbul used to be Constantinople, capital of the Byzantine Empire. That's also called Eastern Rome.",
          ("Istanbul used to be Constantinople,", "the Byzantine Empire.", "Eastern Rome.")),
    705: ("About 200 years ago, Yi Seong-gye, the founding king, united Korea.",
          ("About 200 years ago,", "Yi Seong-gye,", "the founding king,")),
}

CONDITIONS = {
    682: ("The shopkeeper says business is the least of their concerns and hopes for peace soon.",
          "The quick dismissal and modest hope sound natural in the more serious local condition."),
    683: ("People are collapsing from an epidemic. The shopkeeper rebukes the player for asking about business.",
          "Preserve the alarm and the angry question. Keep the subject and verb together so the collapse reads without a pause."),
    684: ("The shopkeeper puts food first because people need it to survive.",
          "Both short thoughts are clear, including the immediate concern for survival."),
    685: ("The merchant points to the thriving town and says they cannot stop smiling.",
          "Keep the invitation to look around and the short expression of good humor."),
    686: ("The merchant would rather the player did not ask and says trade is impossible in these conditions.",
          "The rhetorical question gives the complaint a spoken rhythm and leaves the cause to the situation."),
    687: ("The regularly scheduled ship sank, leaving the town in trouble.",
          "Keep the regular run, the fact that it sank, and the separate sentence about the consequences for the town."),
}
NOTES = precedent.NOTES | {key: pair[1] for key, pair in CONDITIONS.items()} | {
    656: "The direct answer keeps the distinction between individual sales here and the larger deals available elsewhere.",
    657: "Keep the friendly tag question on one line. The clean building label is the same 交易所 that the town menu calls Market.",
    693: "The friendly question remains. I hear restores the qualification in the Japanese before the nickname attributed to people abroad.",
    696: "Name the old city and its role as capital together. The second sentence gives the alternate name of the empire.",
    705: "Tie the founding title to the unified kingdom and preserve Yi Seong-gye and the approximate two centuries.",
}
MEANINGS = precedent.MEANING | {key: pair[0] for key, pair in CONDITIONS.items()}


def facility(arm):
    pointer, = unpack_from("<I", arm, FACILITY_FIELD)
    start = pointer - 0x02000000
    return dict(field=FACILITY_FIELD, pointer=pointer, nul_terminated_hex=arm[start:arm.index(0, start)+1].hex())


def main():
    assert not ROOT.exists()
    release, ledger, shared_review = map(base.load, (parent.RELEASE, base.LEDGER, PENDING))
    assert base.digest(CLEAN) == release["clean_input_sha256"] == shared_review["clean_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    runtime = precedent.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(CLEAN)
    ja, arm, common = clean.read_file(ARM), runtime.arm, runtime.common
    assert all(ja[a:b] == arm[a:b] for a, b in precedent.SOURCE_RANGES)
    assert precedent.selectors(ja) == precedent.selectors(arm)
    labels = {side: facility(binary) for side, binary in (("clean", ja), ("registered", arm))}
    assert bytes.fromhex(labels["clean"]["nul_terminated_hex"]).decode("cp932") == "交易所\0"
    assert bytes.fromhex(labels["registered"]["nul_terminated_hex"]) == b"Market\0"

    source = precedent.common_message_entries(clean.read_file(COMMON), ja)
    directory = native.digest(arm[precedent.DIRECTORY_OFFSET:precedent.TABLE_OFFSET])
    previous = precedent.owned_entries(common, arm, directory)
    credited = {(r["file_path"], r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    historical = {x["message_ID"]: x for p in (PRIOR_COUNTRIES, PRIOR_CONDITIONS) for x in base.load(p)["records"]
                  if x["message_ID"] in NUMBERS}
    assert sorted(historical) == list(NUMBERS)
    rows = {}
    for n in NUMBERS:
        ident = f"COMMON_MESSAGE_{n}"
        original, installed, prior = source[n], previous[n], historical[n]
        assert (COMMON, ident) in credited and all(prior["review"].values())
        assert prior["source_hex"] == original.text.hex() and prior["staged_hex"] == installed.text.hex()
        old = " ".join(installed.text.decode("ascii").split())
        english, phrases = EDITS.get(n, (old, ()))
        assert all(b"%" not in value for value in (original.text, installed.text))
        context = ("Alternative country briefing in a Square shop." if n >= 688 else
                   "Alternative reply to asking about business in town." if n >= 682 or n == 658 else
                   "The Square shopkeeper distinguishes their retail goods from bulk trading.")
        rows[n] = dict(id=ident, message_ID=n, file_path=COMMON, speaker="Shopkeeper", context=context,
            source_meaning=MEANINGS[n], localization_note=NOTES[n], previous_English=old,
            clean_Japanese=original.text.decode("cp932"), english=english, protected_phrases=list(phrases),
            finding="wrap" if n in EDITS and english == old else "prose" if n in EDITS else "retention",
            decision="revision" if n in EDITS else "retention",
            source_reference=precedent.reference(original), current_reference=precedent.reference(installed),
            source_hex=original.text.hex(), current_hex=installed.text.hex(),
            original_substitution_count=0, review=dict.fromkeys(GATES, True) | {"formatting": False})

    pack = precedent.compile_layouts
    storage = FunctionType(pack.__code__, pack.__globals__ | {"PHRASES": {n: phrases for n, (_, phrases) in EDITS.items()}})
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    target_common, target_arm, after, allocation = repack(common, arm, rows, storage({n: rows[n] for n in EDITS}))
    assert allocation["changed_visible_templates"] == list(EDITS)
    new_runtime = precedent.with_components(runtime, target_arm, target_common)
    cpu, get, provider = new_runtime.machine(target_arm, target_common, new_runtime.raw, new_runtime.plan)
    painter, _, font = precedent.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    pages = []
    for n, row in rows.items():
        value = after[n].text
        pointer = get(0x5528C, n)
        assert bytes(cpu.mem_read(pointer, len(value)+1)) == value + b"\0"
        native_text, lines = precedent.native_layout(cpu, value, n, ())
        assert 0 < len(lines) <= 4 and all(lines) and " ".join(lines) == row["english"]
        assert all(any(phrase in line for line in lines) for phrase in row["protected_phrases"]), (n, lines, row["protected_phrases"])
        row.update(staged_hex=value.hex(), staged_reference=precedent.reference(after[n]), visible_lines=lines,
                   formatter_parent=0x02054014, native_displays=[])
        if n not in EDITS:
            assert value == previous[n].text
            continue
        old_text, old_lines = precedent.native_layout(cpu, previous[n].text, n, ())
        assert old_lines != lines
        for label, text in (("before", old_text), ("revised", native_text)):
            plane, glyphs = precedent.render_portrait(painter, target_arm, kanji, text)
            assert [g["code"] for g in glyphs] == precedent.glyph_codes(text)
            pages.append((f"{n} {label}", plane))
            if label == "revised":
                row["native_displays"].append(dict(glyph_count=len(glyphs), ink_sha256=native.digest(plane),
                    visible_lines=lines, display_hex=text.hex()))
    assert tuple(rows[657]["visible_lines"]) == EDITS[657][1]
    assert provider.reads and bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    for old in shared_review["records"]:
        current = after[old["message_ID"]]
        assert precedent.reference(current) == old["current_reference"] and current.text.hex() == old["current_hex"]

    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, target_arm)
    image.replace_file(COMMON, target_common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    review = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), candidate_sha256=base.digest(ROM), records=list(rows.values()))
    base.save(MANUSCRIPT, review)
    base.save(PROOF, review | dict(previous_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        target_ARM9_sha256=native.digest(target_arm), target_COMMON_sha256=native.digest(target_common),
        entire_parent_inverse=True, manuscript_sha256=base.digest(MANUSCRIPT), allocation=allocation,
        font=font, facility_caption=labels, sheets=precedent.portrait_sheets(ROOT, pages),
        evidence={str(p):base.digest(p) for p in (PRIOR_COUNTRIES, PRIOR_CONDITIONS, PENDING, parent.RELEASE)}))
    print(f"Reviewed {len(rows)} Square records, with {len(EDITS)} revised native pages.")


if __name__ == "__main__":
    main()
