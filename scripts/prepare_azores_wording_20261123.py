"""Bind the Azores wording revisions to the observed source and native consumers."""

import json
from hashlib import sha256
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.observe_lisbon_azores_voyage_20261123 import RELEASE
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, COMMON, OUT, digest, read, reference
from scripts.verify_lisbon_azores_voyage_20261123 import REPORT, load_exact, text_at, town
from scripts.verify_personal_gameplay_v841 import get_machine


OUTPUT = OUT.with_name("azores_wording_source_review_20261123.json")
DOCK = {
    65: ("Dock at %s?", "The short question states the requested action and names the stop."),
    66: ("Dock at %s?", "The brief phrasing suits the casual, direct question."),
    67: ("Shall we dock at %s?", "The invitation preserves the speaker's collaborative tone."),
    68: ("Shall we put in at %s?", "The nautical expression preserves this older voice."),
    69: ("Want to dock at %s?", "The informal question preserves the speaker's voice and names the action directly."),
    70: ("Shall we stop at %s?", "The measured question preserves Manuel's courtesy and asks whether to make this port call."),
    297: ("Discovered %s.", "The brief system notice states the discovery and the original place name."),
}
NAME_CALLS = ((0x7877C, 0x78788, 0x78794, 0x78798), (0x78944, 0x78958, 0x78968, 0x7896C))


def village_names(arm, raw):
    cpu, get = get_machine(arm, raw)
    villages, towns = get(0xCB118), get(0xCB178)
    names = []
    for index in range(24):
        obj = get(0xCACAC, villages, index)
        vt, = unpack_from("<I", raw, obj - BASE)
        assert vt == 0x0215AF74
        getter, = unpack_from("<I", raw, vt + 8 - BASE)
        assert getter == 0x020CAD98
        pointer = get(getter - BASE, obj)
        names.append(dict(index=index, native_getter=getter, name_address=pointer, English=text_at(raw, pointer).decode("ascii")))
    obj = towns + 4 + 103 * 108
    vt, = unpack_from("<I", raw, obj - BASE)
    getter, = unpack_from("<I", raw, vt + 8 - BASE)
    town_name = get(getter - BASE, obj)
    assert cpu.mem_read(BASE, len(raw)) == raw
    assert names[13]["English"] == "Azores" and names[13]["name_address"] == 0x0215AE30
    assert town_name == 0x0215D040 and text_at(raw, town_name) == b"Azores"
    return names, town_name


def main():
    assert not OUTPUT.exists()
    release, observed = read(RELEASE), read(REPORT)
    assert digest(release["candidate"]) == release["candidate_sha256"] == observed["candidate_sha256"]
    assert digest("work/clean.nds") == release["clean_input_sha256"]
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    clean, installed = map(NdsImage.open, ("work/clean.nds", release["candidate"]))
    source, arm = (rom.read_file(ARM) for rom in (clean, installed))
    clean_rows = common_message_entries(clean.read_file(COMMON), source)
    current = owned_entries(installed.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    evidence = {row["key"]: row for row in observed["records"]}
    raw = load_exact(evidence[70]["snapshot"])
    names, town_name = village_names(arm, raw)
    owners = []
    for start, name_call, print_call, end in NAME_CALLS:
        assert source[start:end] == arm[start:end] and unpack_from("<I", arm, name_call)[0] == 0xE12FFF31
        owners.append(dict(span=[start, end], native_getter_call=name_call + BASE, body_formatter_call=print_call + BASE,
                           exact_clean_and_current_code_hex=arm[start:end].hex()))
    assert arm[0x15AE30:0x15AE3A] == b"Azores\0\0Na"
    assert arm[0x15D040:0x15D046] == b"Azores"
    assert len(b"the Azores\0") > 8
    gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    records = []
    for key, (english, note) in DOCK.items():
        jp, old = clean_rows[key], current[key]
        assert jp.text.count(b"%s") == old.text.count(b"%s") == english.count("%s") == 1
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON,
            speaker="Discovery notice" if key == 297 else "Original docking voice table",
            context="The discovery notice names the new location before the docking question. The original name substitution provides the selected place.",
            source_meaning="The selected place has been discovered." if key == 297 else "Ask whether to make a port call at the selected place.",
            source_Japanese=jp.text.decode("cp932"), source_hex=jp.text.hex(), source_reference=town.reference(jp),
            installed_text=old.text.decode("ascii"), installed_reference=town.reference(old), installed_hex=old.text.hex(),
            english=english, example_Azores=english % "the Azores", localization_note=note, review=gates.copy(),
            decision="revise template" if key in (69, 70) else "retain template with reviewed place-name substitution"))
    previous = evidence[0x78C48]
    old = bytes.fromhex(previous["installed_hex"])
    assert previous["source_Japanese"].startswith("提督、") and old.startswith(b"Captain,")
    rank = "Admiral, the village chief asks to hear the promised words."
    revised = old.replace(b"Captain,", b"Admiral,", 1)
    assert len(revised) == len(old) and revised.decode("ascii").split() == rank.split()
    code = MainCodeFile(arm, BASE)
    stage_section = bytes(code.sections[3].data)
    pool_offset = stage_section.index(old + b"\0")
    assert stage_section.find(old + b"\0", pool_offset + 1) == -1
    offset = arm.index(old + b"\0")
    assert offset == 0x173430 and old == text_at(load_exact(previous["snapshot"]), previous["installed_reference"]["text_address"])
    records.append(dict(id="ARM9_PROMISED_WORDS_CHIEF_REQUEST", file_path=ARM, speaker="Manuel Almeida in the observed visit",
        context="After docking, the officer reports the chief's request. The next prompt opens the words editor.",
        source_meaning="Admiral, the village chief asks to hear the promised words.",
        source_Japanese=previous["source_Japanese"], source_hex=previous["source_hex"], source_reference=previous["source_reference"],
        installed_text=old.decode("ascii"), installed_reference=previous["installed_reference"] | dict(ARM9_file_offset=offset, pool_offset=pool_offset),
        installed_hex=old.hex(), english=rank, localization_note="Admiral restores the same source address heard from the lookout at the start of this visit.",
        review=gates.copy(), decision="revise title", stored_length_and_line_break_positions_identical=True))

    result = dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", review_gates=list(gates), records=records,
        village_names=names, separate_Azores_town_name_address=town_name,
        only_proposed_sentence_argument_override=dict(current="Azores", proposed="the Azores", village_index=13, native_paths=owners),
        fixed_rank_repair_fits_existing_slot=True, original_and_registered_context=reference(REPORT),
        formatting_and_registered_installation_pending=True, new_editorial_credit=0)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Bound six docking voices, discovery and the chief request to their exact source and installed records.")


if __name__ == "__main__":
    main()
