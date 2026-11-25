"""Review the observed Online cards and bind the full promotional manuscript."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_online_title_routing_20261115 as routing
from scripts import observe_online_gallery_slides_20261123 as live
from scripts.reconcile_chooser_and_online_dispositions_20261123 import OUT as CHOOSER, PROMOTIONAL
from scripts.reconcile_gallery_caption_dispositions_20261123 import WORKLIST, picture
from scripts.reconcile_legacy_save_dispositions_20261123 import OUT as SAVE
from scripts.seal_shared_text_source_v1 import reference


base, current, native = live.base, live.current, live.current.native
OUT = WORKLIST.with_name("promotional_display_paths_20261123.json")
SHEET = OUT.with_suffix(".png")
RESOURCES = Path("work/analysis/online_resource_pages_v189.json")
CARD_REVIEW = {
    50: ("The urgent invitation to take command and sail into the online world fits the overview's opening frame.", None),
    51: ("The two ways to play and the emphasis on the stories they create match the separate character-drama card.", None),
    52: ("The ports and goods, pirate hunting, and even becoming a wanted outlaw preserve the range of choices.", None),
    53: ("The card invites the reader to open up new waters and promises thrills. The heading carries the royal order.", None),
    54: ("The card says about 50 careers, with experience before a change. That is distinct from the full copy's 50 or more.", None),
    55: ("The heading identifies the adventure career family. The call to uncover ruins and treasures keeps the concrete examples.", None),
    56: ("The card connects trade with market prices and ends with a separate invitation to open a bazaar when you find rarities.", None),
    57: ("Escort, cannon fire, boarding and forming your own pirate fleet give the combat panel its specific pitch.", None),
    58: ("The encounters and the nation-dependent stories preserve the two parts of the source card.", None),
    59: ("The possible vote and the attack target remain explicit. The conditional keeps the outcome uncertain.", None),
    60: ("Forming a fleet with people you meet leads naturally into combining skills and fighting pirates.", None),
    61: ("The visible wording drops the different ship types and the ability to change the number of sails.",
         "Ships come in many types and sizes. Choose the materials, weapons, number of sails, and emblems to make one your own!"),
    62: ("The Japanese names the Leaning Tower of Pisa. The current sentence names the city and loses the landmark.",
         "Explore 3D ruins and cities. From the pyramids to the Leaning Tower of Pisa, a whole world of adventure awaits!"),
}
DISTINCTIONS = {
    3290: "The short card invites you to take command and sail online. The full copy also describes forming fleets, ancient arts, and battles with pirates.",
    3292: "The card promotes cooperation or playing alone. The full introduction names the Age of Discovery, the early 1500s in Europe, and the three player roles.",
    3294: "This second body under the drama heading explains choosing a nation, with Lisbon, Seville, and London as examples.",
    3295: "The stored heading describes freedom in how you live. The guide's separate heading and card frame that idea as play choices.",
    3296: "The short card mentions ports, goods, pirates, and becoming wanted. The full progression adds seamanship, better ships, guild work, and investment.",
    3297: "The full heading links the king's orders to further adventures. The guide phrases the royal-orders invitation separately.",
    3298: "The guide summarizes new waters and their thrills. The full body specifies rare clothing and goods, inland treasure, storms, and privateering.",
    3299: "The stored heading invites the reader to live freely as a sailor on the world's seas. The guide has a separate shorter heading.",
    3300: "The card says about 50 professions. The long copy says 50 or more and names the three career families, guilds, and effects on skill growth.",
    3301: "The stored invitation links a voyage across vast seas to making your name as an explorer. The guide heading abbreviates it.",
    3302: "The card invites exploration of ruins and treasures. The manuscript also describes unfamiliar life, natural wonders and discoveries made together in 3D.",
    3303: "The stored trade heading pairs enjoyment with making money. The independent guide uses a shorter market pitch.",
    3304: "The card describes hundreds of goods, market influence, and opening a bazaar. The full body discusses investment, alliances, favorable terms, and local specialties.",
    3306: "The card covers naval combat, escorts and becoming pirates. The full body also frames piracy outside towns and gaining renown from fighting it.",
    3307: "The stored heading emphasizes how much the story changes with your nation. The guide heading expresses the same relationship with its own wording.",
    3308: "The card keeps encounters and stories by nation. The long body starts in Europe and ties guild work and discoveries to fame and royal permission to sail farther.",
    3309: "The longer heading ties a continuously changing world to variety in adventure. The guide has a shorter invitation.",
    3310: "The card uses a player's vote in a naval battle as its example. The full copy uses royal orders over allied ports and changing trade prices.",
    3311: "The stored heading invites the reader to depart with people met in towns. The guide caption and fleet card use shorter wording.",
    3312: "Both teach fleet formation and cooperation. The full body adds guild assignments, asking around in towns, named skills, sunsets, and tavern conversation.",
    3313: "The stored heading specifies the open seas and sailing your own ship. The guide uses a separate shorter headline.",
    3314: "The card discusses the ship alone. The full manuscript also gives character build, hairstyles, period clothes, hats, and hundreds of items.",
    3315: "The stored heading emphasizes fidelity to the historical world. The guide expresses the idea as a short invitation to explore.",
    3316: "The card gives the pyramids and Leaning Tower as examples of 3D places. The manuscript adds the Parthenon, changing seas, inland routes, the Nile and excavation.",
    3317: "The standalone tie-in heading introduces the archived outline. In the verified DS sequence the introduction explains the tie-in in prose.",
    3318: "The archived introduction names the Windows edition. The current introductory screen calls it a PC title and describes the tie-in in its own words.",
    3319: "The manuscript specifies joining the Windows game and completing a quest. The separate DS instructions tell players to get the village name and Promised Words from a character, then enter them in Rota Nova.",
}


def nation_schedule(case):
    assert case == "nation"
    original, _, _, source, donor = live.schedule("online")
    events = original[:6] + [dict(start=t, duration=8, buttons=[b])
        for t, b in ((2100, "DOWN"), (2300, "DOWN"), (2500, "A"), (3300, "B"))]
    return events, [2690, 2840, 2890, 2940, 3000, 3060, 3120, 3180], 3550, source, donor


def capture_nation():
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    driver = live.driver
    scope = vars(driver) | dict(ROOT=live.ROOT, parent=current, FOCUS=set(range(3668)),
        get_schedule=nation_schedule, __file__=__file__)
    FunctionType(driver.main.__code__, scope)("nation")


def checked_capture(release, case):
    root = live.ROOT / case
    receipt, trace, capture = (root / p for p in ("terminal.json", "requests.json", "capture/capture_report.json"))
    terminal, requests, report = map(base.load, (receipt, trace, capture))
    schedule, frames, end, _, donor = (live.schedule if case == "online" else nation_schedule)(case)
    assert not donor and not report.get("battery_save_preloaded")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["scripted_input_schedule"] == schedule and report["exact_requested_capture_frames"] == frames
    assert all(base.digest(p) == digest for p, digest in terminal["evidence"].items())
    assert requests["all_host_slots_restored_and_core_file_exact"] and not requests["mismatches"] and not requests["errors"]
    assert not requests["source_requests"] and terminal["COMMON_requests"] == 0
    assert len(requests["rows"]) == len(terminal["caption_calls"]) == {"online": 13, "nation": 1}[case]
    shots = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    assert set(frames) <= shots.keys()
    return shots, terminal["evidence"] | {str(receipt): base.digest(receipt)}


def native_scope(ja, en, previous):
    for lock in previous["parent_native_span_locks"]:
        lo, hi = lock["start"], lock["end"]
        assert ja[lo:hi] == en[lo:hi] and native.digest(en[lo:hi]) == lock["sha256"]
    originals = [routing.route_cases(data) for data in (ja, en)]
    assert originals == [previous["clean_routing"], previous["current_routing"]]
    return dict(checked_ROMs=["clean", "installed"], category_selection_cases_per_ROM=6,
        native_guide_text_draws_per_ROM=13, guide_steps_per_ROM=26,
        native_extras_text_draws_per_ROM=6, native_extras_exit_cases_per_ROM=1,
        COMMON_requests_at_scanned_entrypoints=0, exact_bound_routing_receipt=str(routing.OUTPUT))


def rgb5(image):
    return image.convert("RGB").point(lambda channel: channel >> 3)


def art_ink(art, screenshot):
    assert (art.width, art.height) == (256, 192)
    assert set(art.indices) == {0, 1, 15}
    screen = rgb5(screenshot.crop((0, 192, 256, 384))).load()
    palette = [tuple(channel >> 3 for channel in entry[:3]) for entry in art.palette]
    points = [(i % 256, i // 256) for i, index in enumerate(art.indices) if index]
    assert all(screen[x, y] == palette[art.indices[y * 256 + x]] for x, y in points)
    xs, ys = zip(*points, strict=True)
    bounds = [min(xs), min(ys) + 192, max(xs) + 1, max(ys) + 193]
    assert 0 < bounds[0] < bounds[2] < 256 and 228 < bounds[1] < bounds[3] < 359
    return dict(complete_opaque_ink_and_outline_pixels=len(points), bounds=bounds)


def resource_owner(owner, ja, en):
    at = owner["filename_pointer"] - routing.BASE
    name = owner["path"][1:].encode("ascii") + b"\0"
    assert ja[at:at + len(name)] == en[at:at + len(name)] == name
    return owner["path"]


def classify_cards(clean, rom, ja, en, prior, shots, nation):
    inventory = base.load(RESOURCES)
    for lock in inventory["code_ranges"]:
        lo, hi = lock["start_offset"], lock["end_exclusive"]
        assert ja[lo:hi] == en[lo:hi] and native.digest(en[lo:hi]) == lock["sha256"]
    cards, anchors = {}, []
    for n, (page, row, hold, count) in enumerate(zip(inventory["pages"], prior["online_pages"],
            live.FIRST_HOLDS, live.SLIDE_COUNTS, strict=True), 50):
        desc, at = page["descriptor_offset"], page["page_data_offset"]
        assert ja[desc:desc + 12] == en[desc:desc + 12]
        assert ja[at:at + 16] == en[at:at + 16]
        _, image_table, art_owner, size = unpack_from("<4I", en, at)
        assert count == size == page["image_count"]
        assert art_owner == page["caption_art"]["owner_address"]
        start, stop = image_table - routing.BASE, image_table - routing.BASE + 4 * size
        assert ja[start:stop] == en[start:stop] == bytes().join(
            im["owner_address"].to_bytes(4, "little") for im in page["screenshots"])
        path = resource_owner(page["caption_art"], ja, en)
        assert path == f"/_pxl/online/Online{n}.pxl"
        source, current_asset = (im.read_file(path) for im in (clean, rom))
        art = PxlImage.from_bytes(current_asset)
        manuscript = Path(f"translations/extras_online{n}_graphics_v1.json")
        proof = base.load(manuscript)
        assert proof["file_path"] == path and proof["source_file_sha256"] == native.digest(source)
        asset_table = {}
        for owner in page["screenshots"]:
            filename = resource_owner(owner, ja, en)
            payload = rom.read_file(filename)
            pixels = rgb5(PxlImage.from_bytes(payload).render()).tobytes()
            asset_table[pixels] = dict(path=filename, installed_sha256=native.digest(payload))
        observed = {}
        native_ink = []
        holds = [shots[f] for f in sorted(shots) if hold <= f <= hold + 185 * count]
        if n == 58:
            holds.extend(nation[frame] for frame in nation_schedule("nation")[1])
        for capture in holds:
            frame = capture["frame"]
            image = picture(capture)
            pixels = rgb5(image.crop((0, 0, 256, 192))).tobytes()
            if pixels not in asset_table:
                continue
            matched = asset_table[pixels]
            observed.setdefault(matched["path"], matched | dict(exact_upper_RGB5_pixels=49152, screenshot=capture))
            native_ink.append(art_ink(art, image) | dict(frame=frame, captured= capture["path"]))
        assert len(observed) == count, (n, count, sorted(observed))
        assert picture(shots[hold]).tobytes() == picture(row["screenshot"]).tobytes()
        anchors.append((n, picture(shots[hold]), PxlImage.from_bytes(source).render()))
        note, draft = CARD_REVIEW[n]
        cards[row["id"]] = dict(card_path=path, clean_sha256=native.digest(source), installed_sha256=native.digest(current_asset),
            manuscript=str(manuscript), manuscript_sha256=base.digest(manuscript),
            caption_review=row, original_page_descriptor_offset=at,
            current_card_English=proof["records"][0]["text"], individual_source_finding=note,
            working_English_revision=draft, decision="draft revision pending integration" if draft else "retain registered English",
            original_slides_and_current_holds=list(observed.values()), exact_ink_checks=native_ink)
    assert sum(len(r["original_slides_and_current_holds"]) for r in cards.values()) == 23
    return cards, anchors


def main():
    release, old, pending, inventory = map(base.load, (current.RELEASE, CHOOSER, SAVE, WORKLIST))
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"] == old["candidate_sha256"] == pending["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == inventory["clean_sha256"]
    clean, rom = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (i.read_file(current.ARM) for i in (clean, rom))
    assert native.digest(en) == release["target_ARM9_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    current_common = rom.read_file(current.COMMON)
    assert native.digest(current_common) == release["target_COMMON_sha256"]
    installed = owned_entries(current_common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    records = {r["message_ID"]: r for r in base.load(PROMOTIONAL)["records"]}
    worklist = {r["message_ID"]: r for r in inventory["records"]}
    shots, capture_evidence = checked_capture(release, "online")
    nation, nation_evidence = checked_capture(release, "nation")
    offline = native_scope(ja, en, base.load(routing.OUTPUT))
    cards, anchors = classify_cards(clean, rom, ja, en, old, shots, nation)
    extras = {r["id"]: r for r in old["about_extras_pages"]}
    for row in extras.values():
        picture(row["screenshot"])
        assert all(row["review"].values())
        assert old["COMMON_lookups_by_run"]["tie_in_advance"] == 0
    decisions = []
    for item in old["evidenced_related_but_distinct"]:
        key = item["message_ID"]
        jp, stored, draft, prior = source[key], installed[key], records[key], worklist[key]
        assert reference(jp) == item["source_reference"] == prior["source_reference"]
        assert reference(stored) == item["installed_reference"] == prior["installed_reference"]
        assert jp.text.hex() == stored.text.hex() == item["source_hex"] == draft["clean_hex"]
        assert draft["english"] == item["source_draft"]["english"]
        owners = item["related_displayed_owners"]
        assert all(o in cards or o in extras for o in owners)
        decisions.append(item | dict(draft_source_review=draft["review"],
            full_copy_distinction=DISTINCTIONS[key], verified_title_path="Independent guide card or About Extras panel.",
            exact_archived_copy_requested_by_these_title_paths=False, other_direct_consumer_unverified=True))
    focused = {r["message_ID"] for r in decisions}
    before = set(pending["remaining_needing_distinct_disposition"])
    assert len(focused) == 27 and focused == DISTINCTIONS.keys() and focused <= before
    sheet = Image.new("RGB", (768, 5 * 194), "#1f2830")
    draw = ImageDraw.Draw(sheet)
    for i, (n, shot, source_card) in enumerate(anchors):
        x, y = i % 3 * 256, i // 3 * 194
        draw.text((x + 4, y + 2), f"Online {n} / Japanese source and emulator", fill="white")
        sheet.paste(source_card.crop((0, 52, 256, 138)), (x, y + 17))
        sheet.paste(shot.crop((0, 238, 256, 328)), (x, y + 103))
    sheet.save(SHEET)
    base.save(OUT, dict(candidate_sha256=candidate, promotion_records=decisions, online_cards=cards,
        offline_title_router=offline, earlier_about_extras_live_holds=extras, new_observed_online_slides=23,
        verified_online_and_extras_COMMON_requests=0, other_direct_common_consumers_unverified=True,
        reviewed_title_content_scope=sorted(focused), remaining_outside_checked_title_content=sorted(before - focused),
        new_dialogue_credit=0, new_ROM=False, hardware=False,
        display_sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence=capture_evidence | nation_evidence | {str(p): base.digest(p) for p in (RESOURCES, CHOOSER, SAVE, WORKLIST,
            routing.OUTPUT, PROMOTIONAL, current.RELEASE, Path(__file__))}))
    print("Verified 23 original slides and all 13 raster cards, including two wording revisions for later integration.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--capture-nation", action="store_true")
    (capture_nation if cli.parse_args().capture_nation else main)()
