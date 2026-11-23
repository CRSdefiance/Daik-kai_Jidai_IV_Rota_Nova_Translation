"""Play both complete scenes with their original commands in an initialized Lil run."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType
from PIL import Image, ImageChops, ImageDraw

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import replay_hamburg_ceramics_cross_route_20261120 as precedent
from scripts import stage_seville_stockholm_trends_20261121 as build
from scripts import verify_seville_stockholm_trends_20261121 as offline
from scripts.replay_lil_ceramics_wrap_20261111 import body_masks, masks, photos
from scripts.source_locked_derivation_v5118 import checked_text


base, native = build.base, build.native
ROOT = build.ROOT / "emulator"
CASES = {"seville": (176, 10), "stockholm": (185, 8)}
ARCHIVE = "/data/SC2.DK4"
LIVE = ROOT / "gameplay.json"
SHEET = ROOT / "comparison.png"
REPLAY_SUFFIX = "-retry"


def prepare():
    assert not ROOT.exists()
    staged, release = map(base.load, (build.PROOF, build.parent.RELEASE))
    assert base.digest(build.ROM) == staged["candidate_sha256"]
    assert base.digest(build.parent.ROM) == release["candidate_sha256"] == staged["predecessor_sha256"]
    precedent_setup = base.load(precedent.SETUP)
    historical = Path(precedent_setup["source_scene_scope"])
    assert historical.is_file()
    reference = base.load("work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json")
    original = next(row for row in reference["fixtures"] if row["case"] == "static_target")
    prelude = bytes.fromhex(original["original_B22_prelude_hex"])
    original_inputs = base.load(precedent.prior.INPUTS)
    inventory, _, _ = native.scoped_inventory()
    for name, (index, panel_count) in CASES.items():
        folder = ROOT / name
        folder.mkdir(parents=True)
        versions = {}
        for side, rom in (("before", build.parent.ROM), ("after", build.ROM)):
            image = base.NdsImage.open(rom)
            arm = image.read_file(native.ARM)
            bank = native.IlnkContainer.parse(image.read_file(ARCHIVE))
            entry, scene = bank.blocks[22], bank.blocks[index]
            assert entry[8:56] == prelude
            complete, _ = inventory(arm, scene)
            end = 8 + unpack_from("<H", scene, 4)[0]
            logical = bytearray(entry[:8] + prelude + scene[8:end])
            pack_into("<H", logical, 4, len(logical) - 8)
            fixture = bytes(logical) + bytes(-len(logical) % 4)
            inserted, _ = inventory(arm, fixture)
            for a, b in zip(complete, inserted[9:], strict=True):
                assert a["whole_command_hex"] == b["whole_command_hex"]
                assert a["offset"] + len(prelude) == b["offset"]
            assert sum(c["word"] == 0x4000 for c in complete) == panel_count
            bank.blocks[22] = fixture
            image.replace_file(ARCHIVE, bank.to_bytes())
            target = folder / f"{side}_Lil_Entry_RESEARCH_ONLY.nds"
            image.save(target)
            bank.blocks[22] = entry
            image.replace_file(ARCHIVE, bank.to_bytes())
            assert bytes(image.rom.save()) == rom.read_bytes()
            versions[side] = dict(path=str(target), sha256=base.digest(target),
                                  underlying_ROM_sha256=base.digest(rom))
        frames = [3070 + 240 * i for i in range(panel_count)]
        return_holds = [frames[-1] + step for step in (120, 360, 610)]
        end = return_holds[-1] + 80
        base.save(folder / "fixture_receipt.json", dict(fixture_ROMs=versions, original_block=index,
                  representative_frames=frames, scene_edges=[2100, *return_holds], end=end))
        base.save(folder / "inputs.json", original_inputs +
                  [dict(start=f, duration=5, buttons=["A"]) for f in range(2600, end, 240)])

    patch, rebuilt = build.ROOT / "translation.xdelta", build.ROOT / "clean_rebuilt.nds"
    make_xdelta(native.CLEAN, build.ROM, patch)
    apply_xdelta(native.CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == build.ROM.read_bytes()


def capture(name, side):
    folder = ROOT / name
    setup = folder / "fixture_receipt.json"
    code = checked_text(getsource(precedent.prior.capture), {
        "frames = [2100, *setup['representative_frames'], 7030, 7270, 7520]":
            'frames = sorted(set(setup["scene_edges"] + setup["representative_frames"]))',
        "    folder = ROOT / side": "    folder = ROOT / (side + REPLAY_SUFFIX)",
    })
    env = vars(precedent.prior) | dict(ROOT=folder, SETUP=setup, REPLAY_SUFFIX=REPLAY_SUFFIX)
    exec(compile(code, __file__ + "::complete-town-replay", "exec"), env)
    env["capture"](side)


def verify():
    assert not LIVE.exists() and not SHEET.exists()
    draft, display = map(base.load, (build.review.OUTPUT, offline.PROOF))
    candidate = base.digest(build.ROM)
    assert candidate == display["candidate_sha256"]
    receipts = {r["id"]: r for r in display["receipts"] if r["file_path"] == ARCHIVE}
    evidence, cases, panels = {str(offline.PROOF): base.digest(offline.PROOF)}, {}, []
    for name, (index, panel_count) in CASES.items():
        folder = ROOT / name
        setup = base.load(folder / "fixture_receipt.json")
        schedule = base.load(folder / "inputs.json")
        reports = []
        for side in ("before", "after"):
            path = folder / (side + REPLAY_SUFFIX) / "capture_report.json"
            report = base.load(path)
            fixture = setup["fixture_ROMs"][side]
            assert report["ROM_sha256"] == fixture["sha256"] == base.digest(fixture["path"])
            assert report["frames"] == setup["end"] and report["scripted_input_schedule"] == schedule
            assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
            assert not report.get("battery_save_preloaded")
            assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
            reports.append(report)
            evidence[str(path)] = base.digest(path)
        old, new = map(photos, reports)
        rows = [r for r in draft["records"] if r["file_path"] == ARCHIVE and r["block"] == index]
        assert len(rows) == panel_count
        covered = []
        for row, frame in zip(rows, setup["representative_frames"], strict=True):
            before, a = old[frame]
            after, b = new[frame]
            diff = ImageChops.difference(a, b)
            change = diff.crop((0, 0, 256, 360)).getbbox()
            advance = diff.crop((0, 360, 256, 384)).getbbox()
            assert advance in (None, (224, 0, 240, 16)), (name, row["id"], advance)
            if row["decision"] == "revision":
                assert change and 16 <= change[0] < change[2] <= 232 and 296 <= change[1] < change[3] <= 360, (
                    name, row["id"], change)
                page, = receipts[row["id"]]["pages"]
                ink = masks(bytes.fromhex(page["native_plane_hex"]))
                if row["kind"] == "system-FE":
                    # The scene composites the FE painter's palette index 15 as dark ink.
                    assert not ink[0] and ink[1]
                    ink = [ink[1], set()]
                assert body_masks(b) == ink, (name, row["id"], frame)
            else:
                assert change is None, (name, row["id"], change)
            covered.append(dict(id=row["id"], frame=frame, before=before, after=after,
                                body_change=change, advance_indicator_differs=advance is not None))
            if change or row is rows[-1]:
                panels.append((name, row["id"], a, b))
        matching = setup["scene_edges"]
        assert all(ImageChops.difference(old[f][1], new[f][1]).getbbox() is None for f in matching)
        assert new[matching[-1]][0]["framebuffer_sha256"] != new[setup["representative_frames"][-1]][0]["framebuffer_sha256"]
        for suffix in ("fixture_receipt.json", "inputs.json"):
            evidence[str(folder / suffix)] = base.digest(folder / suffix)
        cases[name] = dict(records=covered, matched_entry_and_return_framebuffers=matching)

    sheet = Image.new("RGB", (944, 153 * len(panels)), "#242932")
    draw = ImageDraw.Draw(sheet)
    for line, (name, ident, before, after) in enumerate(panels):
        for column, (status, image) in enumerate((("Before", before), ("After", after))):
            x, y = 472 * column + 6, 153 * line
            draw.text((x, y + 4), f"{status} / {name.title()} / {ident}", fill="white")
            crop = image.crop((12, 294, 244, 360))
            sheet.paste(crop.resize((464, 132), Image.Resampling.NEAREST), (x, y + 17))
    sheet.save(SHEET)
    base.save(LIVE, dict(candidate_sha256=candidate, cases=cases, initialized_scene=True,
                         natural_town_trigger=False, hardware=False, sheet={str(SHEET): base.digest(SHEET)},
                         evidence=evidence))
    print("All 18 Lil scene panels and the original returns passed.")


if __name__ == "__main__":
    p = ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("prepare", "verify", "startup", *CASES))
    p.add_argument("side", nargs="?", choices=("before", "after"))
    args = p.parse_args()
    if args.action == "startup":
        FunctionType(precedent.startup.__code__, precedent.startup.__globals__ | {"build": build})()
    elif args.action in CASES:
        capture(args.action, args.side)
    else:
        globals()[args.action]()
