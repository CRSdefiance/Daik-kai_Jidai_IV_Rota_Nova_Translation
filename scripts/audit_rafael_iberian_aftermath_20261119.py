"""Check the observed Sofala pages and the original modal-to-dialogue transitions."""

from argparse import ArgumentParser

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import audit_rafael_sailing_modes_playback_20261119 as display
from scripts import replay_rafael_iberian_aftermath_20261119 as play
from scripts import verify_rafael_iberian_aftermath_20261119 as offline
from scripts.verify_all_items_gallery_v535 import glyph_pixels

base, build = play.base, play.build
PROOF = play.ROOT / "verified_appointment.json"
REBOUND = build.ROOT / "sofala_playback_rebound.json"


def progressive_frame(page, name, begin, end, pictures, font):
    plane = bytes.fromhex(page["native_plane_hex"])
    assert len(plane) == 216 * 64 and set(plane) == {0, 1}
    wanted = b"".join(plane[i:i + 216] + bytes(12) for i in range(0, len(plane), 216))
    header = glyph_pixels(font, b"", (), name, 16, 277, 6)
    for n, (shot, image) in sorted(pictures.items()):
        if not begin + 25 < n < end - 4:
            continue
        ink = bytes(c == display.DARK for c in image.crop((16, 296, 244, 360)).get_flattened_data())
        if ink != wanted:
            continue
        shown = {(x, y) for y in range(276, 289) for x in range(14, 18 + len(name) * 6)
                 if image.getpixel((x, y)) == display.STEEL}
        assert shown == header, (name, n)
        return shot
    raise AssertionError((name, begin, end))


def main():
    assert not PROOF.exists()
    folder = play.ROOT / "route0_English"
    terminal = folder / "terminal.json"
    info = base.load(terminal)
    assert info["terminal"] and info["frames"] == play.FRAMES and info["all_callbacks_readonly_andhost_slots_restored"]
    evidence = {str(terminal): base.digest(terminal)}
    for key in ("report", "observer", "run_plan"):
        p = info[key]
        assert base.digest(p) == info[key + "_sha256"]
        evidence[p] = info[key + "_sha256"]
    report, trace, plan = (base.load(info[k]) for k in ("report", "observer", "run_plan"))
    setup, painter = map(base.load, (play.FIXTURES, offline.PROOF))
    fixture, = setup["fixtures"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"] == report["ROM_sha256"]
    assert setup["exact_candidate_inverse"] and base.digest(build.ROM) == setup["candidate_sha256"] == painter["candidate_sha256"]
    assert plan["displayed_original_block"] == 55 and plan["entry_opening_block"] == 44
    assert (plan["original_exchange_commands"], plan["original_exchange_speeches"]) == (74, 30)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(plan["inputs"]) and base.digest(plan["inputs"]) == plan["inputs_sha256"]
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    picture_map = display.captures(report)
    image = base.NdsImage.open(play.FIXTURE)
    file = image.read_file("/data/SC0.DK4")
    block = build.native.IlnkContainer.parse(file).blocks[44]
    font = GameAsciiFont.from_arm9(image.read_file(build.native.ARM))
    names_path = build.review.workflow.NAMES
    names = {r["actor_ID"]: r["current_consumers"][0]["text"] for r in base.load(names_path)["records"]}
    resident = {r["offset"]: r["word"] for r in fixture["all_fixture_commands"]}
    words = {r["fixture_command_offset"]: (r["id"], r["source_selector"]) for r in fixture["original_text_records"]}
    pages = {r["id"]: r["pages"][0] for r in painter["revisions"] if r["id"].startswith("DK4_MES_B55_")}
    assert len(pages) == 6
    pages[offline.REWARD] = painter["retained_reward_display"]["pages"][0]
    speeches, holds, observed_commands = [], [], []
    finished = None
    for returned in trace["rows"]:
        source = returned["source"]
        if returned["kind"] != "after_command" or (
            source.get("classification"), source.get("route"), source.get("block")
        ) != ("original_SC_cache", 0, 44):
            continue
        entered = trace["rows"][returned["entry_row"]]
        assert source["whole_resident_payload_exact_ROM"] and source["actual_sha256"] == source["registered_sha256"] == build.native.digest(block)
        assert returned["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
        at, word = source["instruction_offset"], source["first_word"]
        assert word == resident[at] == entered["source"]["first_word"]
        assert not observed_commands or at > observed_commands[-1]
        observed_commands.append(at)
        if word == 0:
            assert returned["result_words"][0] == 0
            finished = returned
            break
        if at not in words:
            continue
        ident, selector = words[at]
        speeches.append(ident)
        if ident not in pages:
            continue
        n, m = entered["frame"], returned["frame"]
        if selector == 254:
            shot = display.matching_frame(pages[ident], selector, n, m, picture_map, {})
        else:
            shot = progressive_frame(pages[ident], names[selector], n, m, picture_map, font)
        holds.append(dict(id=ident, speaker=selector, frame=shot["frame"], capture=shot,
                          complete_body_and_name_or_absent_name=True))
    assert finished is not None and len(speeches) == len(set(speeches))
    observed = {h["id"] for h in holds}
    required = {f"DK4_MES_B55_R{n:04}" for n in (12, 24, 36, 40, 44, 54)}
    assert required <= observed and observed == pages.keys() & set(speeches)
    transitions = []
    for ident in ("DK4_MES_B55_R0036", offline.REWARD):
        i = speeches.index(ident)
        assert all(dict(words.values())[speeches[j]] != 254 for j in (i - 1, i + 1))
        transitions.append(speeches[i - 1:i + 2])
    samples = [(h["id"], picture_map[h["frame"]][1]) for h in holds]
    later = min(n for n in picture_map if n > finished["frame"] + 60)
    samples.append(("After the original scene return", picture_map[later][1]))
    sheets = []
    for start in range(0, len(samples), 6):
        batch = samples[start:start + 6]
        sheet = Image.new("RGB", (1040, ((len(batch) + 1) // 2) * 404), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(batch):
            x, y = (i % 2) * 520, (i // 2) * 404
            draw.text((x + 4, y + 2), label, fill="white")
            sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 16))
        path = folder / f"sofala_playback_{1 + start // 6}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    evidence.update({str(p): base.digest(p) for p in (play.FIXTURES, play.FIXTURE, offline.PROOF, names_path)})
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], speeches=speeches,
        original_commands_observed=len(observed_commands) - 10, checked_pages=holds,
        revised_pages_verified=len(holds) - 1, distinct_modal_transitions=transitions,
        retained_reward=offline.REWARD, normal_return_result=finished["result_words"],
        return_capture=picture_map[later][0], sheets=sheets, evidence=evidence,
        initialized_fixture=True, natural_activation=False, hardware=False))
    print(f"Verified {len(speeches)} observed speeches, {len(holds) - 1} revised pages, the retained reward and the original scene return.")


def rebind():
    assert not REBOUND.exists()
    prior = offline.PRIOR_ROOT
    old_path = prior / "sofala_fixture/verified_appointment.json"
    terminal = base.load(prior / "sofala_fixture/route0_English/terminal.json")
    old_display = base.load(prior / "native_display/native_display.json")
    new_display = base.load(offline.PROOF)
    old = base.load(old_path)
    before = prior / build.ROM.name
    assert old["candidate_sha256"] == old_display["candidate_sha256"] == base.digest(before)
    assert new_display["candidate_sha256"] == base.digest(build.ROM)
    assert all(base.digest(p) == h for p, h in old["evidence"].items())
    assert all(base.digest(s["path"]) == s["sha256"] for s in old["sheets"])
    assert base.digest(terminal["observer"]) == terminal["observer_sha256"]
    trace = base.load(terminal["observer"])
    owners = {(r["source"]["route"], r["source"]["block"]) for r in trace["rows"]
              if r["source"].get("classification") == "original_SC_cache" and r["kind"] == "after_command"}
    assert owners == {(0, 44), (0, 127)}
    a, b = map(build.native.files, map(base.NdsImage.open, (before, build.ROM)))
    path = "/data/SC0.DK4"
    assert a.keys() == b.keys() and {p for p in a if a[p] != b[p]} == {path}
    first, second = (build.native.IlnkContainer.parse(files[path]).blocks for files in (a, b))
    assert [i for i, (x, y) in enumerate(zip(first, second, strict=True)) if x != y] == [57, 58]
    matching = {n: build.native.digest(second[n]) for n in (44, 55, 127)}
    assert old_display["retained_reward_display"] == new_display["retained_reward_display"]
    assert [r for r in old_display["revisions"] if r["id"].startswith("DK4_MES_B55_")] == [
        r for r in new_display["revisions"] if r["id"].startswith("DK4_MES_B55_")
    ]
    old.update(candidate_sha256=base.digest(build.ROM), observed_candidate_sha256=base.digest(before),
               exact_unchanged_blocks_needed_by_fixture_and_return=matching, replays_on_current_rom=0)
    old["evidence"].update({str(old_path): base.digest(old_path), str(before): base.digest(before),
                            str(offline.PROOF): base.digest(offline.PROOF)})
    base.save(REBOUND, old)
    print("Reused the Sofala fixture and return after verifying exact matching blocks, runtime and glyph planes.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--rebind", action="store_true")
    (rebind if parser.parse_args().rebind else main)()
