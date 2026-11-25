"""Classify town nameplates and joined actor names on the registered Deck ROM."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import register_deck_comments_20261119 as current
from scripts import register_square_shop_followup_20261119 as square
from scripts import review_barmaid_town_labels_20261115 as labels
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_barmaid_town_labels_20261115 import paint

base, native = current.base, current.native
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUTPUT = BOOK / "joined_actor_names_20261119_v1.json"
ROOT = Path("work/joined_actor_names_20261119")
PREVIEW = ROOT / "joined_name_review.png"
ROLE_REVIEW = Path("translations/square_shopkeeper_labels_contextual_final_review_v1.json")
BASE, TABLE = labels.BASE, labels.TABLE
GETTERS = {"dialogue": 0x7ED88, "catalogue": 0x7EDD4, "joined_short": 0x7EA48, "joined_full": 0x7EA8C}
SQUARE_ACTORS = {82: "ヨーロッパ男", 83: "ヨーロッパ女"}
HOSTESSES = {195: "Nelly Alexandria", 204: "Verisa Sao Jorge"}
REFERENCES = {
    0x0207EA48: (0x0201F370, 0x0207EDB4, 0x020A2324, 0x020A70A0),
    0x0207EA8C: (0x020151F0, 0x020153D8, 0x0202BC48, 0x02037614, 0x02037D7C, 0x0203D508,
                 0x0203E24C, 0x020539F4, 0x0207EDEC, 0x02080674, 0x0208CF28, 0x0208DE44),
    0x0207EAF4: (),
}


def native_references(image, arm):
    sections = MainCodeFile(arm, BASE).sections
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda _, n: image.rom.files[n])
    branches, pointers = {a: [] for a in REFERENCES}, {a: [] for a in REFERENCES}
    for section in (*sections, *overlays.values()):
        data = section.data
        for offset in range(0, len(data) - 3, 4):
            address = section.ramAddress + offset
            word, = unpack_from("<I", data, offset)
            if word in pointers:
                pointers[word].append(address)
            if word & 0x0E000000 == 0x0A000000 and word >> 28 != 15:
                words = word & 0x00FFFFFF
                signed = words - 0x01000000 if words & 0x00800000 else words
                target = address + 8 + 4 * signed
                if target in branches:
                    branches[target].append(address)
    assert {a: tuple(v) for a, v in branches.items()} == REFERENCES
    assert pointers == {0x0207EA48: [], 0x0207EA8C: [], 0x0207EAF4: [0x02148438]}
    return dict(aligned_arm_branches=branches, aligned_exact_pointers=pointers,
        range="ARM9 SDK sections and decompressed ARM9 overlays",
        title_and_widget_ownership_mapped={0x020151F0: "Deck personnel panel",
            0x020153D8: "Deck room panel", 0x020539F4: "FU current captain substitution",
            0x0207EDB4: "Dialogue getter branch", 0x0207EDEC: "Catalogue getter branch",
            0x02148438: "Actor virtual secondary field getter"})


def lookup_all(runtime, clean_arm):
    cpu, get, provider = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    models = bytes(cpu.mem_read(runtime.actor_root, 0x1A04))
    town_root = get(0xCB178)
    town_models = bytes(cpu.mem_read(town_root, 4 + 90 * 108))
    rows, towns = {}, []
    assert get(0x7F244) == 3
    for n in range(207):
        obj = runtime.actor_root + (0x19E4 if n == 3 else 4 + 32 * n)
        values = {}
        for key, off in GETTERS.items():
            ptr = get(off, obj)
            text = labels.read_text(cpu, ptr)
            values[key] = dict(getter=BASE+off, runtime_result_pointer=ptr, text=text, hex=text.encode("cp932").hex())
        rows[n] = dict(actor_ID=n, actor_object=obj, short_and_joined=values, original_faction=get(0x7E958, obj))
    expected = {82: "Shopkeeper ヨーロッパ男", 83: "Shopkeeper ヨーロッパ女"}
    findings = {n: item["short_and_joined"]["joined_full"]["text"] for n, item in rows.items()
                if not all(o["text"].isascii() for o in item["short_and_joined"].values())}
    assert findings == expected
    for n, secondary in SQUARE_ACTORS.items():
        values = rows[n]["short_and_joined"]
        assert values["dialogue"]["text"] == values["catalogue"]["text"] == "Shopkeeper"
        assert values["joined_short"]["text"] == values["joined_full"]["text"] == expected[n]
        field = TABLE + n * 32 + 4
        primary = labels.read_static(clean_arm, field - 4)
        original = labels.read_static(clean_arm, field)
        installed = labels.read_static(runtime.arm, field)
        assert primary["text"] == "広場の店主" and original == installed and installed["text"] == secondary
        rows[n].update(clean_role=primary, clean_and_current_regional_secondary_field=original,
            disposition="Retain Shopkeeper in the scene header. The joined-name draw needs a reachable UI caller before changing the preserved regional metadata.")
    for n, joined in HOSTESSES.items():
        primary, town = joined.split(" ", 1)
        values = rows[n]["short_and_joined"]
        assert values["dialogue"]["text"] == values["catalogue"]["text"] == primary
        assert values["joined_short"]["text"] == values["joined_full"]["text"] == joined
        assert labels.read_static(runtime.arm, TABLE + n * 32 + 4)["text"] == town
        rows[n].update(clean_town=labels.read_static(clean_arm, TABLE + n * 32 + 4),
            disposition="Keep the reviewed town in the composed name. The ordinary dialogue name is the personal name.")

    for index in range(90):
        town = town_root + 4 + index * 108
        culture = get(0xB51B4, town)
        ident = get(0xB2D28, town, 0)
        actor = get(0xB2CD8, town, 0)
        field = 0x11948C + culture * 14 + 1
        assert ident == runtime.arm[field] == clean_arm[field] and 82 <= ident <= 91
        assert actor == rows[ident]["actor_object"]
        actual_name = labels.read_text(cpu, get(GETTERS["dialogue"], actor))
        assert actual_name == "Shopkeeper"
        towns.append(dict(town_ID=index, culture=culture, actor_ID=ident, actor_field_offset=field,
            original_square_role_selector=0, dialogue_name=actual_name))
    assert bytes(cpu.mem_read(runtime.actor_root, len(models))) == models
    assert bytes(cpu.mem_read(town_root, len(town_models))) == town_models and not provider.reads
    assert all(values["text"].isascii() for n, row in rows.items() for key, values in row["short_and_joined"].items()
        if not (n in SQUARE_ACTORS and key.startswith("joined_")))
    return cpu, rows, towns


def verified_retention():
    role = base.load(ROLE_REVIEW)
    rows = [r for r in role["records"] if r["actor_ID"] in SQUARE_ACTORS]
    assert len(rows) == 2
    assert all(r["source_Japanese"] == "広場の店主" and r["english"] == "Shopkeeper" and all(r["review"].values())
               for r in rows)
    replay = base.load(square.REVIEW)["observed_gameplay"]
    assert replay["candidate_sha256"] == base.digest(square.ROM)
    assert replay["ordinary_input"] and replay["original_shop_choices_replayed"]
    sheets = replay["sheets"]
    assert all(base.digest(s["path"]) == s["sha256"] for s in sheets)
    return rows, dict(candidate_sha256=replay["candidate_sha256"], retained_prior_observation=True,
        prior_build_ordinary_shop_reply_holds=sum(map(len, replay["complete_holds"].values())),
        earlier_replay_sheets=sheets)


def main():
    assert not OUTPUT.exists() and not ROOT.exists()
    release, ledger = map(base.load, (current.RELEASE, base.LEDGER))
    assert base.digest(current.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean = base.NdsImage.open(current.stage.CLEAN)
    assert base.digest(current.stage.CLEAN) == release["clean_input_sha256"]
    ja = clean.read_file(current.stage.ARM)
    runtime = RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    for start, end in ((0x15108, 0x15334), (0x15334, 0x154E8), (0x7EA48, 0x7EB3C),
                       (0x7ED88, 0x7EE08), (0x539EC, 0x539FC)):
        assert ja[start:end] == runtime.arm[start:end]
    references = native_references(runtime.image, runtime.arm)
    assert references == native_references(clean, ja)
    cpu, rows, towns = lookup_all(runtime, ja)
    retained, previous = verified_retention()
    font = GameAsciiFont.from_arm9(runtime.arm)
    guard = bytes(cpu.mem_read(runtime.actor_root, 0x1A04))
    previews, cases = Image.new("RGB", (496, 4 * 62), "#253039"), []
    draw = ImageDraw.Draw(previews)
    for i, (n, name) in enumerate(HOSTESSES.items()):
        for j, spec in enumerate(labels.CALLERS):
            img, receipt = paint(cpu, font, rows[n]["actor_object"], name, spec, True)
            y = (i * 2 + j) * 62
            draw.text((8, y + 4), f"{n}   {name}   {spec[-1]} cells", fill="white")
            line = img.crop((0, 24, img.width, 36)).point(lambda p: 25 if p else 245)
            previews.paste(line.resize((line.width * 2, 24), Image.Resampling.NEAREST), (8, y + 24))
            cases.append(receipt | {"actor": n})
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == guard
    ROOT.mkdir(parents=True)
    previews.save(PREVIEW)
    base.save(OUTPUT, dict(format="dk4-joined-actor-name-scope-v1", runtime=runtime.receipt(),
        candidate_sha256=release["candidate_sha256"], original_lookup_cases=len(rows)*len(GETTERS),
        original_town_square_selector_cases=towns, actor_output_inventory=list(rows.values()), caller_references=references,
        observed_previous_square_replay=previous, individual_square_nameplate_retentions=retained,
        earlier_wrongly_assumed_retention_outside_scope=False,
        joined_hostess_native_panels=cases, visual_sheet=str(PREVIEW), visual_sheet_sha256=base.digest(PREVIEW),
        joined_shopkeeper_reachable_display_established=False, original_RAM_actor_and_town_records_exact=True,
        native_execution_only=True, new_gameplay_runs=0, new_editorial_credit=0, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in (ROLE_REVIEW, square.REVIEW, current.RELEASE, Path(__file__))}))
    print("Verified 828 original actor getters, 90 Square selectors and four complete composed-name glyph planes.")


if __name__ == "__main__":
    main()
