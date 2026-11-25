"""Observe the docked Ceuta Square and verify ordinary town dialogue holds."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import observe_ceuta_and_lisbon_20261122 as visits
from scripts import verify_tripoli_copenhagen_20261122 as prior


stage, ROOT = visits.stage, visits.ROOT
base, native = stage.base, stage.native
check, masks, town, visual = prior.check, prior.masks, prior.town, prior.visual
OUTPUT = ROOT / "verified_visits.json"
LABELS = {
    51: ("Barkeep", "The greeting invites the party to order and leads into the drink menu."),
    656: ("Shopkeeper", "The short answer distinguishes the shop's retail sales from bulk trade."),
    657: ("Shopkeeper", "The sailor tag and the direction to use the Market are easy to follow."),
    658: ("Shopkeeper", "The shopkeeper sounds open to a purchase without promising a deal."),
}


def ceuta_square_schedule(case):
    assert case == "ceuta_square"
    former, _, _, history, donor = visits.schedule("ceuta")
    events = [row for row in former if row["start"] <= 2801]
    for frame, action in visits.prior.precedent.VISITS:
        controls = dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action])
        events.append(dict(start=frame, duration=8, **controls))
    return events, [3720, *(frame + 149 for frame, _ in visits.prior.precedent.VISITS)], 11700, history, donor


def observe_ceuta_square():
    precedent = visits.prior
    scope = vars(precedent.playback) | dict(ROOT=ROOT, parent=SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF),
        observer=precedent.precedent.scoped_observer, get_schedule=ceuta_square_schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(precedent.playback.main), __file__ + "::ordinary-docked-ceuta", "exec"), scope)
    scope["main"]("ceuta_square")


def verify():
    assert not OUTPUT.exists()
    parent, proof = map(base.load, (stage.parent.RELEASE, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and parent["candidate_sha256"] == proof["predecessor_sha256"]
    assert base.digest(native.CLEAN) == parent["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (native.CLEAN, stage.ROM))
    arm, common = (rom.read_file(path) for path in (town.ARM, town.COMMON))
    assert native.digest(arm) == parent["target_ARM9_sha256"] and native.digest(common) == parent["target_COMMON_sha256"]
    source = check.common_message_entries(clean.read_file(town.COMMON), clean.read_file(town.ARM))
    installed = check.owned_entries(common, arm, check.sha256(arm[check.DIRECTORY_OFFSET:check.TABLE_OFFSET]).hexdigest())
    ctx = town.RegisteredRuntime(stage.parent.RELEASE, parent["own_registered_startup"], captain=3)
    assert ctx.image.read_file(town.ARM) == arm and ctx.common == common
    cpu, _, _ = ctx.machine(arm, common, ctx.raw, ctx.plan)
    font = check.GameAsciiFont.from_arm9(arm)
    renderer, _, _ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    captures = FunctionType(prior.captures.__code__, prior.captures.__globals__ | dict(ROOT=ROOT))
    results, sheets, all_evidence = {}, [], {}
    for case, caption, schedule in (("ceuta_square", "Ceuta", ceuta_square_schedule), ("lisbon", "Lisbon", visits.schedule)):
        report, requests, evidence = captures(case, schedule, candidate)
        frames = check.shots(report)
        entry = frames[3720]
        pictures = [(f"{caption} / town entry", check.captured(entry).convert("RGB"))]
        evidence[entry["path"]] = entry["PNG_sha256"]
        observations = []
        target = [row for row in requests if row["frame"] > 3720 and row["message_ID"] in LABELS]
        for direct, copied in zip(target[::2], target[1::2], strict=True):
            assert (direct["PC"], copied["PC"]) == (0x0205528C, 0x020534F4)
            assert dict(direct, PC=copied["PC"]) == copied
            key = direct["message_ID"]
            frame = min(n for n in frames if 0 < n-direct["frame"] <= 160)
            captured = frames[frame]
            image = check.captured(captured).convert("RGB")
            jp, en = source[key], installed[key]
            assert b"%" not in jp.text and b"%" not in en.text
            body, lines = town.native_layout(cpu, en.text, key, ())
            assert 1 <= len(lines) <= 4 and " ".join(lines) == " ".join(en.text.decode("ascii").split())
            pixels, codes = town.render_portrait(renderer, arm, kanji, body)
            assert [item["code"] for item in codes] == town.glyph_codes(body)
            assert masks.mask_check(bytes(pixels), 228, image), (case, key, frame)
            who, reason = LABELS[key]
            ink, bounds = check.complete_mask(font, who, image, 16, 277, (98, 97, 98))
            evidence[captured["path"]] = captured["PNG_sha256"]
            observations.append(dict(message_ID=key, capture=captured, original_requests=(direct, copied),
                source_reference=check.reference(jp), current_reference=check.reference(en),
                Japanese=jp.text.decode("cp932"), English=en.text.decode("ascii"), decision="retention",
                localization_note=reason, review=dict.fromkeys(town.GATES, True), new_editorial_credit=0,
                complete_body=dict(lines=lines, full_plane_sha256=check.sha256(bytes(pixels)).hexdigest()),
                nameplate=dict(text=who, pixels=ink, bounds=bounds)))
            pictures.append((f"{caption} / {who} / COMMON {key}", image))
        assert observations
        for index in range(0, len(pictures), 6):
            path, digest = visual.make_sheet(ROOT / f"{case}_ordinary_{1+index//6}.png", pictures[index:index+6])
            sheets.append(dict(path=path, sha256=digest))
        results[caption] = dict(panels=observations, entry=entry,
            unreviewed_message_ids=sorted({r["message_ID"] for r in requests if r["message_ID"] not in LABELS}),
            donor_sha256=report["battery_save_preloaded"]["source_sha256"])
        all_evidence.update(evidence)
    assert all(base.digest(path) == digest for path, digest in all_evidence.items())
    base.save(OUTPUT, dict(candidate_sha256=candidate, visits=results, evidence=all_evidence, sheets=sheets,
        ordinary_saved_gameplay=True, original_controller_and_touch=True, hardware=False, new_editorial_credit=0))
    print({name: [row["message_ID"] for row in data["panels"]] for name, data in results.items()}, flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("capture_ceuta", "verify"))
    action = cli.parse_args().action
    (observe_ceuta_square if action == "capture_ceuta" else verify)()
